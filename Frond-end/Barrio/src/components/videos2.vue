<template>
  <div class="video-container">
    <div v-if="videos.length > 0">
      <div v-for="(video, index) in videos" :key="index" class="video-card">
        <video :src="video.url" controls></video>
        <div class="video-info">
          <p class="description">{{ video.descripcion }}</p>
          <p class="likes">❤️ {{ video.likes }} Likes</p>
        </div>
        <div class="menu">
          <button @click="toggleMenu(index)">⋮</button>
          <div v-if="menuIndex === index" class="dropdown">
            <button @click="confirmDelete(index)">🗑 Eliminar Video</button>
          </div>
        </div>
      </div>
    </div>
    <p v-else class="no-videos">No hay videos disponibles.</p>
  </div>

  <div v-if="showConfirm" class="confirm-overlay">
    <div class="confirm-box">
      <p>¿Seguro que quieres eliminar el video "<strong>{{ videos[videoToDelete]?.descripcion }}</strong>"?</p>
      <div class="confirm-buttons">
        <button class="delete-btn" @click="deleteVideo">Sí, eliminar</button>
        <button class="cancel-btn" @click="showConfirm = false">Cancelar</button>
      </div>
    </div>
  </div>
</template>


<script>
import { useUsuarios } from "@/stores/usuario";
import { watch, onMounted, ref } from "vue";
import axios from "axios";

export default {
  setup() {
    const videos = ref([]);
    const defaultVideo = "default.mp4";
    const menuIndex = ref(null);
    const showConfirm = ref(false);
    const videoToDelete = ref(null);
    const storeUsuario = useUsuarios();

    const getUrlvideo = (path) => {
      return path.startsWith("http") ? path : `http://127.0.0.1:8000/${path}`;
    };

    const cargarVideos = async () => {
      const documento = storeUsuario.usuario?.documento;
      if (!documento) {
        console.error("❌ No hay un documento de usuario disponible.");
        return;
      }

      try {
        console.log("🔍 Consultando videos del usuario con documento:", documento);
        const response = await axios.get(`http://127.0.0.1:8000/listarvideosdef/${documento}`);
        console.log("✅ Respuesta de la API:", response.data);

        videos.value = response.data.map(video => ({
          url: getUrlvideo(video.url || defaultVideo),
          descripcion: video.descripcion || "Sin descripción",
          likes: video.likes || 0,
        }));
      } catch (error) {
        console.error("❌ Error al cargar los videos:", error);
      }
    };

    const toggleMenu = (index) => {
      menuIndex.value = menuIndex.value === index ? null : index;
    };

    const confirmDelete = (index) => {
      videoToDelete.value = index;
      showConfirm.value = true;
    };

    const deleteVideo = () => {
      if (videoToDelete.value !== null) {
        videos.value.splice(videoToDelete.value, 1);
      }
      showConfirm.value = false;
      videoToDelete.value = null;
    };

    onMounted(() => {
      cargarVideos();
    });

    watch(
      () => storeUsuario.usuario?.documento,
      async (nuevoDocumento) => {
        if (nuevoDocumento) {
          console.log("🔄 Documento actualizado:", nuevoDocumento);
          await cargarVideos();
        }
      },
      { immediate: true }
    );

    return {
      videos,
      defaultVideo,
      menuIndex,
      showConfirm,
      videoToDelete,
      toggleMenu,
      confirmDelete,
      deleteVideo,
    };
  },
};
</script>


<style scoped>

.video-container {
display: flex;
flex-wrap: wrap; /* Para que pasen a la siguiente línea si no caben */
gap: 10px; /* Espacio entre los videos */
padding: 20px;
justify-content: center; /* Centra los videos */
}

.video-card {
flex: 0 1 calc(33.33% - 20px); /* Ocupa 1/3 del ancho con espacio entre ellos */
max-width: 300px; /* Controla el tamaño máximo */
background: #f9f9f9;
border-radius: 15px;
padding: 15px;
box-shadow: 0 5px 15px rgba(0, 0, 0, 0.15);
transition: transform 0.2s ease-in-out;
}

.video-card:hover {
transform: scale(1.05);
}

.video-card video {
width: 100%;
border-radius: 10px;
}


/* Información del video */
.video-info {
  margin-top: 10px;
  text-align: center;
}

.video-name {
  font-size: 18px;
  font-weight: bold;
  color: #333;
}

.description {
  font-size: 14px;
  color: #666;
  margin-top: 5px;
}

.likes {
  font-size: 14px;
  color: #ff5252;
  font-weight: bold;
  margin-top: 5px;
}

/* Menú de opciones */
.menu {
  position: absolute;
  top: 10px;
  right: 10px;
}

.menu button {
  background: none;
  border: none;
  font-size: 20px;
  cursor: pointer;
}

.dropdown {
  position: absolute;
  top: 25px;
  right: 0;
  background: white;
  border-radius: 5px;
  box-shadow: 0 3px 10px rgba(0, 0, 0, 0.2);
  padding: 5px;
}

.dropdown button {
  background: none;
  border: none;
  cursor: pointer;
  padding: 8px 12px;
  font-size: 14px;
  width: 100%;
  transition: background 0.2s;
}

.dropdown button:hover {
  background: #ff5252;
  color: white;
}

/* Fondo de la ventana de confirmación */
.confirm-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  animation: fadeIn 0.3s ease-in-out;
  z-index: 1000; /* Asegura que esté por encima de todo */
}

/* Ventana de confirmación */
.confirm-box {
  background: white;
  padding: 20px;
  border-radius: 10px;
  text-align: center;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.3);
  width: 320px;
  position: relative;
  z-index: 1100; /* Más alto que el overlay */
}

.confirm-box p {
  font-size: 16px;
  color: #333;
}

/* Botones de la confirmación */
.confirm-buttons {
  margin-top: 15px;
}

.confirm-buttons button {
  margin: 5px;
  padding: 8px 15px;
  border: none;
  border-radius: 5px;
  font-size: 14px;
  cursor: pointer;
  transition: transform 0.2s;
}

.delete-btn {
  background: #ff5252;
  color: white;
}

.cancel-btn {
  background: gray;
  color: white;
}

.confirm-buttons button:hover {
  transform: scale(1.05);
}

/* Animación de entrada */
@keyframes fadeIn {
  from {
    opacity: 0;
    transform: scale(0.9);
  }
  to {
    opacity: 1;
    transform: scale(1);
  }
}

</style>

  