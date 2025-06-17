#----------- Librerias ----------#
#----------- FLASK ----------#
from flask import Flask
from config import Config
#----------- Modulos ----------#
app = Flask(__name__)
app.config.from_object(Config)

token = app.config["TOKENWTHASAPP"]
