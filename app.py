#----------- Librerias ----------#
import logging
from datetime import datetime
import os
import sys

#----------- FLASK ----------#
from flask import Flask, request, jsonify
from config import Config

#----------- Modulos ----------#
from logs.create_folder import Create_folder, logs_continue
from bot.actions import ControllerBot


app = Flask(__name__)
app.config.from_object(Config)

token = app.config["TOKENWTHASAPP"]
logger = logging.getLogger(__name__)

# current_directory = '/'.join(os.path.abspath(__file__).replace('\\', '/').split('/')[:-1])
# sys.path.append(current_directory)

log_folder = './logs/logs_app'
Create_folder(log_folder)
path_log_name = f"{log_folder}/app.log"


def logs_continue_app( msg: str):
    logs_continue(msg, './logs/logs_app/app.log')

@app.route('/webhook', methods=['GET'])
def verify():
    mode = request.args.get('hub.mode')
    token = request.args.get('hub.verify_token')
    challenge = request.args.get('hub.challenge')
    print(f"Received verification request: mode={mode}, token={token}, challenge={challenge}")
    print(f"Expected token: {app.config['TOKENWTHASAPP']}")
    if mode == "subscribe" and token == app.config["TOKENWTHASAPP"]:
        return challenge, 200
    else:
        return "Token de verificación inválido", 403


@app.route('/webhook', methods=['POST'])
def receive_message():
    try:
        data = request.get_json()   
        if not data:
            msg = "No se recibieron datos en la solicitud"
            logger.error(msg)
            logs_continue_app(msg)
            return jsonify({"error": "No se recibieron datos"}), 400

        if not data.get("entry"):
            msg = "No se encontró el campo 'entry' en los datos"
            logger.error(msg)
            logs_continue_app(msg)
            return jsonify({"error": "No se encontró el campo 'entry' en los datos"}), 400
        
        if "statuses" in data["entry"][0]["changes"][0]["value"]:
            msg = "Mensaje de estado recibido, no se procesará"
            logger.info(msg)
            logs_continue_app(msg)
            return jsonify({"status": "success"}), 200
        
        messages = data.get("entry")[0].get("changes")[0].get("value", {}).get("messages", [])
        message = messages[0].get("text", {}).get("body", "")

        if not message:
            msg = "No se encontró el campo 'text' o 'body' en el mensaje"
            logger.error(msg)
            logs_continue_app(msg)
            return jsonify({"error": "No se encontró el campo 'text' o 'body' en el mensaje"}), 400
        
        phone_number = messages[0].get("from", "")

        bot = ControllerBot(phone_number)

        bot.texto_simple("Hola, ¿cómo puedo ayudarte hoy?")
        msg = f"Mensaje recibido de {phone_number}: {message}"
        logger.info(msg)
        logs_continue_app(msg)

        return jsonify({"status": "success"}), 200
    except Exception as e:
        msg = f"Error al procesar el mensaje: {e}"
        logger.error(msg)
        logs_continue_app(msg)
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)