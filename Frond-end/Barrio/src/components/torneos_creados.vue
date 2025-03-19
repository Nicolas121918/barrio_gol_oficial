<template>
  <div class="tournaments-container">
    <!-- Buscador -->
    <div class="search-container">
      <input v-model="searchQuery" type="text" placeholder="Buscar torneo..." class="search-input" />
      <select v-model="searchType" class="search-select">
        <option value="">Todos</option>
        <option value="torneo">Torneo</option>
        <option value="partido">Partido</option>
      </select>
      <router-link to="torneos">
        <button class="btn-donate">Volver</button>
      </router-link>
    </div>

    <!-- Torneos y Partidos del equipo -->
    <div class="section joined-section">
      <h2>Torneos y partidos del equipo</h2>
      <div class="card-container">
        <p v-if="filteredJoinedItems.length === 0" class="no-results-message">
          No hay torneos o partidos con coincidencias
        </p>
        <transition-group name="fade" tag="div" class="card-list">
          <div v-for="item in filteredJoinedItems" :key="item.id" class="card">
            <div class="card-header"> <span>{{ item.type === 'torneo' ? 'Torneo' : 'Partido' }}</span> </div>
            <div v-if="item.logo" class="card-logo-container">
              <img :src="getImagenUrl(item.logo)" alt="Logo" class="card-logo" />
            </div>
            <h3 class="card-title" v-html="highlightText(item.name)"></h3>
            <button @click="viewItem(item)" class="card-button">Ver</button>
          </div>
        </transition-group>
      </div>
    </div>
  </div>
</template>

<script>
import { useUsuarios } from "@/stores/usuario";
import axios from "axios";

export default {
  
  data() {
    return {
      searchQuery: "",
      searchType: "",
      joinedItems: [],
      datos : []
    };
  },
  computed: {
    filteredJoinedItems() {
      return this.joinedItems.filter(item => {
        const nameMatches = item.name.toLowerCase().includes(this.searchQuery.toLowerCase());
        const typeMatches = this.searchType ? item.type === this.searchType : true;
        return nameMatches && typeMatches;
      });
    }
  },
  methods: {
    async fetchTorneos() {
      try {
        const usuarioStore = useUsuarios();
        const documentoCreador = usuarioStore.usuario.documento;
        const response = await axios.get(`http://localhost:8000/listartorneosi/${documentoCreador}`);
        this.joinedItems = response.data.map(torneo => ({
          id: torneo.id,
          name: torneo.nombre,
          type: "torneo",
          logo: torneo.logoTeam
        }));
      } catch (error) {
        console.error("Error obteniendo torneos:", error);
      }
    },
    viewItem(item) {
      console.log(`Viendo ${item.type}: ${item.name}`);
    },
 getImagenUrl : (path) => {
  return path ? `http://127.0.0.1:8000/${path}` : '';
},
    
    highlightText(text) {
      if (!this.searchQuery) return text;
      const regex = new RegExp(`(${this.searchQuery})`, "gi");
      return text.replace(regex, '<mark>$1</mark>');
    }
  },
  mounted() {
    this.fetchTorneos();
  }
};
</script>

  <style scoped>
  .tournaments-container {
    display: flex;
    flex-direction: column;
    gap: 2rem;
    padding: 1rem;
    margin-top: 20%;
  }
  
  .search-container {
    display: flex;
    gap: 1rem;
  }
  
  .back-button {
    background-color: #7d6c6c;
    color: white;
    border: none;
    padding: 0.8rem;
    border-radius: 5px;
    cursor: pointer;
  }
  
  .separator {
    height: 2rem;
  }
  </style>
  
  <style scoped>
  .tournaments-container {
    display: flex;
    flex-direction: column;
    gap: 2rem;
    background-color: rgba(0, 0, 0, 0.438);
    padding: 1rem;
    
  }
  
  .search-container {
    display: flex;
    justify-content: space-between;
    gap: 1rem;
    margin-bottom: 1.5rem;
  }
  
  .search-input {
    padding: 0.8rem;
    font-size: 1rem;
    border: 1px solid #ddd;
    border-radius: 5px;
    width: 70%;
    transition: all 0.3s ease;
  }
  
  .search-input:focus {
    border-color: #c50000;
    outline: none;
  }
  
  .search-select {
    padding: 0.8rem;
    font-size: 1rem;
    border: 1px solid #ddd;
    border-radius: 5px;
    width: 25%;
  }
  
  .section {
    padding: 1.5rem;
    border: 1px solid #ddd;
    border-radius: 8px;
    background-color: #000000;
    text-align: center;
    color: white;
    
  }
  .btn-donate {
  --clr-font-main: hsla(0 0% 20% / 100);
  --btn-bg-1: rgb(255, 255, 255);
  --btn-bg-2: rgb(212, 174, 6);
  --btn-bg-color: rgb(0, 0, 0);
  --radii: 0.5em;
  cursor: pointer;
  padding: 0.9em 1.4em;
  min-width: 120px;
  min-height: 44px;
  font-size: var(--size, 1rem);
  font-weight: 500;
  transition: 0.8s;
  background-size: 280% auto;
  background-image: linear-gradient(
    325deg,
    var(--btn-bg-2) 0%,
    var(--btn-bg-1) 55%,
    var(--btn-bg-2) 90%
  );
  border: none;
  font-family: Cambria, Cochin, Georgia, Times, 'Times New Roman', serif;
  border-radius: var(--radii);
  color: var(--btn-bg-color);
  box-shadow:
    0px 0px 20px rgba(71, 184, 255, 0.5),
    0px 5px 5px -1px rgba(58, 125, 233, 0.25),
    inset 4px 4px 8px rgba(175, 230, 255, 0.5),
}

.btn-donate:hover {
  background-position: right top;
}

.btn-donate:is(:focus, :focus-visible, :active) {
  outline: none;
  box-shadow:
    0 0 0 3px var(--btn-bg-color),
    0 0 0 6px var(--btn-bg-2);
}

@media (prefers-reduced-motion: reduce) {
  .btn-donate {
    transition: linear;
  }
}

  .card-container {
    display: flex;
    flex-wrap: wrap;
    gap: 1.5rem;
    justify-content: center;
  }
  
  .card-list {
    display: flex;
    flex-wrap: wrap;
    gap: 1.5rem;
    transition: opacity 0.5s ease;
    
  }
  
  .card {
    background-color: #000000;
    border: 3px solid #ffd000;
    border-radius: 8px;
    padding: 1.5rem;
    text-align: center;
    width: 220px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    transition: transform 0.3s ease, box-shadow 0.3s ease;
    color: rgb(0, 0, 0);
    font-family:Georgia, 'Times New Roman', Times, serif;
    box-shadow: 0 0 10px white;
    
  }
  .children{
    box-shadow: 0 0 5px white;
    margin-bottom: 3%;
    padding: 1%;
    font-family:Georgia, 'Times New Roman', Times, serif;
    font-size: 120%;
    border: solid rgb(255, 188, 3);
    color: rgb(0, 0, 0);
    text-shadow: 
      1px 1px 3px rgb(255, 255, 255), /* Sombra oscura a la derecha y abajo */
      -1px -1px 3px rgb(255, 255, 255), /* Sombra oscura a la izquierda y arriba */
      1px -1px 3px rgb(255, 255, 255), /* Sombra oscura a la derecha y arriba */
      -1px 1px 3px rgb(255, 255, 255), /* Sombra oscura a la izquierda y abajo */
      0 0 2px rgb(238, 255, 255);
  }
  .card:hover {
    transform: translateY(-10px);
    box-shadow: 0 20PX 60px  rgb(255, 188, 3);
    color: black;
    border: white solid;
  }
  
  .card-header {
    font-size: 1.3rem;
    font-weight: 600;
    margin-bottom: 1rem;
    border-bottom: solid rgb(255, 188, 3);
    margin-bottom: 10%;
    color: #ffc400;
  }
  
  .card-logo-container {
    width: 80px;
    height: 80px;
    margin-bottom: 1.5rem;
    border-radius: 50%;
    overflow: hidden;
  }
  
  .card-logo {
    width: 100%;
    height: 100%;
    object-fit: cover;
    
  }
  
  .card-no-logo {
    display: flex;
    justify-content: center;
    align-items: center;
    margin-bottom: 1.5rem;
    background-color: #000000;
    border-radius: 50%;
    font-size: 1.5rem;
    color: #888;
    height: 28%;
    text-align: center;
    
  }
  
  .no-logo-text {
    font-style: italic;
    color: #888;
  }
  
  .card-title {
    font-size: 1.2rem;
    font-weight: 600;
    margin-bottom: 1rem;    
    text-shadow: 
      2px 2px 3px rgb(255, 255, 255), /* Sombra oscura a la derecha y abajo */
      -2px -2px 3px rgb(255, 255, 255), /* Sombra oscura a la izquierda y arriba */
      2px -2px 3px rgb(255, 255, 255), /* Sombra oscura a la derecha y arriba */
      -2px 2px 3px rgb(255, 255, 255), /* Sombra oscura a la izquierda y abajo */
      0 0 2px rgb(238, 255, 255);

    border: solid white;
    width: 100%;

  }
  
  .card-button {
    background-color: #ffc400;
    color: rgb(0, 0, 0);
    border: none;
    padding: 0.8rem 1.2rem;
    border-radius: 5px;
    cursor: pointer;
    font-size: 110%;
    transition: background-color 0.3s ease;
    font-family:Arial, Helvetica, sans-serif;
    box-shadow: 0 0 5px rgb(231, 231, 233);
    border: 1px solid rgb(124, 123, 123);
  }
  
  .card-button:hover {
    background-color: #ff9900;
    box-shadow: 0 0 40px rgb(255, 230, 0);
    border:1px solid white;
  }
  
  .card-button:focus {
    outline: none;
  }
  
  .mark {
    background-color: rgb(89, 76, 100);
    color: black;
    padding: 0 3px;
  }
  
  /* Transiciones de Fade */
  .fade-enter-active, .fade-leave-active {
    transition: opacity 0.5s ease;
  }
  
  .fade-enter, .fade-leave-to {
    opacity: 0;
  }
  </style>
  