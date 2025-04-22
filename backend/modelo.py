from sqlalchemy import TIMESTAMP, String, Integer, Column, ForeignKey, Float, DateTime, Text, UniqueConstraint, func
from datetime import datetime  # Importa datetime desde Python
from sqlalchemy.orm import relationship
from conexion import Base  

# Tabla de Usuarios
class Registro(Base):
    __tablename__ = "usuarios"
    documento = Column(String(50), primary_key=True, index=True)
    nombre = Column(String(50), nullable=False)
    ciudad = Column(String(50), nullable=False)
    descripcion = Column(String(160), nullable=False)
    celular = Column(String(50), nullable=False)
    correo = Column(String(50), nullable=False)
    contraseña = Column(String(100), nullable=False)
    fecha_nacimiento = Column(String(50), nullable=False)
    imagen = Column(String(255), nullable=True)
    Edad = Column(Integer, nullable=False)
    posicion = Column(String(50), nullable=False)
    equipo_tiene = Column(Integer, nullable=False,default=0)
    # Relaciones
    solicitudes = relationship("Jugador", back_populates="usuario")
    equipo = relationship("Equipos", back_populates="capitan", uselist=False)
    videos = relationship("UserVideos", back_populates="usuario")
    contacto = relationship("Contacto_usuarios", back_populates="usuario")
    partido = relationship("partidos", back_populates="creador")
    # Un usuario puede dar muchos likes
    likes = relationship("Like", back_populates="usuario", cascade="all, delete-orphan")
    solicitudes_equipo = relationship("SolicitudesIngreso", back_populates="usuario")


# Tabla de Contacto de Usuario
class Contacto_usuarios(Base):
    __tablename__ = 'datos_para_contactar_users' 
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nombre = Column(String(50), nullable=False)
    email = Column(String(50), nullable=False)
    celular = Column(String(50), nullable=False)
    # Relación con Usuario
    usuario_documento = Column(String(50), ForeignKey('usuarios.documento'))
    #relacion bidireccional hace una relacion inversa
    usuario = relationship("Registro", back_populates="contacto")


# Tabla de PQRS (Quejas, Reclamos, Solicitudes)
class Contacto(Base):
    __tablename__ = 'PQRS_Usuarios'
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nombre = Column(String(50), nullable=False)
    queja_reclamo_quest = Column(String(50), nullable=False)
    email = Column(String(50), nullable=False)
    celular = Column(String(50), nullable=False)
    comentario = Column(String(150), nullable=False)
    fecha_radicacion = Column(String(50), nullable=False)
    ciudad = Column(String(50), nullable=False)

# Tabla de Solicitudes (Jugador en un equipo)
class Jugador(Base):
    __tablename__ = 'solicitud_join_players'  
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nombre = Column(String(100), nullable=False)
    posicion = Column(String(50), nullable=False)
    email = Column(String(100), nullable=False)
    celular = Column(String(15), nullable=False)
    equipo = Column(String(50), nullable=False)
    Edad = Column(String(10), nullable=False)
    # Relación con Usuario
    usuario_documento = Column(String(50), ForeignKey('usuarios.documento'))
    usuario = relationship("Registro", back_populates="solicitudes")



# Tabla de Videos de Usuario
class UserVideos(Base):
    __tablename__ = "uservideos"

    id = Column(Integer, primary_key=True, index=True)
    url = Column(String(250), nullable=False)
    descripcion = Column(String(500), nullable=True)
    likes = Column(Integer, default=0)  # Este campo podría eliminarse si cuentas los likes en una consulta
    usuario_documento = Column(String(50), ForeignKey("usuarios.documento"))
    
    usuario = relationship("Registro", back_populates="videos")

    # Un video puede recibir muchos likes
    likes_rel = relationship("Like", back_populates="video", cascade="all, delete-orphan")
    
  # Asegúrate de importar Base correctamente


# Tabla de Likes
class Like(Base):
    __tablename__ = "likes"
    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(String(50), ForeignKey("usuarios.documento"), nullable=False)
    video_id = Column(Integer, ForeignKey("uservideos.id"), nullable=False)

    # Restricción para que un usuario no pueda dar like más de una vez al mismo video
    __table_args__ = (UniqueConstraint("usuario_id", "video_id", name="unique_like"),)

    # Relaciones
    usuario = relationship("Registro", back_populates="likes")
    video = relationship("UserVideos", back_populates="likes_rel")

# Tabla de Equipos
class Equipos(Base):
     __tablename__ = 'Equipos_de_barrio_gol'
     Id_team = Column(Integer, primary_key=True, index=True)
     nombreteam = Column(String(50), nullable=False)
     puntos = Column(Integer, default=0)
     nivel = Column(Integer, default=1)
     Descripcion = Column(String(100), nullable=False)
     numeropeople = Column(Integer, nullable=False)
     capitanteam = Column(String(100), nullable=False, unique=True)
     requisitos_join = Column(String(100), nullable=False)
     location = Column(String(150), nullable=False)
     logoTeam = Column(String(255), nullable=False)
     # Relación con el usuario que es el capitán del equipo
     capitan_documento = Column(String(50), ForeignKey('usuarios.documento'))
     capitan = relationship("Registro", back_populates="equipo")
     solicitudes_recibidas = relationship("SolicitudesIngreso", back_populates="equipo")
class SolicitudesIngreso(Base):
    __tablename__ = "solicitudes_ingreso"

    id = Column(Integer, primary_key=True, index=True)
    documento_usuario = Column(String(50), ForeignKey("usuarios.documento"))
    id_equipo = Column(Integer, ForeignKey("Equipos_de_barrio_gol.Id_team"))
    estado = Column(String(20), default="pendiente")  # pendiente, aceptado, rechazado
    fecha_solicitud = Column(String(50))  # puedes poner date también

    usuario = relationship("Registro", back_populates="solicitudes_equipo")
    equipo = relationship("Equipos", back_populates="solicitudes_recibidas")

class GaleriaEquipo(Base):
    __tablename__ = 'galeria_equipo'

    id = Column(Integer, primary_key=True, index=True)
    id_team = Column(Integer, ForeignKey('Equipos_de_barrio_gol.Id_team'), nullable=False)
    descripcion = Column(String(255), nullable=False)
    tipo_media = Column(String(20), nullable=False)  # 'imagen' o 'video'
    archivo_url = Column(String(255), nullable=False)
    
    equipo = relationship("Equipos", backref="galeria")
# Tabla de Torneos
class Torneos(Base):
    __tablename__ = 'Torneos_Barrio_Gol'

    id_torneo = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    documento_creador = Column(String(50), ForeignKey('usuarios.documento'))
    tp_futbol = Column(String(100), nullable=False)
    tipo_torneo = Column(String(100), nullable=False)
    fecha_inicio = Column(String(50), nullable=False)
    ubicacion = Column(String(255), nullable=False)
    como_llegar = Column(String(500), nullable=True)
    lugar = Column(String(255), nullable=False)

    imagen_cancha = Column(String(255), nullable=True)

    numero_participantes = Column(Integer, nullable=False)
    premiacion = Column(String(255), nullable=False)
    reglas = Column(String(1000), nullable=False)

    categorias = Column(String(255), nullable=False)
    costo_inscripcion = Column(Float, nullable=False)

    torneo_logo = Column(String(255), nullable=True)
    estado = Column(String(50), default="en espera", nullable=False)
    id_ganador = Column(Integer,nullable=True)
    solicitudes = relationship("SolicitudesTorneo", back_populates="torneo")
    
    # Relaciones
class SolicitudesTorneo(Base):
    __tablename__ = 'SolicitudesTorneo'

    id_solicitud = Column(Integer, primary_key=True, index=True)
    id_torneo = Column(Integer, ForeignKey('Torneos_Barrio_Gol.id_torneo'))
    id_equipo = Column(String(50))
    estado = Column(String(50), default="pendiente", nullable=False)  # Pendiente, aceptado, rechazado

    torneo = relationship("Torneos", back_populates="solicitudes")
class partidos(Base):
    __tablename__ = 'Partidos_Barrio_Gol'

    id_Partido = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    hora = Column(String(100), nullable=False)
    dia = Column(String(50), nullable=False)
    apuesta = Column(Float, nullable=False)
    ubicacionpartido = Column(String(150), nullable=False)
    logomatch = Column(String(255), nullable=True)
    imagen_cancha = Column(String(255), nullable=True)
    tipo_futbol = Column(String(50), nullable=False)
    equipo_local = Column(String(100), nullable=False)
    equipo_visitante = Column(String(100), nullable=True)
    estado_partido = Column(String(50), default="buscando_competidor")
    ganador = Column(String(100), nullable=True)
    Documento_Creador_P = Column(String(50), ForeignKey('usuarios.documento'))

    # Nuevos campos
    reglas = Column(Text, nullable=True)
    como_llegar = Column(Text, nullable=True)

    goles_local = Column(Integer, default=0)  # Nuevos campos
    goles_visitantes = Column(Integer, default=0)  # Nuevos campos

    creador = relationship("Registro", back_populates="partido")
    solicitudes = relationship("SolicitudUnirse", back_populates="partido")
class SolicitudUnirse(Base):
    __tablename__ = 'solicitudes_unirse_partido'

    id_solicitud = Column(Integer, primary_key=True, index=True)
    id_usuario = Column(Integer, nullable=False)
    id_equipo = Column(Integer, nullable=False)
    id_partido = Column(Integer, ForeignKey('Partidos_Barrio_Gol.id_Partido'), nullable=False)
    estado = Column(String(50), default='pendiente')  # Puede ser 'pendiente', 'aceptada', o 'rechazada'

    partido = relationship("partidos", back_populates="solicitudes")

class Messages(Base):
    __tablename__ = 'Chatmessages'
    id = Column(Integer, primary_key=True, autoincrement=True)
    team_id = Column(Integer,nullable=False)
    sender = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    timestamp = Column(DateTime, default=datetime.now) 

# Tabla de Reportes de Usuario
class ReporteUsuario(Base):
    __tablename__ = 'reportes_usuario'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    documento_reportante = Column(String(50), ForeignKey('usuarios.documento'), nullable=False)
    documento_reportado = Column(String(50), ForeignKey('usuarios.documento'), nullable=False)
    motivo = Column(String(100), nullable=False)
    comentario = Column(String(500), nullable=True)
    fecha_reporte = Column(DateTime, default=datetime.utcnow)

    # Relaciones con la tabla de usuarios
    reportante = relationship("Registro", foreign_keys=[documento_reportante], backref="reportes_realizados")
    reportado = relationship("Registro", foreign_keys=[documento_reportado], backref="reportes_recibidos")
