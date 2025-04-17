<template>
  <header>
    <!-- Header de escritorio -->
    <div class="d-none d-md-block">
      <Headerapp />
    </div>
    <!-- Header para móviles -->
    <div class="d-block d-md-none">
      <headermobile />
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
    loop
    muted
    @click="togglePlayPause(index)"
  ></video>

  <!-- Overlay de info -->
  <div class="overlay-info">
    <div class="info-left">
      <img :src="getProfilePic(video.uploaderProfilePic)" alt="Profile" class="profile-pic-large" />
      <div class="text-info">
        <h3 class="uploader-name">@{{ video.uploaderName }}</h3>
        <p class="descripcion2">{{ video.description }}</p>
      </div>
    </div>

    <div class="info-right">
      <button
        @click="likeVideo(index)"
        class="like-button-modern"
        :class="{ 'zoom-in': likedIndex === index }"
      >
        <img
          :src="likedVideos[video.id] ? '/imagenes/balondeoro.png' : '/imagenes/corazon.png'"
          alt="Like"
          class="like-icon-large"
          @error="setFallback(video.id)"
        />
        <span class="like-count">{{ video.likes }}</span>
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
      this.$router.push(`/perfiles/${documento}`);
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
          if (index !== currentIndex && video) video.pause();
        });
      }
    },
    playCurrentVideo() {
      const video = this.$refs.videoPlayer[this.currentIndex];
      if (video) video.play();
      this.pauseOthers(this.currentIndex);
    },
    togglePlayPause(index) {
      const video = this.$refs.videoPlayer[index];
      if (video) video.paused ? video.play() : video.pause();
      this.pauseOthers(index);
    },
    async likeVideo(index) {
      const store = useUsuarios();
      const video = this.videosurls[index];
      if (!store.usuario.documento) return;

      try {
        this.likedVideos = {
          ...this.likedVideos,
          [video.id]: !this.likedVideos[video.id],
        };

        await axios.post(`http://127.0.0.1:8000/likes/${video.id}/${store.usuario.documento}`);
        const res = await axios.get(`http://127.0.0.1:8000/like/${video.id}`);
        this.videosurls[index].likes = res.data.likes;

        localStorage.setItem("likedVideos", JSON.stringify(this.likedVideos));
      } catch (err) {
        console.error("Error al dar/quitar like:", err);
      }
    },
    setFallback(videoId) {
      this.likedVideos[videoId] = false;
    },
    loadLikedVideos() {
      const stored = localStorage.getItem("likedVideos");
      if (stored) this.likedVideos = JSON.parse(stored);
    },
    async getvideosurl() {
      try {
        const res = await axios.get("http://localhost:8000/listarvideos");
        this.videosurls = res.data.map(video => ({
          ...video,
          url: this.getUrlvideo(video.url),
        }));
      } catch (err) {
        console.error("Error al obtener los videos:", err);
      }
    },
    getUrlvideo(path) {
      return path.startsWith("http") ? path : `http://127.0.0.1:8000/${path}`;
    },
    subirVideo() {
      this.$router.push("/subirvideo");
    },
  },
};
</script>

<style scoped>
.app-container {
  font-family: 'Verdana', sans-serif;
  color: #ffffff;
  background: linear-gradient(to bottom, #000000, #0000006e);
  min-height: 80vh;
  min-width: 50vw;
  display: flex;
  flex-direction: column;
  padding: 0 5px;
  margin-top: 17%;
}

.video-feed {
  display: flex;
  justify-content: center;
  align-items: center;
  height: calc(65vh);
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
  width: 100%;
  height: 100%;
}

.video {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.upload-video-button {
  padding: 10px 20px;
  border: none;
  border-radius: 8px;
  background: linear-gradient(45deg, #828181, #000000);
  color: #fff;
  font-size: 18px;
  font-family: Georgia, 'Times New Roman', Times, serif;
  font-weight: bold;
  width: 80%;
  max-width: 400px;
  margin: 20px auto;
  display: flex;
  justify-content: center;
  align-items: center;
  border: solid white 1px;
  transition: all 0.3s ease;
}

.upload-video-button:hover {
  background: linear-gradient(45deg, #000000, #828181);
  transform: scale(1.05);
  box-shadow: 0 0 10px white;
}

.video-info {
  background: rgba(0, 0, 0, 0.6);
  padding: 1rem;
  color: white;
  position: absolute;
  bottom: 10px;
  left: 0;
  right: 0;
  text-align: center;
}

.profile-button {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.profile-pic {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  margin-bottom: 10px;
}

.uploader-name {
  font-size: 1.2rem;
  font-weight: bold;
}

.descripcion {
  font-size: 14px;
  margin-top: 5px;
}

.descripcion2 {
  font-size: 12px;
}

.like-button {
  display: flex;
  align-items: center;
  background: none;
  border: none;
  cursor: pointer;
  margin-top: 10px;
}

.like-icon {
  width: 25px;
  height: 25px;
  margin-right: 10px;
}

.video-navigation {
  display: flex;
  justify-content: space-between;
  margin-top: 10px;
}

button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}
.overlay-info {
  position: absolute;
  bottom: 20px;
  left: 10px;
  right: 10px;
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
  padding: 10px;
  background: linear-gradient(to top, rgba(0, 0, 0, 0.7), transparent 90%);
  border-radius: 16px;
}

.info-left {
  display: flex;
  align-items: center;
  gap: 10px;
  max-width: 70%;
}

.profile-pic-large {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  border: 2px solid rgb(255, 255, 255);
  box-shadow: 0 0 6px rgba(255, 255, 255, 0.5);
}

.text-info {
  color: white;
  font-family: 'Segoe UI', sans-serif;
}


.descripcion2 {
  font-size: 14px;
  margin: 4px 0 0;
}

.info-right {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-right: 10px;
}

.like-button-modern {
  background: transparent;
  border: none;
  cursor: pointer;
  color: white;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.like-icon-large {
  width: 30px;
  height: 30px;
  margin-bottom: 4px;
}

.like-count {
  font-size: 14px;
  font-weight: bold;
  color: white;
  text-shadow: 0 0 3px black;
}



@media (min-width: 320px) and (max-width: 480px) {
  .app-container {

  margin-top: 40%;
}

}
@media (min-width: 481px) and (max-width: 600px) {
  .app-container {

  margin-top: 35%;
}

}
@media (min-width: 601px) and (max-width: 768px) {
  .app-container {

  margin-top: 30%;
}

}
@media (min-width: 769px) and (max-width: 1024px) {
  .app-container {
  margin-top: 25%;
}

}
@media (min-width: 1025px) and (max-width: 1440px) {
  .app-container {

  margin-top: 20%;
}

}
@media (min-width: 1441px) and (max-width: 1920px) {
  .app-container {

  margin-top: 20%;
}

}
@media (min-width: 1921px) and (max-width: 2560px) {
  .app-container {

  margin-top: 15%;
}

}
@media (min-width: 2561px) and (max-width: 3840px) {
  .app-container {

  margin-top: 15%;
}

}
@media (min-width: 3841px) and (max-width: 5120px) {
  .app-container {

  margin-top: 15%;
}

}
@media (max-width: 768px) {
  .overlay-info {
    flex-direction: column;
    align-items: flex-start;
    gap: 10px;
    padding: 8px;
  }

  .info-left {
    max-width: 100%;
    gap: 8px;
  }

  .uploader-name {
    font-size: 14px;
  }

  .descripcion2 {
    font-size: 12px;
  }

  .like-icon-large {
    width: 24px;
    height: 24px;
  }

  .like-count {
    font-size: 12px;
  }
}




</style>
