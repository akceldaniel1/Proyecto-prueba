# Proyecto-prueba

Sistema completo que automatiza la extracción, procesamiento y visualización de datos de proyectos de ley del Congreso de Colombia tomados en línea (https://www.camara.gov.co/secretaria/proyectos-de-ley  )
 Permite consultar, buscar y analizar información legislativa de manera intuitiva.

Funcionalidades
🔧 Módulo ETL
•	 Extracción automática de datos de proyectos de ley
•	Limpieza y validación de datos
•	Almacenamiento en base de datos SQLite
•	Manejo robusto de errores
🌐 API REST (FastAPI)
•	GET /proyectos/ - Listar todos los registros
•	GET /proyectos/{id} - Consultar por ID específico
•	GET /proyectos/buscar/{palabra} - Filtrar por palabra clave
•	GET /proyectos/fecha/{fecha} - Filtrar por fecha
•	 Documentación automática en /docs
•	CORS habilitado para frontend
🎨 Frontend (Vue.js)
•	Tabla responsive con todos los proyectos
•	Búsqueda en tiempo real por palabra clave
•	Modal de detalles al seleccionar proyecto
•	Ordenamiento por columnas
•	Diseño moderno y responsive
•	Estados de carga y manejo de errores
Instalación y Ejecución
1.	Instalar dependencias: 
pip install -r requirements.txt

2.	Ejecutar el ETL (para obtener datos) : para revisar por consola.
# Instalar dependencias
pip install requests beautifulsoup4 pandas lxml

# Ejecutar proceso completo
python -m etl.etl

# Verificar base de datos
python -m etl.check_db
# Ver datos extraídos
python -m etl.show_data
3.	Iniciar la API :
uvicorn api.main:app --reload --host 0.0.0.0 --port 8000

4.	Ejecutar el frontend :
 Acceder a la aplicación
•	Frontend: http://localhost:3000
•	API Documentation: http://localhost:8000/docs
•	Health Check: http://localhost:8000/health

Endpoints de la API
GET /proyectos/                                       #Listar todos los proyectos
GET /proyectos/1                                     # Obtener proyecto con ID 1
GET /proyectos/buscar/educacion           # Buscar por palabra clave
GET /proyectos/fecha/2024-01-15          # Filtrar por fecha
GET /health                                              # Verificar estado del servicio
GET /docs                                                # Documentación interactiva


Asistencia de IA en el Desarrollo
1. Solución de Errores y Debugging
•	Diagnóstico de errores CORS: Identificación y solución completa del error "Access-Control-Allow-Origin"
•	Configuración CORS en FastAPI: Implementación de middleware correcto para permitir requests del frontend
•	Manejo de imports relativos: Corrección de errores de importación entre módulos
•	Resolución de dependencias: Configuración adecuada de paths y imports
2. Optimización y Mejores Prácticas
•	Estructura de proyecto: Organización modular y mantenible
•	Configuración CORS: Setup seguro para desarrollo y producción
•	Manejo de conexiones: Pool de conexiones a base de datos eficiente
•	Validación de datos: Schemas con Pydantic para integridad de datos
3. documentación de código.
se utiliza la IA para documentación de códigos y puntos relevantes dentro de este para el entendimiento externo 
Con error antes de la IA
 
Entregable 
 

