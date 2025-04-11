from datetime import datetime
from fastapi import FastAPI,UploadFile,File ,Form , Depends, HTTPException, Query,WebSocket
from sqlalchemy.orm import Session
import bcrypt
from modelo import Registro, SolicitudesIngreso
import uvicorn
from pydantic import BaseModel
from fastapi_socketio import SocketManager
from conexion import engine, get_db
from modelo import Base, Contacto,Jugador,Contacto_usuarios,Equipos, ReporteUsuario, SolicitudesTorneo,UserVideos,Torneos,partidos,Equipos,Registro,Messages as Mensajes
from schemas import RegistroBase as clie,LoginRequest, ReporteUsuarioSchema, SolicitudUnirseCreate
from schemas import ContactForm
from schemas import Contactousuers
from modelo import GaleriaEquipo
from schemas import JugadorForm
from schemas import DatosTeams,Message
from modelo import Like
from modelo import SolicitudUnirse
from schemas import Torneo,Partidos,DatosTeams
from typing import List, Optional
from fastapi.middleware.cors import CORSMiddleware
import os

from fastapi.staticfiles import StaticFiles
from fastapi import HTTPException
import logging
from sqlalchemy import func


app = FastAPI()


app.mount("/media", StaticFiles(directory="media"), name="media")
app.mount("/micarpeta", StaticFiles(directory="micarpeta"), name="micarpeta")
app.mount("/logosteams", StaticFiles(directory="logosteams"), name="logosteams")
app.mount("/videos", StaticFiles(directory="videos"), name="videos")
app.mount("/logosteams", StaticFiles(directory="logosteams"), name="logosteams")
app.mount("/logostorneos", StaticFiles(directory="logostorneos"), name="logostorneos")
app.mount("/logospartidos", StaticFiles(directory="logospartidos"), name="logospartidos")
os.makedirs("imagenes", exist_ok=True)
os.makedirs("logos", exist_ok=True)


## permisos endpoints
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
    
)
Base.metadata.create_all(bind=engine)



## Endpoint Para Login
@app.post("/iniciar")
async def iniciar_sesion(login: LoginRequest, db: Session = Depends(get_db)):
    cliente = db.query(Registro).filter(Registro.correo == login.correo).first()
    
    if not cliente:     
        raise HTTPException(status_code=400, detail="Usuario no existe")
    
    if not bcrypt.checkpw(login.contraseña.encode('utf-8'), cliente.contraseña.encode('utf-8')):
        raise HTTPException(status_code=400, detail="Contraseña incorrecta")
    
    return {
        "documento": cliente.documento,
        "nombreUsuario": cliente.nombre,
        "correo": cliente.correo,
        "ciudad": cliente.ciudad,
        "descripcion": cliente.descripcion,
        "fechaNacimiento": cliente.fecha_nacimiento,
        "imagen" : cliente.imagen,
        "celular" : cliente.celular,
        "Edad" : cliente.Edad,
        "posicion" : cliente.posicion,
        "equiposTiene": cliente.equipo_tiene,  # Se añade la clave correcta
    }
## Endpoint Para Registrar usuarios
@app.post("/insertarc", response_model=clie)
async def registrar_cliente(
    documento: int = Form(...),
    fecha_nacimiento : str = Form(...),
    nombre: str = Form(...),
    ciudad : str = Form(...),
    descripcion : str = Form(...),
    correo: str = Form(...),
    contraseña: str = Form(...),
    file: UploadFile = File(None),
    celular : str = Form(...),
    Edad : int = Form(...),
    posicion : str = Form(...),
    equipos_tiene: Optional[int] = Form(None),
    db: Session = Depends(get_db)
):
    cliente_existente = db.query(Registro).filter(Registro.correo == correo).first()
    Name_Exist = db.query(Registro).filter(Registro.nombre == nombre).first()
    documento_existente = db.query(Registro).filter(Registro.documento == documento).first()

    if cliente_existente:
        raise HTTPException(status_code=400, detail="El correo ya está registrado")
    if Name_Exist:
        raise HTTPException(status_code=400, detail="El Nombre Ya Esta Registrado")
    if documento_existente:
        raise HTTPException(status_code=400, detail="El documento ya está registrado")
    if file and file.content_type not in ["image/jpeg", "image/png", "image/gif", "image/bmp", "image/svg+xml", "image/webp"]:
        raise HTTPException(status_code=400, detail="Formato de archivo no soportado")
    
    if file:
        file_location = f"micarpeta/{file.filename}"
        os.makedirs("micarpeta", exist_ok=True)
        with open(file_location, "wb") as buffer:
            buffer.write(await file.read())
        ruta_Imagen = f"micarpeta/{file.filename}"

    encriptacion = bcrypt.hashpw(contraseña.encode('utf-8'), bcrypt.gensalt())

    nuevo_cliente = Registro(
        descripcion=descripcion,
        documento=documento,
        celular=celular,
        fecha_nacimiento=fecha_nacimiento,
        nombre=nombre,
        correo=correo,
        ciudad=ciudad,
        Edad=Edad,
        posicion=posicion,
        contraseña=encriptacion.decode('utf-8'),
        imagen=ruta_Imagen if file else None,
        equipo_tiene=equipos_tiene  # Se añade la asignación correcta
    )
    # Crear el registro en la tabla de datos de contacto del usuario
    datos_contacto_usuario = Contacto_usuarios(
        nombre=nombre,
        email=correo,
        celular=celular,
        usuario_documento=documento  # Relacionamos con el usuario creado
    )
    
    db.add(nuevo_cliente)
    db.add(datos_contacto_usuario)
    db.commit()
    db.refresh(nuevo_cliente)

    return nuevo_cliente



#endpoint para ver los videos
from sqlalchemy.orm import joinedload

from sqlalchemy.orm import joinedload
from modelo import UserVideos, Like
@app.get("/listarvideos")
async def listar_videos(db: Session = Depends(get_db)):
    lista_videos = (
        db.query(UserVideos)
        .options(joinedload(UserVideos.usuario))
        .order_by(UserVideos.id.desc())  # 👈 Aquí se hace el orden descendente
        .all()
    )

    if not lista_videos:
        raise HTTPException(status_code=404, detail="No hay videos todavía")

    return [
        {
            "id": video.id,
            "url": video.url,
            "documento": video.usuario.documento,
            "uploaderName": video.usuario.nombre if video.usuario else "Desconocido",
            "uploaderProfilePic": video.usuario.imagen if video.usuario and video.usuario.imagen else "default.png",
            "description": video.descripcion if video.descripcion else "Sin descripción",
            "likes": db.query(Like).filter(Like.video_id == video.id).count(),
        }
        for video in lista_videos
    ]
@app.delete("/eliminarvideo/{video_id}")
async def eliminar_video(video_id: int, db: Session = Depends(get_db)):
    video = db.query(UserVideos).filter(UserVideos.id == video_id).first()

    if not video:
        raise HTTPException(status_code=404, detail="Video no encontrado")

    db.delete(video)
    db.commit()

    return {"message": "Video eliminado correctamente"}



@app.get("/listarvideosdef/{documento}")
async def listar_videos_por_documento(documento: str, db: Session = Depends(get_db)):
    lista_videos = (
        db.query(UserVideos)
        .filter(UserVideos.usuario_documento == documento)
        .options(joinedload(UserVideos.usuario))  # Cargar la relación con Usuario
        .all()
    )

    if not lista_videos:
        raise HTTPException(status_code=404, detail="No hay videos para este usuario")

    return [
        {
            "id": video.id,
            "url": video.url,
            "uploaderName": video.usuario.nombre if video.usuario else "Desconocido",
            "uploaderProfilePic": video.usuario.imagen if video.usuario and video.usuario.imagen else "default.png",
            "description": video.descripcion.strip() if video.descripcion else "Sin descripción",
            "likes": db.query(Like).filter(Like.video_id == video.id).count(),
        }
        for video in lista_videos
    ]



@app.post("/likes/{video_id}/{usuario_id}")
async def toggle_like(video_id: int, usuario_id: int, db: Session = Depends(get_db)):
    # Verificar si el video existe
    video = db.query(UserVideos).filter(UserVideos.id == video_id).first()
    if not video:
        raise HTTPException(status_code=404, detail="Video no encontrado")

    # Buscar si el usuario ya dio like a este video
    like_existente = db.query(Like).filter(Like.video_id == video_id, Like.usuario_id == usuario_id).first()

    if like_existente:
        # Si el like ya existe, eliminarlo y restar un like al video
        db.delete(like_existente)
        video.likes = max(0, video.likes - 1)  # Evita valores negativos
        mensaje = "Like eliminado"
    else:
        # Si el like no existe, agregarlo y sumar un like al video
        nuevo_like = Like(video_id=video_id, usuario_id=usuario_id)
        db.add(nuevo_like)
        video.likes += 1  # Aumenta el contador de likes
        mensaje = "Like agregado"

    # Guardar cambios en la base de datos
    db.commit()
    db.refresh(video)  # Asegura que la actualización se refleje en la consulta

    return {"message": mensaje, "likes": video.likes}

@app.get("/like/{video_id}")
async def contar_likes(video_id: int, db: Session = Depends(get_db)):
    total_likes = db.query(Like).filter(Like.video_id == video_id).count()
    return {"video_id": video_id, "likes": total_likes}


## Endpoint Para Enviar el Formulario De contacto
@app.post("/contacto/")
async def crear_contacto(form_data: ContactForm, db: Session = Depends(get_db)):

    nuevo_contacto = Contacto(
        nombre=form_data.nombre,
        queja_reclamo_quest=form_data.queja_reclamo_quest,
        email=form_data.email,
        celular=form_data.celular,
        comentario=form_data.comentario,
        fecha_radicacion = form_data.fecha_radicacion,
        ciudad = form_data.ciudad
    )


    db.add(nuevo_contacto)
    db.commit()
    db.refresh(nuevo_contacto)  
    
    return {"message": "Formulario enviado correctamente", "data": nuevo_contacto}

@app.get("/api/usuario/{user_id}", response_model=clie) 
def obtener_usuario(user_id: int, db: Session = Depends(get_db)):
    usuario = db.query(Registro).filter(Registro.documento == user_id).first()
    if usuario is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    return {
        "documento": usuario.documento,
        "nombre": usuario.nombre,
        "ciudad": usuario.ciudad,
        "descripcion": usuario.descripcion,
        "celular": usuario.celular,
        "correo": usuario.correo,
        "contraseña": usuario.contraseña,
        "fecha_nacimiento": usuario.fecha_nacimiento,
        "Edad": usuario.Edad,
        "posicion": usuario.posicion,
        "imagen": usuario.imagen,
        "equipos_tiene": usuario.equipo_tiene  # Cambio aquí
    }




from fastapi import FastAPI, Form, File, UploadFile, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional
import os
import shutil

## Endpoint Para Crear la tabla de datos basicos apartir de las pqrs del usuario
@app.post("/contactos/")
async def crear_contacto(form_data: Contactousuers, db: Session = Depends(get_db)):

    nuevo_contacto = Contacto_usuarios(
        nombre=form_data.nombre,
        email=form_data.email,
        celular=form_data.celular,
    )
  
    db.add(nuevo_contacto)
    db.commit()
    db.refresh(nuevo_contacto) 
    
    return {"message": "Formulario enviado correctamente", "data": nuevo_contacto}

@app.post("/jugadores/")
async def crear_jugador(form_data: JugadorForm, db: Session = Depends(get_db)):
    nuevo_jugador = Jugador(
        nombre=form_data.nombre,
        Edad=form_data.Edad,
        posicion=form_data.posicion,
        email=form_data.email,
        celular=form_data.celular,
        equipo=form_data.equipo,
    )
    db.add(nuevo_jugador)
    db.commit()
    db.refresh(nuevo_jugador)
    
    return {"message": "Formulario Enviado correctamente En pocas horas Recibira Notificaciones de su Solicitud", "data": nuevo_jugador}

## Endpoint Para Crear los Equipos
@app.get("/equipos/{id_equipo}/info")
async def obtener_info_equipo(id_equipo: int, db: Session = Depends(get_db)):
    equipo = db.query(Equipos).filter(Equipos.Id_team == id_equipo).first()
    if not equipo:
        raise HTTPException(status_code=404, detail="Equipo no encontrado")

    # Obtener el líder del equipo
    registro_lider = db.query(Registro).filter(Registro.documento == equipo.capitan.documento).first()

    lider = {
        "nombre": equipo.capitan.nombre,
        "documento": equipo.capitan.documento,
        "logo": registro_lider.imagen if registro_lider else None
    } if equipo.capitan else None

    # Obtener los miembros del equipo, excluyendo al líder
    miembros = (
        db.query(Registro)
        .filter(Registro.equipo_tiene == id_equipo, Registro.documento != equipo.capitan.documento)
        .all()
    )

    miembros_info = [
        {
            "nombre": miembro.nombre,
            "documento": miembro.documento,
            "logo": miembro.imagen
        }
        for miembro in miembros
    ]

    # Contar cantidad de integrantes (incluyendo al líder)
    cantidad_integrantes = len(miembros) + (1 if lider else 0)

    return {
        "equipo": {
            "id_team": equipo.Id_team,
            "nombreteam": equipo.nombreteam,
            "Descripcion": equipo.Descripcion,
            "logoTeam": equipo.logoTeam
        },
        "lider": lider,
        "miembros": miembros_info,
        "cantidad_integrantes": cantidad_integrantes
    }


@app.get("/equipos/{id_equipo}/detalle", response_model=dict)
async def obtener_equipo_detalle(id_equipo: int, db: Session = Depends(get_db)):
    equipo = db.query(Equipos).filter(Equipos.Id_team == id_equipo).first()
    if not equipo:
            raise HTTPException(status_code=404, detail="Equipo no encontrado")

        # Obtener el documento del capitán
    documento_capitan = equipo.capitan_documento  # Aquí ya tenemos el documento correcto

        # Filtrar miembros excluyendo al capitán
    miembros = db.query(Registro).filter(
            Registro.equipo_tiene == id_equipo, 
            Registro.documento != documento_capitan  # Excluir al capitán por su documento
        ).all()

    return {
            "equipo": {
                "id": equipo.Id_team,
                    "nombre": equipo.nombreteam,
                "descripcion": equipo.Descripcion,
                "numero_integrantes": equipo.numeropeople,
                "capitan": equipo.capitanteam,  # Mantiene el nombre del capitán en los detalles
                "ubicacion": equipo.location,
                "logo": equipo.logoTeam,
                
            },
            "miembros": [{"nombre": miembro.nombre, "documento": miembro.documento, "imagen":miembro.imagen , "fecha_nacimiento" : miembro.fecha_nacimiento} for miembro in miembros]
        }
@app.post("/equipos/salir")
async def salir_equipo(
    documento_user: str = Form(...),  # Cambié int -> str porque en el modelo es String(50)
    db: Session = Depends(get_db)
):
    # Verificar si el usuario existe
    usuario = db.query(Registro).filter(Registro.documento == documento_user).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    # Verificar si el usuario está en un equipo
    if usuario.equipo_tiene == 0:
        raise HTTPException(status_code=400, detail="El usuario no pertenece a ningún equipo")

    # Eliminar la relación con el equipo
    usuario.equipo_tiene = 0  # Cambiar a 0 en lugar de None
    db.commit()

    return {"mensaje": f"{usuario.nombre} ha salido del equipo"}

@app.post("/equipos/expulsar")
async def expulsar_miembro(
    id_team: int = Form(...),
    documento_miembro: str = Form(...),
    db: Session = Depends(get_db)
):
    # Buscar el equipo
    equipo = db.query(Equipos).filter(Equipos.Id_team == id_team).first()
    if not equipo:
        raise HTTPException(status_code=404, detail="Equipo no encontrado")

    # Buscar al miembro dentro del equipo
    miembro = db.query(Registro).filter(
        Registro.documento == documento_miembro,
        Registro.equipo_tiene == id_team
    ).first()

    if not miembro:
        raise HTTPException(status_code=404, detail="Miembro no encontrado en el equipo")

    # Evitar que el capitán sea expulsado
    if miembro.documento == equipo.capitan_documento:
        raise HTTPException(status_code=403, detail="No puedes expulsar al capitán del equipo")

    # Expulsar (quitar del equipo)
    miembro.equipo_tiene = 0
    db.commit()

    return {"mensaje": f"{miembro.nombre} ha sido expulsado del equipo"}
@app.post("/equipos/{id_equipo}/solicitar_union")
async def solicitar_union_equipo(id_equipo: int, documento_usuario: str, db: Session = Depends(get_db)):
    # Buscar si ya existe una solicitud del usuario al equipo
    solicitud_existente = db.query(SolicitudesIngreso).filter_by(
        documento_usuario=documento_usuario,
        id_equipo=id_equipo
    ).first()

    if solicitud_existente:
        return {"mensaje": "Ya has enviado una solicitud a este equipo."}

    # Crear nueva solicitud
    nueva_solicitud = SolicitudesIngreso(
        documento_usuario=documento_usuario,
        id_equipo=id_equipo,
        estado="pendiente",
        fecha_solicitud=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    )
    db.add(nueva_solicitud)
    db.commit()
    db.refresh(nueva_solicitud)

    return {"mensaje": "Solicitud enviada correctamente."}

@app.get("/solicitudes_pendientes/{id_equipo}")
def solicitudes_pendientes_equipo(id_equipo: int, db: Session = Depends(get_db)):
    solicitudes = (
        db.query(SolicitudesIngreso, Registro)
        .join(Registro, SolicitudesIngreso.documento_usuario == Registro.documento)
        .filter(SolicitudesIngreso.id_equipo == id_equipo)
        .filter(SolicitudesIngreso.estado == "pendiente")
        .all()
    )

    resultados = []
    for solicitud, usuario in solicitudes:
        resultados.append({
            "id_solicitud": solicitud.id,  # Aquí lo agregamos
            "documento_usuario": solicitud.documento_usuario,
            "nombre_usuario": usuario.nombre,
            "logo_usuario": usuario.imagen,
            "fecha_solicitud": solicitud.fecha_solicitud,
        })

    return resultados
@app.post("/solicitudes_ingreso/{id_solicitud}/aceptar")
async def aceptar_solicitud_ingreso(id_solicitud: int, db: Session = Depends(get_db)):
    # Buscar la solicitud por ID
    solicitud = db.query(SolicitudesIngreso).filter(SolicitudesIngreso.id == id_solicitud).first()
    if not solicitud:
        raise HTTPException(status_code=404, detail="Solicitud no encontrada")
    
    # Buscar al usuario por su documento
    usuario = db.query(Registro).filter(Registro.documento == solicitud.documento_usuario).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    # Verificar si ya pertenece a un equipo
    if usuario.equipo_tiene != 0:
        raise HTTPException(status_code=400, detail="El usuario ya pertenece a un equipo")

    # Cambiar el estado de la solicitud a "aceptada"
    solicitud.estado = "aceptada"

    # Asignar el ID del equipo al usuario
    usuario.equipo_tiene = solicitud.id_equipo

    # Guardar los cambios en la base de datos
    db.commit()

    return {"mensaje": "Solicitud aceptada con éxito", "usuario": usuario.nombre, "nuevo_equipo_id": usuario.equipo_tiene}

## Endpoint para listar los equipos
@app.get("/listarteams", response_model=list[DatosTeams])
async def listar_equipos(db: Session = Depends(get_db)):
    equipos = db.query(Equipos).all()
    
    if not equipos:
        raise HTTPException(status_code=404, detail="⚠️ No hay equipos registrados aún")

    return equipos

@app.get("/equipos/{id_equipo}/integrantes")
async def contar_integrantes(id_equipo: int, db: Session = Depends(get_db)):
    equipo = db.query(Equipos).filter(Equipos.Id_team == id_equipo).first()

    if not equipo:
        raise HTTPException(status_code=404, detail="Equipo no encontrado")

    # Contar todos los miembros asociados al equipo
    conteo = db.query(Registro).filter(
        Registro.equipo_tiene == id_equipo
    ).count()

    return conteo

@app.get("/actualizar_puntos_nivel/{id_equipo}")
def actualizar_puntos_y_nivel(id_equipo: int, db: Session = Depends(get_db)):
    equipo = db.query(Equipos).filter(Equipos.Id_team == id_equipo).first()
    if not equipo:
        raise HTTPException(status_code=404, detail="Equipo no encontrado")

    # Obtener todos los partidos donde el equipo fue local o visitante
    partidos_equipo = db.query(partidos).filter(
        (partidos.equipo_local == id_equipo) |
        (partidos.equipo_visitante == id_equipo)
    ).all()

    puntos = 0
    for partido in partidos_equipo:
        if partido.ganador == id_equipo:
            puntos += 200
        else:
            puntos -= 100

    # Actualizar puntos y nivel
    equipo.puntos = puntos if puntos > 0 else 0  # No permitir puntos negativos

    if equipo.puntos >= 5000:
        equipo.nivel = 4
    elif equipo.puntos >= 2500:
        equipo.nivel = 3
    elif equipo.puntos >= 900:
        equipo.nivel = 2
    else:
        equipo.nivel = 1

    db.commit()
    db.refresh(equipo)

    return {
        "id_equipo": equipo.Id_team,
        "nombre": equipo.nombreteam,
        "puntos_actualizados": equipo.puntos,
        "nivel_actualizado": equipo.nivel,
        "partidos_totales": len(partidos_equipo)
    }


#equipo actualizar------

from fastapi import Form, File, UploadFile, HTTPException
import os



@app.put("/usuario/actualizar-foto")
async def actualizar_foto_perfil(
    correo: str,  # El correo se enviará en el cuerpo de la solicitud
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    # Busca el usuario por correo
    usuario = db.query(Registro).filter(Registro.correo == correo).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    # Verifica el formato de archivo
    if file.content_type not in ["image/jpeg", "image/png", "image/gif", "image/bmp", "image/svg+xml", "image/webp"]:
        raise HTTPException(status_code=400, detail="Formato de archivo no soportado")
    # Guarda el archivo
    file_location = f"micarpeta/{file.filename}"
    os.makedirs("micarpeta", exist_ok=True)
    with open(file_location, "wb") as buffer:
        buffer.write(await file.read())

    # Actualiza la foto de perfil
    usuario.imagen = file_location
    db.commit()
    db.refresh(usuario)
    return {"message": "Foto de perfil actualizada", "ruta": file_location}

@app.get("/equipos/{id_equipo}/lider", response_model=dict)
async def obtener_lider_equipo(id_equipo: int, db: Session = Depends(get_db)):
    equipo = db.query(Equipos).filter(Equipos.Id_team == id_equipo).first()
    if not equipo:
        raise HTTPException(status_code=404, detail="Equipo no encontrado")
    
    if not equipo.capitan:
        raise HTTPException(status_code=404, detail="Líder del equipo no encontrado en la base de datos")
    
    registro = db.query(Registro).filter(Registro.equipo_tiene == id_equipo).first()
    
    return {
        "lider": {
            "nombre": equipo.capitan.nombre,
            "documento": equipo.capitan.documento,
            "correo": equipo.capitan.correo,
            "telefono": equipo.capitan.celular,
            "imagen": registro.imagen,
            "fecha_nacimiento" : registro.fecha_nacimiento
        },
    
    }
@app.get("/es_lider/{documento}")
def verificar_si_es_lider(documento: int, db: Session = Depends(get_db)):
    # Verificar si hay un equipo donde el documento sea el del capitán
    equipo = db.query(Equipos).filter(Equipos.capitan_documento == documento).first()
    
    return {"esLider": equipo is not None}


@app.delete("/equipos/eliminar/{id_equipo}")
async def eliminar_equipo(id_equipo: int, db: Session = Depends(get_db)):
    # Buscar el equipo por ID
    equipo = db.query(Equipos).filter(Equipos.Id_team == id_equipo).first()
    if not equipo:
        raise HTTPException(status_code=404, detail="Equipo no encontrado")

    # Desasociar a todos los miembros del equipo (poner equipo_tiene en 0)
    db.query(Registro).filter(Registro.equipo_tiene == id_equipo).update(
        {Registro.equipo_tiene: 0}, synchronize_session=False
    )

    # Eliminar el equipo
    db.delete(equipo)
    db.commit()

    return {
        "mensaje": f"✅ El equipo '{equipo.nombreteam}' fue eliminado y sus miembros quedaron sin equipo"
    }

@app.get("/equipos_traer/{id_equipo}", response_model=DatosTeams)
async def obtener_equipo(id_equipo: int, db: Session = Depends(get_db)):
    equipo = db.query(Equipos).filter(Equipos.Id_team == id_equipo).first()
    if not equipo:
        raise HTTPException(status_code=404, detail="Equipo no encontrado")
    return equipo



@app.put("/equipos/actualizar/{id_equipo}")
async def actualizar_equipo(
    id_equipo: int,
    nueva_descripcion: str = Form(None),
    nuevo_logo: UploadFile = File(None),
    db: Session = Depends(get_db)
):
    equipo = db.query(Equipos).filter(Equipos.Id_team == id_equipo).first()

    if not equipo:
        raise HTTPException(status_code=404, detail="Equipo no encontrado")

    if nueva_descripcion:
        equipo.Descripcion = nueva_descripcion

    if nuevo_logo:
        # Guardar el nuevo logo
        file_location = f"logosteams/{nuevo_logo.filename}"
        os.makedirs("logosteams", exist_ok=True)
        with open(file_location, "wb") as buffer:
            buffer.write(await nuevo_logo.read())

        equipo.logoTeam = file_location

    db.commit()
    return {"mensaje": "Equipo actualizado correctamente"}

@app.put("/usuario/actualizar-nombre")
async def actualizar_nombre(
    correo: str = Query(...),
    nombre: str = Form(...),  # Recibimos el nombre como parámetro en el cuerpo del formulario
    db: Session = Depends(get_db)
):
    # Buscar el usuario por correo
    usuario = db.query(Registro).filter(Registro.correo == correo).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    # Actualizar el nombre del usuario
    usuario.nombre = nombre
    db.commit()
    db.refresh(usuario)

    return {"message": "Nombre actualizado", "nombre": usuario.nombre}


## Endpoint Para Actualizar la ciudad sin ID en la URL
@app.put("/usuario/actualizar-ciudad")
async def actualizar_ciudad(
    correo: str = Query(...),
    ciudad: str = Form(...),
    db: Session = Depends(get_db)
):
    # Busca el usuario por correo
    usuario = db.query(Registro).filter(Registro.correo == correo).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    # Actualiza la ciudad
    usuario.ciudad = ciudad
    db.commit()
    db.refresh(usuario)

    return {"message": "Ciudad actualizada", "ciudad": usuario.ciudad}


## Endpoint Para Actualizar la descripción sin ID en la URL
@app.put("/usuario/actualizar-descripcion")
async def actualizar_descripcion(
    correo: str = Query(...),
    descripcion: str = Form(...),
    db: Session = Depends(get_db)
):
    # Busca el usuario por correo
    usuario = db.query(Registro).filter(Registro.correo == correo).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    # Actualiza la descripción
    usuario.descripcion = descripcion
    db.commit()
    db.refresh(usuario)
    return {"message": "Descripción actualizada", "descripcion": usuario.descripcion}


# Configurar logs para ver errores en la consola
logging.basicConfig(level=logging.INFO)
from fastapi import APIRouter

router = APIRouter()


## Endpoint Para Subir Video
@app.post("/subirvideo", response_model=dict)
async def subir_video(
    correo: str = Form(...),
    video: UploadFile = File(...),
    descripcion: str = Form(...),  # Nuevo campo
    db: Session = Depends(get_db),
):
    if video.content_type not in ["video/mp3", "video/mp4", "video/mkv", "video/avi", "video/mov", "video/webm"]:
        raise HTTPException(status_code=400, detail="Formato de video no soportado")

    usuario = db.query(Registro).filter(Registro.correo == correo).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    video_location = f"videos/{video.filename}"
    os.makedirs("videos", exist_ok=True)
    with open(video_location, "wb") as buffer:
        buffer.write(await video.read())

    ruta_video = f"videos/{video.filename}"
    nuevo_video = UserVideos(
        url=ruta_video,
        descripcion=descripcion,  # Guardar la descripción
        usuario_documento=usuario.documento
    )

    db.add(nuevo_video)
    db.commit()
    db.refresh(nuevo_video)

    return {"mensaje": "Video subido correctamente", "ruta": ruta_video}





@app.get("/id_equipo/{documento}")
def obtener_equipo_por_documento(documento: int, db: Session = Depends(get_db)):
    # Buscar al usuario en la base de datos por su documento
    usuario = db.query(Registro).filter(Registro.documento == documento).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    # Buscar el equipo donde el usuario es capitán
    equipo = db.query(Equipos).filter(Equipos.capitan_documento == usuario.documento).first()
    if not equipo:
        raise HTTPException(status_code=404, detail="El usuario no lidera ningún equipo")
    
    return {"Id_team": equipo.Id_team}


## Endpoint Para Crear los Equipos
@app.post("/Teams")
async def registrar_cliente(
    nombreteam: str = Form(...),
    Descripcion: str = Form(...),
    numeropeople: int = Form(...),
    documento_cap: int = Form(...),
    capitanteam: str = Form(...),
    requisitos_join: str = Form(...),
    location: str = Form(...),
    logoteam: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    file_location = f"logosteams/{logoteam.filename}"
    os.makedirs("logosteams", exist_ok=True)
    with open(file_location, "wb") as buffer:
        buffer.write(await logoteam.read())

    ruta_Imagen = f"logosteams/{logoteam.filename}"
    
    # Buscar al capitán en la base de datos por su documento
    capitan = db.query(Registro).filter(Registro.documento == documento_cap).first()
    if not capitan:
        raise HTTPException(status_code=404, detail="Capitán no encontrado en la base de datos")

    # Crear el equipo
    nuevo_Team = Equipos(
        nombreteam=nombreteam,
        Descripcion=Descripcion,
        numeropeople=numeropeople,
        capitanteam=capitanteam,
        requisitos_join=requisitos_join,
        location=location,
        logoTeam=ruta_Imagen,
        capitan_documento=capitan.documento,  # Asociar el documento del capitán
    )


    db.add(nuevo_Team)
    db.commit()
    db.refresh(nuevo_Team)  # Para obtener el ID generado por la base de datos

    # Actualizar el equipo_tiene del capitán con el ID del nuevo equipo
    capitan.equipo_tiene = nuevo_Team.Id_team
    db.commit()  # Guardar el cambio en la base de datos

    return nuevo_Team


#-------------------------------------partido----------------------------------------------------------------
@app.post("/crearPartido")
async def crear_partido(
    name: str = Form(...),
    hora: str = Form(...),
    dia: str = Form(...),
    apuesta: float = Form(...),
    ubicacionpartido: str = Form(...),
    tipo_futbol: str = Form(...),
    equipo_local: str = Form(...),
    Documento_Creador_P: str = Form(...),
    reglas: Optional[str] = Form(None),
    como_llegar: Optional[str] = Form(None),
    logomatch: Optional[UploadFile] = File(None),
    imagen_cancha: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db)
):
    try:
        # Guardar logo del partido si se envió
        logomatch_path = None
        if logomatch:
            os.makedirs("logospartidos", exist_ok=True)
            logomatch_path = f"logospartidos/{logomatch.filename}"
            with open(logomatch_path, "wb") as buffer:
                shutil.copyfileobj(logomatch.file, buffer)

        # Guardar imagen de cancha si se envió
        imagen_cancha_path = None
        if imagen_cancha:
            os.makedirs("imagenescancha", exist_ok=True)
            imagen_cancha_path = f"imagenescancha/{imagen_cancha.filename}"
            with open(imagen_cancha_path, "wb") as buffer:
                shutil.copyfileobj(imagen_cancha.file, buffer)

        # Crear el partido
        nuevo_partido = partidos(
            name=name,
            hora=hora,
            dia=dia,
            apuesta=apuesta,
            ubicacionpartido=ubicacionpartido,
            tipo_futbol=tipo_futbol,
            equipo_local=equipo_local,
            equipo_visitante=None,  # Aún no se ha aceptado el visitante
            estado_partido="en_proceso",
            ganador=None,
            Documento_Creador_P=Documento_Creador_P,
            logomatch=logomatch_path,
            imagen_cancha=imagen_cancha_path,
            reglas=reglas,
            como_llegar=como_llegar,
            goles_local=0,  # Inicializar goles
            goles_visitantes=0  # Inicializar goles
            
        )

        db.add(nuevo_partido)
        db.commit()
        db.refresh(nuevo_partido)

        return {
            "mensaje": "Partido creado exitosamente",
            "id_partido": nuevo_partido.id_Partido
        }

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error al crear partido: {str(e)}")
@app.get("/partidos_finalizados")
async def partidos_finalizados(db: Session = Depends(get_db)):
    # Cambiar 'partidos' a un nombre diferente para evitar el conflicto
    partidos_lista = db.query(PartidosModel).filter(PartidosModel.estado_partido == "finalizado").all()

    if not partidos_lista:
        raise HTTPException(status_code=404, detail="No hay partidos finalizados")

    # Devolver los datos de los partidos finalizados
    return [
        {
            "id_partido": partido.id_Partido,
            "nombre_partido": partido.name,
            "logo_partido": partido.logomatch,
            "fecha": partido.dia,
            "equipos": [
                {
                    "nombre": equipo_local.nombreteam,
                    "logo": equipo_local.logoTeam
                },
                {
                    "nombre": equipo_visitante.nombreteam,
                    "logo": equipo_visitante.logoTeam
                }
            ]
        }
        for partido in partidos_lista
        if (equipo_local := db.query(Equipos).filter(Equipos.Id_team == partido.equipo_local).first()) and
           (equipo_visitante := db.query(Equipos).filter(Equipos.Id_team == partido.equipo_visitante).first())
    ]


@app.get("/listar_partidos_filtrados/{documento}/{equipo_local}")
async def listar_partidos_filtrados(documento: str, equipo_local: str, db: Session = Depends(get_db)):
    partidos_filtrados = (
        db.query(
            partidos,
            Registro.imagen.label("logo_creador"),
            Registro.nombre.label("nombre_creador"),
            Registro.documento.label("documento_creador"),
            Equipos.Id_team.label("id_equipo"),
            Equipos.nombreteam.label("nombre_equipo"),
            Equipos.logoTeam.label("logo_equipo"),
        )
        .join(Registro, partidos.Documento_Creador_P == Registro.documento)  # Relacionar con usuarios
        .join(Equipos, partidos.equipo_local == Equipos.Id_team)  # Relacionar con equipos
        .filter(
            partidos.Documento_Creador_P != documento,
            partidos.equipo_local != equipo_local,
            partidos.estado_partido == "en_proceso",
        )
        .all()
    )

    if not partidos_filtrados:
        raise HTTPException(status_code=404, detail="No hay partidos disponibles según los filtros aplicados.")

    # Devolver directamente la lista de partidos con los datos del creador y equipo local
    return [
        {
            **partido.__dict__,
            "creador": {
                "documento": documento_creador,
                "nombre": nombre_creador,
                "logo": logo_creador,
            },
            "equipo_local": {
                "id": id_equipo,
                "nombre": nombre_equipo,
                "logo": logo_equipo,
            }
        }
        for partido, nombre_creador, logo_creador, documento_creador, id_equipo, nombre_equipo, logo_equipo in partidos_filtrados
    ]

@app.get("/listarpartidos/{excluir_name}", response_model=List[Partidos])
async def listar_partidos(excluir_name: str, db: Session = Depends(get_db)):
    excluir_name = excluir_name.strip().lower()
    lista_Partidos = db.query(partidos).filter(func.lower(partidos.id_Partido) != excluir_name).all()

    if not lista_Partidos:
        raise HTTPException(status_code=404, detail="No hay partidos disponibles")
    return lista_Partidos

from modelo import partidos as PartidosModel  # ← O mejor: cambia el nombre del modelo a "Partidos"

@app.get("/partidos_finalizados/{documento}", response_model=List[Partidos])
async def partidos_finalizados(documento: str, db: Session = Depends(get_db)):
    resultados = db.query(PartidosModel).filter(
        PartidosModel.Documento_Creador_P == documento,
        PartidosModel.estado_partido == "finalizado"
    ).all()

    if not resultados:
        raise HTTPException(status_code=404, detail="No hay partidos finalizados para este usuario.")
    return resultados

@app.get("/partidos_en_espera/{documento}", response_model=List[Partidos])
async def partidos_en_espera(documento: str, db: Session = Depends(get_db)):
    resultados = db.query(PartidosModel).filter(
        PartidosModel.Documento_Creador_P == documento,
        PartidosModel.estado_partido.in_(["en_proceso", "en_juego"])
    ).order_by(PartidosModel.id_Partido.desc()).all()

    if not resultados:
        raise HTTPException(status_code=404, detail="No hay partidos en espera para este usuario.")
    return resultados

@app.get("/partido/{id_partido}", response_model=Partidos)
async def obtener_partido_por_id(id_partido: int, db: Session = Depends(get_db)):
    partido = db.query(PartidosModel).filter(
        PartidosModel.id_Partido == id_partido
    ).first()
    if not partido:
        raise HTTPException(status_code=404, detail="Partido no encontrado.")
    return partido

@app.post("/solicitar_unirse/")
async def solicitar_unirse(solicitud: SolicitudUnirseCreate, db: Session = Depends(get_db)):
    # Verificar si el partido existe
    partido = db.query(partidos).filter(partidos.id_Partido == solicitud.id_partido).first()
    if not partido:
        raise HTTPException(status_code=404, detail="Partido no encontrado")

    # Verificar si ya existe una solicitud pendiente para el mismo equipo en este partido
    solicitud_existente = db.query(SolicitudUnirse).filter(
        SolicitudUnirse.id_partido == solicitud.id_partido,
        SolicitudUnirse.id_equipo == solicitud.id_equipo,
        SolicitudUnirse.estado == 'pendiente'
    ).first()

    if solicitud_existente:
        raise HTTPException(status_code=400, detail="Solicitud ya enviada por este equipo")

    # Crear la solicitud de unirse
    nueva_solicitud = SolicitudUnirse(
        id_usuario=solicitud.id_usuario,
        id_equipo=solicitud.id_equipo,
        id_partido=solicitud.id_partido,
        estado='pendiente'
    )

    db.add(nueva_solicitud)
    db.commit()
    db.refresh(nueva_solicitud)

    return {"mensaje": "Solicitud enviada con éxito", "id_solicitud": nueva_solicitud.id_solicitud}

def solicitar_unirse(id_partido: int, solicitud: SolicitudUnirseCreate, db: Session = Depends(get_db)):
    # Verificar si el partido existe
    partido = db.query(partidos).filter(partidos.id_Partido == id_partido).first()
    if not partido:
        raise HTTPException(status_code=404, detail="Partido no encontrado")

    # Crear la solicitud de unirse
    nueva_solicitud = SolicitudUnirse(
        id_usuario=solicitud.id_usuario,
        id_equipo=solicitud.id_equipo,
        id_partido=id_partido,
        estado='pendiente'
    )

    db.add(nueva_solicitud)
    db.commit()
    db.refresh(nueva_solicitud)

    return {"mensaje": "Solicitud enviada con éxito", "id_solicitud": nueva_solicitud.id_solicitud}
  # lista los torneos de un usuario


@app.post("/aceptar_solicitud/{id_solicitud}")
async def aceptar_solicitud(id_solicitud: int, db: Session = Depends(get_db)):
    # Buscar la solicitud
    solicitud = db.query(SolicitudUnirse).filter(SolicitudUnirse.id_solicitud == id_solicitud).first()
    if not solicitud:
        raise HTTPException(status_code=404, detail="Solicitud no encontrada")

    # Buscar el partido
    partido = db.query(partidos).filter(partidos.id_Partido == solicitud.id_partido).first()
    if not partido:
        raise HTTPException(status_code=404, detail="Partido no encontrado")

    # Actualizar el estado de la solicitud
    solicitud.estado = 'aceptada'
    partido.equipo_visitante = solicitud.id_equipo
    partido.estado_partido = 'en_Juego'

    db.commit()

    return {"mensaje": "Solicitud aceptada, partido en juego"}

@app.post("/rechazar_solicitud/{id_solicitud}")
async def rechazar_solicitud(id_solicitud: int, db: Session = Depends(get_db)):
    # Buscar la solicitud
    solicitud = db.query(SolicitudUnirse).filter(SolicitudUnirse.id_solicitud == id_solicitud).first()
    if not solicitud:
        raise HTTPException(status_code=404, detail="Solicitud no encontrada")

    # Actualizar el estado de la solicitud a rechazada
    solicitud.estado = 'rechazada'

    db.commit()

    return {"mensaje": "Solicitud rechazada correctamente"} 

@app.get("/solicitudes_pendientesPartidos/{id_partido}")
async def solicitudes_pendientes(id_partido: int, db: Session = Depends(get_db)):
    # Buscar las solicitudes pendientes para un partido específico
    solicitudes = db.query(SolicitudUnirse).filter(SolicitudUnirse.id_partido == id_partido, SolicitudUnirse.estado == 'pendiente').all()
    
    if not solicitudes:
        raise HTTPException(status_code=404, detail="No hay solicitudes pendientes para este partido")

    return {"solicitudes_pendientes": solicitudes}

class GolesUpdate(BaseModel):
    goles_local: int
    goles_visitante: int


@app.post("/actualizar_goles/{id_partido}")
async def actualizar_goles(id_partido: int, goles: GolesUpdate, db: Session = Depends(get_db)):
    # Buscar el partido en la base de datos
    partido = db.query(partidos).filter(partidos.id_Partido == id_partido).first()
    if not partido:
        raise HTTPException(status_code=404, detail="Partido no encontrado")

    # Actualizar los goles
    partido.goles_local = goles.goles_local
    partido.goles_visitantes = goles.goles_visitante

    # Determinar el ganador
    if goles.goles_local > goles.goles_visitante:
        partido.ganador = partido.equipo_local
    elif goles.goles_local < goles.goles_visitante:
        partido.ganador = partido.equipo_visitante
    else:
        partido.ganador = "Empate"

    # Marcar el partido como finalizado
    partido.estado_partido = "finalizado"

    # Guardar los cambios en la base de datos
    db.commit()
    db.refresh(partido)

    return {"mensaje": "Goles actualizados y partido finalizado", "id_partido": id_partido}


@app.get("/resultado_detallado/{id_partido}")
async def resultado_detallado(id_partido: int, db: Session = Depends(get_db)):
    # Buscar el partido en la base de datos
    partido = db.query(partidos).filter(partidos.id_Partido == id_partido).first()
    if not partido:
        raise HTTPException(status_code=404, detail="Partido no encontrado")
    
    if partido.estado_partido != "finalizado":
        raise HTTPException(status_code=400, detail="El partido aún no ha finalizado")

    # Obtener los equipos
    equipo_local = db.query(Equipos).filter(Equipos.Id_team == partido.equipo_local).first()
    equipo_visitante = db.query(Equipos).filter(Equipos.Id_team == partido.equipo_visitante).first()

    if not equipo_local or not equipo_visitante:
        raise HTTPException(status_code=404, detail="Uno o ambos equipos no encontrados")

    # Si fue empate
    if partido.ganador is None or partido.ganador == "Empate":
        return {
            "nombre_partido": partido.name,
            "logo_partido": partido.logomatch,
            "id_partido": partido.id_Partido,
            "fecha": partido.dia,
            "resultado": "Empate",
            "equipos": [
                {
                    "nombre": equipo_local.nombreteam,
                    "logo": equipo_local.logoTeam,
                    "goles": partido.goles_local
                },
                {
                    "nombre": equipo_visitante.nombreteam,
                    "logo": equipo_visitante.logoTeam,
                    "goles": partido.goles_visitantes
                }
            ]
        }

    # Si hay un ganador
    if str(partido.ganador) == str(equipo_local.Id_team):
        datos_ganador = {
            "nombre": equipo_local.nombreteam,
            "logo": equipo_local.logoTeam,
            "goles": partido.goles_local
        }
        datos_perdedor = {
            "nombre": equipo_visitante.nombreteam,
            "logo": equipo_visitante.logoTeam,
            "goles": partido.goles_visitantes
        }
    elif str(partido.ganador) == str(equipo_visitante.Id_team):
        datos_ganador = {
            "nombre": equipo_visitante.nombreteam,
            "logo": equipo_visitante.logoTeam,
            "goles": partido.goles_visitantes
        }
        datos_perdedor = {
            "nombre": equipo_local.nombreteam,
            "logo": equipo_local.logoTeam,
            "goles": partido.goles_local
        }
    else:
        raise HTTPException(status_code=400, detail="Ganador no coincide con los equipos del partido")

    return {
        "nombre_partido": partido.name,
        "logo_partido": partido.logomatch,
        "ganador": datos_ganador,
        "perdedor": datos_perdedor
    }


@app.post("/actualizar_puntos/{id_partido}")
async def actualizar_puntos(id_partido: int, db: Session = Depends(get_db)):
    # Buscar el partido en la base de datos
    partido = db.query(partidos).filter(partidos.id_Partido == id_partido).first()
    if not partido:
        raise HTTPException(status_code=404, detail="Partido no encontrado")

    if partido.estado_partido != "finalizado":
        raise HTTPException(status_code=400, detail="El partido aún no ha finalizado")

    # Obtener los equipos
    equipo_local = db.query(Equipos).filter(Equipos.Id_team == partido.equipo_local).first()
    equipo_visitante = db.query(Equipos).filter(Equipos.Id_team == partido.equipo_visitante).first()

    if not equipo_local or not equipo_visitante:
        raise HTTPException(status_code=404, detail="Uno o ambos equipos no encontrados")

    # Actualizar puntos según el resultado
    if partido.ganador == partido.equipo_local:
        equipo_local.puntos += 200
        equipo_visitante.puntos -= 100
        if equipo_visitante.puntos < 0:
            equipo_visitante.puntos = 0
    elif partido.ganador == partido.equipo_visitante:
        equipo_visitante.puntos += 200
        equipo_local.puntos -= 100
        if equipo_local.puntos < 0:
            equipo_local.puntos = 0
    else:  # Empate
        equipo_local.puntos += 50
        equipo_visitante.puntos += 50

    # Actualizar niveles según los puntos
    def actualizar_nivel(equipo):
        if equipo.puntos >= 5000:
            equipo.nivel = 4
        elif equipo.puntos >= 2000:
            equipo.nivel = 3
        elif equipo.puntos >= 500:
            equipo.nivel = 2
        else:
            equipo.nivel = 1

    actualizar_nivel(equipo_local)
    actualizar_nivel(equipo_visitante)

    # Guardar los cambios en la base de datos
    db.commit()
    db.refresh(equipo_local)
    db.refresh(equipo_visitante)

    return {
        "mensaje": "Puntos y niveles actualizados correctamente",
        "id_partido": id_partido,
        "equipos": {
            "local": {
                "nombre": equipo_local.nombreteam,
                "puntos": equipo_local.puntos,
                "nivel": equipo_local.nivel
            },
            "visitante": {
                "nombre": equipo_visitante.nombreteam,
                "puntos": equipo_visitante.puntos,
                "nivel": equipo_visitante.nivel
            }
        }
    }

#-------------------------------------TORNEO-----------------------------------------------------------------


from fastapi import APIRouter, Form, UploadFile, File, HTTPException, Depends
from sqlalchemy.orm import Session
import os, shutil

router = APIRouter()


@app.post("/crearTorneo")
async def crear_torneo(
    nombre: str = Form(...),
    documento_creador: str = Form(...),
    tipo_torneo: str = Form(...),
    tipo_futbol: str = Form(...),
    fecha_inicio: str = Form(...),
    ubicacion: str = Form(...),
    como_llegar: str = Form(...),
    lugar: str = Form(...),
    numero_participantes: int = Form(...),
    premiacion: str = Form(...),
    reglas: str = Form(...),
    categorias: str = Form(...),
    costo_inscripcion: float = Form(...),
    imagen_cancha: Optional[UploadFile] = File(None),
    torneo_logo: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db)
):
    # Crear carpetas si no existen
    os.makedirs("imagenes", exist_ok=True)
    os.makedirs("logos", exist_ok=True)

    # Guardar archivos si vienen
    ruta_imagen_cancha = None
    if imagen_cancha:
        ruta_imagen_cancha = f"imagenes/{imagen_cancha.filename}"
        with open(ruta_imagen_cancha, "wb") as buffer:
            shutil.copyfileobj(imagen_cancha.file, buffer)

    ruta_logo_torneo = None
    if torneo_logo:
        ruta_logo_torneo = f"logos/{torneo_logo.filename}"
        with open(ruta_logo_torneo, "wb") as buffer:
            shutil.copyfileobj(torneo_logo.file, buffer)

    # Crear el torneo en la BD
    nuevo_torneo = Torneos(
        nombre=nombre,
        documento_creador=documento_creador,
        tipo_torneo=tipo_torneo,
        tipo_futbol=tipo_futbol,
        fecha_inicio=fecha_inicio,
        ubicacion=ubicacion,
        como_llegar=como_llegar,
        lugar=lugar,
        numero_participantes=numero_participantes,
        premiacion=premiacion,
        reglas=reglas,
        categorias=categorias,
        costo_inscripcion=costo_inscripcion,
        imagen_cancha=ruta_imagen_cancha,
        torneo_logo=ruta_logo_torneo,
        estado="en espera",
        id_ganador=None
    )

    db.add(nuevo_torneo)
    db.commit()
    db.refresh(nuevo_torneo)

    return {"mensaje": "Torneo creado exitosamente", "torneo": nuevo_torneo.id_torneo}


@app.get("/torneosDisponibles/{documento_creador}")
async def obtener_torneos_disponibles(documento_creador: str, db: Session = Depends(get_db)):
    # Filtrar los torneos que no sean del creador especificado
    torneos = db.query(Torneos).filter(
        Torneos.documento_creador != documento_creador  # Excluir los torneos del creador especificado
    ).all()

    if not torneos:
        return {"mensaje": "No se encontraron torneos disponibles."}

    return {"mensaje": "Torneos disponibles encontrados", "torneos": torneos}

@app.get("/torneosFinalizados/{documento_creador}")
async def obtener_torneos_finalizados(documento_creador: str, db: Session = Depends(get_db)):
    # Filtrar los torneos por el documento del creador y estado 'finalizado'
    torneos = db.query(Torneos).filter(
        Torneos.documento_creador == documento_creador, 
        Torneos.estado == "terminado"
    ).all()

    if not torneos:
        return {"mensaje": "No se encontraron torneos finalizados para este creador."}

    return {"mensaje": "Torneos finalizados encontrados", "torneos": torneos}

@app.get("/torneosEnJuego/{documento_creador}")
async def obtener_torneos_en_estado(documento_creador: str, db: Session = Depends(get_db)):
    # Filtrar los torneos por el documento del creador y los estados 'en espera' o 'en_juego'
    torneos = db.query(Torneos).filter(
        Torneos.documento_creador == documento_creador, 
        Torneos.estado.in_(['en espera', 'en_juego'])
    ).all()

    if not torneos:
        return {"mensaje": "No se encontraron torneos en espera o en juego para este creador."}

    return {"mensaje": "Torneos en espera o en juego encontrados", "torneos": torneos}

from fastapi import Form
#listar torneos con informacion del creador:
@app.get("/listar_torneos")
async def listar_torneos(db: Session = Depends(get_db)):
    torneos_con_creador = (
        db.query(
            Torneos,
            Registro.nombre.label("nombre_creador"),
            Registro.imagen.label("imagen_creador"),
            Registro.documento.label("documento_creador"),
        )
        .join(Registro, Torneos.documento_creador == Registro.documento)
        .all()
    )

    if not torneos_con_creador:
        raise HTTPException(status_code=404, detail="No hay torneos registrados.")

    return [
        {
            "id_torneo": torneo.id_torneo,
            "nombre": torneo.nombre,
            "documento_creador": torneo.documento_creador,
            "tipo_torneo": torneo.tipo_torneo,
            "tipo_futbol": torneo.tipo_futbol,
            "creador": {
                "nombre": nombre_creador,
                "imagen": imagen_creador,
                "documento": documento_creador
            }
        }
        for torneo, nombre_creador, imagen_creador, documento_creador in torneos_con_creador
    ]
@app.get("/listar_torneo/{id_torneo}")
async def obtener_torneo_por_id(id_torneo: int, db: Session = Depends(get_db)):
    resultado = (
        db.query(
            Torneos,
            Registro.nombre.label("nombre_creador"),
            Registro.imagen.label("imagen_creador"),
            Registro.documento.label("documento_creador"),
        )
        .join(Registro, Torneos.documento_creador == Registro.documento)
        .filter(Torneos.id_torneo == id_torneo)
        .first()
    )

    if not resultado:
        raise HTTPException(status_code=404, detail="Torneo no encontrado.")

    torneo, nombre_creador, imagen_creador, documento_creador = resultado

    # Convertimos el objeto torneo a diccionario
    torneo_dict = {column.name: getattr(torneo, column.name) for column in torneo.__table__.columns}

    # Agregamos los datos del creador
    torneo_dict["creador"] = {
        "nombre": nombre_creador,
        "imagen": imagen_creador,
        "documento": documento_creador
    }

    return torneo_dict
@app.post("/enviarSolicitud/{id_torneo}")
def enviar_solicitud(id_torneo: int, id_equipo: str, db: Session = Depends(get_db)):
    try:
        # Verificar si ya existe una solicitud
        solicitud_existente = db.query(SolicitudesTorneo).filter_by(
            id_torneo=id_torneo,
            id_equipo=id_equipo
        ).first()

        if solicitud_existente:
            raise HTTPException(status_code=400, detail="Ya enviaste una solicitud a este torneo.")

        nueva_solicitud = SolicitudesTorneo(
            id_torneo=id_torneo,
            id_equipo=id_equipo,
            estado="pendiente"
        )

        db.add(nueva_solicitud)
        db.commit()
        db.refresh(nueva_solicitud)

        return {"mensaje": "Solicitud enviada exitosamente"}

    except Exception as e:
        print("Error:", e)
        raise HTTPException(status_code=500, detail="el equipo ya envio solicitud.")
    
@app.put("/gestionarSolicitud/{id_solicitud}")
async def gestionar_solicitud(id_solicitud: int, estado: str, db: Session = Depends(get_db)):
    if estado not in ["aceptado", "rechazado"]:
        raise HTTPException(status_code=400, detail="Estado inválido")

    solicitud = db.query(SolicitudesTorneo).filter(SolicitudesTorneo.id_solicitud == id_solicitud).first()
    if not solicitud:
        raise HTTPException(status_code=404, detail="Solicitud no encontrada")

    # Solo el creador del torneo puede gestionar las solicitudes
    torneo = db.query(Torneos).filter(Torneos.id_torneo == solicitud.id_torneo).first()
    if not torneo:
        raise HTTPException(status_code=404, detail="Torneo no encontrado")

    if estado == "aceptado":
        # Actualizar el estado de la solicitud y el estado del torneo si es necesario
        solicitud.estado = "aceptado"
        if len([s for s in torneo.solicitudes if s.estado == "aceptado"]) >= torneo.numero_participantes:
            torneo.estado = "en juego"  # Por ejemplo, cambia el estado cuando se llena el número de participantes
    elif estado == "rechazado":
        solicitud.estado = "rechazado"

    db.commit()
    db.refresh(solicitud)

    return {"mensaje": f"Solicitud {estado} con éxito", "solicitud": solicitud.id_solicitud}


@app.get("/listartorneosi/{documento_creador}", response_model=List[Torneo])
async def listar_torneos(documento_creador: str, db: Session = Depends(get_db)):
    # Limpiar el documento del usuario a buscar
    documento_creador = documento_creador.strip()
    lista_Torneos = db.query(Torneos).filter(Torneos.Documento_Creador_Torneo == documento_creador).all() 
    if not lista_Torneos:
        raise HTTPException(status_code=404, detail="No hay Torneos disponibles para este creador")
    return lista_Torneos

@app.get("/solicitudes_pendientestorneo/{id_torneo}")
async def solicitudes_pendientestorneo(id_torneo: int, db: Session = Depends(get_db)):
    solicitudes = (
        db.query(SolicitudesTorneo, Equipos)
        .join(Equipos, SolicitudesTorneo.id_equipo == Equipos.Id_team)
        .filter(SolicitudesTorneo.id_torneo == id_torneo)
        .filter(SolicitudesTorneo.estado == "pendiente")
        .all()
    )

    if not solicitudes:
        return {"mensaje": "No hay solicitudes pendientes para este torneo."}

    resultado = []
    for solicitud, equipo in solicitudes:
        resultado.append({
            "id_solicitud": solicitud.id_solicitud,
            "id_equipo": equipo.Id_team,
            "nombre_equipo": equipo.nombreteam,
            "logo_equipo": equipo.logoTeam,
            "estado": solicitud.estado
        })

    return resultado

@app.get("/solicitudes_aceptadas/{id_torneo}")
async def solicitudes_aceptadas(id_torneo: int, db: Session = Depends(get_db)):
    solicitudes = (
        db.query(SolicitudesTorneo, Equipos)
        .join(Equipos, SolicitudesTorneo.id_equipo == Equipos.Id_team)
        .filter(SolicitudesTorneo.id_torneo == id_torneo)
        .filter(SolicitudesTorneo.estado == "aceptado")
        .all()
    )

    if not solicitudes:
        return {"mensaje": "No hay solicitudes aceptadas para este torneo."}

    resultado = []
    for solicitud, equipo in solicitudes:
        resultado.append({
            "id_solicitud": solicitud.id_solicitud,
            "id_equipo": equipo.Id_team,
            "nombre_equipo": equipo.nombreteam,
            "logo_equipo": equipo.logoTeam,
            "estado": solicitud.estado
        })

    return resultado

@app.get("/solicitudes_rechazadas/{id_torneo}")
async def solicitudes_rechazadas(id_torneo: int, db: Session = Depends(get_db)):
    solicitudes = (
        db.query(SolicitudesTorneo, Equipos)
        .join(Equipos, SolicitudesTorneo.id_equipo == Equipos.Id_team)
        .filter(SolicitudesTorneo.id_torneo == id_torneo)
        .filter(SolicitudesTorneo.estado == "rechazado")
        .all()
    )

    if not solicitudes:
        return {"mensaje": "No hay solicitudes rechazadas para este torneo."}

    resultado = []
    for solicitud, equipo in solicitudes:
        resultado.append({
            "id_solicitud": solicitud.id_solicitud,
            "id_equipo": equipo.Id_team,
            "nombre_equipo": equipo.nombreteam,
            "logo_equipo": equipo.logoTeam,
            "estado": solicitud.estado
        })

    return resultado
#------------------------------------------USUARIO----------------------------

# Endpoint GET para obtener todos los usuarios a diferencia de el usuario actual
@app.get("/usuarios/{documento_user}", response_model=list[clie])
async def obtener_usuarios(documento_user : str, db: Session = Depends(get_db)):
    documento_user = documento_user.strip().lower()
    # Consultar todos los registros de usuarios en la base de datos en excepcion a el que coincida con documento_user
    usuarios = db.query(Registro).filter(func.lower(Registro.documento)!=documento_user ).all()
    # Si no hay usuarios registrados, lanzar un error 404
    if not usuarios:
        raise HTTPException(status_code=404, detail="No se encontraron usuarios")

    # Devolver los usuarios encontrados
    return usuarios


@app.put("/usuarios/actualizar/{documento_user}")
def actualizar_equipo(
    documento_user: int,
    db: Session = Depends(get_db)
):
    
    # documento capitan conexion equipos
    equipo = db.query(Equipos).filter(Equipos.capitan_documento == documento_user).first()

    if not equipo:
        raise HTTPException(status_code=404, detail="No se encontró un equipo con ese documento de capitán")
    

    # documento tiene equipo tabla registro 
    usuario = db.query(Registro).filter(Registro.documento == documento_user).first()

    if not usuario:
        raise HTTPException(status_code=404, detail="No se encontró un usuario con ese documento")

    usuario.equipo_tiene = equipo.Id_team
    db.commit()
    db.refresh(usuario)

    return {"mensaje": "Equipo del usuario actualizado correctamente", "usuario": usuario}




# Configurar el manejador de Socket.IO
socket_manager = SocketManager(app=app, mount_location="/socket.io")

@app.post("/chat/send")
async def send_message(message: Message, db: Session = Depends(get_db)):
    # Obtener información del remitente
    sender = db.query(Registro).filter(Registro.documento == message.sender).first()
    if not sender:
        raise HTTPException(status_code=404, detail="Remitente no encontrado")

    # Crear el nuevo mensaje
    new_message = Mensajes(
        team_id=message.team_id,
        sender=message.sender,  # Aquí se guarda solo el documento del remitente
        content=message.content,
        timestamp=datetime.now()  # Agregar la hora actual
    )
    db.add(new_message)
    db.commit()
    db.refresh(new_message)

    # Emitir el mensaje en tiempo real a los clientes conectados
    await socket_manager.emit("nuevoMensaje", {
        "team_id": message.team_id,
        "sender": {
            "documento": sender.documento,
            "nombre": sender.nombre,
            "imagen": sender.imagen  # Cambia "imagen" a "profilePicture" si es necesario
        },
        "content": message.content,
        "timestamp": new_message.timestamp.strftime("%Y-%m-%d %H:%M:%S")  # Formatear la hora
    })

    return {"message": "Mensaje enviado correctamente"}


@app.post("/reportar_usuario/")
def reportar_usuario(
    documento_reportante: str = Form(...),
    documento_reportado: str = Form(...),
    motivo: str = Form(...),
    comentario: str = Form(...),
    db: Session = Depends(get_db)
):
    nuevo_reporte = ReporteUsuario(
        documento_reportante=documento_reportante,
        documento_reportado=documento_reportado,
        motivo=motivo,
        comentario=comentario,
        fecha_reporte=datetime.now()
    )
    db.add(nuevo_reporte)
    db.commit()
    db.refresh(nuevo_reporte)
    return {"mensaje": "Reporte enviado correctamente", "reporte_id": nuevo_reporte.id}

@app.get("/chat/{team_id}")
def get_messages(team_id: str, db: Session = Depends(get_db)):
    # Obtener los mensajes del equipo
    messages = db.query(Mensajes).filter(Mensajes.team_id == team_id).all()

    # Construir la respuesta con los datos del remitente
    response = []
    for message in messages:
        sender = db.query(Registro).filter(Registro.documento == message.sender).first()
        if not sender:
            # Si el remitente no existe, omitir el mensaje o manejarlo de otra forma
            print(f"⚠️ Remitente no encontrado para el mensaje con ID: {message.id}")
            continue

        response.append({
            "content": message.content,
            "timestamp": message.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
            "sender": {
                "documento": sender.documento,
                "nombre": sender.nombre,
                "imagen": sender.imagen
            }
        })

    return {"messages": response}

    
@app.websocket("/ws/{team_id}")
async def websocket_endpoint(websocket: WebSocket, team_id: int, db: Session = Depends(get_db)):
    await websocket.accept()
    await socket_manager.connect(websocket, team_id)

    try:
        while True:
            data = await websocket.receive_json()  # Se espera JSON del cliente
            documento = data.get("documento")  # ID del usuario que envía el mensaje
            contenido = data.get("content")

            if not documento or not contenido:
                await websocket.send_json({"error": "Datos incompletos"})
                continue

            sender = db.query(Registro).filter(Registro.documento == documento).first()
            if not sender:
                await websocket.send_json({"error": "Usuario no encontrado"})
                continue

            timestamp = datetime.now()

            # Guardar el mensaje en la base de datos (opcional)
            # new_message = Message(team_id=team_id, sender_id=documento, content=contenido, timestamp=timestamp)
            # db.add(new_message)
            # db.commit()

            # Emitir el mensaje a todos los clientes conectados al equipo
            await socket_manager.emit_to_team(team_id, "nuevoMensaje", {
                "team_id": team_id,
                "sender": {
                    "documento": sender.documento,
                    "nombre": sender.nombre,
                    "imagen": sender.imagen
                },
                "content": contenido,
                "timestamp": timestamp.strftime("%Y-%m-%d %H:%M:%S")
            })

    except WebSocketDisconnect:
        await socket_manager.disconnect(websocket, team_id)
        print(f"WebSocket desconectado para el equipo {team_id}")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

from uuid import uuid4

UPLOAD_DIR = "media/publicaciones"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post("/galeria/subir")
async def subir_publicacion(
    id_team: int = Form(...),
    descripcion: str = Form(...),
    tipo_media: str = Form(...),  # 'imagen' o 'video'
    archivo: UploadFile = File(...),
    db: Session = Depends(get_db)  # ⬅️ Esto es lo que te falta
):
    # Validar tipo de media
    if tipo_media not in ['imagen', 'video']:
        raise HTTPException(status_code=400, detail="Tipo de media inválido")

    # Guardar archivo con nombre único
    extension = archivo.filename.split('.')[-1]
    nombre_archivo = f"{uuid4()}.{extension}"
    ruta_archivo = os.path.join(UPLOAD_DIR, nombre_archivo)

    with open(ruta_archivo, "wb") as buffer:
        shutil.copyfileobj(archivo.file, buffer)

    url_final = f"/media/publicaciones/{nombre_archivo}"

    nueva_publicacion = GaleriaEquipo(
        id_team=id_team,
        descripcion=descripcion, 
        tipo_media=tipo_media,
        archivo_url=url_final
    )

    db.add(nueva_publicacion)
    db.commit()
    db.refresh(nueva_publicacion)

    return {"mensaje": "Publicación subida exitosamente", "publicacion": nueva_publicacion.id}

@app.get("/galeria/{id_team}")
def obtener_galeria(id_team: int, db: Session = Depends(get_db)):
    publicaciones = db.query(GaleriaEquipo).filter_by(id_team=id_team).all()
    return publicaciones
 
@app.delete("/galeria/{id_publicacion}")
def eliminar_publicacion(id_publicacion: int, db: Session = Depends(get_db)):
    publicacion = db.query(GaleriaEquipo).filter_by(id=id_publicacion).first()
    if not publicacion:
        raise HTTPException(status_code=404, detail="Publicación no encontrada")
    
    # Eliminar archivo del sistema (opcional)
    try:
        os.remove(publicacion.archivo_url.strip('/'))  # quitar la barra inicial si la tiene
    except:
        pass  # archivo ya no existe

    db.delete(publicacion)
    db.commit()
    return {"mensaje": "Publicación eliminada"}