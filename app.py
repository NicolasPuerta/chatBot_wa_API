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
from bot.main import MainBot
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
        data = request.get_json()

        # Guardar el JSON recibido en logs
        logs_continue_app(f"JSON recibido correctamente: {data}")

        # Verificar si hay mensajes en el payload
        entry = data.get("entry", [])[0]
        changes = entry.get("changes", [])[0]
        value = changes.get("value", {})

        if "messages" in value:
            messages = value["messages"]

            for msg in messages:

                # Filtrar solo mensajes de texto
                if msg.get("type") == "text":
                    text = msg["text"]["body"]
                    sender = msg["from"]

                    logs_continue_app(f"Mensaje de texto recibido de {sender}: {text}")

                    bot = MainBot(sender)
                    response = bot.response_process(text)

                    logger.info(f"Mensaje de {sender}: {text}")
                    logger.info(f"Respuesta enviada: {response}")
                    logs_continue_app(f"{sender}: {text}")
                    logs_continue_app(f"Respuesta: {response}")

                if msg.get("type") == "interactive":
                    selection = msg["interactive"]["list_reply"]["description"]
                    sender = msg["from"]
                    logs_continue_app(f"Mensaje de texto recibido de {sender}: {selection}")

                    bot = MainBot(sender)
                    response = bot.response_process(selection)
                    logger.info(f"Mensaje de {sender}: {selection}")
                    logger.info(f"Respuesta enviada: {response}")
                    logs_continue_app(f"{sender}: {selection}")
                    logs_continue_app(f"Respuesta interactiva: {response}")

                if msg.get("type") == "image":
                    id_image = msg["image"]["id"]
                    caption = msg["image"]["caption"] if "caption" in msg["image"] else ""
                    sender = msg["from"]
                    logs_continue_app(f"Mensaje de imagen recibido de {sender}: {caption} - ID: {id_image}")

                    bot = MainBot(sender)
                    response = bot.response_process(caption, id_imagen=id_image)
                    logger.info(f"Mensaje de {sender}: {caption} - ID: {id_image}")
                    logger.info(f"Respuesta enviada: {response}")
                    logs_continue_app(f"{sender}: {caption} - ID: {id_image}")
                    logs_continue_app(f"Respuesta: {response}")


        # Siempre responder 200 para que WhatsApp no reintente
        return "EVENT_RECEIVED", 200

    except Exception as e:
        logs_continue_app(f"Error en receive_message: {e}")
        return "ERROR", 500

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