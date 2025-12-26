"""
Archivo __init__.py para el paquete app
"""
from flask import Flask

def create_app():
    """Factory para crear la aplicación Flask"""
    app = Flask(__name__)
    return app
