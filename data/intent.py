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
            "response" : "¡Genial! ¿Qué producto te gustaría comprar? 🛒\nUna vez que elijas un producto, te empezaré a pedir los datos necesarios para el envío.", 
            "options": [
                    "Lampara led personalizada 18*24 cm $60.000",
                    "Lampara led personalizada 24*28 cm $70.000",
                ]
            }
        
        return productos

    if "pedido_datos".lower() in intents.lower():
        datos = {
            "intent": "pedido_datos",
            "response" : message
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