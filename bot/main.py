# ----------------- libreries----------------- #
import sys
import os
import json
from random import choice
from datetime import datetime, timedelta
#------------------- Acciones del Bot -------------------#
CURRENT_PATH = '/'.join(os.path.abspath(__file__).replace('\\', '/').split('/')[:-2])
sys.path.append(CURRENT_PATH)

from bot.actions import ControllerBot
from database.actions import Database
from database.models.Usuarios import Usuario
from database.models.Pedidos import Pedido
from database.models.Imagenes import Imagen

from data.actions import ControllerGemini
from data.intent import haggle_intents


# === Cargar datos ===
with open(f"{CURRENT_PATH}/data/intents.json", encoding="utf-8") as f:
    intents = json.load(f)

class MainBot:
    def __init__(self, to):
        self.sender = to
        self.bot = ControllerBot(self.sender)
        self.database = Database()
        self.gemini = ControllerGemini()
    
    def response_process(self, message, id_imagen=None):
        """
        Procesa el mensaje recibido y devuelve una respuesta generada por Gemini.
        """
        response = self.gemini.generate_response(message, self.sender)
        if not response:
            return "Error al generar la respuesta con Gemini."

        if response['intent'] == 'fallback':
            usuario_ = self.database.obtener_usuario(self.bot.to)
            if usuario_:
                usuario_.estado = response["intent"]
                usuario_actualizado = self.database.actualizar_usuario(usuario_)
                if not usuario_actualizado:
                    return {"error": "Error al actualizar el usuario en la base de datos."}
            proceso = self.main_process_message(response["response"])
            if 'Mensaje Enviado a' not in proceso or "error" in proceso:
                return {"error": f"Error al enviar el mensaje: {message}", "message": proceso, "intento": "saludo"}
            return proceso
        
        if response["intent"] == "error":
            proceso = self.main_process_message(response["response"])
            if 'Mensaje Enviado a' not in proceso or "error" in proceso:
                return {"error": f"Error al enviar el mensaje: {message}", "message": proceso, "intento": "saludo"}
            return proceso
        if response["intent"] == "saludo":
            usuario_ = self.database.obtener_usuario(self.bot.to)
            if not usuario_:
                usuario = Usuario(telefono=self.bot.to, estado="ordenar_compra")
                new_usuario = self.database.insertar_usuario(usuario)
                if not new_usuario:
                    return "Error al insertar el usuario en la base de datos."
            proceso = self.main_process_message(response["response"])
            if 'Mensaje Enviado a' not in proceso or "error" in proceso:
                return {"error": f"Error al enviar el mensaje: {message}", "message": proceso, "intento": "saludo"}
            return proceso
    
        if response["intent"] == "ordenar_compra":
            usuario_ = self.database.obtener_usuario(self.bot.to)
            if usuario_:
                usuario_.estado = response["intent"]
                usuario_actualizado = self.database.actualizar_usuario(usuario_)
                if not usuario_actualizado:
                    return {"error": "Error al actualizar el usuario en la base de datos."}
            proceso = self.main_process_send_list(response)
            if 'Mensaje Enviado a' not in proceso or "error" in proceso or proceso == None:
                return {"error": f"Error al enviar el mensaje: {message}", "message": proceso, "intento": "compra"}
            return proceso

        """ Leer imagenes, guardar datos, cambiar estados """

        if "pedido_datos" in response["intent"]:
            usuario_ = self.database.obtener_usuario(self.bot.to)
            if usuario_:
                usuario_.estado = response["intent"]
                if response["intent"] == "pedido_datos":    
                    Pedido_ = Pedido(cliente_id=usuario_.id, estado="pendiente_datos", tipo=f"{message}")
                    nuevo_pedido = self.database.insertar_pedido(Pedido_)
                    ## enviar mensaje de confirmación de pedido
                    if not nuevo_pedido:
                        return {"error": "Error al insertar el pedido en la base de datos."}
                if response["intent"] == "pedido_datos_Nombre":
                    usuario_.nombre_cliente = message
                elif response["intent"] == "pedido_datos_Direccion":
                    ultimo_pedido = self.database.obtener_ultimo_pedido(usuario_.id)
                    if ultimo_pedido:
                        ultimo_pedido.direccion = message
                        pedido_actualizado = self.database.actualizar_pedido(ultimo_pedido)
                        if not pedido_actualizado:
                            return {"error": "Error al actualizar el pedido en la base de datos."}
                elif response["intent"] == "pedido_datos_Especificacion":
                    ultimo_pedido = self.database.obtener_ultimo_pedido(usuario_.id)
                    if ultimo_pedido:
                        ultimo_pedido.descripcion = message
                        pedido_actualizado = self.database.actualizar_pedido(ultimo_pedido)
                        if not pedido_actualizado:
                            return {"error": "Error al actualizar el pedido en la base de datos."}
                elif response["intent"] == "pedido_datos_Imagen":
                    guardar_imagen = self.main_obtener_imagenes(id_imagen)
                    if not guardar_imagen["success"]:
                        return {"error": f"Error al obtener la imagen: {guardar_imagen['error']}"}
                    ultimo_pedido = self.database.obtener_ultimo_pedido(usuario_.id)

                    dias_entrega = [0,3,5]
                    dia_actual = datetime.now()
                    fecha_entrega = min(
                        [d for d in dias_entrega if d != dia_actual.weekday()],
                        key=lambda x: (x - dia_actual.weekday()) % 7
                    )
                    fecha_entrega_final = dia_actual + timedelta((fecha_entrega - dia_actual.weekday()) % 7)
                    ultimo_pedido.fecha = fecha_entrega_final.strftime("%Y-%m-%d")
                    pedido_actualizado = self.database.actualizar_pedido(ultimo_pedido)
                    
                    if ultimo_pedido:
                        imagen_ = Imagen(id=id_imagen, pedido_id=ultimo_pedido.id, url=guardar_imagen["url"])
                        self.database.insertar_imagen(imagen_)

                usuario_actualizado = self.database.actualizar_usuario(usuario_)
                if not usuario_actualizado:
                    return {"error": "Error al actualizar el usuario en la base de datos."}
                proceso = self.main_process_message(response["response"])  
                if 'Mensaje Enviado a' not in proceso or "error" in proceso:
                    return {"error": f"Error al enviar el mensaje: {message}", "message": proceso, "intento": "pedido_datos"}        
            return proceso

        """ Confirmar pedido, guardar detalles, cambiar estado """
        # if response["intent"] == "confirmar_pedido":
        #     usuario_ = self.database.obtener_usuario(self.bot.to)
        #     Pedido_ = self.database.obtener_ultimo_pedido(usuario_.id)
        #     if Pedido_:
        #         Pedido_.detalles = message
        #         Pedido_.estado = "confirmado"
        #         pedido_actualizado = self.database.actualizar_pedido(Pedido_)
        #         if not pedido_actualizado:
        #             return {"error": "Error al actualizar el pedido en la base de datos."}
        #     if usuario_:
        #         usuario_.estado = "estado_confirmar_pedido"
        #         usuario_actualizado = self.database.actualizar_usuario(usuario_)

        #         if not usuario_actualizado:
        #             return {"error": "Error al actualizar el usuario en la base de datos."}
        #     proceso = self.main_process_send_buttons(response)
        #     if 'Mensaje Enviado a' not in proceso or "error" in proceso:
        #         return {"error": f"Error al enviar el mensaje: {message}", "message": proceso, "intento": "pedido"}
        #     return proceso

        """ El dia de envio habilitado enviar mensaje """

    def main_process_message(self, mensaje):
        msg = self.bot.texto_simple(mensaje)
        return msg

    def main_obtener_imagenes(self, mensaje):
        msg = self.bot.obtener_imagenes(mensaje)
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

