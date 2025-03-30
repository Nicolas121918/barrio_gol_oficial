from fastapi import FastAPI,UploadFile,File ,Form , Depends, HTTPException, Query,WebSocket
from sqlalchemy.orm import Session
import bcrypt
import uvicorn
from pydantic import BaseModel
from fastapi_socketio import SocketManager
from conexion import engine, get_db
from modelo import Base, Contacto,Jugador,Contacto_usuarios,Equipos, ReporteUsuario,UserVideos,Torneos,partidos,Equipos,Registro,Messages as Mensajes
from schemas import RegistroBase as clie,LoginRequest, ReporteUsuarioSchema
from schemas import ContactForm
from schemas import Contactousuers
from modelo import GaleriaEquipo
from schemas import JugadorForm
from schemas import DatosTeams,Message
from modelo import Like
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
    reglas: Optional[str] = Form(None),         # NUEVO CAMPO
    como_llegar: Optional[str] = Form(None),    # NUEVO CAMPO
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
            equipo_visitante=None,
            estado_partido="en_proceso",
            ganador=None,
            Documento_Creador_P=Documento_Creador_P,
            logomatch=logomatch_path,
            imagen_cancha=imagen_cancha_path,
            reglas=reglas,                   # ← Nuevo
            como_llegar=como_llegar         # ← Nuevo
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


@app.get("/equipos/es_capitan/{documento}", response_model=bool)
async def es_capitan(documento: int, db: Session = Depends(get_db)):
    equipo = db.query(Equipos).filter(Equipos.capitan_documento == documento).first()
    return equipo is not None

## Endpoint para lista los equipos
@app.get("/listarteams", response_model=list[DatosTeams])
async def listar_clientes(db: Session = Depends(get_db)):
    return db.query(Equipos).all()  # Listado sin error

@app.delete("/equipos/eliminar/{id_equipo}")
async def eliminar_equipo(
    id_equipo: int,
    db: Session = Depends(get_db)
):
    # Buscar el equipo en la base de datos
    equipo = db.query(Equipos).filter(Equipos.Id_team == id_equipo).first()
    if not equipo:
        raise HTTPException(status_code=404, detail="Equipo no encontrado")

    # Desasociar a todos los miembros del equipo
    db.query(Registro).filter(Registro.equipo_tiene == id_equipo).update({"equipo_tiene": 0})

    # Eliminar el equipo
    db.delete(equipo)
    db.commit()
    return {"mensaje": f"El equipo {equipo.nombreteam} ha sido eliminado y todos los miembros quedaron sin equipo"}



## endpoint para listar nombre de  equipos
@app.get("/equipo/lista", response_model=List[str])
async def listar_equipos(db: Session = Depends(get_db)):
    lista_Equipos = db.query(Equipos.nombreteam).all() 
    if not lista_Equipos:
        raise HTTPException(status_code=404, detail="No hay Equipos Todavia")
    return [equipo.nombreteam for equipo in lista_Equipos]  


@app.get('/verificar-equipo/{id_usuario}')
def verificar_equipo(id_usuario: int, db: Session = Depends(get_db)):
    equipo = db.query(Equipos).filter(Equipos.id_usuario == id_usuario).first()
    if equipo:
        return {"asociado": True, "Id_team": equipo.Id_team, "nombreteam": equipo.nombreteam}
    return {"asociado": False}

@app.post("/equipos/unirse")
async def unirse_equipo(
    documento_user: str = Form(...),  # Cambio de int a str porque documento es string
    id_equipo: int = Form(...),
    db: Session = Depends(get_db)
):
    # Verificar si el usuario existe
    usuario = db.query(Registro).filter(Registro.documento == documento_user).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    # Verificar si el equipo existe
    equipo = db.query(Equipos).filter(Equipos.Id_team == id_equipo).first()  # Asegurar que usas la columna correcta
    if not equipo:
        raise HTTPException(status_code=404, detail="Equipo no encontrado")

    # Verificar si el usuario ya está en un equipo
    if usuario.equipo_tiene and usuario.equipo_tiene != 0:
        raise HTTPException(status_code=400, detail="El usuario ya pertenece a un equipo")

    # Asociar usuario al equipo
    usuario.equipo_tiene = equipo.Id_team  # Actualizar con el ID correcto
    db.commit()

    return {"mensaje": f"{usuario.nombre} se ha unido al equipo {equipo.nombreteam}"}


""" @app.get("/equipos/{id_equipo}/lider", response_model=dict)
async def obtener_lider_equipo(id_equipo: int, db: Session = Depends(get_db)):
    equipo = db.query(Equipos).filter(Equipos.Id_team == id_equipo).first()
    if not equipo:
        raise HTTPException(status_code=404, detail="Equipo no encontrado")

    if not equipo.capitan:  
        raise HTTPException(status_code=404, detail="Líder del equipo no encontrado en la base de datos")

    return {
        "lider": {
            "nombre": equipo.capitan.nombre,
            "documento": equipo.capitan.documento,
            "correo": equipo.capitan.correo,
            "telefono": equipo.capitan.celular,
        }
    }
 """




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

    return {"mensaje": f"has salido del equipo"}

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
    
@app.get("/equipos/{id_equipo}/miembros")
async def listar_miembros(id_equipo: int, db: Session = Depends(get_db)):
    miembros = db.query(Registro).filter(Registro.equipo_tiene == id_equipo).all()
    if not miembros:
        raise HTTPException(status_code=404, detail="Este equipo no tiene miembros")
    return [{"nombre": miembro.nombre, "documento": miembro.documento} for miembro in miembros]

@app.get("/equipos_traer/{id_equipo}", response_model=DatosTeams)
async def obtener_equipo(id_equipo: int, db: Session = Depends(get_db)):
    equipo = db.query(Equipos).filter(Equipos.Id_team == id_equipo).first()
    if not equipo:
        raise HTTPException(status_code=404, detail="Equipo no encontrado")
    return equipo

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
# Endpoint para crear torneos
@app.post("/crearTorneo")
async def crear_torneo(
    correo_usuario: str = Form(...),

    # Información básica
    nombre: str = Form(...),
    tipo: str = Form(...),
    categoria: str = Form(...),
    formato: str = Form(...),

    # Fechas
    fecha_inicio: str = Form(...),
    fecha_final: str = Form(...),
    fecha_limite_inscripcion: str = Form(...),
    # dias_de_juego: str = Form(...),

    # Participación y reglas
    descripcion_reglas: str = Form(...),
    cantidad_participantes: int = Form(...),
    requiere_uniforme: str = Form(...),
    duracion_partido: str = Form(...),
    # organizacion_partidos: str = Form(...),

    # Ubicación
    direccion: str = Form(...),
    descripcion_llegada: str = Form(...),
    #ubicacion_mapa: str = Form(...),

    # Archivos
    imagen_torneo: UploadFile = File(...),
    foto_cancha: UploadFile = File(...),
    #logoTeam: UploadFile = File(...),

    # Costos y premios
    precioInscripcion: float = Form(...),
    precioArbitrajeTorneo: float = Form(...),
    #apuestaTorneo: float = Form(...),
    premio_principal: str = Form(...),
    premios_adicionales: Optional[str] = Form(None),

    db: Session = Depends(get_db)
):
    # Buscar al usuario en la base de datos
    usuario = db.query(Registro).filter(Registro.correo.ilike(correo_usuario.strip())).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    # Guardar archivos
    os.makedirs("archivos_torneos", exist_ok=True)

    '''ruta_logo = f"archivos_torneos/{logoTeam.filename}"
    with open(ruta_logo, "wb") as buffer:
        buffer.write(await logoTeam.read())'''

    ruta_imagen_torneo = f"archivos_torneos/{imagen_torneo.filename}"
    with open(ruta_imagen_torneo, "wb") as buffer:
        buffer.write(await imagen_torneo.read())

    ruta_foto_cancha = f"archivos_torneos/{foto_cancha.filename}"
    with open(ruta_foto_cancha, "wb") as buffer:
        buffer.write(await foto_cancha.read())

    # Crear el torneo
    nuevo_torneo = Torneos(
        nombre=nombre,
        tipo=tipo,
        categoria=categoria,
        formato=formato,

        fecha_inicio=fecha_inicio,
        fecha_final=fecha_final,
        fecha_limite_inscripcion=fecha_limite_inscripcion,
        #dias_de_juego=dias_de_juego,

        cantidad_participantes=cantidad_participantes,
        requiere_uniforme=requiere_uniforme,
        descripcion_reglas=descripcion_reglas,
        duracion_partido=duracion_partido,
        # organizacion_partidos=organizacion_partidos,

        direccion=direccion,
        descripcion_llegada=descripcion_llegada,
        #ubicacion_mapa=ubicacion_mapa,

        imagen_torneo=ruta_imagen_torneo,
        foto_cancha=ruta_foto_cancha,
        #logoTeam=ruta_logo,

        precioInscripcion=precioInscripcion,
        precioArbitrajeTorneo=precioArbitrajeTorneo,
        #apuestaTorneo=apuestaTorneo,
        premio_principal=premio_principal,
        premios_adicionales=premios_adicionales,

        Documento_Creador_Torneo=usuario.documento,
        Nombre_Creador_Torneo=usuario.nombre
    )

    db.add(nuevo_torneo)
    db.commit()
    db.refresh(nuevo_torneo)

    return {"mensaje": "Torneo creado exitosamente", "id": nuevo_torneo.id_Torneo}



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



@app.get("/listartorneos/{excluir_id}", response_model=List[Torneo])
async def listar_torneos(excluir_id: str, db: Session = Depends(get_db)):
    # Limpiar el nombre del usuario a excluir
    excluir_id = excluir_id.strip().lower()
    lista_Torneos = db.query(Torneos).filter(func.lower(Torneos.Nombre_Creador_Torneo) != excluir_id).all() 

    if not lista_Torneos:
        raise HTTPException(status_code=404, detail="No hay Torneos disponibles")
    return lista_Torneos



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
        PartidosModel.estado_partido.in_(["en_proceso", "jugando"])
    ).all()

    if not resultados:
        raise HTTPException(status_code=404, detail="No hay partidos en espera para este usuario.")
    return resultados

  # lista los torneos de un usuario
@app.get("/listartorneosi/{documento_creador}", response_model=List[Torneo])
async def listar_torneos(documento_creador: str, db: Session = Depends(get_db)):
    # Limpiar el documento del usuario a buscar
    documento_creador = documento_creador.strip()
    lista_Torneos = db.query(Torneos).filter(Torneos.Documento_Creador_Torneo == documento_creador).all() 
    if not lista_Torneos:
        raise HTTPException(status_code=404, detail="No hay Torneos disponibles para este creador")
    return lista_Torneos


@app.get("/listarpartidosi/{id_partido}", response_model=List[Partidos])
async def listar_partidos(id_partido: int, db: Session = Depends(get_db)):
    lista_Partidos = db.query(partidos).filter(partidos.id_Partido == id_partido).all()
    if not lista_Partidos:
        raise HTTPException(status_code=404, detail="No hay partidos disponibles con ese ID")
    return lista_Partidos






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

""" Guardar y enviar mensajes en tiempo real """
@app.post("/chat/send")
async def send_message(message: Message, db: Session = Depends(get_db)):
    new_message = Mensajes(
        team_id=message.team_id,
        sender=message.sender,
        content=message.content
    )
    db.add(new_message)
    db.commit()
    db.refresh(new_message)

    # Emitir el mensaje en tiempo real a los clientes conectados
    await socket_manager.emit("nuevoMensaje", {
        "team_id": message.team_id,
        "sender": message.sender,
        "content": message.content
    })

    return {"message": "Mensaje enviado correctamente"}


@app.post("/reportar_usuario/")
def reportar_usuario(reporte: ReporteUsuarioSchema, db: Session = Depends(get_db)):
    nuevo_reporte = ReporteUsuario(
        documento_reportado=reporte.documento_reportado,
        documento_reportante=reporte.documento_reportante,
        motivo=reporte.motivo,
        comentario=reporte.descripcion,
        fecha_reporte=reporte.fecha_reporte
    )
    db.add(nuevo_reporte)
    db.commit()
    db.refresh(nuevo_reporte)
    return {"mensaje": "Reporte enviado correctamente", "reporte_id": nuevo_reporte.id}

""" Obtener los mensajes de un equipo """
@app.get("/chat/{team_id}")
def get_messages(team_id: int, db: Session = Depends(get_db)):
    messages = db.query(Mensajes).filter(Mensajes.team_id == team_id).all()
    return {"messages": messages}




""" WebSocket para recibir mensajes en tiempo real """
@app.websocket("/ws/{team_id}")
async def websocket_endpoint(websocket: WebSocket, team_id: int):
    await websocket.accept()
    await socket_manager.connect(websocket)

    try:
        while True:
            data = await websocket.receive_text()
            message = {"team_id": team_id, "content": data}

            """ emit funcion para emitir los mensajes a todos los usuarios conectados a el equipo En tiempo real
            sin recargar pagina """
            await socket_manager.emit("nuevoMensaje", message)
    except:
        await socket_manager.disconnect(websocket)

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

    url_final = f"/{UPLOAD_DIR}/{nombre_archivo}"  # esto depende si sirves archivos estáticos

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