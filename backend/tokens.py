from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException
from jose import JWTError, jwt

# Configuración del esquema de autenticación
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

SECRET_KEY = "SECRET_KEY"  # Cambia esto por tu clave secreta
ALGORITHM = "HS256"  # Algoritmo utilizado para firmar el token

# Función para extraer el documento del token
def obtener_documento_usuario(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        documento = payload.get("documento")
        if documento is None:
            raise HTTPException(status_code=401, detail="Token inválido")
        return documento
    except JWTError:
        raise HTTPException(status_code=401, detail="No se pudo validar el token")
