# --------------- Libraries ---------------
from flask import jsonify
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import json
import os
import sys


CURRENT_PATH = '/'.join(os.path.abspath(__file__).replace('', '/').split('/')[:-1])
sys.path.append(CURRENT_PATH)
# --------------- Modules ---------------
from config import Config   

# # === Cargar datos ===
# with open(f"{CURRENT_PATH}/data/intents.json", encoding="utf-8") as f:
#     intents = json.load(f)

class ControllerBot:
    def __init__(self, to ):
        self.to = to
        self.config = Config()
        # self.session = requests.Session()
        # retries = Retry(
        #     total=5, backoff_factor=1, status_forcelist=[500, 502, 503, 504])
        # self.session.mount('https://', HTTPAdapter(max_retries=retries))
        # self.intents = intents
        # self.message_user = message_user

        self.url = f"https://graph.facebook.com/v22.0/{self.config.PHONE_NUMBER_ID}/messages"

# --------------- Bot Actions ---------------
    def texto_simple(self, message):
        # Saludos = self.intents.get("saludo", {})
        # response = Saludos.get("responses", [])
        payload = json.dumps({
            "messaging_product": "whatsapp",
            "to": self.to,
            "type": "text",
            "text": {
                "body": message
            }
        })
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.config.TOKENWTHASAPP}',
        }
        try:
            requests.post(self.url, headers=headers, data=payload)
        except Exception as e:
            msg = f"Error en la solicitud: {e}"
            return msg

    def productos(self):
        pass
    def enviar_productos(self):
        pass
    def pedido(self):
        pass
    def compra(self):
        pass