from flask import Flask, request
import logging

logging.basicConfig(level=logging.INFO)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'uma-chave'

@app.before_request
def log_request_info():
    app.logger.info("Requisição recebida: %s %s", request.method, request.path)

from src import routes