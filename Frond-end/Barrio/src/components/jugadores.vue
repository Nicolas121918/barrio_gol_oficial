<template>
  <header>
    <Headerapp />
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
            <h3 v-html="highlightName(profile.nombre)"></h3>
            <p class="profile-city">Ciudad: {{ profile.ciudad }}</p>
            <p class="profile-position">Posición: {{ profile.posicion }}</p>
          </div>
          <button class="inspect-button" @click="verPerfil(profile.documento)">
Inspeccionar
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
import axios from "axios";
import Perfiles from "./perfiles.vue";
import { useUsuarios } from "@/stores/usuario";
export default {
  name: "ProfileViewer",
  components: {
    Headerapp,
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
.profile-viewer {
    
  max-width: 800px;
  margin: auto;
  padding: 20px;
  font-family: Arial, sans-serif;
  background-color: #000000;
  border: 3px solid white;
  border-radius: 10px;
  box-shadow: 3px 8px 15px rgb(255, 255, 255);
  transition: transform 0.3s, box-shadow 0.3s;
  margin-top: 15%;
}

.profile-viewer:hover {
  transform: scale(1.02);
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
  background-color: #222222;
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
  border: 2px solid #000000;
  cursor: pointer;
}

.profile-info {
  flex-grow: 1;
}

.profile-info h3 {
  margin: 0;
  font-size: 18px;
  text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.3);
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
  max-width: 250px;  /* Limita el tamaño de la imagen para que no sea tan grande */
  max-height: 250px;
  border: 5px solid white;
  border-radius: 10px;
}

.modal-overlay:hover {
  cursor: pointer;
}
</style>
