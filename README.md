# 🤖 Chatbot de WhatsApp para Gestión de Pedidos

Este proyecto es un chatbot inteligente conectado a la **API de WhatsApp** que permite a los usuarios realizar pedidos fácilmente. Los pedidos son gestionados automáticamente: se agendan en Google Calendar, se almacenan en archivos Excel y se generan gráficas de ventas.

## 📁 Estructura del Proyecto

```
CHATBOT_WA_API/
├── bot/
│   ├── actions.py          # Lógica de respuestas del bot
│   └── main.py             # Punto de entrada del servidor y Flask
│
├── data/
│   └── intents.json        # Intenciones de conversación para el NLP
│
├── database/
│   ├── model.py            # Conexión a PostgreSQL con SQLAlchemy
│   ├── actions.py          # Inicialización de tablas
│   └── models/             # Modelos ORM: Usuario, Pedido, Imagen
│
├── Docker/
│   ├── docker-compose.yml  # Orquestación de servicios (Flask, PostgreSQL, ngrok)
│   └── Dockerfile          # Imagen del servicio Flask
│
├── uploads/                # Carpeta donde se almacenan imágenes subidas
├── logs/                   # Archivos de logs del sistema
├── test/                   # Pruebas unitarias y de integración
├── .env                    # Variables de entorno (NO subir a GitHub)
├── app.py                  # Wrapper general o launcher principal
├── config.py               # Configuración global del proyecto
├── requirements.txt        # Dependencias del proyecto
```

## ✅ Funcionalidades

- 📲 Recepción de pedidos vía **API de WhatsApp**
- 🤖 Respuestas automáticas usando intents (`intents.json`)
- 📅 Agendamiento de pedidos en **Google Calendar**
- 🖼️ Subida y asociación de imágenes a pedidos
- 🧾 Registro de pedidos por usuario
- 📁 Generación de archivos Excel:
  - `pedidos_confirmados.xlsx`
  - `pedidos_enviados.xlsx`
- 📊 Gráficas automáticas de ventas por cliente, fecha y producto

## 🔧 Requisitos Previos

- Cuenta de WhatsApp Business API 
- API de Google Calendar habilitada con archivo `credentials.json`
- Python 3.10+
- Docker y Docker Compose

## 🛠️ Instalación

1. Clona el repositorio:

```bash
git clone https://github.com/tu_usuario/CHATBOT_WA_API.git
cd CHATBOT_WA_API
```

2. Crea el entorno virtual e instala dependencias:

```bash
python -m venv env
source env/bin/activate  # En Windows: env\Scripts\activate
pip install -r requirements.txt
```

3. Configura el archivo `.env`:

```
WHATSAPP_TOKEN=tu_token_api
GOOGLE_CREDENTIALS=credentials.json
CALENDAR_ID=xxx@group.calendar.google.com
DATABASE_URL=postgresql://postgres:secret@chatbot_postgres:5432/chatbotdb
```

4. Inicializa la base de datos (si aún no existen las tablas):

```bash
python database/actions.py
```

5. Corre el servidor:

```bash
python bot/main.py
```

O con Docker:

```bash
docker-compose -f Docker/docker-compose.yml up --build
```
## 📦 ¿Qué hace cada módulo?

| Módulo         | Descripción |
|----------------|-------------|
| `uploads/`         | Almacenamiento de imagenes |
| `bot/`         | Procesamiento de mensajes entrantes y lógica de conversación |
| `database/`    | Manejo de la base de datos y modelos (pedidos, usuarios, etc.) |
| `data/intents.json` | Define intenciones y frases para el NLP del bot |
| `Docker/`      | Archivos para contenerizar la app |
| `logs/`        | Logs de funcionamiento del bot |
| `test/`        | Casos de prueba para funciones clave |
| `config.py`    | Variables de configuración globales del sistema |

## 📈 Gráficas de Ventas

Al confirmar o enviar pedidos, el sistema genera automáticamente visualizaciones:

- 📦 Ventas por producto
- 👤 Ventas por cliente
- 🗓️ Ventas por fecha

Las gráficas se guardan en `/logs/ventas/` o se pueden servir vía Flask en un endpoint tipo `/stats`.

## 👨‍💻 Desarrollador

**Nicolas Puerta**  
[GitHub](https://github.com/NicolasPuerta) - [LinkedIn](https://www.linkedin.com/in/nicolas-puerta-207155231/)
