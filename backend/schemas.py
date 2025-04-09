from pydantic import BaseModel
from fastapi import File, Form, UploadFile
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

class SolicitudIngresoOut(BaseModel):
    id: int
    documento_usuario: str
    id_equipo: int
    estado: str
    fecha_solicitud: str

    class Config:
        orm_mode = True

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
    id_torneo: int
    nombre: str
    documento_creador: str

    tipo_torneo: str  # Eliminación directa, liga, grupos, etc.
    tipo_futbol: str  # Futbol 5, Futbol 7, Futbol 11, mixto, etc.

    fecha_inicio: str
    ubicacion: str
    como_llegar: str  # Indicaciones de llegada
    lugar: str
    
    imagen_cancha: Optional[UploadFile] = File(None)
    torneo_logo: Optional[UploadFile] = File(None)
    numero_participantes: int
    premiacion: str
    reglas: str

    categorias: str  # Ej: "juvenil, libre, femenina"
    costo_inscripcion: float

    torneo_logo: Optional[str] = None  # Imagen representativa del torneo
    estado: Optional[str] = "en espera"
    id_ganador: Optional[int] = None


class SolicitudTorneo(BaseModel):
    id_solicitud: int
    id_torneo: int
    documento_equipo: str
    estado: Optional[str] = "pendiente"  # Estado por defecto es pendiente

from pydantic import BaseModel
from typing import Optional

# Esquema para el partido
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

    # Nuevos campos
    reglas: Optional[str] = None
    como_llegar: Optional[str] = None
    goles_local: int = 0  # Nuevo campo
    goles_visitantes: int = 0  # Nuevo campo

    class Config:
        orm_mode = True  # Cambié 'from_attributes' por 'orm_mode'

# Esquema base para la solicitud de unirse a un partido
class SolicitudUnirseBase(BaseModel):
    id_usuario: int
    id_equipo: int
    id_partido: int

# Esquema para la creación de una solicitud de unirse a un partido
class SolicitudUnirseCreate(SolicitudUnirseBase):
    id_partido: int
    

# Esquema para una solicitud de unirse a un partido, con información adicional
class SolicitudUnirse(SolicitudUnirseBase):
    id_solicitud: int
    estado: str

    class Config:
        orm_mode = True
class GolesUpdate(BaseModel):
    goles_local: int
    goles_visitante: int

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