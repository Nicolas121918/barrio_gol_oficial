<template>
  <header>

    <!-- Header de escritorio -->
    <div class="d-none d-md-block">
      <headerapp></headerapp>
    </div>

    <!-- Header para móviles -->
    <div class="d-block d-md-none">
      <headermobile></headermobile>
    </div>
  </header>

  <div class="profile-container">
    <button class="back-button" @click="goBack">Volver</button>

    <div class="usuario">
      <div class="reportar">
        <ReportarUsuario :documentoReportado="userProfile.documento" />
  </div>
      <div class="team-info" v-if="team.name" @mouseover="isTeamInfoVisible = true" @mouseleave="isTeamInfoVisible = false">
        
        <img class="team-logo" :src="teamLogoUrl" alt="Logo del equipo" />
        
        <div class="team-hover-info" v-if="isTeamInfoVisible || isTeamInfoClicked" @click="toggleTeamInfo">
          <p class="equipp">Equipo:</p>
          <p><span class="label">Nombre:</span> <strong class="value">{{ team.name }}</strong></p>
          <p><span class="label">Ciudad:</span> <strong class="value">{{ team.city || 'N/A' }}</strong></p>
          <p><span class="label">Descripción:</span> <strong class="value">{{ team.description || 'N/A' }}</strong></p>
        </div>
      </div>
      <div v-else class="no-team-info">
        <p><strong class="juador_sin">Jugador sin equipo</strong></p>
      </div>

      <div class="profile-info">
        <div class="profile-header">
          <img class="profile-picture" :src="profilePictureUrl" alt="Foto de perfil" @click="showImage = true" />
          <div class="user-details">
            <h2>{{ userProfile.name }}</h2>
            <p>Ciudad: {{ userProfile.city }}</p>
            <p>Edad: {{ userProfile.Edad }}</p>
            <p>Posición: {{ userProfile.position }}</p>
            <p>Email: {{ maskedEmail }}</p>
            <p><strong>Descripción:</strong> {{ userProfile.description }}</p>
          </div>
        </div>
      </div>
    </div>

    <div v-if="showImage" class="image-modal" @click="showImage = false">
      <img class="large-image" :src="profilePictureUrl" alt="Foto de perfil" @click="showImage = true" />
    </div>

    <div class="videos-section">
      <h3>Videos del Usuario</h3>

      <!-- Buscador de videos -->
      <input type="text" v-model="searchQuery" placeholder="Buscar video por nombre..." class="video-search"/>

      <div class="videos-grid">
        <div class="video-card" v-for="video in filteredVideos" :key="video.url">          
          <div class="video-content">
            <video
              ref="video"
              :src="video.url"
              class="video"
              @mouseover="playVideo($event)"
              @mouseleave="pauseVideo($event)"
              :title="video.description"
            >
              Tu navegador no soporta el video.
            </video>
            <p class="descr">{{ video.description }}</p>
            <br> 
            
            <p class="likes">
                <img class="likeee" src="../assets/imagenes/like.png" alt=""> {{ video.likes }} Likes
            </p>
            
            <button @click="verVideo" class="boton_ver">Ver</button>
          </div>
        </div>
      </div>
    </div>  
  </div>
</template>

<script>
import axios from 'axios';
import Headerapp from './Headerapp.vue';
import headermobile from './headermobile.vue';
import ReportarUsuario from './ReportarUsuario.vue';

export default {
  components: {
    Headerapp,
    headermobile,
    ReportarUsuario
  },
  data() {
    return {
      isTeamInfoVisible: false,
      isTeamInfoClicked: false,
      showImage: false,
      searchQuery: '',  // Nuevo campo para la búsqueda
      userProfile: {
        documento: '', 
        picture: '',
        name: '',
        city: '',
        Edad: '',
        position: '',
        correo: '',
        description: '',
        equipos_tiene: '',
        videos: []
      },
      team: {
        logo: '',
        name: '',
        city: '',
        description: ''
      }
    };
  },
  computed: {
    maskedEmail() {
      if (!this.userProfile.correo) return '';
      const emailParts = this.userProfile.correo.split('@');
      const maskedName = emailParts[0].slice(0, 3) + '*******';
      return `${maskedName}@${emailParts[1]}`;
    },
    profilePictureUrl() {
      return this.userProfile.picture
        ? `http://127.0.0.1:8000/${this.userProfile.picture}`
        : 'default.png';
    },
    teamLogoUrl() {
  return this.team && this.team.logo
    ? `http://127.0.0.1:8000/${this.team.logo}`
    : 'default-team.png';
},
    // Filtrar videos según el nombre ingresado en searchQuery
    filteredVideos() {
      if (!this.searchQuery) {
        return this.userProfile.videos;
      }
      return this.userProfile.videos.filter(video =>
        video.description.toLowerCase().includes(this.searchQuery.toLowerCase())
      );
    }
  },
  methods: {
    async fetchUserData() {
      const documento = this.$route.params.documento; 
      try {
        const userResponse = await axios.get(`http://localhost:8000/api/usuario/${documento}`);
        this.userProfile = {
          documento: documento,
          picture: userResponse.data.imagen || '',
          name: userResponse.data.nombre,
          city: userResponse.data.ciudad || 'N/A',
          Edad: userResponse.data.Edad || 'N/A',
          position: userResponse.data.posicion || 'N/A',
          correo: userResponse.data.correo,
          description: userResponse.data.descripcion || 'N/A',
          equipos_tiene: userResponse.data.equipos_tiene || 0, 
          videos: []
        };
        if (userResponse.data.equipos_tiene > 0) {
  const teamResponse = await axios.get(`http://localhost:8000/equipos_traer/${userResponse.data.equipos_tiene}`);
  this.team = {
    logo: teamResponse.data.logoTeam || '',
    name: teamResponse.data.nombreteam || '',
    city: teamResponse.data.location || '',
    description: teamResponse.data.Descripcion || ''
  };
} else {
  this.team = { logo: '', name: '', city: '', description: '' }; // Objeto vacío en lugar de null
}
        const videosResponse = await axios.get(`http://localhost:8000/listarvideosdef/${documento}`);
        this.userProfile.videos = videosResponse.data.map(video => ({
          url: `http://127.0.0.1:8000/${video.url}`,
          description: video.description,
          likes: video.likes
        }));

      } catch (error) {
        console.error('Error cargando datos del usuario:', error);
      }
    },
    playVideo(event) {
      event.target.play();
    },
    pauseVideo(event) {
      event.target.pause();
    },
    verVideo(id) {
      this.$router.push(`/one_video/${id}`);
    },
    toggleTeamInfo() {
      this.isTeamInfoClicked = !this.isTeamInfoClicked;
    },
    goBack() {
      this.$router.go(-1);
    }
  },
  mounted() {
    this.fetchUserData();
  }
};
</script>


<style scoped>
.profile-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 2rem;
  background: linear-gradient(145deg, #000000, #1a1a1a);
  width: 100%;
  margin: 0 auto;
  max-width: 1100px;
  border: 2px solid white;
  box-shadow: 0 0 30px rgb(0, 0, 0);
  color: white;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  border-radius: 16px;
  margin-top: 20vb;
}

.back-button {
  padding: 10px 20px;
  background-image: url("https://static.vecteezy.com/system/resources/thumbnails/000/549/015/small/vector-apr-2018-19.jpg");
  color: black;  
  border: 2px solid white;
  border-radius: 8px;
  font-weight: bold;
  cursor: pointer;
  font-size: 1rem;
  margin-bottom: 1rem;
  align-self: flex-start;
  transition: 0.3s;
}

.back-button:hover {
  font-size: 1.1rem;
  color: white;
  box-shadow: 0 0 20px white;
}

.profile-header {
  display: flex;
  flex-direction: row;
  align-items: center;
  gap: 1.5rem;
  flex-wrap: wrap;
  text-align: center;
  justify-content: center;
}


.profile-picture {
  width: 150px;
  height: 150px;
  border-radius: 50%;
  object-fit: cover;
  border: 3px solid #ffd700;
  box-shadow: 0 0 10px white;
  transition: 0.3s;
}

.profile-picture:hover {
  transform: scale(1.1);
  box-shadow: 0 0 20px #ffd700;
}

.user-details h2 {
  font-size: 1.8rem;
  color: #ffd700;
  text-shadow: 0 0 10px rgba(255, 215, 0, 0.8);
  padding: 10px 15px;
  border-radius: 8px;
  margin-bottom: 1rem;
  transition: transform 0.3s;
}

.user-details h2:hover {
  transform: scale(1.1);
  text-shadow: 0 0 15px white;
}

.user-details p {
  font-size: 1rem;
  margin: 5px 0;
}

.boton_ver {
  background: linear-gradient(45deg, #333, #999);
  color: white;
  padding: 10px 20px;
  font-size: 1rem;
  font-weight: bold;
  border: none;
  border-radius: 10px;
  cursor: pointer;
  transition: all 0.3s ease;
  border: solid 1px white;
  position: relative;
  overflow: hidden;
}

.boton_ver:hover {
  transform: scale(1.05);
  box-shadow: 0 0 15px rgba(255, 215, 0, 0.8);
}

.boton_ver::before {
  content: "";
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: rgba(255, 255, 255, 0.2);
  transform: skewX(-45deg);
  transition: left 0.5s;
}

.boton_ver:hover::before {
  left: 100%;
}

.team-info {
  display: flex;
  justify-content: center;
  align-items: center;
  margin: 1rem 0;
  position: relative;
  cursor: pointer;
}

.team-logo {
  width: 70px;
  height: 70px;
  border-radius: 50%;
  object-fit: cover;
  border: 2px solid white;
  box-shadow: 0 0 15px #fff;
  transition: 0.3s;
}

.team-logo:hover {
  transform: scale(1.1);
}

.team-hover-info {
  position: absolute;
  top: 0;
  right: 0;
  background-color: white;
  padding: 1rem;
  border-radius: 10px;
  box-shadow: 0 6px 18px rgba(0, 0, 0, 0.2);
  width: 230px;
  font-size: 0.95rem;
  animation: fadeIn 0.6s ease-in-out;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.team-hover-info .label {
  font-weight: bold;
  color: black;
}

.team-hover-info .value {
  color: #464646;
}

.team-hover-info .join-button {
  margin-top: 15px;
  background-color: gold;
  color: black;
  padding: 10px 15px;
  font-size: 1rem;
  border-radius: 8px;
  border: none;
  cursor: pointer;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
  transition: 0.3s ease;
}

.team-hover-info .join-button:hover {
  background-color: #d4af37;
  transform: scale(1.05);
}

.videos-section {
  margin-top: 2rem;
  padding: 1.5rem;
  width: 100%;
  background: linear-gradient(90deg, rgba(212, 212, 212, 0.2), rgba(255, 215, 0, 0));
  border: 2px solid #7e7e7e;
  border-radius: 10px;
  color: #ffd700;
  text-align: center;
}

.video{
  width: 50%;
  height: auto;
  border-radius: 8px;
  box-shadow: 0 0 10px #949494;
}

.likeee{
  width: 20px;
  height: 20px;
  margin-right: 5px;
}

.videos-section h3 {
  font-size: 2rem;
  margin-bottom: 1rem;
  color: white;
  text-shadow: 0 0 10px white;
  border: 2px solid white;
  padding: 0.5rem;
  border-radius: 8px;
  background: linear-gradient(90deg, rgba(224, 197, 108, 0.2), rgba(255, 215, 0, 0));
}

.videos-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 1rem;
  width: 100%;
}

.video-card {
  width: 50%;  
  background-color: #030303;
  border: 2px solid white;
  border-radius: 8px;
  padding: 1rem;
  box-shadow: 0 0 10px #949494;
  transition: 0.3s;
}

.video-card:hover {
  transform: scale(1.05);
  box-shadow: 0 0 20px #ffc400;
}

.usuarios {
  display: flex;
  flex-direction: row;
  flex-wrap: wrap;
  justify-content: center;
  gap: 1rem;
}



/* --------- Media Queries ----------- */

@media (max-width: 768px) {
  .profile-header {
    flex-direction: column;
  }

  .team-info {
    justify-content: center;
  }

  .videos-section h3 {
    font-size: 1.5rem;
  }

  .profile-container {
    margin-top: 10%;
    padding: 1rem;
  }
}

@media (max-width: 480px) {
  .profile-picture {
    width: 100px;
    height: 100px;
  }

  .user-details h2 {
    font-size: 1.3rem;
  }

  .boton_ver {
    font-size: 0.9rem;
    padding: 8px 16px;
  }
}
</style>

