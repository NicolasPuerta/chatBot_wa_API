#----------- Librerias ----------#
import logging
from datetime import datetime
import os
import sys

#----------- FLASK ----------#
from flask import Flask, request, jsonify, send_from_directory
from config import Config
from flask_socketio import SocketIO

#----------- Modulos ----------#
from database.models.Usuarios import Usuario
from logs.create_folder import Create_folder, logs_continue
from bot.actions import ControllerBot
from bot.main import RankedResponse
from database.init_db import init_db
from database.actions import Database

db = Database()

app = Flask(__name__)
app.config.from_object(Config)

token = app.config["TOKENWTHASAPP"]
logger = logging.getLogger(__name__)

# current_directory = '/'.join(os.path.abspath(__file__).replace('\\', '/').split('/')[:-1])
# sys.path.append(current_directory)

log_folder = './logs/logs_app'
Create_folder(log_folder)
path_log_name = f"{log_folder}/app.log"

UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# crear las tablas si no existen

def logs_continue_app( msg: str):
    logs_continue(msg, './logs/logs_app/app.log')

init_db()
logger.info("Todas las tablas han sido creadas exitosamente.")
logs_continue_app("Todas las tablas han sido creadas exitosamente.")

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
        logger.info(f"Headers: {dict(request.headers)}")
        logger.info(f"Raw Body: {request.data.decode()}")
        logs_continue_app(f"Headers: {dict(request.headers)}")
        logs_continue_app(f"Raw Body: {request.data.decode()}")

        # Obtener JSON
        data = request.get_json(silent=True)
        if not data:
            msg = "❌ No se recibió JSON válido"
            logger.warning(msg)
            logs_continue_app(msg)
            return jsonify({"error": msg}), 400

        logger.info(f"JSON recibido correctamente: {data}")
        logs_continue_app(f"JSON recibido correctamente: {data}")

        if data.get("object") != "whatsapp_business_account":
            msg = "Objeto no válido en la solicitud"
            logger.error(msg)
            logs_continue_app(msg)
            return jsonify({"error": msg}), 400

        # Validar entrada y cambios
        entry = data.get("entry")
        if not entry or not isinstance(entry, list) or len(entry) == 0:
            msg = "No se encontró 'entry'"
            logger.error(msg)
            logs_continue_app(msg)
            return jsonify({"error": msg}), 400

        changes = entry[0].get("changes")
        if not changes or not isinstance(changes, list) or len(changes) == 0:
            msg = "No se encontró 'changes'"
            logger.error(msg)
            logs_continue_app(msg)
            return jsonify({"error": msg}), 400

        value = changes[0].get("value")
        if not value or not isinstance(value, dict):
            msg = "No se encontró 'value'"
            logger.error(msg)
            logs_continue_app(msg)
            return jsonify({"error": msg}), 400

        # Ignorar mensajes de estado
        if "statuses" in value:
            msg = "Mensaje de estado recibido"
            logger.info(msg)
            logs_continue_app(msg)
            return jsonify({"status": "ignored"}), 200

        # Obtener mensajes
        messages = value.get("messages")
        if not messages or not isinstance(messages, list) or len(messages) == 0:
            msg = "No se encontró 'messages'"
            logger.error(msg)
            logs_continue_app(msg)
            return jsonify({"error": msg}), 400

        message_text = messages[0].get("text", {}).get("body", "")
        phone_number = messages[0].get("from", "")

        if not message_text:
            msg = "No se encontró texto en el mensaje"
            logger.error(msg)
            logs_continue_app(msg)
            return jsonify({"error": msg}), 400 
        
        # Procesar con el bot
        bot = RankedResponse(phone_number)
        response = bot.Classify(message_text)

        if message_text.get("type") == "image":
            bot.main_obtener_imagenes(message_text.get("image", {}).get("id", ""))
            return jsonify({"status": "ignored"}), 200
        
        if not response or isinstance(response, dict):
            logger.error(f"response: {response}")
            logs_continue_app(f"response: {response}")
            msg = "No se pudo clasificar el mensaje"
            logger.error(msg)
            logs_continue_app(msg)
            return jsonify({"status": "ignored"}), 200

        # OK
        logger.info(f"Mensaje de {phone_number}: {message_text}")
        logger.info(f"Respuesta enviada: {response}")
        logs_continue_app(f"{phone_number}: {message_text}")
        logs_continue_app(f"Respuesta: {response}")

        return jsonify({"status": "success"}), 200

    except Exception as e:
        msg = f"Error inesperado: {str(e)}"
        logger.exception(msg)
        logs_continue_app(msg)
        return jsonify({"error": msg}), 500
    

@app.route('/stats', methods=['GET'])
def stats():
    pass

@app.route('/uploads/<filename>', methods=['GET'])
def uploaded_file(filename):
    """
    Serve files from the upload folder.
    """
    upload_folder = app.config['UPLOAD_FOLDER']
    return send_from_directory(upload_folder, filename)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000,debug=True )