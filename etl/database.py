
import sqlite3
import pandas as pd
from .config import DB_PATH, logging

def crear_tabla():
    """
    Crea la tabla en la base de datos si no existe
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        
        cur.execute('''
            CREATE TABLE IF NOT EXISTS proyectos_ley (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                no_camara TEXT,
                no_senado TEXT,
                proyecto TEXT NOT NULL,
                tipo TEXT,
                autor TEXT NOT NULL,
                estado TEXT,
                comision TEXT,
                origen TEXT,
                legislatura TEXT,
                fecha_extraccion TEXT,
                UNIQUE(no_camara, no_senado, proyecto)
            )
        ''')
        
        conn.commit()
        conn.close()
        logging.info(" Tabla 'proyectos_ley' verificada/creada")
        
    except Exception as e:
        logging.error(f" Error al crear tabla: {e}")

def insertar_datos(data):
    """
    Inserta datos en la base de datos
    Args:
        data (list): Lista de diccionarios con datos a insertar
    """
    if not data:
        logging.warning(" No hay datos para insertar")
        return
    
    try:
        conn = sqlite3.connect(DB_PATH)
        
        # Convertir a DataFrame y insertar
        df = pd.DataFrame(data)
        df.to_sql("proyectos_ley", conn, if_exists="append", index=False)
        
        conn.close()
        logging.info(f" {len(data)} registros insertados en la base de datos")
        
    except Exception as e:
        logging.error(f" Error al insertar datos: {e}")

def obtener_tablas():
    """
    Obtiene lista de tablas en la base de datos
    Returns:
        list: Nombres de las tablas
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        
        cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tablas = [row[0] for row in cur.fetchall()]
        
        conn.close()
        return tablas
        
    except Exception as e:
        logging.error(f" Error al obtener tablas: {e}")
        return []

def contar_registros(tabla_nombre="proyectos_ley"):
    """
    Cuenta registros en una tabla
    Args:
        tabla_nombre (str): Nombre de la tabla
    Returns:
        int: Número de registros
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        
        cur.execute(f"SELECT COUNT(*) FROM {tabla_nombre};")
        count = cur.fetchone()[0]
        
        conn.close()
        return count
        
    except Exception as e:
        logging.error(f" Error al contar registros: {e}")
        return 0