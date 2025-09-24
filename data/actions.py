import os
import json
import re
import sys
from urllib import response
import google.generativeai as genai
from intent import haggle_intents

CURRENT_PATH = '/'.join(os.path.abspath(__file__).replace('\\', '/').split('/')[:-2])
sys.path.append(CURRENT_PATH)
# --------------- Modules ---------------
from config import Config   
print(Config.GEMINI_API_KEY)
class ControllerGemini():
    def __init__(self):
        self.config = Config()
        genai.configure(api_key=self.config.GEMINI_API_KEY)
        self.model = genai.GenerativeModel("gemini-1.5-flash")

    def generate_response(self, message):

        prompt = f"""
            Actúa como un asistente de una emppresa de lamppara LED, llamada iluminaria Store. El usuario dice: "{message}".
            productos: Lampara led personalizada 18*24 cm $60.000, Lampara led personalizada 24*28 cm $70.000
            Devuelve SOLO JSON, sin texto adicional, con la siguiente estructura:
            {{
                "intent": "<nombre_del_intent>", los intents son: saludo, ordenar_compra, pedido_datos(cuando el usuario confirme o le interece alguno de los productos), confirmar_pedido. En caso de no relacionarlo con alguna de estas manda un fallback
                "response": "<texto_para_el_usuario>", en este vas a dar un respuesta corta y concreta 
            }}
        """
        try:
            response = self.model.generate_content(prompt)
            try:
                raw_text = response.candidates[0].content.parts[0].text.strip()
                raw_text = re.sub(r"```(?:json)?", "", raw_text)
                parsed = json.loads(raw_text)
            except Exception:
                parsed = {
                    "intent": "error",
                    "response": "Lo siento, no entendí tu mensaje. ¿Podrías reformularlo?"
                }
            response_final = haggle_intents(parsed["intent"], parsed["response"])
            return response_final
        except Exception as e:
            return f"Error generating response: {e}"
        
if __name__ == "__main__":
    controller = ControllerGemini()
    test_message = "me gusta esta lampara, Lampara led personalizada 18*24 cm $60.000"
    response = controller.generate_response(test_message)
    print(response)
