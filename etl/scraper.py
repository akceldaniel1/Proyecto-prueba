# etl/scraper.py
import requests
from bs4 import BeautifulSoup
from .config import SOURCE_URL, REQUEST_TIMEOUT, MAX_RECORDS, logging
from datetime import datetime

def extraer_proyectos_ley():
    """
    Extrae datos de proyectos de ley desde la página web
    Returns:
        list: Lista de diccionarios con los datos extraídos
    """
    try:
        logging.info(f" Conectando a: {SOURCE_URL}")
        response = requests.get(SOURCE_URL, timeout=REQUEST_TIMEOUT)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, "html.parser")
        tabla = soup.find("table")
        
        if not tabla:
            raise Exception("No se encontró la tabla de proyectos de ley")
        
        data = []
        filas = tabla.find_all("tr")[1:MAX_RECORDS + 1]  # Limitar registros
        
        for fila in filas:
            celdas = fila.find_all("td")
            if len(celdas) >= 9:
                registro = {
                    "no_camara": celdas[0].get_text(strip=True),
                    "no_senado": celdas[1].get_text(strip=True),
                    "proyecto": celdas[2].get_text(strip=True),
                    "tipo": celdas[3].get_text(strip=True),
                    "autor": celdas[4].get_text(strip=True),
                    "estado": celdas[5].get_text(strip=True),
                    "comision": celdas[6].get_text(strip=True),
                    "origen": celdas[7].get_text(strip=True),
                    "legislatura": celdas[8].get_text(strip=True),
                    "fecha_extraccion": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                data.append(registro)
        
        logging.info(f" Extraídos {len(data)} registros de proyectos de ley")
        return data
        
    except requests.RequestException as e:
        logging.error(f" Error de conexión: {e}")
        return []
    except Exception as e:
        logging.error(f" Error inesperado en extracción: {e}")
        return []

def limpiar_datos(data):
    """
    Limpia y valida los datos extraídos
    Args:
        data (list): Datos crudos extraídos
    Returns:
        list: Datos limpios y validados
    """
    if not data:
        return []
    
    datos_limpios = []
    for registro in data:
        registro_limpio = {}
        for key, value in registro.items():
            # Limpiar textos y manejar valores vacíos
            if isinstance(value, str):
                value = value.strip()
                registro_limpio[key] = value if value else "No especificado"
            else:
                registro_limpio[key] = value
        
        # Validar campos obligatorios
        if registro_limpio.get('proyecto') and registro_limpio.get('autor'):
            datos_limpios.append(registro_limpio)
        else:
            logging.warning(f" Registro omitido por datos incompletos: {registro_limpio}")
    
    logging.info(f"🧹 Datos limpiados: {len(datos_limpios)} registros válidos")
    return datos_limpios