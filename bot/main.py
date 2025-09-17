# ----------------- libreries----------------- #
import sys
import os
import json
from random import choice
#------------------- Acciones del Bot -------------------#
CURRENT_PATH = '/'.join(os.path.abspath(__file__).replace('\\', '/').split('/')[:-2])
sys.path.append(CURRENT_PATH)

from bot.actions import ControllerBot
from database.actions import Database
from database.models.Usuarios import Usuario
from database.models.Pedidos import Pedido
# === Cargar datos ===
with open(f"{CURRENT_PATH}/data/intents.json", encoding="utf-8") as f:
    intents = json.load(f)

class RankedResponse:
    def __init__(self, to, intents_list = intents):
        self.intents = intents_list.get("intents", [])
        self.bot = ControllerBot(to)
        self.database = Database()

    def __classify_intents__(self, message, tag):
        if message in ["Saludo", "Compra"]:
            return self.intents[message]["responses"]
        for i in self.intents:
            if any(message.lower() in pattern.lower() for pattern in i["patterns"]):
                if i["tag"] == tag:
                    return i["responses"]
        return False
    
    def Classify(self, message):
        """
        Clasifica el mensaje recibido y devuelve una respuesta basada en la intención.
        """
        # Aquí podrías implementar un modelo de clasificación más avanzado
        # Por simplicidad, se usa una búsqueda simple en los intents
        usuario_ = self.database.obtener_usuario(self.bot.to)

        if not usuario_ or "hola" in message.lower():
            usuario = Usuario(telefono=self.bot.to, estado="Estado_inicial")
            new_usuario = self.database.insertar_usuario(usuario)
            if not new_usuario:
                return "Error al insertar el usuario en la base de datos."
            # Selecciona un mensaje aleatorio de las respuestas de saludo
            mensaje = choice(self.__classify_intents__(message, "saludo"))
            proceso = self.main_process_message(mensaje)
            if 'Mensaje Enviado a' not in proceso:
                return {"error": f"Error al enviar el mensaje: {proceso}", "message": mensaje, "intento": "saludo"}
            return proceso
        
        if usuario_.estado == "Estado_inicial" or "compra" in message.lower():
            mensaje = self.__classify_intents__(message, "compra")
            usuario_.estado = "Estado_elección_compra"
            usuario_actualizado = self.database.actualizar_usuario(usuario_)
            if not usuario_actualizado:
                return {"error": "Error al actualizar el usuario en la base de datos."}
            proceso = self.main_process_send_list(mensaje)
            if 'Mensaje Enviado a' not in proceso:
                return {"error": f"Error al enviar el mensaje: {proceso}", "message": mensaje, "intento": "compra" }
            return proceso
        
        if usuario_.estado == "Estado_elección_compra":
            mensaje = self.__classify_intents__(message, "datos")
            usuario_.estado = "estado_datos_pedido"
            Pedido_ = Pedido(cliente_id=usuario_.id)
            nuevo_pedido = self.database.insertar_pedido(Pedido_)
            ## enviar mensaje de confirmación de pedido
            if not nuevo_pedido:
                return {"error": "Error al insertar el pedido en la base de datos."}
            usuario_actualizado = self.database.actualizar_usuario(usuario_)
            if not usuario_actualizado:
                return {"error": "Error al actualizar el usuario en la base de datos."}
            pass

        if  usuario_.estado == "estado_datos_pedido":
            mensaje = self.__classify_intents__(message, "pedido")
            proceso = self.main_process_send_buttons(mensaje)
            usuario_.estado = "estado_confirmar_pedido"
            ## enviar mensaje de los datos del pedido
            usuario_actualizado = self.database.actualizar_usuario(usuario_)
            if not usuario_actualizado:
                return {"error": "Error al actualizar el usuario en la base de datos."}
            if 'Mensaje Enviado a' not in proceso:
                return {"error": f"Error al enviar el mensaje: {proceso}", "message": mensaje, "intento": "pedido"}
            return proceso

        if usuario_.estado == "estado_confirmar_pedido":
            mensaje = self.__classify_intents__(message, "confirmar")
            proceso = self.main_process_send_buttons(mensaje)
            if 'Mensaje Enviado a' not in proceso:
                return {"error": f"Error al enviar el mensaje: {proceso}", "message": mensaje, "intento": "confirmar"}
            return proceso

        return {"error": "No se encontró una intención para este mensaje."}

    def main_obtener_imagenes(self, mensaje):
        msg = self.bot.obtener_imagenes(mensaje)
        return msg
    def main_process_message(self, mensaje):
        msg = self.bot.texto_simple(mensaje)
        return msg

    def main_process_send_buttons(self, mensaje):
        """
        Envía un mensaje con botones interactivos al usuario.
        """
        msg = self.bot.enviar_botones(mensaje)
        return msg
    
    def main_process_send_list(self, mensaje):
        """
        Envía un mensaje con una lista de productos al usuario.
        """
        msg = self.bot.enviar_lista(mensaje)
        return msg