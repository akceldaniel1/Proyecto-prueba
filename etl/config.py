
import os
import logging
from datetime import datetime

# Configuración de paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_DIR = os.path.join(BASE_DIR, "..", "database")
os.makedirs(DB_DIR, exist_ok=True)  # Crear carpeta si no existe
DB_PATH = os.path.join(DB_DIR, "proyectos_ley.db")

# Configuración de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(os.path.join(BASE_DIR, 'etl.log')),
        logging.StreamHandler()
    ]
)

# URL de datos
SOURCE_URL = "https://www.camara.gov.co/secretaria/proyectos-de-ley"

# Configuración de scraping
REQUEST_TIMEOUT = 15
MAX_RECORDS = 20