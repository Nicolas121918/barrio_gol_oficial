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
  <div class="profile-viewer">
    <div class="search-bar" :class="{ 'searching': searchQuery }">
      <input
        v-model="searchQuery"
        type="text"
        placeholder="Buscar por nombre, ciudad o posición..."
        class="search-input"
      />
    </div>
    <div class="profiles" :class="{ 'search-active': searchQuery }">
      <template v-if="filteredProfiles.length > 0">
        <div
          v-for="profile in filteredProfiles"
          :key="profile.id"
          class="profile-card"
          :class="{
            'highlight': isHighlighted(profile.nombre),
            'single-match': filteredProfiles.length === 1
          }">
          <img 
            :src="getImagenUrl(profile.imagen)" 
            alt="Foto de perfil" 
            class="profile-photo" 
            @click="openModal(getImagenUrl(profile.imagen))"
          />
          <div class="profile-info">
            <h3 class="tituloo" v-html="highlightName(profile.nombre)"></h3>
            <p class="profile-city">Ciudad: {{ profile.ciudad }}</p>
            <p class="profile-position">Posición: {{ profile.posicion }}</p>
          </div>
          <button class="inspect-button" @click="verPerfil(profile.documento)">
Ver Perfil
</button>
        </div>
        
      </template>
      <p v-else class="no-results">
        {{ searchQuery ? `No hay resultados para "${searchQuery}"` : 'Comienza a escribir para buscar...' }}
      </p>
    </div>

    <!-- Modal de imagen -->
    <div v-if="isModalOpen" class="modal-overlay" @click="closeModal">
<div class="modal-content">
  <img 
    :src="selectedImage" 
    alt="Imagen completa" 
    class="modal-image"
  />

</div>
</div>
  </div>
</template>

<script>
import Headerapp from "./Headerapp.vue";
import headermobile from "./headermobile.vue";
import axios from "axios";
import { useUsuarios } from "@/stores/usuario";
export default {
  name: "ProfileViewer",
  components: {
    Headerapp,
    headermobile,
  },
  data() {
    return {
      searchQuery: "",
      profiles: [],
      isModalOpen: false,
      selectedImage: "", 

    };
  },
  computed: {
    filteredProfiles() {
      const normalizedQuery = this.removeAccents(this.searchQuery.toLowerCase());

      return this.profiles.filter(
        (profile) =>
          this.removeAccents(profile.nombre.toLowerCase()).includes(normalizedQuery) ||
          this.removeAccents(profile.ciudad.toLowerCase()).includes(normalizedQuery) ||
          this.removeAccents(profile.posicion.toLowerCase()).includes(normalizedQuery)
      );
    },
  },
  methods: {
    isHighlighted(name) {
      const normalizedQuery = this.removeAccents(this.searchQuery.toLowerCase());
      return (
        normalizedQuery &&
        this.removeAccents(name.toLowerCase()).includes(normalizedQuery)
      );
    },
    highlightName(name) {
      if (!this.searchQuery) return name;

      const regex = new RegExp(`(${this.searchQuery})`, "gi");
      return name.replace(regex, '<span class="highlight-text">$1</span>');
    },
    verPerfil(documento) {
  this.$router.push(`/perfiles/${documento}`); // Redirige usando el documento
},
    removeAccents(str) {
      return str.normalize("NFD").replace(/[̀-ͯ]/g, "");
    },
    openModal(imageUrl) {
  this.selectedImage = imageUrl; 
  this.isModalOpen = true;
},
closeModal() {
  this.isModalOpen = false;
  this.selectedImage = "";
},
    saveSearchQuery() {
      localStorage.setItem("searchQuery", this.searchQuery);
    },
    loadSearchQuery() {
      this.searchQuery = localStorage.getItem("searchQuery") || "";
    },
    async getUsuarios() {
      const movistore = useUsuarios()
    try {
      const response = await axios.get(`http://localhost:8000/usuarios/${movistore.usuario.documento}`);
      this.profiles = response.data; // Asignar los usuarios obtenidos a la variable `usuarios`
    } catch (error) {
      console.error('Error al obtener los torneos:', error);
    }
  },

   getImagenUrl : (path) =>{
    return `http://127.0.0.1:8000/${path}`;
  },
  
  },
  watch: {
    searchQuery: "saveSearchQuery",
  },
  created() {
    this.loadSearchQuery();
    this.getUsuarios();
  },
};


</script>

<style scoped>
/* Estilos generales para el contenedor principal */
.profile-viewer {
  max-width: 800px;
  margin: auto;
  padding: 20px;
  font-family: Arial, sans-serif;
  background-color: #000000;
  border: 3px solid white;
  border-radius: 10px;
  box-shadow: 3px 8px 15px rgb(255, 255, 255);
  margin-top: 50%;
}

.profile-viewer:hover {
  box-shadow: 0 12px 20px rgb(255, 230, 8);
}

.search-bar {
  margin-bottom: 20px;
}

.search-bar.searching {
  background-color: #f0e6d2;
  border: 2px solid #d4af37;
  border-radius: 8px;
  padding: 10px;
  transition: background-color 0.3s, border-color 0.3s;
}

.search-input {
  width: 100%;
  padding: 12px;
  font-size: 16px;
  border: 1px solid #ccc;
  border-radius: 5px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  transition: box-shadow 0.3s, border-color 0.3s;
  text-align: center;
}

.search-input:focus {
  border-color: #d4af37;
  box-shadow: 0 6px 10px rgba(0, 0, 0, 0.15);
}

.profiles {
  display: flex;
  flex-direction: column;
  gap: 20px;
  min-height: 200px;
}

.profiles.search-active {
  border-radius: 10px;
  padding: 10px;
  transition: background-color 0.3s, border-color 0.3s;
}

.profile-card {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 15px;
  padding: 15px;
  border: 2px solid #ccc;
  border-radius: 10px;
  background: linear-gradient(to bottom, #222222, #111111);

  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s, box-shadow 0.3s;
  width: 100%;
  box-shadow: 0 0 10px white;
}

.profile-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
  background-color: #f4f4f4;
  color: black;
  border: solid rgb(255, 213, 0) 1px;
  box-shadow: 0 0 20px rgb(255, 238, 0);
}

.profile-card.highlight {
  border-color: #d4af37;
  background-color: #696969;
}

.profile-card.single-match {
  border-color: #007bff;
  background-color: #faffcc;
  color: black;
}

.profile-photo {
  width: 70px;
  height: 70px;
  border-radius: 50%;
  object-fit: cover;
  border: 2px solid #ffffff;
  cursor: pointer;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}
.tituloo{
  color: rgb(255, 213, 0);
 font-family: Georgia, 'Times New Roman', Times, serif;
 font-size: 50%;
 text-decoration: underline;
}
.profile-photo:hover {
  transform: scale(1.05);
  box-shadow: 0 0 10px gold;
}

.profile-info {
  flex-grow: 1;
}

.profile-info h3 {
  margin: 0;
  font-size: 18px;
  text-shadow: 1px 1px 2px rgba(123, 255, 0, 0.3);
}

.profile-info h3 .highlight-text {
  background-color: #d4af37;
  color: white;
  padding: 0 3px;
  border-radius: 3px;
  text-decoration: underline;
}

.profile-city, .profile-position {
  font-size: 14px;
  color: #808080;
}

.inspect-button {
  padding: 8px 15px;
  background-image: url('https://static.vecteezy.com/system/resources/thumbnails/000/549/015/small/vector-apr-2018-19.jpg');
  color: rgb(0, 0, 0);
  font-weight: bold;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  box-shadow: 0 0px 8px rgba(247, 247, 247, 0.932);
  transition: background-color 0.3s, box-shadow 0.3s;
  border: 3px solid black;
}

.inspect-button:hover {
  background-color: #bfa328;
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.2);
  transform: scale(1.1);
}

.inspect-button:active {
  background-color: #9e8f24;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.no-results {
  text-align: center;
  color: #666;
  font-style: italic;
  margin-top: 20px;
  font-size: 180%;
}

/* Estilos del modal */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 50vw;
  background: rgba(0, 0, 0, 0.8);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-content {
  position: relative;
}

.modal-image {

  width: 80vh;
  height: 70vh;
  border: 5px solid white;
  border-radius: 10px;
  margin: auto;
}

.modal-overlay:hover {
  cursor: pointer;
}


@media (min-width: 320px) and (max-width: 480px) {
  .profile-viewer {
    max-width: 400px;
    margin: auto;
    padding: 5%;
    font-family: Arial, sans-serif;
    background-color: #000000;
    border: 3px solid white;
    border-radius: 10px;
    box-shadow: 3px 8px 15px rgb(255, 255, 255);
    margin-top: 50%;
  }
.profile-viewer:hover {
  box-shadow: 0 12px 20px rgb(255, 230, 8);
}
  
  .search-bar {
    margin-bottom: 15px;
  }

  
  .search-input {
    width: 100%;
    padding: 3%;
    font-size: 1rem;
    border: 1px solid #ccc;
    border-radius: 5px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    transition: box-shadow 0.3s, border-color 0.3s;
    text-align: center;
  }
  
  .search-input:focus {
    border-color: #d4af37;
    box-shadow: 0 6px 10px rgba(0, 0, 0, 0.15);
  }
  
  .profiles {
    display: flex;
    flex-direction: column;
    gap: 20px;
    min-height: 200px;
  }
  
  .profiles.search-active {
    border-radius: 10px;
    padding: 10px;
    transition: background-color 0.3s, border-color 0.3s;
  }
  
  .profile-card {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 15px;
    padding: 15px;
    border: 2px solid #ccc;
    border-radius: 10px;
    background-color: #222222;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    transition: transform 0.3s, box-shadow 0.3s;
    width: 100%;
    box-shadow: 0 0 10px white;
  }
             
  .profile-photo {
    width: 70px;
    height: 70px;
    border-radius: 50%;
    object-fit: cover;
    border: 2px solid #ffffff;
    cursor: pointer;
  }

  .profile-info {
    flex-grow: 1;
  }
  
  .profile-info h3 {
    margin: 0;
    font-size: 18px;
    text-shadow: 1px 1px 2px rgb(0, 0, 0);
  }
  
  .profile-info h3 .highlight-text {
    background-color: #d4af37;
    color: white;
    padding: 0 3px;
    border-radius: 3px;
    text-decoration: underline;
  }
  
  .profile-city, .profile-position {
    font-size: 1.05rem;
    color: #808080;
  }
  
  .inspect-button {
    padding: 1% 1%;
    background-image: url('https://static.vecteezy.com/system/resources/thumbnails/000/549/015/small/vector-apr-2018-19.jpg');
    color: rgb(0, 0, 0);
    font-weight: bold;
    border: none;
    border-radius: 5px;
    cursor: pointer;
    box-shadow: 0 0px 8px rgba(247, 247, 247, 0.932);
    transition: background-color 0.3s, box-shadow 0.3s;
    border: 3px solid black;
    margin-left: -10%;
    margin-top: 10%;
  }
  
  .inspect-button:hover {
    background-color: #bfa328;
    box-shadow: 0 6px 12px rgba(0, 0, 0, 0.2);
    transform: scale(1.1);
  }
  
  .inspect-button:active {
    background-color: #9e8f24;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    
  }
  
  .no-results {
    text-align: center;
    color: #666;
    font-style: italic;
    margin-top: 20px;
    font-size: 180%;
  }
  
  /* Estilos del modal */
  .modal-overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0, 0, 0, 0.8);
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 1000;
  }
  
  .modal-content {
    position: relative;
  }
  
  .modal-image {
    max-width: 100%;  
    max-height: 100%;
    border: 5px solid white;
    border-radius: 10px;
  }
  
  .modal-overlay:hover {
    cursor: pointer;
  }
  

  
}
/*  Media queries para diferentes tamaños de pantalla  desde 481 px hasta 600px */
@media (min-width: 481px) and (max-width: 600px) {
  .profile-viewer {
    max-width: 100%;
    margin: auto;
    padding: 5%;
    font-family: Arial, sans-serif;
    background-color: #000000;
    border: 3px solid white;
    border-radius: 10px;
    box-shadow: 3px 8px 15px rgb(255, 255, 255);
    margin-top: 40%;
  }
.profile-viewer:hover {
  box-shadow: 0 12px 20px rgb(255, 230, 8);
}
  
  .search-bar {
    margin-bottom: 15px;
  }

  
  .search-input {
    width: 100%;
    padding: 3%;
    font-size: 1rem;
    border: 1px solid #ccc;
    border-radius: 5px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    transition: box-shadow 0.3s, border-color 0.3s;
    text-align: center;
  }
  
  .search-input:focus {
    border-color: #d4af37;
    box-shadow: 0 6px 10px rgba(0, 0, 0, 0.15);
  }
  
  .profiles {
    display: flex;
    flex-direction: column;
    gap: 20px;
    min-height: 200px;
  }
  
  .profiles.search-active {
    border-radius: 10px;
    padding: 10px;
    transition: background-color 0.3s, border-color 0.3s;
  }
  
  .profile-card {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 15px;
    padding: 15px;
    border: 2px solid #ccc;
    border-radius: 10px;
    background-color: #222222;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    transition: transform 0.3s, box-shadow 0.3s;
    width: 100%;
    box-shadow: 0 0 10px white;
  }
             
  .profile-photo {
    width: 70px;
    height: 70px;
    border-radius: 50%;
    object-fit: cover;
    border: 2px solid #ffffff;
    cursor: pointer;
  }

  .profile-info {
    flex-grow: 1;
  }
  .profile-info h3 {
    margin: 0;
    font-size: 18px;
    text-shadow: 1px 1px 2px rgb(0, 0, 0);
  }
  
  .profile-info h3 .highlight-text {
    background-color: #d4af37;
    color: white;
    padding: 0 3px;
    border-radius: 3px;
    text-decoration: underline;
  }
  
  .profile-city, .profile-position {
    font-size: 1.05rem;
    color: #808080;
  }
  
  .inspect-button {
    padding: 1% 1%;
    background-image: url('https://static.vecteezy.com/system/resources/thumbnails/000/549/015/small/vector-apr-2018-19.jpg');
    color: rgb(0, 0, 0);
    font-weight: bold;
    border: none;
    border-radius: 5px;
    cursor: pointer;
    box-shadow: 0 0px 8px rgba(247, 247, 247, 0.932);
    transition: background-color 0.3s, box-shadow 0.3s;
    border: 3px solid black;
    margin-left: -10%;
  }
  
  .inspect-button:hover {
    background-color: #bfa328;
    box-shadow: 0 6px 12px rgba(0, 0, 0, 0.2);
    transform: scale(1.1);
  }
  
  .inspect-button:active {
    background-color: #9e8f24;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    
  }
  
  .no-results {
    text-align: center;
    color: #666;
    font-style: italic;
    margin-top: 20px;
    font-size: 180%;
  }
  /* Estilos del modal */
  .modal-overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0, 0, 0, 0.8);
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 1000;
  }
  
  .modal-content {
    position: relative;
  }
  
  .modal-image {
    max-width: 80%;  
    max-height: 80%;
    border: 5px solid white;
    border-radius: 10px;
  }
  
  .modal-overlay:hover {
    cursor: pointer;
  }
  
}
@media (min-width: 601px) and (max-width: 768px) {

  .profile-viewer {
    width: 130%;
    max-width: 150%;
    margin: auto;
    padding: 5%;
    font-family: Arial, sans-serif;
    background-color: #000000;
    border: 3px solid white;
    border-radius: 10px;
    box-shadow: 3px 8px 15px rgb(255, 255, 255);
    margin-top: 40%;
    margin-left: -15%;
  } 
  .profile-viewer:hover {
  box-shadow: 0 12px 20px rgb(255, 230, 8);
}

  
  .search-bar {
    margin-bottom: 15px;
  }

  
  .search-input {
    width: 100%;
    padding: 3%;
    font-size: 1rem;
    border: 1px solid #ccc;
    border-radius: 5px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    transition: box-shadow 0.3s, border-color 0.3s;
    text-align: center;
  }
  
  .search-input:focus {
    border-color: #d4af37;
    box-shadow: 0 6px 10px rgba(0, 0, 0, 0.15);
  }
  
  .profiles {
    display: flex;
    flex-direction: column;
    gap: 20px;
    min-height: 200px;
  }
  
  .profiles.search-active {
    border-radius: 10px;
    padding: 10px;
    transition: background-color 0.3s, border-color 0.3s;
  }
  
  .profile-card {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 15px;
    padding: 15px;
    border: 2px solid #ccc;
    border-radius: 10px;
    background-color: #222222;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    transition: transform 0.3s, box-shadow 0.3s;
    width: 100%;
    box-shadow: 0 0 10px white;
  }
             
  .profile-photo {
    width: 70px;
    height: 70px;
    border-radius: 50%;
    object-fit: cover;
    border: 2px solid #ffffff;
    cursor: pointer;
  }

  
  .profile-info {
    flex-grow: 1;
  }
  .profile-info h3 {
    margin: 0;
    font-size: 18px;
    text-shadow: 1px 1px 2px rgb(0, 0, 0);
  }
  
  .profile-info h3 .highlight-text {
    background-color: #d4af37;
    color: white;
    padding: 0 3px;
    border-radius: 3px;
    text-decoration: underline;
  }
  
  .profile-city, .profile-position {
    font-size: 1.05rem;
    color: #808080;
  }
  
  .inspect-button {
    padding: 1% 1%;
    background-image: url('https://static.vecteezy.com/system/resources/thumbnails/000/549/015/small/vector-apr-2018-19.jpg');
    color: rgb(0, 0, 0);
    font-weight: bold;
    border: none;
    border-radius: 5px;
    cursor: pointer;
    box-shadow: 0 0px 8px rgba(247, 247, 247, 0.932);
    transition: background-color 0.3s, box-shadow 0.3s;
    border: 3px solid black;
    margin-left: -10%;
  }
  
  .inspect-button:hover {
    background-color: #bfa328;
    box-shadow: 0 6px 12px rgba(0, 0, 0, 0.2);
    transform: scale(1.1);
  }
  
  .inspect-button:active {
    background-color: #9e8f24;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    
  }
  
  .no-results {
    text-align: center;
    color: #666;
    font-style: italic;
    margin-top: 20px;
    font-size: 180%;
  }
  
  /* Estilos del modal */
  .modal-overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0, 0, 0, 0.8);
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 1000;
  }
  
  .modal-content {
    position: relative;
  }
  
  .modal-image {
    max-width: 60%;  
    max-height: 60%;
    border: 5px solid white;
    border-radius: 10px;
  }
  
  .modal-overlay:hover {
    cursor: pointer;
  }

  
}

@media (min-width: 769px) and (max-width: 1024px) {

  .profile-viewer {
    width: 140%;
    max-width: 150%;
    margin: auto;
    padding: 5%;
    font-family: Arial, sans-serif;
    background-color: #000000;
    border: 3px solid white;
    border-radius: 10px;
    box-shadow: 3px 8px 15px rgb(255, 255, 255);
    margin-top: 40%;
    margin-left: -20%;
  } 
  .profile-viewer:hover {
  box-shadow: 0 12px 20px rgb(255, 230, 8);
}

  
  .search-bar {
    margin-bottom: 15px;
  }

  
  .search-input {
    width: 100%;
    padding: 3%;
    font-size: 1rem;
    border: 1px solid #ccc;
    border-radius: 5px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    transition: box-shadow 0.3s, border-color 0.3s;
    text-align: center;
  }
  
  .search-input:focus {
    border-color: #d4af37;
    box-shadow: 0 6px 10px rgba(0, 0, 0, 0.15);
  }
  
  .profiles {
    display: flex;
    flex-direction: column;
    gap: 20px;
    min-height: 200px;
  }
  
  .profiles.search-active {
    border-radius: 10px;
    padding: 10px;
    transition: background-color 0.3s, border-color 0.3s;
  }
  
  .profile-card {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 15px;
    padding: 15px;
    border: 2px solid #ccc;
    border-radius: 10px;
    background-color: #222222;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    transition: transform 0.3s, box-shadow 0.3s;
    width: 100%;
    box-shadow: 0 0 10px white;
  }
             
  .profile-photo {
    width: 70px;
    height: 70px;
    border-radius: 50%;
    object-fit: cover;
    border: 2px solid #ffffff;
    cursor: pointer;
  }

  .profile-info {
    flex-grow: 1;
  }
  .profile-info h3 {
    margin: 0;
    font-size: 18px;
    text-shadow: 1px 1px 2px rgb(0, 0, 0);
  }
  
  .profile-info h3 .highlight-text {
    background-color: #d4af37;
    color: white;
    padding: 0 3px;
    border-radius: 3px;
    text-decoration: underline;
  }
  
  .profile-city, .profile-position {
    font-size: 1.05rem;
    color: #808080;
  }
  
  .inspect-button {
    padding: 1% 1%;
    background-image: url('https://static.vecteezy.com/system/resources/thumbnails/000/549/015/small/vector-apr-2018-19.jpg');
    color: rgb(0, 0, 0);
    font-weight: bold;
    border: none;
    border-radius: 5px;
    cursor: pointer;
    box-shadow: 0 0px 8px rgba(247, 247, 247, 0.932);
    transition: background-color 0.3s, box-shadow 0.3s;
    border: 3px solid black;
    margin-left: -10%;
  }
  
  .inspect-button:hover {
    background-color: #bfa328;
    box-shadow: 0 6px 12px rgba(0, 0, 0, 0.2);
    transform: scale(1.1);
  }
  
  .inspect-button:active {
    background-color: #9e8f24;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    
  }
  
  .no-results {
    text-align: center;
    color: #666;
    font-style: italic;
    margin-top: 20px;
    font-size: 180%;
  }
  
  /* Estilos del modal */
  .modal-overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0, 0, 0, 0.8);
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 1000;
  }
  
  .modal-content {
    position: relative;
  }
  
  .modal-image {
    max-width: 50%;  
    max-height: 50%;
    border: 5px solid white;
    border-radius: 10px;
  }
  
  .modal-overlay:hover {
    cursor: pointer;
  }

}


@media (min-width: 1025px) and (max-width: 1440px) {
  .profile-viewer {
    width: 180%;
    max-width: 200%;
    margin: auto;
    padding: 5%;
    font-family: Arial, sans-serif;
    background-color: #000000;
    border: 3px solid white;
    border-radius: 10px;
    box-shadow: 3px 8px 15px rgb(255, 255, 255);
    margin-top: 40%;
    margin-left: -35%;
  } 
  .profile-viewer:hover {
  box-shadow: 0 12px 20px rgb(255, 230, 8);
}

  
  .search-bar {
    margin-bottom: 15px;
  }

  
  .search-input {
    width: 100%;
    padding: 3%;
    font-size: 1rem;
    border: 1px solid #ccc;
    border-radius: 5px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    transition: box-shadow 0.3s, border-color 0.3s;
    text-align: center;
  }
  
  .search-input:focus {
    border-color: #d4af37;
    box-shadow: 0 6px 10px rgba(0, 0, 0, 0.15);
  }
  
  .profiles {
    display: flex;
    flex-direction: column;
    gap: 20px;
    min-height: 200px;
  }
  
  .profiles.search-active {
    border-radius: 10px;
    padding: 10px;
    transition: background-color 0.3s, border-color 0.3s;
  }
  
  .profile-card {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 15px;
    padding: 15px;
    border: 2px solid #ccc;
    border-radius: 10px;
    background-color: #222222;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    transition: transform 0.3s, box-shadow 0.3s;
    width: 100%;
    box-shadow: 0 0 10px white;
  }
             
  .profile-photo {
    width: 70px;
    height: 70px;
    border-radius: 50%;
    object-fit: cover;
    border: 2px solid #ffffff;
    cursor: pointer;
  }

  .profile-info {
    flex-grow: 1;
  }
  .profile-info h3 {
    margin: 0;
    font-size: 18px;
    text-shadow: 1px 1px 2px rgb(0, 0, 0);
  }
  
  .profile-info h3 .highlight-text {
    background-color: #d4af37;
    color: white;
    padding: 0 3px;
    border-radius: 3px;
    text-decoration: underline;
  }
  
  .profile-city, .profile-position {
    font-size: 1.05rem;
    color: #808080;
  }
  
  .inspect-button {
    padding: 1% 1%;
    background-image: url('https://static.vecteezy.com/system/resources/thumbnails/000/549/015/small/vector-apr-2018-19.jpg');
    color: rgb(0, 0, 0);
    font-weight: bold;
    border: none;
    border-radius: 5px;
    cursor: pointer;
    box-shadow: 0 0px 8px rgba(247, 247, 247, 0.932);
    transition: background-color 0.3s, box-shadow 0.3s;
    border: 3px solid black;
    margin-left: -10%;
  }
  
  .inspect-button:hover {
    background-color: #bfa328;
    box-shadow: 0 6px 12px rgba(0, 0, 0, 0.2);
    transform: scale(1.1);
  }
  
  .inspect-button:active {
    background-color: #9e8f24;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    
  }
  
  .no-results {
    text-align: center;
    color: #666;
    font-style: italic;
    margin-top: 20px;
    font-size: 180%;
  }
  
  /* Estilos del modal */
  .modal-overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0, 0, 0, 0.8);
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 1000;
  }
  
  .modal-content {
    position: relative;
  }
  
  .modal-image {
    max-width: 50%;  
    max-height: 50%;
    border: 5px solid white;
    border-radius: 10px;
  }
  
  .modal-overlay:hover {
    cursor: pointer;
  }

  
}
@media (min-width: 1441px) and (max-width: 1920px) {

  .profile-viewer {
    width: 200%;
    max-width: 250%;
    margin: auto;
    padding: 5%;
    font-family: Arial, sans-serif;
    background-color: #000000;
    border: 3px solid white;
    border-radius: 10px;
    box-shadow: 3px 8px 15px rgb(255, 255, 255);
    margin-top: 40%;
    margin-left: -40%;
  } 
  .profile-viewer:hover {
  box-shadow: 0 12px 20px rgb(255, 230, 8);
}

  
  .search-bar {
    margin-bottom: 15px;
  }

  
  .search-input {
    width: 100%;
    padding: 3%;
    font-size: 1rem;
    border: 1px solid #ccc;
    border-radius: 5px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    transition: box-shadow 0.3s, border-color 0.3s;
    text-align: center;
  }
  
  .search-input:focus {
    border-color: #d4af37;
    box-shadow: 0 6px 10px rgba(0, 0, 0, 0.15);
  }
  
  .profiles {
    display: flex;
    flex-direction: column;
    gap: 20px;
    min-height: 200px;
  }
  
  .profiles.search-active {
    border-radius: 10px;
    padding: 10px;
    transition: background-color 0.3s, border-color 0.3s;
  }
  
  .profile-card {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 15px;
    padding: 15px;
    border: 2px solid #ccc;
    border-radius: 10px;
    background-color: #222222;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    transition: transform 0.3s, box-shadow 0.3s;
    width: 100%;
    box-shadow: 0 0 10px white;
  }
             
  .profile-photo {
    width: 70px;
    height: 70px;
    border-radius: 50%;
    object-fit: cover;
    border: 2px solid #ffffff;
    cursor: pointer;
  }

  
  .profile-info {
    flex-grow: 1;
  }
  .profile-info h3 {
    margin: 0;
    font-size: 18px;
    text-shadow: 1px 1px 2px rgb(0, 0, 0);
  }
  
  .profile-info h3 .highlight-text {
    background-color: #d4af37;
    color: white;
    padding: 0 3px;
    border-radius: 3px;
    text-decoration: underline;
  }
  
  .profile-city, .profile-position {
    font-size: 1.05rem;
    color: #808080;
  }
  
  .inspect-button {
    padding: 1% 1%;
    background-image: url('https://static.vecteezy.com/system/resources/thumbnails/000/549/015/small/vector-apr-2018-19.jpg');
    color: rgb(0, 0, 0);
    font-weight: bold;
    border: none;
    border-radius: 5px;
    cursor: pointer;
    box-shadow: 0 0px 8px rgba(247, 247, 247, 0.932);
    transition: background-color 0.3s, box-shadow 0.3s;
    border: 3px solid black;
    margin-left: -10%;
  }
  
  .inspect-button:hover {
    background-color: #bfa328;
    box-shadow: 0 6px 12px rgba(0, 0, 0, 0.2);
    transform: scale(1.1);
  }
  
  .inspect-button:active {
    background-color: #9e8f24;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    
  }
  
  .no-results {
    text-align: center;
    color: #666;
    font-style: italic;
    margin-top: 20px;
    font-size: 180%;
  }
  
  /* Estilos del modal */
  .modal-overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0, 0, 0, 0.8);
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 1000;
  }
  
  .modal-content {
    position: relative;
  }
  
  .modal-image {
    max-width: 35%;  
    max-height: 50%;
    border: 5px solid white;
    border-radius: 10px;
  }
  
  .modal-overlay:hover {
    cursor: pointer;
  }

  
}
@media (min-width: 1921px) and (max-width: 2560px) {

  .profile-viewer {
    width: 250%;
    max-width: 300%;
    margin: auto;
    padding: 10%;
    font-family: Arial, sans-serif;
    background-color: #000000;
    border: 3px solid white;
    border-radius: 10px;
    box-shadow: 3px 8px 15px rgb(255, 255, 255);
    margin-top: 40%;
    margin-left: -60%;
  } 
  .profile-viewer:hover {
  box-shadow: 0 12px 20px rgb(255, 230, 8);
}

  
  .search-bar {
    margin-bottom: 15px;
  }

  
  .search-input {
    width: 100%;
    padding: 3%;
    font-size: 2rem;
    border: 1px solid #ccc;
    border-radius: 5px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    transition: box-shadow 0.3s, border-color 0.3s;
    text-align: center;
  }
  
  .search-input:focus {
    border-color: #d4af37;
    box-shadow: 0 6px 10px rgba(0, 0, 0, 0.15);
  }
  
  .profiles {
    display: flex;
    flex-direction: column;
    gap: 20px;
    min-height: 200px;
  }
  
  .profiles.search-active {
    border-radius: 10px;
    padding: 10px;
    transition: background-color 0.3s, border-color 0.3s;
  }
  
  .profile-card {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 15px;
    padding: 15px;
    border: 2px solid #ccc;
    border-radius: 10px;
    background-color: #222222;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    transition: transform 0.3s, box-shadow 0.3s;
    width: 100%;
    box-shadow: 0 0 10px white;
  }
             
  .profile-photo {
    width: 70px;
    height: 70px;
    border-radius: 50%;
    object-fit: cover;
    border: 2px solid #ffffff;
    cursor: pointer;
  }
  .profile-info {
    flex-grow: 1;
  }
  .profile-info h3 {
    margin: 0;
    font-size: 18px;
    text-shadow: 1px 1px 2px rgb(0, 0, 0);
  }
  
  .profile-info h3 .highlight-text {
    background-color: #d4af37;
    color: white;
    padding: 0 3px;
    border-radius: 3px;
    text-decoration: underline;
  }
  
  .profile-city, .profile-position {
    font-size: 1.05rem;
    color: #808080;
  }
  
  .inspect-button {
    padding: 1% 1%;
    background-image: url('https://static.vecteezy.com/system/resources/thumbnails/000/549/015/small/vector-apr-2018-19.jpg');
    color: rgb(0, 0, 0);
    font-weight: bold;
    border: none;
    border-radius: 5px;
    cursor: pointer;
    box-shadow: 0 0px 8px rgba(247, 247, 247, 0.932);
    transition: background-color 0.3s, box-shadow 0.3s;
    border: 3px solid black;
    margin-left: -10%;
  }
  
  .inspect-button:hover {
    background-color: #bfa328;
    box-shadow: 0 6px 12px rgba(0, 0, 0, 0.2);
    transform: scale(1.1);
  }
  
  .inspect-button:active {
    background-color: #9e8f24;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    
  }
  
  .no-results {
    text-align: center;
    color: #666;
    font-style: italic;
    margin-top: 20px;
    font-size: 180%;
  }
  
  /* Estilos del modal */
  .modal-overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0, 0, 0, 0.8);
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 1000;
  }
  
  .modal-content {
    position: relative;
  }
  
  .modal-image {
    max-width: 25%;  
    max-height: 20%;
    border: 5px solid white;
    border-radius: 10px;
  }
  .modal-overlay:hover {
    cursor: pointer;
  }


  
}
@media (min-width: 2561px) and (max-width: 3840px) {

  
}
@media (min-width: 3841px) and (max-width: 5120px) {

  
}


</style>
