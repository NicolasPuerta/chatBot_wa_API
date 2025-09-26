import os
import json
import re
import sys
from urllib import response
import google.generativeai as genai

CURRENT_PATH = '/'.join(os.path.abspath(__file__).replace('\\', '/').split('/')[:-2])
sys.path.append(CURRENT_PATH)
# --------------- Modules ---------------
from data.intent import haggle_intents
from config import Config   
from database.actions import ActionsDB


class ControllerGemini():
    def __init__(self):
        self.config = Config()
        genai.configure(api_key=self.config.GEMINI_API_KEY)
        self.model = genai.GenerativeModel("gemini-1.5-flash")
        self.user = ActionsDB()
        self.intents = {"saludo" : "Un saludo amigable y que refleje lo que es la empresa, siempre saludar cuando un usuario inicia una conversacion o te pase un NONE en estado",
                        "ordenar_compra" : "Este mensaje generalmente se activa cuando el estado del usuario esta en 'saludo'. El bot reesponde con una lista de productos y pregunta cual le interesa", 
                        "pedido_datos" : "Cuando el usuario ha seleccionado un producto o ha confirmado que quiere hacer un pedido, el bot solicita los datos necesarios para completar el pedido, los cuales son los siguientres: Nombre completo, Dirección de entrega, Especificación (algo que quiere que vaya en la lámpara), Imagen (opcional). Este intent es diferente ya que lo vas a clasificar de la siguiente forma y con ese orden 'pedido_orden_Nombre', 'pedido_orden_Direccion', 'pedido_orden_Especificacion', 'pedido_orden_Imagen'.", 
                        "confirmar_pedido" : "siempre va despues de que pedido_datos, el bot resume la informacion del pedido y pregunta si desea confirmar y finalizar la compra, proporcionando opciones claras para confirmar o cancelar el pedido. En caso de cancelar devolver un agradecimiento y poner en estado fallback o saludo", 
                        "fallback" : "Siempre que se solicite información de la empresa o no puedas relacionarlo con alguno de los intents", 
                        "error" : "Genuinamente no entendiste el mensaje del usuario y o consideras que el usuario esta respondiendo algo fuera de contexto, responde con un mensaje de error pidiendo que reformule su pregunta o mensaje"}
        
    def generate_response(self, message, to):
        Usuario_texting = self.user.get_user_by_id(to)
        usuario_estado = Usuario_texting.estado if Usuario_texting else None
        usuario_respuesta_bot = Usuario_texting.respuesta_bot if Usuario_texting else None
        prompt = f"""
            Eres un asistente conversacional para una tienda de lámparas LED personalizadas llamada Iluminaria Store. Tu tarea es ayudar a los usuarios a través de una serie de pasos para completar sus pedidos de manera eficiente y amigable.
            El usuario dice: "{message}".
            El estado actual del usuario es: "{usuario_estado}".
            La última respuesta del bot fue: "{usuario_respuesta_bot}".
            Tus posibles estados son las llaves y sus condiciones son los valores: {list(self.intents)}
            productos: Lampara led personalizada 18*24 cm $60.000, Lampara led personalizada 24*28 cm $70.000. Cada producto viene con control rgb, osea cambia de color y tiene diferentes modos de iluminacion, no lleva pilas, pero si su debido adaptador y base.
            Devuelve SOLO JSON, sin texto adicional, con la siguiente estructura:
            {{
                "intent": "<nombre_del_intent>", los intents son: saludo, ordenar_compra, pedido_datos, confirmar_pedido. En caso de no relacionarlo con alguna de estas manda un fallback
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
