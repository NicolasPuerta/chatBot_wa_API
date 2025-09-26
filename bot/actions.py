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


CURRENT_PATH = '/'.join(os.path.abspath(__file__).replace('\\', '/').split('/')[:-2])
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
            return f"Mensaje Enviado a {self.to} - enviar_botones"
        except Exception as e:
            msg = f"Error en la solicitud: {e}"
            return msg

    def enviar_botones(self, message):
        options = message.get("options", [])
        if not options:
            msg = "No se encontraron options para enviar."
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
        options = message.get("options", [])

        if not options:
            msg = "No se encontraron options para enviar."
            return msg
        if not isinstance(options, list):
            msg = "Los productos deben ser una lista."
            return msg
        # Limita el total a 10 filas
        options = options[:10]

        text = message.get("response", "Elige un producto de la lista 👇")
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
                            { "id" : f"producto_{i+1}", "title": "Lampara LED", "description": desc[:72]} for i, desc in enumerate(options)
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
            print(response)
            # if not response.ok:
            #     return f"Error {response.status_code}: {response.text}"
            return f"Mensaje Enviado a {self.to} - enviar_lista"
        except Exception as e:
            msg = f"Error en la solicitud: {e}"
            return msg


    def obtener_imagenes(self, meta_id):
        meta_url = f"https://graph.facebook.com/v22.0/{meta_id}?fields=url"
        headers = {
            'Authorization': f'Bearer {self.config.TOKENWTHASAPP}',
        }

        try:
            # Paso 1: Obtener metadata con la URL
            meta_resp = requests.get(meta_url, headers=headers)
            meta_resp.raise_for_status()

            data = meta_resp.json()
            file_url = data.get("url")
            if not file_url:
                return {"success": False, "error": "No se encontró la URL de la imagen."}

            # Paso 2: Descargar archivo binario
            img_resp = requests.get(file_url, headers=headers, stream=True)
            img_resp.raise_for_status()

            # Inferir extensión
            content_type = img_resp.headers.get("Content-Type", "")
            if "png" in content_type:
                ext = ".png"
            elif "jpeg" in content_type:
                ext = ".jpg"
            elif "gif" in content_type:
                ext = ".gif"
            else:
                ext = ".bin"

            os.makedirs("uploads", exist_ok=True)
            nombre_archivo = f"{uuid4().hex}{ext}"
            ruta = os.path.join("uploads", nombre_archivo)

            with open(ruta, "wb") as f:
                for chunk in img_resp.iter_content(1024):
                    f.write(chunk)

            return {"success": True, "path": ruta}

        except Exception as e:
            return {"success": False, "error": str(e)}

if __name__ == "__main__":
    bot = ControllerBot("573014253106")
    # bot.enviar_botones({"options": ["Opción 1", "Opción 2", "Opción 3"], "Texto": "Elige una opción:"})
    bot.enviar_lista({ 
            "intent": "ordenar_compra",
            "response" : "¡Genial! ¿Qué producto te gustaría comprar? 🛒. Una vez que elijas un producto, te empezaré a pedir los datos necesarios para el envío.", 
            "options": [
                    "Lampara led personalizada 18*24 cm $60.000",
                    "Lampara led personalizada 24*28 cm $70.000",
                ]
            })