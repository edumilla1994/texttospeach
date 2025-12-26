"""
Configuración de la aplicación Edge-TTS Web
"""
import os
from pathlib import Path

# Rutas base
BASE_DIR = Path(__file__).resolve().parent
UPLOAD_FOLDER = BASE_DIR / "uploads"
MEDIA_FOLDER = BASE_DIR / "media"
TEXT_AUDIO_FOLDER = MEDIA_FOLDER / "text_audio"
PDF_AUDIO_FOLDER = MEDIA_FOLDER / "pdf_audio"
LOG_FOLDER = BASE_DIR / "logs"

# Crear carpetas si no existen
UPLOAD_FOLDER.mkdir(exist_ok=True)
MEDIA_FOLDER.mkdir(exist_ok=True)
TEXT_AUDIO_FOLDER.mkdir(exist_ok=True)
PDF_AUDIO_FOLDER.mkdir(exist_ok=True)
LOG_FOLDER.mkdir(exist_ok=True)

# Configuración de Flask
class Config:
    """Configuración base"""
    DEBUG = False
    TESTING = False
    MAX_CONTENT_LENGTH = 50 * 1024 * 1024  # 50 MB max file size
    UPLOAD_FOLDER = str(UPLOAD_FOLDER)
    PERMANENT_SESSION_LIFETIME = 3600

class DevelopmentConfig(Config):
    """Configuración desarrollo"""
    DEBUG = True

class ProductionConfig(Config):
    """Configuración producción"""
    DEBUG = False

# Límites
MAX_PALABRAS_TEXTO = 1000
MAX_PAGINAS_PDF = 50

# Voces disponibles
VOCES_ESPANOL = {
    "es-ES-ElviraNeural": "👩 Mujer española (Elvira)",
    "es-ES-AlvaroNeural": "👨 Hombre español (Álvaro)",
    "es-MX-DaliaNeural": "👩 Mujer mexicana (Dalia)",
    "es-AR-EloiseNeural": "👩 Mujer argentina (Eloise)",
}
