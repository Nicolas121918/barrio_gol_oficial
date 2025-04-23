<template>
  <div class="princ_videohome">
    <div class="loader">
      <div data-glitch="BIENVENIDO A BARRIOGOL" class="glitch">BIENVENIDO A BARRIOGOL</div>
    </div>

    <label class="container_play_stop">
      <input checked="checked" type="checkbox" @change="togglePlay">
      <svg viewBox="0 0 384 512" height="1em" xmlns="http://www.w3.org/2000/svg" class="play">
        <path d="M73 39c-14.8-9.1-33.4-9.4-48.5-.9S0 62.6 0 80V432c0 17.4 9.4 33.4 24.5 41.9s33.7 8.1 48.5-.9L361 297c14.3-8.7 23-24.2 23-41s-8.7-32.2-23-41L73 39z"></path>
      </svg>
      <svg viewBox="0 0 320 512" height="1em" xmlns="http://www.w3.org/2000/svg" class="pause">
        <path d="M48 64C21.5 64 0 85.5 0 112V400c0 26.5 21.5 48 48 48H80c26.5 0 48-21.5 48-48V112c0-26.5-21.5-48-48-48H48zm192 0c-26.5 0-48 21.5-48 48V400c0 26.5 21.5 48 48 48h32c26.5 0 48-21.5 48-48V112c0-26.5-21.5-48-48-48H240z"></path>
      </svg>
    </label>

    <div class="video-container" :class="{ active: isPlaying }">
      <video class="video_video" ref="videoElement" muted loop playsinline>
        <source src="../assets/videos/video.mp4" type="video/mp4" />
      </video>
    </div>
  </div>
</template>

<script>
export default {
  name: "VideoBackground",
  data() {
    return {
      isPlaying: false,
    };
  },
  methods: {
    togglePlay(event) {
      const video = this.$refs.videoElement;
      this.isPlaying = event.target.checked;
      if (this.isPlaying) {
        video.play();
      } else {
        video.pause();
      }
    },
  },
};
</script>

<style scoped>
.princ_videohome {
  height: 100%;
  width: 100%;
  margin: 0;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}

.glitch {
  font-size: 20px;
  font-weight: 800;
  color: #fff;
  letter-spacing: 5px;
  z-index: 1;
  animation: shift 10s ease-in-out infinite alternate;
}

.glitch:before,
.glitch:after {
  display: block;
  content: attr(data-glitch);
  position: absolute;
  top: 0;
  left: 0;
  opacity: 0.8;
}

.glitch:before {
  animation: glitch 0.4s cubic-bezier(0.25, 0.46, 0.45, 0.94) both infinite;
  color: #8b00ff;
  z-index: -1;
}

.glitch:after {
  animation: glitch 0.4s cubic-bezier(0.25, 0.46, 0.45, 0.94) reverse both infinite;
  color: #00e571;
  z-index: -2;
}

@keyframes glitch {
  0% {
    transform: translate(0);
  }
  20% {
    transform: translate(-1px, 1px);
  }
  40% {
    transform: translate(-2px, -2px);
  }
  60% {
    transform: translate(2px, 2px);
  }
  80% {
    transform: translate(2px, -2px);
  }
  100% {
    transform: translate(0);
  }
}

@keyframes shift {
  0%, 40%, 44%, 58%, 61%, 65%, 69%, 73%, 100% {
    transform: skewX(0deg);
  }
  41% {
    transform: skewX(5deg);
  }
  42% {
    transform: skewX(-5deg);
  }
  59% {
    transform: skewX(5deg) skewY(5deg);
  }
  60% {
    transform: skewX(-5deg) skewY(-5deg);
  }
  63% {
    transform: skewX(5deg) skewY(-5deg);
  }
  70% {
    transform: skewX(-20deg) skewY(-10deg);
  }
  71% {
    transform: skewX(5deg) skewY(-5deg);
  }
}

.container_play_stop {
  --color: #000000;
  --size: 30px;
  display: flex;
  justify-content: center;
  align-items: center;
  position: relative;
  cursor: pointer;
  font-size: var(--size);
  user-select: none;
  fill: var(--color);
}

.container_play_stop .play {
  position: absolute;
  animation: keyframes-fill .5s;
}

.container_play_stop .pause {
  position: absolute;
  display: none;
  animation: keyframes-fill .5s;
}

.container_play_stop input:checked ~ .play {
  display: none;
}

.container_play_stop input:checked ~ .pause {
  display: block;
}

.container_play_stop input {
  position: absolute;
  opacity: 0;
  cursor: pointer;
  height: 0;
  width: 0;
}

@keyframes keyframes-fill {
  0% {
    transform: rotate(-180deg) scale(0);
    opacity: 0;
  }
  50% {
    transform: rotate(-10deg) scale(1.2);
  }
}

.video-container {
  display: flex;
  align-items: center;
  justify-content: flex-end;
  width: auto;
  height: auto;
  opacity: 0;
  visibility: hidden;
  transition: opacity 0.5s ease-in-out, visibility 0.5s ease-in-out;
  margin-top: 5%;
}

.video_video {
  width: 60%;
  height: 60%;
}

.video-container.active {
  opacity: 1;
  visibility: visible;
}

@media (max-width: 320px) {
  .video-container {
    display: flex;
    align-items: center;
    justify-content: flex-end;
    width: 100%;
    height: auto;
    opacity: 0;
    visibility: hidden;
    transition: opacity 0.5s ease-in-out, visibility 0.5s ease-in-out;
    margin-top: 30%;
  }
  .video_video {
    width: 100%;
    height: 100%;
  }
  .princ_videohome {
    height: 100%;
    width: 100%;
    margin-top: 60%;
  }
}

@media (max-width: 480px) {
  .video-container {
    display: flex;
    align-items: center;
    justify-content: flex-end;
    width: 100%;
    height: auto;
    opacity: 0;
    visibility: hidden;
    transition: opacity 0.5s ease-in-out, visibility 0.5s ease-in-out;
    margin-top: 10%;
  }
  .video_video {
    width: 100%;
    height: 100%;
  }
  .princ_videohome {
    height: 100%;
    width: 100%;
    margin-top: 60%;
  }
}

@media (min-width: 481px) and (max-width: 600px) {
  .video-container {
    display: flex;
    align-items: flex-end;
    justify-content: flex-start;
    width: 130%;
    height: auto;
    opacity: 0;
    visibility: hidden;
    transition: opacity 0.5s ease-in-out, visibility 0.5s ease-in-out;
    margin-top: 10%;
    margin-left:30%;
  }
  .video_video {
    width: 100%;
    height: 100%;
  }
  .princ_videohome {
    height: 100%;
    width: 100%;
    margin-top: 5%;
  }
  .glitch {
  font-size: 120%;
  font-weight: 800;
  color: #ffffff;
  letter-spacing: 5px;
  z-index: 1;
  animation: shift 10s ease-in-out infinite alternate;
  position: relative;
  left: 2%;
}
.container_play_stop {
  --color: #ddff00b7;
  --size: 180%;
  cursor: pointer;
  font-size: var(--size);
  user-select: none;
  fill: var(--color);
  position:absolute ;
  z-index:  99999;
  top: 50%;
  left: 50%;
}

}

@media (min-width: 601px) and (max-width: 768px) {
  /* Estilos para pantallas entre 601px y 768px */
  .glitch {
  font-size: 40px;
  font-weight: 800;
  color: #ffffff;
  letter-spacing: 5px;
  z-index: 1;
  animation: shift 10s ease-in-out infinite alternate;
}
  .video-container {
    display: flex;
    align-items: center;
    justify-content: flex-end;
    margin-right: 0%;
    width: 110%;
    height: auto;
    opacity: 0;
    visibility: hidden;
    transition: opacity 0.5s ease-in-out, visibility 0.5s ease-in-out;
    margin-top: 5%;
  }
  .video_video {
    width: 100%;
    height: 100%;
  }
  .princ_videohome {
    height: 100%;
    width: 110%;
    margin-top: 5%;
  }
  .container_play_stop {
  --color: #ddff00b7;
  --size: 60px;
  cursor: pointer;
  font-size: var(--size);
  user-select: none;
  fill: var(--color);
  position:absolute ;
  z-index:  99999;
  top: 55%;
  left: 58%;
}


}

@media (min-width: 769px) and (max-width: 1024px) {
  /* Estilos para pantallas entre 769px y 1024px */
  .glitch {
  font-size: 45px;
  font-weight: 800;
  color: #ffffff;
  letter-spacing: 5px;
  z-index: 1;
  animation: shift 10s ease-in-out infinite alternate;
}
  .video-container {
    display: flex;
    align-items: center;
    justify-content: flex-end;
    margin-right: 0%;
    width: 70%;
    height: auto;
    opacity: 0;
    visibility: hidden;
    transition: opacity 0.5s ease-in-out, visibility 0.5s ease-in-out;
    margin-top: 5%;
  }
  .video_video {
    width: 100%;
    height: 100%;
  }
  .princ_videohome {
    height: 100%;
    width: 100%;
    margin-top: 5%;
  }
}

@media (min-width: 1025px) and (max-width: 1280px) {
  /* Estilos para pantallas entre 1025px y 1280px */
  .glitch {
  font-size: 45px;
  font-weight: 800;
  color: #ffffff;
  letter-spacing: 5px;
  z-index: 1;
  animation: shift 10s ease-in-out infinite alternate;
}
  .video-container {
    display: flex;
    align-items: center;
    justify-content: flex-end;
    margin-right: 0%;
    width: 70%;
    height: auto;
    opacity: 0;
    visibility: hidden;
    transition: opacity 0.5s ease-in-out, visibility 0.5s ease-in-out;
    margin-top: 5%;
  }
  .video_video {
    width: 100%;
    height: 100%;
  }
  .princ_videohome {
    height: 100%;
    width: 100%;
    margin-top: 5%;
  }
}

@media (min-width: 1281px) and (max-width: 2000px) {
  /* Estilos para pantallas entre 1281px y 1440px */

  .glitch {
  font-size: 30px;
  font-weight: 800;
  color: #ffffff;
  letter-spacing: 5px;
  z-index: 1;
  animation: shift 10s ease-in-out infinite alternate;
}
  .video-container {
    display: flex;
    align-items: center;
    justify-content: flex-end;
    margin-right: 0%;
    width: 70%;
    height: auto;
    opacity: 0;
    visibility: hidden;
    transition: opacity 0.5s ease-in-out, visibility 0.5s ease-in-out;
    border: solid black 5px;
  }
  .video_video {
    width: 100%;
    height: 100%;
  }
  .princ_videohome {
    height: 100%;
    width: 100%;
  }
  .container_play_stop {
  --color: #ddff00b7;
  --size: 50px;
  cursor: pointer;
  font-size: var(--size);
  user-select: none;
  fill: var(--color);
  position:absolute ;
  z-index:  99999;
  top: 60%;
}

}








</style>
