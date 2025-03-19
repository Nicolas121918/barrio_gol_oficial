<template>
   <header>
    <Headerapp/>
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
            <img :src="getProfilePic(video.uploaderProfilePic)" alt="Profile" class="profile-pic" /> 
            <div class="details">
              <h3>{{ video.uploaderName }}</h3>
              <p>{{ video.description }}</p>
            </div>
            <div class="video-actions">
              <button
  @click="likeVideo(index)"
  class="like-button"
  :class="{'zoom-in': likedIndex === index}"
>
  <img 
    :src="likedVideos[video.id] ? '../assets/imagenes/balondeoro.png' : 'ruta/corazon.png'" 
    alt="Like"
    class="like-icon"
  />
  {{ video.likes }}
</button>

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
import { useUsuarios } from "@/stores/usuario";
export default {
  components: {
    Headerapp,
  },
  data() {
    return {
      videosurls: [],
      currentIndex: 0,
      likedVideos: {},
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
    nextVideo() {
      if (this.currentIndex < this.videosurls.length - 1) {
        this.currentIndex++;
        this.playCurrentVideo();
      }
    },
    previousVideo() {
      if (this.currentIndex > 0) {
        this.currentIndex--;
        this.playCurrentVideo();
      }
    },
    getProfilePic(path) {
      return path ? `http://127.0.0.1:8000/${path}` : "default.png";
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
      console.log(movistore.usuario.documento)
      if (!movistore.usuario.documento) {
        console.error("⚠ No se encontró un usuario válido en el store.");
        console.error(movistore.usuario.documento);
        return;
      }
      console.log("✅ Usuario encontrado:", movistore.usuario);
      const video = this.videosurls[index];
      try {
        await axios.post(
          `http://127.0.0.1:8000/likes/${video.id}/${movistore.usuario.documento}`
        );
        const likeCountResponse = await axios.get(
          `http://127.0.0.1:8000/like/${video.id}`
        );
        this.videosurls[index].likes = likeCountResponse.data.likes;
        this.videosurls = [...this.videosurls];
        this.likedVideos[video.id] = !this.likedVideos[video.id];
        localStorage.setItem("likedVideos", JSON.stringify(this.likedVideos));
      } catch (error) {
        console.error("Error al dar/quitar like:", error);
      }
    },
    loadLikedVideos() {
      const storedLikes = localStorage.getItem("likedVideos");
      if (storedLikes) {
        this.likedVideos = JSON.parse(storedLikes);
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
      return path.startsWith("http") ? path : `http://127.0.0.1:8000/${path}`;
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

.video-info {
  padding: 1.5rem;
  width: 30%;
  display: flex;
  flex-direction: column;
}

.profile-pic {
  width: 60px;
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
  margin-bottom: 1.5rem;
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
  background: #3498db;
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
  background: #2980b9;
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

</style>
