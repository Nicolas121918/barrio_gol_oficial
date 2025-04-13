
<template>
   <header>

    <!-- Header de escritorio -->
    <div class="d-none d-md-block">
      <Headerapp></Headerapp>
    </div>

    <!-- Header para móviles -->
    <div class="d-block d-md-none">
      <headermobile></headermobile>
    </div>

  </header>
  <div class="app-container">
    <div class="video-feed" @wheel="handleScroll">
      <transition-group name="slide" tag="div" class="video-list">
        <div
          v-for="(video, index) in videosurls"
          :key="video.url"
          class="video-container"
          v-show="currentIndex === index"
        >
          <video
            ref="videoPlayer"
            :src="getUrlvideo(video.url)"
            class="video"
            :autoplay="currentIndex === index"
            :loop="true"
            :muted="false"
            @click="togglePlayPause(index)"
          ></video>
          
          <div class="video-info">
            <button  class="profile-button" @click="verPerfil(video.documento)">
      <div class="top-section">
        <img :src="getProfilePic(video.uploaderProfilePic)" alt="Profile" class="profile-pic" /> 
        <h2 class="uploader-name">{{ video.uploaderName }}</h2>
      </div>
      <p class="descripcion">descripcion video:</p>
      <p class="descripcion2">{{ video.description }}</p>
    </button> 
    <div class="video-actions">
      <div class="video-actions">
        <button
  @click="likeVideo(index)"
  class="like-button"
  :class="{'zoom-in': likedIndex === index}"
>
  <img 
    :src="likedVideos[video.id] 
      ? '/imagenes/balondeoro.png' 
      : '/imagenes/corazon.png'" 
    alt="Like"
    class="like-icon"
    @error="setFallback(video.id)"
  />
  {{ video.likes }}
</button>


            </div>
    </div>
  </div>
        </div>
      </transition-group>
    </div>
    <div class="video-navigation">
      <button @click="previousVideo" :disabled="currentIndex === 0">⬆</button>
      <button @click="nextVideo" :disabled="currentIndex === videosurls.length - 1">⬇</button>
    </div>
    <button class="upload-video-button" @click="subirVideo">
  <router-link to="/subirvideo" style="text-decoration: none; color: inherit;">
    Subir Videos
  </router-link>
</button>
  </div>
</template>
<script>
import axios from "axios";
import Headerapp from "./Headerapp.vue";
import headermobile from "./headermobile.vue";
import { useUsuarios } from "@/stores/usuario";
export default {
  components: {
    Headerapp,
    headermobile,
  },
  data() {
    return {
      videosurls: [],
      currentIndex: 0,
      likedVideos: {},
      balonDeOro: '../assets/imagenes/like.png',
      balonGris: '../assets/imagenes/borrar.png',
    };
  },
  computed: {
    currentVideo() {
      return this.videosurls[this.currentIndex] || null;
    },
  },
  mounted() { 
    this.getvideosurl();
    this.loadLikedVideos();
  },
  methods: {
    handleScroll(event) {
      event.deltaY > 0 ? this.nextVideo() : this.previousVideo();
    },
    verPerfil(documento) {
    this.$router.push(`/perfiles/${documento}`); // Redirige usando el documento
  },
    nextVideo() {
      if (this.currentIndex < this.videosurls.length - 1) {
        this.currentIndex++;
        this.playCurrentVideo();
      }
    },
    setFallback(videoId) {
    this.likedVideos[videoId] = this.likedVideos[videoId] 
      ? this.balonDeOro 
      : this.balonGris;
  },
    previousVideo() {
      if (this.currentIndex > 0) {
        this.currentIndex--;
        this.playCurrentVideo();
      }
    },
    getProfilePic(path) {
  // Si hay una ruta, devuelve la URL completa; de lo contrario, usa la imagen por defecto
  return path 
    ? `http://127.0.0.1:8000/${path}` 
    : "default.png";
},

    pauseOthers(currentIndex) {
      if (this.$refs.videoPlayer) {
        this.$refs.videoPlayer.forEach((video, index) => {
          if (index !== currentIndex && video) {
            video.pause();
          }
        });
      }
    },
    playCurrentVideo() {
      if (this.$refs.videoPlayer) {
        const video = this.$refs.videoPlayer[this.currentIndex];
        if (video) {
          video.play();
        }
        this.pauseOthers(this.currentIndex);
      }
    },
    togglePlayPause(index) {
      const video = this.$refs.videoPlayer[index];
      if (video) {
        video.paused ? video.play() : video.pause();
      }
      this.pauseOthers(index);
    },
    async likeVideo(index) {
  const movistore = useUsuarios();
  if (!movistore.usuario.documento) {
    console.error("⚠ No se encontró un usuario válido en el store.");
    return;
  }

  const video = this.videosurls[index];
  try {
    // Alternar el estado de like localmente antes de la petición
    this.likedVideos = { ...this.likedVideos, [video.id]: !this.likedVideos[video.id] };
    
    await axios.post(`http://127.0.0.1:8000/likes/${video.id}/${movistore.usuario.documento}`);
    
    // Obtener el número de "likes" actualizados
    const likeCountResponse = await axios.get(`http://127.0.0.1:8000/like/${video.id}`);
    
    // Actualizar el número de likes en el estado
    this.videosurls[index].likes = likeCountResponse.data.likes;
    
    // Guardar en localStorage
    localStorage.setItem("likedVideos", JSON.stringify(this.likedVideos));
    
  } catch (error) {
    console.error("Error al dar/quitar like:", error);
  }
},
loadLikedVideos() {
  const storedLikes = localStorage.getItem("likedVideos");
  if (storedLikes) {
    this.likedVideos = JSON.parse(storedLikes) || {};
  }
},

    
    async getvideosurl() {
      try {
        const response = await axios.get("http://localhost:8000/listarvideos");
        this.videosurls = response.data.map(video => ({
          ...video,
          url: this.getUrlvideo(video.url),
        }));
        console.log("Videos obtenidos:", this.videosurls);
      } catch (error) {
        console.error("Error al obtener los datos", error);
      }
    },
    getUrlvideo(path) {
  // Verifica si la URL ya es absoluta (empieza con "http")
  return path.startsWith("http") 
    ? path 
    : `http://127.0.0.1:8000/${path}`;
},
    goToUpload() {
      alert("Función para subir videos. Aquí puedes redirigir a otra página.");
    },
  },
};
</script>



<style scoped>

.upload-video-button {
  padding: 0.8rem 2rem;

  border: none;
  border-radius: 50px;
  font-weight: bold;
  cursor: pointer;
  text-transform: uppercase;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  transition: all 0.3s ease;
  width: 50%;
  margin-top: -5%;
  display: flex;
  justify-content: center;
  align-items: center;
  margin-left: 22%;
  background: linear-gradient(45deg, #828181, #000000); /* Dorado degradado */
  color: rgb(245, 245, 245);
  font-size: 16px;
  font-weight: bold;
  padding: 10px 20px;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: transform 0.3s, box-shadow 0.3s;
  position: relative;
  border: solid white 1px;
  overflow: hidden;
  font-family: Georgia, 'Times New Roman', Times, serif;
  font-size: 150%;
}

.upload-video-button:hover {
  background: linear-gradient(45deg, #000000, #828181); /* Dorado degradado */
  transform: scale(1.05);
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.3);
  box-shadow: 0 0 10px white;
}

.upload-video-button:active {
  transform: scale(1);
  box-shadow: 0 3px 6px rgba(0, 0, 0, 0.2);
}

.app-container {
  font-family: 'Verdana', sans-serif;
  color: #ffffff;
  background: linear-gradient(to bottom, #000000, #0000006e);
  min-height: 50vh;
  display: flex;
  flex-direction: column;
  padding: 0 5px;
  margin-top: 10%;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem;
  background: #e74c3c;
  color: white;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.4);
}

.upload-button {
  background: #f39c12;
  color: #fff;
  padding: 0.8rem 1.5rem;
  border-radius: 50px;
  font-weight: bold;
  cursor: pointer;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  transition: all 0.3s ease;
}

.upload-button:hover {
  background: #e67e22;
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.3);
}

.video-feed {
  display: flex;
  justify-content: center;
  align-items: center;
  height: calc(100vh - 160px);
  overflow: hidden;
  position: relative;
}

.video-list {
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 100%;
  height: 100%;
}

.video-container {
  position: absolute;
  top: 50%;
  left: 0;
  right: 0;
  transform: translateY(-50%);
  display: flex;
  height: 80%;
  width: 90%;
  background: rgb(9, 0, 0);
  border-radius: 25px;
  overflow: hidden;
  box-shadow: 0 6px 15px rgba(0, 0, 0, 0.4);
  transition: transform 0.3s ease;
  border-style: solid;
  border-color: rgba(255, 255, 255, 0.225);
  border-width: 5%;
}

.video {
  width: 70%;
  height: 100%;
  border-radius: 10%;
}



.profile-pic {
  width: 100px;
  height: 60px;
  border-radius: 50%;
  margin-bottom: 1.5rem;
  border: 3px solid #f39c12;
}

.details h3 {
  font-size: 1.2rem;
  font-weight: 600;
  margin-bottom: 0.5rem;
}

.details p {
  font-size: 1rem;
  color: #bbb;
}

.video-actions {
  margin-top: 40%;

}

.like-button {
  background: #2ecc71;
  color: white;
  border: none;
  padding: 0.7rem 1.5rem;
  border-radius: 30px;
  font-weight: bold;
  cursor: pointer;
  font-size: 1.1rem;
  transition: transform 0.2s ease;
}

.like-button:hover {
  background: #27ae60;
  transform: scale(1.1);
}

.comments {
  margin-top: auto;
}

.comment-input {
  margin-top: 1rem;
  padding: 0.6rem;
  width: 100%;
  border: 1px solid #444;
  border-radius: 10px;
  background: #333;
  color: white;
  font-size: 0.9rem;
}

.video-navigation {
  display: flex;
  justify-content: space-between;
  gap: 2rem;
  padding: 1.5rem;
  position: fixed;
  bottom: 40px;
  right: 20px;
  left: 20px;
}

.video-navigation button {
  background: #f7ba05;
  color: white;
  padding: 1.2rem 1.8rem;
  border-radius: 50px;
  font-weight: bold;
  cursor: pointer;
  border: none;
  font-size: 1.5rem;
  transition: all 0.3s ease;
}

.video-navigation button:hover {
  background: #dd9f0573;
  transform: scale(1.1);
}

.video-navigation button:disabled {
  background: #7f8c8d;
  cursor: not-allowed;
}

.like-button.zoom-in {
  animation: zoomIn 0.5s ease-in-out;
}

@keyframes zoomIn {
  0% {
    transform: scale(1);
  }
  50% {
    transform: scale(1.3);
  }
  100% {
    transform: scale(1);
  }
}
.like-icon {
  width: 20px;
  height: 20px;
  margin-right: 5px;
}
.video-info {
  
  width: 50%;
  display: flex;
  flex-direction: column;
  align-items: center;
  position: relative; /* Importante para manejar la superposición */
}

/* Botón estilizado */




/* Contenedor de imagen + nombre */
.top-section {
  display: flex;
  align-items: center;
  gap: 12px;
}

/* Imagen de perfil */
.profile-pic {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  border: 3px solid #fff;
  box-shadow: 0px 3px 10px rgba(0, 0, 0, 0.2);
}

/* Nombre del usuario */
.uploader-name {
  font-size: 13px;
  font-weight: bold;
  color: #fff;
}

/* Caja flotante de descripción */
.descripcion-box {
  position: absolute;
  top: -80px; /* Se posiciona arriba del botón */
  left: 50%;
  transform: translateX(-50%);
  background: rgba(0, 0, 0, 0.85);
  color: #fff;
  padding: 10px 15px;
  border-radius: 10px;
  width: 250px;
  text-align: center;
  box-shadow: 0px 5px 15px rgba(0, 0, 0, 0.3);
  z-index: 10;

  /* Scroll cuando el contenido es largo */
  max-height: 50px;  /* Ajusta la altura máxima */
  overflow-y: auto;  /* Activa el scroll vertical */
}

/* Para que la barra de scroll sea más estética */
.descripcion-box::-webkit-scrollbar {
  width: 5px;
}

.descripcion-box::-webkit-scrollbar-thumb {
  background: #666;
  border-radius: 5px;
}

.descripcion-box::-webkit-scrollbar-track {
  background: transparent;
}


/* Descripción */
.descripcion {
  font-size: 14px;
  opacity: 0.9;
  color: rgb(255, 255, 255);
  height: auto;
  padding: 3%;
  font-family:Georgia, 'Times New Roman', Times, serif;
  width: auto;
}
.descripcion2{
  font-size: 16px;
  opacity: 0.9;
  color: rgb(255, 255, 255);
  height: auto;
  padding: 3%;
  font-family:Georgia, 'Times New Roman', Times, serif;
  width: auto;
  text-decoration: underline;

}

.profile-button {
  display: flex;
  flex-direction: column;
  align-items: center;
  background: linear-gradient(135deg, #000000, #666666);
  border: none;
  border-radius: 12px;
  padding: 15px;
  cursor: pointer;
  transition: transform 0.2s, box-shadow 0.3s;
  width: 100%;
  min-width: 80%;
  max-width: 80%;
  min-height: 180px;
  max-height: 200px;
  
  /* Evita que el contenido se salga */
  overflow: hidden;
}

.profile-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 100%;
  
  /* Permite scroll interno si el contenido es grande */
  max-height: 160px; /* Ajusta según necesidad */
  overflow-y: auto;
  padding-right: 5px; /* Espacio para la barra de scroll */
}

/* Personalización de la barra de scroll */
.profile-content::-webkit-scrollbar {
  width: 5px;
}

.profile-content::-webkit-scrollbar-thumb {
  background: #888;
  border-radius: 5px;
}

.profile-content::-webkit-scrollbar-track {
  background: transparent;
}

</style>