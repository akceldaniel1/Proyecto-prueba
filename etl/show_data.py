# etl/show_data.py
from .database import contar_registros
from .config import DB_PATH, logging
import sqlite3
import os

def mostrar_datos(limite=10):
    """
    Muestra los registros de la base de datos
    Args:
        limite (int): Número máximo de registros a mostrar
    """
    # Verificar si la base de datos existe
    if not os.path.exists(DB_PATH):
        logging.error(f" La base de datos no existe en: {DB_PATH}")
        logging.info(" Ejecuta primero: python -m etl.etl")
        return
    
    # Verificar si hay registros
    total = contar_registros()
    if total == 0:
        logging.warning(" La base de datos no tiene registros")
        return
    
    try:
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        
        logging.info(f" Mostrando primeros {limite} registros de {total}:")
        logging.info("-" * 80)
        
        # Obtener y mostrar registros
        for row in cur.execute(f"SELECT * FROM proyectos_ley LIMIT {limite};"):
            logging.info(f"ID: {row[0]}")
            logging.info(f"Proyecto: {row[3]}")
            logging.info(f"Autor: {row[5]}")
            logging.info(f"Estado: {row[6]}")
            logging.info(f"Extracción: {row[10]}")
            logging.info("-" * 80)
        
        conn.close()
        
    except Exception as e:
        logging.error(f" Error al mostrar datos: {e}")

if __name__ == "__main__":
    mostrar_datos(10)