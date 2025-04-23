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
              'highlight': isHighlighted(profile.name),
              'single-match': filteredProfiles.length === 1
            }"
          >
            <img 
              :src="profile.photo" 
              alt="Foto de perfil" 
              class="profile-photo" 
              @click="openModal(profile.photo)"
            />
            <div class="profile-info">
              <h3 v-html="highlightName(profile.name)"></h3>
              <p class="profile-city">Ciudad: {{ profile.city }}</p>
              <p class="profile-position">Posición: {{ profile.position }}</p>
            </div>
            <router-link class="inspect-button2" to="/perfiles">
              Inspeccionar
            </router-link>
            <button 
              class="inspect-button" 
              :class="{'invited': isInvited(profile.id)}" 
              @click="toggleInvite(profile.id)"
            >
              {{ isInvited(profile.id) ? 'Cancelar Inv' : 'Invitar' }}
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
          <img :src="selectedImage" alt="Imagen completa" class="modal-image" />
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import Headerapp from "./Headerapp.vue";
  
  export default {
    name: "ProfileViewer",
    components: {
      Headerapp,
    },
    data() {
      return {
        searchQuery: "",
        profiles: [
          {
            id: 1,
            name: "Carlos Pérez",
            photo: "https://yt3.googleusercontent.com/gUSlp1a1QDyDcVuCFVQGtRIxNBo1oO3aEbHd2i4iatjnj0GxX8Lz4ILwKqO_8kAu6LQfrto8=s160-c-k-c0x00ffffff-no-rj",
            city: "Bogotá",
            position: "Delantero",
          },
          {
            id: 2,
            name: "Ana Gómez",
            photo: "https://s3.amazonaws.com/prod-wp-tunota/wp-content/uploads/2024/11/foto-team-canguro-para-perfil-hd-4k-imagen.jpg",
            city: "Medellín",
            position: "Defensa",
          },
          {
            id: 3,
            name: "Diego Sebastián",
            photo: "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcT2KeaP3HuofX_Z6TAMwTNPlpeyF2vlEBfUbA&s",
            city: "Cali",
            position: "Mediocampista",
          },
          // Agrega más perfiles según sea necesario
        ],
        isModalOpen: false,
        selectedImage: "",
        invitedProfiles: new Set(),
      };
    },
    computed: {
      filteredProfiles() {
        const normalizedQuery = this.removeAccents(this.searchQuery.toLowerCase());
  
        return this.profiles.filter(
          (profile) =>
            this.removeAccents(profile.name.toLowerCase()).includes(normalizedQuery) ||
            this.removeAccents(profile.city.toLowerCase()).includes(normalizedQuery) ||
            this.removeAccents(profile.position.toLowerCase()).includes(normalizedQuery)
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
      toggleInvite(profileId) {
        if (this.invitedProfiles.has(profileId)) {
          this.invitedProfiles.delete(profileId);
        } else {
          this.invitedProfiles.add(profileId);
        }
      },
      isInvited(profileId) {
        return this.invitedProfiles.has(profileId);
      },
      saveSearchQuery() {
        localStorage.setItem("searchQuery", this.searchQuery);
      },
      loadSearchQuery() {
        this.searchQuery = localStorage.getItem("searchQuery") || "";
      },
    },
    watch: {
      searchQuery: "saveSearchQuery",
    },
    created() {
      this.loadSearchQuery();
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
    width: 100px;
    height: 100px;
    border-radius: 50%;
    object-fit: cover;
    cursor: pointer;
    border: 2px solid #000000;
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
    font-weight: bold;
  }
  
  .profile-city,
  .profile-position {
    font-size: 14px;
    margin: 5px 0;
  }
  
  .inspect-button2 {
    background-color: #d4af37;
    color: white;
    padding: 8px 16px;
    border-radius: 5px;
    text-decoration: none;
    cursor: pointer;
  }
  
  .inspect-button2:hover {
    background-color: #9b7d3e;
  }
  
  .inspect-button {
    background-color: #007bff;
    color: white;
    border: none;
    padding: 8px 16px;
    border-radius: 5px;
    cursor: pointer;
  }
  
  .inspect-button.invited {
    background-color: #ccc;
    color: #666;
  }
  
  .inspect-button:hover {
    background-color: #0056b3;
  }
  
  .no-results {
    text-align: center;
    font-size: 16px;
    color: #ccc;
  }
  
  .modal-overlay {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background-color: rgba(0, 0, 0, 0.7);
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 1000;
  }
  
  .modal-content {
    position: relative;
    max-width: 90%;
    max-height: 90%;
    display: flex;
    justify-content: center;
    align-items: center;
  }
  
  .modal-image {
    max-width: 90vw;
    max-height: 90vh;
    object-fit: contain;
    border-radius: 10px;
  }

  .modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.7);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-content {
  position: relative;
  max-width: 90%;
  max-height: 90%;
  display: flex;
  justify-content: center;
  align-items: center;
}

.modal-image {
  width: auto;
  height: auto;
  max-width: 90vw;
  max-height: 90vh;
  object-fit: contain;
  border-radius: 10px;
  /* Añadimos un tamaño de imagen uniforme */
  display: block;
  margin: 0 auto;
}

  </style>
  