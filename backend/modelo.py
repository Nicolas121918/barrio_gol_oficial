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
    torneo = relationship("Torneos", back_populates="participantes")
    partido = relationship("partidos", back_populates="creador")
    Torneos_create = relationship("Torneos", back_populates="creadormatch")
    # Un usuario puede dar muchos likes
    likes = relationship("Like", back_populates="usuario", cascade="all, delete-orphan")


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
     Descripcion = Column(String(100), nullable=False)
     numeropeople = Column(Integer, nullable=False)
     capitanteam = Column(String(100), nullable=False, unique=True)
     requisitos_join = Column(String(100), nullable=False)
     location = Column(String(150), nullable=False)
     logoTeam = Column(String(255), nullable=False)
     # Relación con el usuario que es el capitán del equipo
     capitan_documento = Column(String(50), ForeignKey('usuarios.documento'))
     capitan = relationship("Registro", back_populates="equipo")

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

    id_Torneo = Column(Integer, primary_key=True, index=True)

    # Información básica
    nombre = Column(String(100), nullable=False)
    tipo = Column(String(50), nullable=False)
    categoria = Column(String(50), nullable=False)
    formato = Column(String(100), nullable=False)

    # Fechas
    fecha_inicio = Column(String(50), nullable=False)
    fecha_final = Column(String(50), nullable=False)
    fecha_limite_inscripcion = Column(String(50), nullable=False)
    dias_de_juego = Column(String(255), nullable=True)  # Por ejemplo: "Sábado, Domingo, Lunes"

    # Participación y reglas
    cantidad_participantes = Column(Integer, nullable=False)
    requiere_uniforme = Column(String(100), nullable=True)
    descripcion_reglas = Column(String(1000), nullable=False)
    duracion_partido = Column(String(100), nullable=True)
    organizacion_partidos = Column(String(100), nullable=True)

    # Ubicación
    direccion = Column(String(255), nullable=False)
    descripcion_llegada = Column(String(500), nullable=True)
    foto_cancha = Column(String(255), nullable=True)
    ubicacion_mapa = Column(String(255), nullable=True)

    # Imágenes y logos
    imagen_torneo = Column(String(255), nullable=True)
    logoTeam = Column(String(255), nullable=True)

    # Costos y premios
    precioInscripcion = Column(Float, nullable=False)
    precioArbitrajeTorneo = Column(Float, nullable=False)
    apuestaTorneo = Column(Float, nullable=True)
    premio_principal = Column(String(255), nullable=True)
    premios_adicionales = Column(String(255), nullable=True)

    # Relación con el creador del torneo
    Documento_Creador_Torneo = Column(String(50), ForeignKey('usuarios.documento'))
    Nombre_Creador_Torneo = Column(String(255), nullable=False)

    # Relaciones
    participantes = relationship("Registro", back_populates="torneo")
    creadormatch = relationship("Registro", back_populates="Torneos_create")

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

    reglas = Column(Text, nullable=True)  # <-- NUEVO
    como_llegar = Column(Text, nullable=True)  # <-- NUEVO

    creador = relationship("Registro", back_populates="partido")


class Messages(Base):
    __tablename__ = 'Chatmessages'
    id = Column(Integer, primary_key=True, autoincrement=True)
    team_id = Column(Integer,nullable=False)
    sender = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    timestamp = Column(TIMESTAMP, server_default=func.current_timestamp())

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
