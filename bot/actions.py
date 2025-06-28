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

    def enviar_botones(self, message):
        options = message.get("Productos", [])
        if not options:
            msg = "No se encontraron productos para enviar."
            return msg
        if not isinstance(options, list):
            msg = "Los productos deben ser una lista."
            return msg
        text = message.get("Texto", " ")

        payload = json.dumps({
            "messaging_product": "whatsapp",
            "to": self.to,
            "type": "interactive",
            "interactive": {
                "type": "button",
                "body": {
                    "text": text
                },
                "action": {
                    "buttons": [
                        {"type": "reply", "reply": {"id": f"opcion_{i+1}", "title": title}} for i, title in enumerate(options)
                    ]
                }
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

    def enviar_lista(self, message):
        payload = json.dumps({
            "messaging_product": "whatsapp",
            "to": self.to,
            "type": "interactive",
            "interactive": {
                "type": "list",
                "body": {
                    "text": "Aquí tienes nuestro catálogo de productos:"
                },
                "footer": {
                    "text": "Selecciona un producto para más detalles"
                },
                "action": {
                    "button": "Ver productos",
                    "sections":
                    [
                        {
                            "title": "Productos destacados",
                            "rows":
                            [
                                {"id": f"prod_{i+1:03}", "title": f"Producto {i+1}", "description": desc} for i, desc in enumerate(message)
                            ] [
                                {
                                    "id": "prod_001",
                                    "title": "Destornillador",
                                    "description": "Destornillador de estrella, $10.000"
                                },
                                {
                                    "id": "prod_002",
                                    "title": "Martillo",
                                    "description": "Martillo de acero reforzado, $25.000"
                                }
                            ]
                        }
                    ]
                }
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
