<template>
    <div class="video-container">
      <div v-if="videos.length > 0">
        <div v-for="(video, index) in videos" :key="video.id" class="video-card">
          <video :src="video.url" controls></video>
          <div class="video-info">
            <p v-if="video.descripcion" class="description">{{ video.descripcion }}</p>
            <br>
            <p class="likes">
                <img class="likeee" src="../assets/imagenes/like.png" alt=""> {{ video.likes }} Likes
            </p>
          </div>
          <div class="menu">
            <button class="trespuntos" @click="toggleMenu(index)">Eliminar</button>
            <div v-if="menuIndex === index" class="dropdown">
              <button @click="confirmDelete(video.id)">🗑 Eliminar Video</button>
            </div>
            <br><br>
          </div>
        </div>
      </div>
      <p v-else class="no-videos">No hay videos disponibles.</p>
    </div>
  
    <div v-if="showConfirm" class="confirm-overlay">
      <div class="confirm-box">
        <p>¿Seguro que quieres eliminar el video "<strong>{{ videos.find(v => v.id === videoIdToDelete)?.descripcion || 'Sin descripción' }}</strong>"?</p>
        <div class="confirm-buttons">
          <button class="delete-btn" @click="deleteVideo">Sí, eliminar</button>
          <button class="cancel-btn" @click="showConfirm = false">Cancelar</button>
        </div>
      </div>
    </div>
  </template>
  <style scoped>
 .video-container {
  display:flex;
  flex-direction: row;
  gap: 20px; /* Espaciado entre elementos */
  justify-content: center; /* Centrar los elementos */
  align-items: start;
  width: 100%;
  max-width: 1200px; /* Limita el ancho máximo */
  margin: 0 auto; /* Centrar en la pantalla */
}

.video-card {
  width: 300px; /* Ajustar el tamaño de la tarjeta */
  max-width: 100%; 
  background: #000000;
  border-radius: 15px;
  padding: 15px;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.15);
  transition: transform 0.2s ease-in-out;
  border: solid white;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.video-card:hover {
  transform: scale(1.05);
}
.video-card video {
  width: 100%;
  height: 200px; /* Altura fija para todos */
  object-fit: cover; /* Recorta para ajustarse */
  border-radius: 10px;
}
.trespuntos{
    background-color: red;
    color: white;
    font-weight: bold;
    padding: 5px 10px;
    border-radius: 5px;
    text-shadow: 2px 2px 3px rgb(202, 0, 0); /* Agrega borde negro al texto */
    font-size: 16px;
    display: inline-block;
    border: solid white;
  }
  .video-info {
    width: 100%; /* Que ocupe todo el ancho de la tarjeta */
  overflow: hidden; /* Oculta el desbordamiento */
  text-overflow: ellipsis; /* Agrega "..." si el texto es muy largo */
  text-align: center;
  }
  .video-name {
    font-size: 18px;
    font-weight: bold;
    color: #333;
  }
  .description {
    font-size: 14px;
    color: #ffffff;
    margin-top: 5px;
    font-family:Verdana, Geneva, Tahoma, sans-serif;
  }
  .likes {
    font-size: 14px;
    color: #ffd152;
    font-weight: bold;
    margin-top: 5px;
  }
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
    z-index: 1000;
  }
  .likeee {
            width: 20px; 
            height: 20px; 
            border-radius: 50%; 
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
            transition: transform 0.3s ease;
        }
        .likeee:hover {
            transform: scale(1.1); 
        }
  .confirm-box {
    background: white;
    padding: 20px;
    border-radius: 10px;
    text-align: center;
    box-shadow: 0 5px 15px rgba(0, 0, 0, 0.3);
    width: 320px;
    position: relative;
    z-index: 1100; 
  }
  .confirm-box p {
    font-size: 16px;
    color: #333;
  }
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
  .no-videos{
    font-size: 30px;
    color: rgb(177, 177, 177);
  }
  </style>
    <script>
    import { useUsuarios } from "@/stores/usuario";
    import { watch, onMounted, ref } from "vue";
    import axios from "axios";
    
    export default {
      setup() {
        const videos = ref([]);
        const menuIndex = ref(null);
        const showConfirm = ref(false);
        const videoIdToDelete = ref(null);
        const movistore = useUsuarios();
    
        const getUrlvideo = (path) => path?.startsWith("http") ? path : `http://127.0.0.1:8000/${path}`;
    
        const cargarVideos = async () => {
          const documento = movistore.usuario.documento;
          console.log(movistore.usuario.documento)
          if (!documento) {
            console.error("❌ No hay un documento de usuario disponible.");
            return;
          }
          try {
            console.log("🔍 Consultando videos del usuario con documento:", documento);
            const response = await axios.get(`http://127.0.0.1:8000/listarvideosdef/${documento}`);
            console.log("✅ Respuesta de la API:", response.data);
    
            videos.value = response.data.map(video => ({
              id: video.id,
              url: getUrlvideo(video.url ?? "default.mp4"),
              descripcion: video.description?.trim() || "Sin descripción",
              likes: Number(video.likes) || 0,
            }));
    
            console.log("📜 Lista final de videos:", videos.value);
          } catch (error) {
            console.error("❌ Error al cargar los videos:", error.response?.data || error);
          }
        };
    
        const toggleMenu = (index) => {
          menuIndex.value = menuIndex.value === index ? null : index;
        };
    
        const confirmDelete = (id) => {
          videoIdToDelete.value = id;
          showConfirm.value = true;
          console.log("📌 ID a eliminar:", videoIdToDelete.value);
        };
    
        const deleteVideo = async () => {
          if (!videoIdToDelete.value) {
            console.error("🚨 Error: No hay un ID válido para eliminar.");
            return;
          }
    
          try {
            console.log("🗑️ Eliminando video con ID:", videoIdToDelete.value);
            await axios.delete(`http://127.0.0.1:8000/eliminarvideo/${videoIdToDelete.value}`);
            
            // Recargar la lista después de la eliminación
            await cargarVideos();
            console.log("✅ Video eliminado correctamente");
          } catch (error) {
            console.error("❌ Error al eliminar el video:", error);
          }
    
          showConfirm.value = false;
          videoIdToDelete.value = null;
        };
    
        onMounted(cargarVideos);
    
        watch(() => movistore.usuario?.documento, (nuevoDocumento) => {
          if (nuevoDocumento) {
            console.log("🔄 Documento actualizado:", nuevoDocumento);
            cargarVideos();
          }
        }, { immediate: true });
    
        return {
          videos,
          menuIndex,
          showConfirm,
          videoIdToDelete,
          toggleMenu,
          confirmDelete,
          deleteVideo,
        };
      },
    };
    
    </script>