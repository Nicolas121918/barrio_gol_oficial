<template>
  <header>
    <Headerapp></Headerapp>
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
import ReportarUsuario from './ReportarUsuario.vue';

export default {
  components: {
    Headerapp,
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
  padding: 10px;
  background-color: rgb(0, 0, 0);
  width: 155%;
  margin-left: -24%;
  border: solid white;
  box-shadow: 0 0 30px rgb(0, 0, 0);
  margin-top: 17%;
  color: white;
  font-family:serif;
}

.back-button {
  padding: 10px 20px;
  background-image: url("https://static.vecteezy.com/system/resources/thumbnails/000/549/015/small/vector-apr-2018-19.jpg");
  color: rgb(0, 0, 0);  
  border: 3px solid white;
  text-shadow: rgb(223, 0, 0) 0 0 40px;
  border-radius: 4px;
  cursor: pointer;
  font-size: 1rem;
  z-index: 10;
  margin-right: 100%;
}

.back-button:hover {
  font-size: 1.2rem;
  color: white;
  transform: scale(1);
  box-shadow: 0 0 40px white;
}
.team-hover-info {
  position: absolute;
  color: #201f1f;
  text-align: left;
  top: 0;
  right: 70px;
  background-color: white;
  padding: 15px;
  border: 1px solid #ddd;
  border-radius: 10px;
  box-shadow: 0 6px 18px rgba(0, 0, 0, 0.2);
  width: 230px;
  font-size: 1rem;
  transition: all 0.4s ease-in-out;
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

.team-hover-info p {
  margin: 10px 0;
  line-height: 1.6;
}

.team-hover-info .label {
  font-weight: bold;
  color: black;
  text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.5);
}

.team-hover-info .value {
  color: rgb(70, 70, 70);
  font-weight: normal;
  
}

.team-hover-info .join-button {
  display: block;
  margin-top: 15px;
  background-color: gold;
  color: black;
  border: none;
  padding: 12px 18px;
  font-size: 1rem;
  border-radius: 8px;
  cursor: pointer;
  transition: background-color 0.3s ease, transform 0.2s ease;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
}

.team-hover-info .join-button:hover {
  background-color: #d4af37;
  transform: scale(1.05);
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.3);
}

.team-hover-info:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.3);
}

.profile-info {
  width: 100%;
  display: flex;
  justify-content: center;
  margin-bottom: 30px;
}

.profile-header {
  display: flex;
  flex-direction: row;
  align-items: center;
  gap: 20px;
}

.profile-picture {
  width: 150px;
  height: 150px;
  border-radius: 50%;
  object-fit: cover;
  border: solid rgb(255, 166, 2);
  box-shadow: 0 0 10px white;
}
.profile-picture:hover{
    transform: scale(1.1);
    box-shadow: 0 0 20px rgb(255, 230, 9);
    
}

.user-details h2 {
  margin: 0;
  color: white;
  font-size: 220%;
  font-family: Georgia, 'Times New Roman', Times, serif;
  text-align: center;
  border-bottom: 0.5px solid white;
  text-shadow: 0 0 10px rgb(255, 174, 0);

  font-size: 160%;
  font-weight: bold;
  font-family: Cambria, Cochin, Georgia, Times, 'Times New Roman', serif;
  color: #ffd700; /* Dorado */
  text-shadow: 0 0 10px rgba(255, 215, 0, 0.8);
  padding: 10px 15px;
  border-radius: 8px;
  margin-bottom: 20px;
  

}
.boton_ver {
  background: linear-gradient(45deg, #151515, #9f9f9f); /* Dorado degradado */
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
}

.boton_ver::before {
  content: "";
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: rgba(255, 255, 255, 0.3);
  transform: skewX(-45deg);
  transition: left 0.5s;
}
.likes {
  display: flex;
  align-items: center;
  gap: 5px; /* Espacio entre la imagen y el texto */
}

.likeee {
  width: 20px;
  height: 20px;
}

.boton_ver:hover::before {
  left: 100%;
}

.boton_ver:hover {
  transform: scale(1.1);
  box-shadow: 0 0 15px rgba(255, 215, 0, 0.8);
}

.user-details h2:hover {
    transform: scale(1.2);
    text-shadow: 0 0 20px rgb(255, 255, 255);
}

.user-details p {
  margin: 5px 0;
  font-size: 1.1rem;

  
}

.team-info {
  display: flex;
  justify-content: flex-end;
  align-items: center;
  position: relative;
  margin-bottom: 30px;
  cursor: pointer;
  width: 20%;
  margin-left: 100%
}

.team-logo {
  width: 70px;
  height: 70px;
  border-radius: 50%;
  object-fit: cover;
  border: solid black;
  box-shadow: 0 0 20px white;
}
.team-logo:hover{
    transform: scale(1.1);
}

.descr{
  color: aliceblue;
  font-size: 120%;
}
.no-team-info {
  font-size: 1.5rem;
  color: #949494;
  margin-left: 70%;
}

  .videos-section {
    width: 90%;
    margin-top: 2%;
    padding: 20px;
    display: flex;
    flex-direction: column;
    align-items: center;  
    font-weight: bold;
    font-family: Cambria, Cochin, Georgia, Times, 'Times New Roman', serif;
    color: #ffd700; /* Dorado */
    text-shadow: 0 0 10px rgba(255, 215, 0, 0.8);
    border: 2px solid #7e7e7e; /* Borde dorado */
    padding: 10px 15px;
    border-radius: 8px;
    margin-bottom: 20px;
    background: linear-gradient(90deg, rgba(212, 212, 212, 0.2), rgba(255, 215, 0, 0));
  }
  
  .videos-section h3 {
  font-size: 2.2rem;
  font-weight: bold;
  font-family: Cambria, Cochin, Georgia, Times, 'Times New Roman', serif;
  color: #ffd700; /* Dorado */
  text-shadow: 0 0 10px rgba(255, 215, 0, 0.8);
  border: 2px solid #ffd700; /* Borde dorado */
  padding: 10px 15px;
  border-radius: 8px;
  margin-bottom: 20px;
  background: linear-gradient(90deg, rgba(224, 197, 108, 0.2), rgba(255, 215, 0, 0));
  box-shadow: 0 0 10px rgba(255, 215, 0, 0.5);
}

.videos-section h3 {
    font-size: 2.2rem;
    margin-bottom: 20px;
    
    font-family:Cambria, Cochin, Georgia, Times, 'Times New Roman', serif;
    color: white;
    text-shadow: 0 0 10px white;
    border: 2px solid white;
    margin-bottom: 3%;
    padding: 1%;
    box-shadow: 0 0 4px #ddd;
  }

  .videos-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
    gap: 20px;
    width: 100%;
  }
  .video-card {
    display: flex;
    flex-direction: column;
    align-items: center;
    text-align: center;
    border: 1px solid #ddd;
    border-radius: 8px;
    padding: 5px;
    background-color: #030303;
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
    transition: transform 0.3s;
    border: solid white;
    box-shadow: 0 0 10px#949494;
  }

  .video-card:hover {
    transform: scale(1.05);
    box-shadow: 0 0 20px#ffc400;
  }

  .video-content {
    display: flex;
    flex-direction: column;
    align-items: center;
    
    
  }
.usuarios{
    display: flex;
    flex-direction: row;
}
.image-modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.8);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.image-modal .large-image {
  max-width: 90%;
  max-height: 90%;
  border-radius: 10px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  animation: fadeIn 0.3s ease-in-out;
}
.like-icon {
   width: 20px;
   height: 20px;
   margin-right: 5px;
 }
/* Animación para que el modal aparezca suavemente */
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
.video-content {
  width: 80%;
  overflow: hidden; /* Evita que el video se desborde */
  display: flex;
  justify-content: center;
  align-items: center;
}

.video {
  max-width: 100%; /* Evita que el video sea más grande que su contenedor */
  width: 100%;
  height: 200px;
  border-radius: 8px;
  margin-bottom: 10px;
  object-fit: cover;
  border: 1px solid white;
  box-shadow: 0 0 5px #949494;
}


#letra {
  font-size: 1rem;
  color: #ffffff;
}
#letra:hover{
    color: #ffffff; /* Cambia el color del enlace al pasar el ratón */
    background-color: transparent; 
}


#letra-link:focus {
  outline: none; /* Asegura que no aparezca el borde en el foco */
}
.video-search {
  width: 100%;
  max-width: 300px;
  padding: 10px;
  margin-bottom: 15px;
  border: 2px solid rgb(255, 255, 255);
  border-radius: 25px;
  outline: none;
  font-size: 16px;
  color: rgb(255, 255, 255);
  background-color: #222;
  transition: all 0.3s ease-in-out;
  box-shadow: 2px 2px 10px rgba(255, 215, 0, 0.4);
}



.video-search:focus {
  border-color: gold;
  box-shadow: 0 0 12px rgba(255, 215, 0, 0.8);
  background-color: #111;
  color: rgba(255, 215, 0, 0.7);
}
  
.juador_sin {
  color: #000000; /* Rojo suave para destacar */
  font-weight: bold;
  font-size: 15px;
  background-color: #a3a3a3; /* Fondo rosado claro */
  padding: 5px 10px;
  border-radius: 5px;
  display: inline-block;
  text-align: center;
  min-width: 200px;
}
.equipp{
  text-align: center;
  color: #000000;
  font-size: 17px;
}
H12{
  color: white;
}
</style>
