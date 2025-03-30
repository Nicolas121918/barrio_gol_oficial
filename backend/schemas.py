from pydantic import BaseModel
from fastapi import Form
from typing import Optional
from datetime import datetime

class RegistroBase(BaseModel):
    documento: str = Form(...)
    nombre: str = Form(...)
    ciudad :str = Form(...)
    descripcion:str = Form(...)
    celular: str = Form(...)
    correo: str = Form(...)
    contraseña: str = Form(...)
    fecha_nacimiento: str = Form(...)
    Edad : int = Form(...)
    posicion : str = Form(...)
    imagen : Optional[str]=None
    equipos_tiene: Optional [int]  = 0
    

class LoginRequest(BaseModel):
    correo: str
    contraseña: str

    

class ContactForm(BaseModel):
    nombre: str
    queja_reclamo_quest: str
    email: str 
    celular: str
    comentario: str
    fecha_radicacion : str
    ciudad : str
    
class Contactousuers(BaseModel):
    nombre : str
    email : str 
    celular : str


class JugadorForm(BaseModel):
    nombre : str
    posicion : str
    email : str 
    celular : str 
    equipo : str
    Edad : str

class DatosTeams(BaseModel):
    Id_team: int    
    nombreteam : str
    Descripcion : str
    numeropeople : int
    capitanteam : str
    requisitos_join : str
    location : str
    logoTeam : Optional[str]=None
    
    class PublicacionGaleria(BaseModel):
        id_team: int
        descripcion: str
        tipo_media: str  # 'imagen' o 'video'
        archivo_url: Optional[str] = None

class videos(BaseModel):
    id: int
    url: str
    descripcion: str
    likes: int = 0  # Inicialmente 0 likes

# Schema para recibir datos al dar un like
class LikeCreate(BaseModel):
    video_id: int

# Schema para mostrar información de un like
class LikeResponse(BaseModel):
    id: int
    video_id: int
    usuario_id: int
    timestamp: datetime
    class Config:
        from_attributes = True  # ✅ Convierte objetos SQLAlchemy a JSON                                                                                         
    

# Schema para contar likes en un video
class LikeCountResponse(BaseModel):
    video_id: int
    total_likes: int

     
from pydantic import BaseModel
from typing import Optional, List

class Torneo(BaseModel):
    id_Torneo: int

    # Información básica
    nombre: str
    tipo: str  # Microfútbol, Penales, 1 vs 1, etc.
    categoria: str  # Libre, Juvenil, Infantil, etc.
    formato: str  # Libre, Eliminación directa, Torneo relámpago, etc.

    # Fechas
    fecha_inicio: str
    fecha_final: str
    fecha_limite_inscripcion: str
    dias_de_juego: Optional[List[str]] = None  # Lista de días o fechas si aplica

    # Participación
    cantidad_participantes: int
    requiere_uniforme: str  # Texto libre, por ejemplo: "camiseta blanca", "sí", "no aplica"
    
    # Reglas y descripción
    descripcion_reglas: str
    duracion_partido: str  # Ejemplo: "2 tiempos de 20 minutos", "1 solo tiempo", etc.
    organizacion_partidos: str  # Ej: "aleatoria", "manual", "por grupos"

    # Ubicación
    direccion: str
    descripcion_llegada: str
    foto_cancha: Optional[str] = None  # URL o nombre del archivo
    ubicacion_mapa: Optional[str] = None  # URL de Google Maps (opcional)

    # Recursos visuales
    imagen_torneo: Optional[str] = None  # Imagen representativa

    # Costos y premios
    precio_inscripcion: float
    precio_arbitraje: float
    premio_principal: str
    premios_adicionales: Optional[str] = None

    # Creador del torneo
    nombre_creador: str

class Partidos(BaseModel):
    id_Partido: int
    name: str
    hora: str
    dia: str
    apuesta: float
    ubicacionpartido: str
    logomatch: Optional[str] = None
    imagen_cancha: Optional[str] = None
    tipo_futbol: str
    equipo_local: str
    equipo_visitante: Optional[str] = None
    estado_partido: Optional[str] = "buscando_competidor"
    ganador: Optional[str] = None
    Documento_Creador_P: str

    reglas: Optional[str] = None  # <-- NUEVO
    como_llegar: Optional[str] = None  # <-- NUEVO

    class Config:
        from_attributes = True


class Message(BaseModel):
    team_id: int
    sender: str
    content: str


class ReporteUsuarioSchema(BaseModel):
    documento_reportado: str
    documento_reportante: str
    motivo: str
    descripcion: Optional[str] = None
    fecha_reporte: datetime