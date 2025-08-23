# etl/etl.py
from .scraper import extraer_proyectos_ley, limpiar_datos
from .database import crear_tabla, insertar_datos, contar_registros
from .config import logging

def ejecutar_etl():
    """
    Ejecuta el proceso completo ETL (Extract, Transform, Load)
    """
    logging.info(" Iniciando proceso ETL de proyectos de ley...")
    
    # 1. Preparar base de datos
    crear_tabla()
    
    # 2. EXTRACT - Extraer datos
    datos_crudos = extraer_proyectos_ley()
    
    if not datos_crudos:
        logging.error(" No se pudieron extraer datos. Abortando ETL.")
        return False
    
    # 3. TRANSFORM - Transformar y limpiar datos
    datos_limpios = limpiar_datos(datos_crudos)
    
    if not datos_limpios:
        logging.error(" No hay datos válidos después de la limpieza.")
        return False
    
    # 4. LOAD - Cargar datos a la base de datos
    insertar_datos(datos_limpios)
    
    # 5. Verificar resultado final
    total_registros = contar_registros()
    logging.info(f" Proceso ETL completado. Total registros: {total_registros}")
    
    return True

if __name__ == "__main__":
    ejecutar_etl()