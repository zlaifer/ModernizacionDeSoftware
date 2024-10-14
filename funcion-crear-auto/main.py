from mapeadores import mapear_respuesta_exitosa, mapear_respuesta_error, mapear_entidad_a_dto
from validadores import validar_api_key, validar_auto_existente, validar_automovil_request
from persistencia import registrar_automovil, consultar_automovil_por_placa
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from modelo import Base
import os

# Configura la conexión a la base de datos
DATABASE_URI = os.getenv('DATABASE_URI')
engine = create_engine(DATABASE_URI)
# Crear la tabla en la base de datos si no existe
Base.metadata.create_all(engine)
# Crear la sesion
Session = sessionmaker(bind=engine)

def crear_automovil(request):
    # Asignar headers
    headers = {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET,POST,PATCH,OPTIONS",
            "Access-Control-Allow-Headers": "*",
            "Access-Control-Max-Age": "3600",
            "Content-Type": "application/json"
        }
    # Validar CORS
    if request.method == "OPTIONS":
        return ("", 200, headers)

    try:
        # Crea una nueva sesión
        session = Session()
        # Validar API-KEY
        validar_api_key(request.headers)
        # Validar request
        validar_automovil_request(request.get_json())
        # Asignar request json
        nuevo_automovil = mapear_entidad_a_dto(request)
        # Validar si ya se encuentra registrado el automovil
        validar_auto_existente(consultar_automovil_por_placa(session, nuevo_automovil.placa))
        # Inserción en la tabla
        automovil_id = registrar_automovil(session, nuevo_automovil)
        return mapear_respuesta_exitosa(automovil_id, headers)
    except Exception as e:
        return mapear_respuesta_error(e, headers)