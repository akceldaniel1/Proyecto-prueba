# etl/check_db.py
from .database import obtener_tablas, contar_registros
from .config import DB_PATH, logging
import os
import sqlite3

def verificar_base_datos():
    """
    Verifica el estado de la base de datos y sus tablas
    """
    logging.info("🔍 Verificando estado de la base de datos...")
    
    # Verificar si la base de datos existe
    if not os.path.exists(DB_PATH):
        logging.error(f"❌ La base de datos no existe en: {DB_PATH}")
        logging.info("💡 Ejecuta primero: python -m etl.etl")
        return False
    
    # Obtener tablas
    tablas = obtener_tablas()
    
    if not tablas:
        logging.warning("⚠️ La base de datos existe pero no tiene tablas")
        return False
    
    logging.info("📊 Tablas en la base de datos:")
    for tabla in tablas:
        count = contar_registros(tabla)
        logging.info(f"   - {tabla}: {count} registros")
    
    # Mostrar estructura de la tabla proyectos_ley
    if "proyectos_ley" in tablas:
        try:
            conn = sqlite3.connect(DB_PATH)
            cur = conn.cursor()
            
            logging.info("\n📋 Estructura de 'proyectos_ley':")
            for row in cur.execute("PRAGMA table_info(proyectos_ley);"):
                logging.info(f"   - {row[1]} ({row[2]})")
            
            conn.close()
            
        except Exception as e:
            logging.error(f"❌ Error al verificar estructura: {e}")
    
    return True

if __name__ == "__main__":
    verificar_base_datos()