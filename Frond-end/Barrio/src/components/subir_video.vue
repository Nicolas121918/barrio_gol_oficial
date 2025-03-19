<template>
  <header>
    <headerapp></headerapp>
  </header>
  <router-link to="/videos" class="volver">
    <button class="volver-button">Volver</button>
  </router-link>
  <div class="video">
    <h1>¡Sube Aquí Tu Video!</h1>
    <form @submit.prevent="subirVideo">
      <input class="selectvideo" type="file" accept="video/*" @change="seleccionarVideo" />
      <input class="desct" type="text" v-model="descripcion" placeholder="Añade una descripción" />
      <button type="submit" class="subirboton">Subir Video</button>
    </form>

    <!-- Mostrar el video cargado -->
    <div v-if="videoUrl" class="video-preview">
      <video controls :src="videoUrl" width="400"></video>
  
    </div>

    <!-- Mensaje de estado -->
    <div v-if="mensaje" class="mensaje">
      {{ mensaje }}
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";
import axios from "axios";
import { useUsuarios } from "@/stores/usuario";
import { useRouter } from "vue-router"; // Importar useRouter

// Store de usuario
const usuarioStore = useUsuarios();
const router = useRouter(); // Crear una instancia del router
const videoSeleccionado = ref(null);
const videoUrl = ref(null); // URL para mostrar el video
const mensaje = ref("");
const correo_usuario = ref(usuarioStore.usuario.correo); // Obtener correo del usuario
const descripcion = ref(""); // Nueva variable para la descripción

const seleccionarVideo = (event) => {
  videoSeleccionado.value = event.target.files[0];
  videoUrl.value = URL.createObjectURL(videoSeleccionado.value); // Genera la URL del video
};

const eliminarVideo = () => {
  videoSeleccionado.value = null;
  videoUrl.value = null; // Eliminar el video y su URL
};

const cambiarVideo = () => {
  videoSeleccionado.value = null;
  videoUrl.value = null; // Permitir cargar un nuevo video
};

const subirVideo = async () => {
  if (!videoSeleccionado.value) {
    mensaje.value = "Por favor selecciona un video.";
    return;
  }

  if (!descripcion.value.trim()) {
    mensaje.value = "Por favor ingresa una descripción.";
    return;
  }

  const formData = new FormData();
  formData.append("video", videoSeleccionado.value);
  formData.append("correo", correo_usuario.value);
  formData.append("descripcion", descripcion.value); // Enviar la descripción

  try {
    const response = await axios.post("http://localhost:8000/subirvideo", formData, {
      headers: {
        "Content-Type": "multipart/form-data",
      },
    });

    // Mostrar la alerta con el mensaje de éxito
    alert("¡El video se subió correctamente!");

    // Limpiar los campos después de subir el video
    videoSeleccionado.value = null;
    videoUrl.value = null; // Limpiar video y URL
    descripcion.value = ""; // Limpiar la descripción después de subir

    // Redirigir al componente anterior (por ejemplo, a la página de videos)
    setTimeout(() => {
      router.push("/videos"); // Cambia "/videos" por la ruta que desees
    }, 2000); // Espera 2 segundos para mostrar la alerta antes de redirigir
  } catch (error) {
    console.error(error);
    mensaje.value = "Ocurrió un error al subir el video.";
  }
};
</script>

<style scoped>
/* Estilo para el contenedor del video */
.video {
  background: linear-gradient(135deg, rgba(84, 82, 76, 0.55), rgba(18, 18, 4, 0.21));
  border-radius: 12px;
  padding: 2.5rem;
  box-shadow: 0 15px 30px rgba(0, 0, 0, 0.2);
  max-width: 500px;
  width: 100%;
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  text-align: center;
  backdrop-filter: blur(6px);
  display: flex;
  flex-direction: column;
  gap: 20px;
  box-sizing: border-box;
  color: #ffffff;
  max-height: 700px;
  overflow: hidden;
  font-family: 'Arial', sans-serif; /* Mejora la tipografía */
}

/* Estilo para el video en el contenedor */
video {
  max-width: 100%;
  max-height: 400px;
  object-fit: cover;
  border-radius: 10px;
}

/* Estilo para el título */
h1 {
  font-size: 2rem;
  color: #fff;
  margin-bottom: 20px;
  font-weight: 600;
  font-family: 'Roboto', sans-serif;
}

/* Estilo para el selector de video */
.selectvideo {
  background-color: #847d20;
  padding: 10px;
  font-size: 16px;
  color: white;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.selectvideo:hover {
  background-color: #6d6b19;
}

/* Estilo para el formulario */
form {
  display: flex;
  flex-direction: column;
  gap: 20px;
  width: 100%;
}

/* Estilo para el campo de archivo */
input[type="file"] {
  padding: 14px;
  border-radius: 8px;
  border: 2px solid #ccc;
  background-color: #f7f7f7;
  font-size: 16px;
  width: 100%;
  box-sizing: border-box;
  transition: border-color 0.3s ease;
}

input[type="file"]:hover {
  border-color: #777;
}

/* Estilo para el botón */
.subirboton {
  padding: 14px 20px;
  background-color: #000000;
  background-image: url('https://i.pinimg.com/736x/82/77/8d/82778d6d72c05cf2808e3bd2bcaeb823.jpg');
  background-size: cover;
  background-position: center;
  color: #fff;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-size: 16px;
  transition: background-color 0.3s ease, transform 0.3s ease;
  width: 50%;
  margin: 0 auto;
}

.subirboton:hover {
  transform: scale(1.1);
  background-color: #333;
}

/* Estilo para el mensaje */
.mensaje {
  margin-top: 20px;
  padding: 12px;
  border-radius: 8px;
  background-color: #f7e0e0;
  color: #000;
  text-align: center;
  font-size: 14px;
  font-family: 'Arial', sans-serif;
}

/* Estilo para el mensaje de error */
.mensaje.error {
  background-color: #f8d7da;
  color: #842029;
  border-color: #842029;
}

/* Estilo para el botón de volver */
.volver {
  position: absolute;
  top: 150px;
  left: 10px;
  z-index: 1000;
}

  .volver-button {
  padding: 10px 20px;
  background-color: #ff04008b;
  font-weight: bold;
  color: rgb(255, 255, 255);
  border: none;
  width: 100px;
  border-radius: 5px;
  font-size: 16px;
  cursor: pointer;
  transition: transform 0.3s ease;
}

.volver-button:hover {
  transform: scale(1.1);
}

/* Estilo para los botones de eliminar y cambiar video */
.eliminar-video, .cambiar-video {
  margin-top: 10px;
  padding: 8px 16px;
  cursor: pointer;
  border-radius: 5px;
  color: white;
  font-weight: bold;
  font-size: 16px;
}

.eliminar-video {
  background-color: #ff4d4d;
}

.cambiar-video {
  background-color: #007bff;
}

.eliminar-video:hover {
  background-color: #e60000;
}

.cambiar-video:hover {
  background-color: #0056b3;
}

.desct {
  padding: 12px 20px;
  border-radius: 8px; /* Bordes redondeados */
  border: 2px solid #ccc; /* Borde gris claro */
  background-color: #f7f7f7; /* Fondo gris suave */
  font-size: 16px; /* Tamaño de fuente adecuado */
  width: 100%; /* Ocupa el 100% del ancho */
  box-sizing: border-box; /* Para no afectar el tamaño total */
  transition: all 0.3s ease; /* Transición suave para el borde y sombra */
  color: #333; /* Color de texto oscuro */
  font-family: 'Roboto', sans-serif; /* Tipografía más moderna */
  text-align: center;
}

.desct::placeholder {
  color: #aaa; /* Color del texto del placeholder */
  font-style: italic; /* Estilo en cursiva para el placeholder */
}

/* Estilo para cuando el campo está en foco */
.desct:focus {
  border-color: #3498db; /* Borde azul claro cuando está en foco */
  box-shadow: 0 0 8px rgba(52, 152, 219, 0.5); /* Sombra sutil en azul */
  outline: none; /* Elimina el borde por defecto */
}

.desct:hover {
  border-color: #888; /* Cambia el borde a gris más oscuro al pasar el ratón */
}
</style>
