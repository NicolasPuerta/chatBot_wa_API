# --------------- Libraries ---------------
from urllib import response
from flask import jsonify
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import json
import os
import sys
from uuid import uuid4


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
            return f"✅ Mensaje Enviado a {self.to} - enviar_botones"
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
            return f"✅ Mensaje Enviado a {self.to} - enviar_botones"
        except Exception as e:
            msg = f"Error en la solicitud: {e}"
            return msg

    def enviar_lista(self, message):
        options = message.get("Productos", [])

        if not options:
            msg = "No se encontraron productos para enviar."
            return msg
        if not isinstance(options, list):
            msg = "Los productos deben ser una lista."
            return msg
        # Limita el total a 10 filas
        options = options[:10]

        text = message.get("Text", " ")
        payload = json.dumps({
            "messaging_product": "whatsapp",
            "to": self.to,
            "type": "interactive",
            "interactive": {
                "type": "list",
                "body": {
                    "text": text
                },
                "action": {
                    "button": "Ver opciones",
                    "sections": [
                        {
                        "title": "Productos disponibles",
                        "rows": 
                        [ 
                            { "id" : f"producto_{i+1}", "title": "Lampara LED", "description": desc[:30]} for i, desc in enumerate(options)
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
            response = requests.post(self.url, headers=headers, data=payload)
            if not response.ok:
                return f"❌ Error {response.status_code}: {response.text}"
            return f"✅ Mensaje Enviado a {self.to} - enviar_lista"
        except Exception as e:
            msg = f"Error en la solicitud: {e}"
            return msg


    def obtener_imagenes(self, meta_id):
        meta_url = f"https://graph.facebook.com/v22.0/{meta_id}"
        headers = {
            'Authorization': f'Bearer {self.config.TOKENWTHASAPP}',
        }
        try:
            response = requests.get(meta_url, headers=headers)
            if response.status_code == 200:
                data = response.json()["url"]
                # Paso 2: Descargar archivo binario
                response = requests.get(data, headers=headers, stream=True)
                ext = ".jpg"  # o infiere desde Content-Type
                nombre_archivo = f"{uuid4().hex}{ext}"
                ruta = os.path.join("uploads", nombre_archivo)

                with open(ruta, 'wb') as f:
                    for chunk in response.iter_content(1024):
                        f.write(chunk)

                return ruta
            else:
                return f"❌ Error al obtener imágenes: {response.status_code} - {response.text}"
        except Exception as e:
            return f"Error al obtener imágenes: {e}"
        pass