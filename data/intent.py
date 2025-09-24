def haggle_intents(
        intents : str,
        message: str
):
    # mirar si si es necesario validar un pedido repitiendo la info
    if intents.lower() == "Saludo".lower():
        return message
    
    if intents.lower() == "ordenar_compra".lower():
        productos = { 
            "intent": "ordenar_compra",
            "response" : "¡Genial! ¿Qué producto te gustaría comprar? 🛒", 
            "options": [
                    "Lampara led personalizada 18*24 cm $60.000",
                    "Lampara led personalizada 24*28 cm $70.000",
                ]
            }
        
        return productos

    if intents.lower() == "pedido_datos".lower():
        datos = {
            "intent": "pedido_datos",
            "response" : "Perfecto, por favor proporciona los siguientes datos para completar tu pedido:\n\n"
                            "1. Nombre completo:\n"
                            "2. Dirección de entrega:\n"
                            "3. Especificación (algo que quiere que vaya en la lámpara):\n"
                            "4. Imagen (opcional):\n"
                            "5. Cedula (Solo si es por interrapidisimo):\n"
                            "6. Método de pago (efectivo, transferencia, etc.)\n\n"
                            "¡Gracias! 😊" 
                }
        return datos
    
    if intents.lower() == "confirmar_pedido".lower():
        confirmacion = {
            "intent": "confirmar_pedido",
            "response": "Gracias por tu pedido (si los datos no son correctos cancelar la compra y volver a enviarlos). ¿Deseas confirmar y finalizar tu compra?",
            "options": [
                                "1. Confirmar Pedido\n"
                                "2. Cancelar Pedido\n\n"
                                ]
                        }
        return confirmacion
    
    if intents.lower() == "fallback".lower():
        return message
    
    if intents.lower() == "error".lower():
        return message