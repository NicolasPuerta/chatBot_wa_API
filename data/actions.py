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
from database.actions import Database


class ControllerGemini():
    def __init__(self):
        self.config = Config()
        genai.configure(api_key=self.config.GEMINI_API_KEY)
        self.model = genai.GenerativeModel("gemini-2.0-flash")
        self.user = Database()
        self.json_devuelta = {
                "intent": "<nombre_del_intent>", 
                "response": "<texto_para_el_usuario>"
            }
        self.intents = {
                "saludo": "Un saludo amigable que refleje la identidad de la empresa. Siempre se usa cuando un usuario inicia una conversación o el estado actual es None.",
                
                "ordenar_compra": "Se activa después de 'saludo'. El bot responde con una lista de productos y pregunta cuál le interesa al usuario.", 
                
                "pedido_datos": "Se activa cuando el usuario confirma que quiere hacer un pedido. El flujo es secuencial y debe pedirse en este orden: \
                    1) pedido_datos (pide el nombre del cliente), \
                    2) pedido_datos_Nombre (pide la dirección de entrega), \
                    3) pedido_datos_Direccion (pide la especificación de la lámpara), \
                    4) pedido_datos_Especificacion (pide la imagen opcional), \
                    5) pedido_datos_Imagen (guarda la imagen y calcula la fecha de entrega). \
                    Una vez completado, se cambia el estado automáticamente a 'confirmar_pedido'.",
                
                "confirmar_pedido": "Se activa cuando ya se tienen todos los datos del pedido. El bot debe resumir la información del pedido y preguntar si desea confirmar o cancelar. Si el usuario cancela, agradecer y volver a 'fallback' o 'saludo'.",
                
                "fallback": "Responde cuando el usuario pide información general de la empresa o el mensaje no encaja en ningún intent válido.",
                
                "error": "Se usa cuando el mensaje del usuario no tiene sentido en el contexto o está fuera de lugar. El bot debe pedir que reformule la pregunta."
            }

        
    def generate_response(self, message, to):
        Usuario_texting = self.user.obtener_usuario(to)
        usuario_estado = Usuario_texting.estado if Usuario_texting else None
        usuario_respuesta_bot = Usuario_texting.respuesta_bot if Usuario_texting else None
        prompt = f"""
                Eres un asistente conversacional para una tienda de lámparas LED personalizadas llamada Iluminaria Store. 
                Tu tarea es guiar al usuario paso a paso hasta completar un pedido de forma clara y amigable.

                El usuario dice: "{message}".
                El estado actual del usuario es: "{usuario_estado}".
                La última respuesta del bot fue: "{usuario_respuesta_bot}".

                Los posibles estados (intents) son: {self.intents}.
                Reglas importantes:
                - El intent 'pedido_datos' es SECUENCIAL. No puedes saltar pasos ni cambiar el orden.
                - El flujo de 'pedido_datos' es: pedido_datos → pedido_datos_Nombre → pedido_datos_Direccion → pedido_datos_Especificacion → pedido_datos_Imagen.
                - Una vez llegues a 'pedido_datos_Imagen', cambia automáticamente el estado a 'confirmar_pedido'.
                - Solo puedes pasar a 'confirmar_pedido' si ya tienes TODOS los datos.
                - Si el usuario escribe algo relacionado con cancelar, responde con un fallback agradeciendo y ofreciendo ayuda futura.
                - Para 'saludo', siempre responder con un mensaje cálido que refleje la identidad de la empresa.
                - Para 'ordenar_compra', muestra los productos disponibles.
                - Productos disponibles: 
                - Lámpara LED personalizada 18*24 cm → $60.000
                - Lámpara LED personalizada 24*28 cm → $70.000
                (Ambas incluyen control RGB con modos de iluminación, adaptador y base. No incluyen pilas).

                Debes responder **solo en formato JSON** con la siguiente estructura:
                {self.json_devuelta}
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
    test_message = "que productos tienes"
    response = controller.generate_response(test_message, "209345678901")
    print(response)
