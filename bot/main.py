# ----------------- libreries----------------- #
import sys
import os
import json
from random import choice
#------------------- Acciones del Bot -------------------#
from bot.actions import ControllerBot

CURRENT_PATH = '/'.join(os.path.abspath(__file__).replace('\\', '/').split('/')[:-1])
sys.path.append(CURRENT_PATH)

# === Cargar datos ===
with open(f"{CURRENT_PATH}/data/intents.json", encoding="utf-8") as f:
    intents = json.load(f)

class RankedResponse:
    def __init__(self, to, intents = intents):
        self.intents = intents
        self.bot = ControllerBot(to)
    def Classify(self, message):
        """
        Clasifica el mensaje recibido y devuelve una respuesta basada en la intención.
        """
        # Aquí podrías implementar un modelo de clasificación más avanzado
        # Por simplicidad, se usa una búsqueda simple en los intents
        clasify_intents = lambda intent: any(keyword in message.lower() for keyword in self.intents.get(intent, {}).get("patterns", []))

        if clasify_intents("compra"):
            mensaje = self.intents["compra"].get("responses", [])
            proceso = self.main_process_send_buttons(mensaje)
            if 'Mensaje Enviado a' not in proceso:
                proceso = f"Error al enviar el mensaje: {proceso}"
            return proceso
        
        if clasify_intents("saludo"):
            mensaje = choice(self.intents["saludo"].get("responses", []))
            proceso = self.main_process_message(mensaje)
            if 'Mensaje Enviado a' not in proceso:
                proceso = f"Error al enviar el mensaje: {proceso}"
            return proceso


    def main_process_message(self, mensaje):
        self.bot.texto_simple(mensaje)
        msg = f"Mensaje Enviado a {self.bot.to}"
        return msg

    def main_process_send_buttons(self, mensaje):
        """
        Envía un mensaje con botones interactivos al usuario.
        """
        self.bot.enviar_botones(mensaje)
        msg = f"Mensaje Enviado a {self.bot.to}"
        return msg