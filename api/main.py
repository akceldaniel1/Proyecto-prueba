# api/main.py - API FastAPI con CORS habilitado
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware 
import sqlite3
from typing import List, Optional
from pydantic import BaseModel
import os

app = FastAPI(
    title="API Proyectos de Ley",
    description="API simple para proyectos de ley del Congreso",
    version="1.0"
)

# CONFIGURACIÓN CORS - IMPORTANTE
origins = [
    "http://localhost:3000",    # Servidor de desarrollo
    "http://127.0.0.1:3000",    # Localhost alternativo
    "http://localhost:8000",    # Mismo puerto de API
    "http://127.0.0.1:8000",    # Localhost API
    "file://",                  # Para archivos locales
    "null",                     # Para origin null
    "*"                         # Para desarrollo (en producción quitar)
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,      # Orígenes permitidos
    allow_credentials=True,
    allow_methods=["*"],        # Métodos HTTP permitidos
    allow_headers=["*"],        # Headers permitidos
)

# Modelo para los datos
class ProyectoLey(BaseModel):
    id: int
    no_camara: Optional[str] = None
    no_senado: Optional[str] = None
    proyecto: str
    tipo: Optional[str] = None
    autor: str
    estado: Optional[str] = None
    comision: Optional[str] = None
    origen: Optional[str] = None
    legislatura: Optional[str] = None
    fecha_extraccion: Optional[str] = None

# Ruta correcta a la base de datos
DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'database', 'proyectos_ley.db')

def get_db():
    """Conexión simple a la base de datos"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # Para obtener diccionarios
    return conn

# 1. Listar todos los registros
@app.get("/proyectos/", response_model=List[ProyectoLey])
def listar_proyectos(limit: int = 100, offset: int = 0):
    """Obtiene todos los proyectos de ley"""
    try:
        conn = get_db()
        cursor = conn.cursor()
        
        cursor.execute(
            "SELECT * FROM proyectos_ley ORDER BY id LIMIT ? OFFSET ?", 
            (limit, offset)
        )
        
        proyectos = [dict(row) for row in cursor.fetchall()]
        conn.close()
        
        if not proyectos:
            raise HTTPException(status_code=404, detail="No hay proyectos en la base de datos")
            
        return proyectos
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener proyectos: {str(e)}")

# 2. Consultar por ID
@app.get("/proyectos/{proyecto_id}", response_model=ProyectoLey)
def obtener_por_id(proyecto_id: int):
    """Obtiene un proyecto específico por su ID"""
    try:
        conn = get_db()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM proyectos_ley WHERE id = ?", (proyecto_id,))
        proyecto = cursor.fetchone()
        conn.close()
        
        if not proyecto:
            raise HTTPException(status_code=404, detail=f"Proyecto con ID {proyecto_id} no encontrado")
            
        return dict(proyecto)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al buscar proyecto: {str(e)}")

# 3. Filtrar por palabra clave
@app.get("/proyectos/buscar/{palabra_clave}", response_model=List[ProyectoLey])
def buscar_por_palabra(palabra_clave: str, limit: int = 50):
    """Busca proyectos por palabra clave en el título"""
    try:
        conn = get_db()
        cursor = conn.cursor()
        
        cursor.execute(
            "SELECT * FROM proyectos_ley WHERE proyecto LIKE ? LIMIT ?",
            (f'%{palabra_clave}%', limit)
        )
        
        proyectos = [dict(row) for row in cursor.fetchall()]
        conn.close()
        
        if not proyectos:
            raise HTTPException(
                status_code=404, 
                detail=f"No se encontraron proyectos con '{palabra_clave}'"
            )
            
        return proyectos
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en la búsqueda: {str(e)}")

# 4. Filtrar por fecha
@app.get("/proyectos/fecha/{fecha}", response_model=List[ProyectoLey])
def filtrar_por_fecha(fecha: str):
    """Filtra proyectos por fecha de extracción"""
    try:
        conn = get_db()
        cursor = conn.cursor()
        
        cursor.execute(
            "SELECT * FROM proyectos_ley WHERE date(fecha_extraccion) = date(?)",
            (fecha,)
        )
        
        proyectos = [dict(row) for row in cursor.fetchall()]
        conn.close()
        
        if not proyectos:
            raise HTTPException(
                status_code=404, 
                detail=f"No hay proyectos para la fecha {fecha}"
            )
            
        return proyectos
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al filtrar por fecha: {str(e)}")

# 5. Endpoint de estadísticas (nuevo)
@app.get("/proyectos/estadisticas/total")
def obtener_estadisticas():
    """Obtiene estadísticas de la base de datos"""
    try:
        conn = get_db()
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*) FROM proyectos_ley")
        total = cursor.fetchone()[0]
        
        conn.close()
        return {"total_proyectos": total}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener estadísticas: {str(e)}")

# Endpoints básicos
@app.get("/")
def inicio():
    return {"message": "API de Proyectos de Ley - Usa /docs para la documentación"}

@app.get("/health")
def health():
    return {"status": "ok", "message": "API funcionando correctamente"}

# Para ejecutar directamente: python -m api.main
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)