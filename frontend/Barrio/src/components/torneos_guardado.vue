<template>
  
    <div class="tournaments-container">
      <!-- Buscador en la parte superior -->
      <div class="search-container">
        <input 
          v-model="searchQuery" 
          type="text" 
          placeholder="Buscar torneo o partido..." 
          class="search-input"
        />
        <select v-model="searchType" class="search-select">
          <option class="opciones" value="">Todos</option>
          <option class="opciones" value="partido">Partido</option>
          <option class="opciones" value="torneo">Torneo</option>
        </select>
        <router-link class="padre" to="equipos">
            <button @click="goBack" class="btn-donate">Volver</button>
      </router-link>
        
      </div>
      <!-- Apartado de Torneos y Partidos Creados -->

  
      <!-- Espacio entre las secciones --
      <!-- Apartado de Torneos y Partidos en los que el Usuario se Unió -->
      <div class="section joined-section">
        <div class="children">
        <h2>Torneos y partidos del equipo</h2>
    </div>
    
        <div class="card-container">
          <!-- Mostrar mensaje si no hay resultados -->
          <p v-if="filteredJoinedItems.length === 0" class="no-results-message">
            No hay partidos o torneos sin coincidencias
          </p>
  
          <!-- Mostrar las tarjetas si hay resultados -->
          <transition-group name="fade" tag="div" class="card-list">
            <div 
              v-for="item in filteredJoinedItems" 
              :key="item.id" 
              class="card"
            >
              <div v-if="item.type === 'torneo'" class="card-header">
                <span>Torneo</span>
              </div>
              <div v-else class="card-header">
                <span>Partido</span>
              </div>
              <div v-if="item.type === 'torneo' && item.logo" class="card-logo-container">
                <img :src="item.logo" alt="Logo" class="card-logo" />
              </div>
              <div v-else class="card-no-logo">
                <span class="no-logo-text">{{ item.type === 'torneo' ? 'Torneo sin logo' : 'Partido' }}</span>
              </div>
              <h3 class="card-title" v-html="highlightText(item.name)"></h3>
              <div class="butons">
              <button @click="viewItem(item)" class="card-button">{{ item.type === 'torneo' ? 'Ver' : 'Ver' }}</button>
            </div>
            </div>
          </transition-group>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        searchQuery: '',
        searchType: '',
        createdItems: [
          { id: 1, name: 'Torneo A', type: 'torneo', logo: 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQgcadZp6orYwW2SrUcyJhyTRredhg_sf_vzQ&s', isCreated: true },
          { id: 2, name: 'Partido A', type: 'partido', logo: null, isCreated: true },
          { id: 3, name: 'Torneo B', type: 'torneo', logo: 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQgcadZp6orYwW2SrUcyJhyTRredhg_sf_vzQ&s', isCreated: true },
          { id: 4, name: 'Partido B', type: 'partido', logo: null, isCreated: true },
        ],
        joinedItems: [
          { id: 5, name: 'Torneo C', type: 'torneo', logo: 'logo-c.png' },
          { id: 6, name: 'Partido C', type: 'partido', logo: null },
          { id: 7, name: 'Torneo D', type: 'torneo', logo:'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQgcadZp6orYwW2SrUcyJhyTRredhg_sf_vzQ&s' },
          { id: 8, name: 'Partido D', type: 'partido', logo: null },
        ],
      };
    },
    computed: {
      filteredCreatedItems() {
        return this.createdItems.filter(item => {
          const nameMatches = item.name.toLowerCase().includes(this.searchQuery.toLowerCase());
          const typeMatches = this.searchType ? item.type === this.searchType : true;
          return nameMatches && typeMatches;
        });
      },
      filteredJoinedItems() {
        return this.joinedItems.filter(item => {
          const nameMatches = item.name.toLowerCase().includes(this.searchQuery.toLowerCase());
          const typeMatches = this.searchType ? item.type === this.searchType : true;
          return nameMatches && typeMatches;
        });
      },
    },
    methods: {
      editItem(item) {
        console.log(`Editando ${item.type === 'torneo' ? 'torneo' : 'partido'}: ${item.name}`);
      },
      viewItem(item) {
        console.log(`Viendo ${item.type === 'torneo' ? 'torneo' : 'partido'}: ${item.name}`);
      },
      goBack() {
        console.log('Volviendo a la pantalla anterior');
      },
      highlightText(text) {
        if (!this.searchQuery) return text;
        const regex = new RegExp(`(${this.searchQuery})`, 'gi');
        return text.replace(regex, '<mark>$1</mark>');
      },
    },
  };
  </script>
  
  <style scoped>
  .tournaments-container {
    display: flex;
    flex-direction: column;
    gap: 2rem;
    padding: 1rem;
  }
  
  .search-container {
    display: flex;
    gap: 1rem;
  }
  
  .back-button {
    background-color: #6c757d;
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
    border-color: #007bff;
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
  --btn-bg-1: hsla(194 100% 69% / 1);
  --btn-bg-2: hsla(217 100% 56% / 1);
  --btn-bg-color: hsla(360 100% 100% / 1);
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
    border: 3px solid #003cff;
    border-radius: 8px;
    padding: 1.5rem;
    text-align: center;
    width: 220px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    transition: transform 0.3s ease, box-shadow 0.3s ease;
    color: rgb(0, 0, 0);
    font-family:Georgia, 'Times New Roman', Times, serif;
    
    
  }
  .children{
    box-shadow: 0 0 5px white;
    margin-bottom: 3%;
    padding: 1%;
    font-family:Georgia, 'Times New Roman', Times, serif;
    font-size: 120%;
    border: solid rgb(10, 7, 180);
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
    box-shadow: 0 20PX 60px rgb(2, 113, 165);
    color: black;
    border: white solid;
  }
  
  .card-header {
    font-size: 1.3rem;
    font-weight: 600;
    margin-bottom: 1rem;
    border-bottom: solid #003cff;
    margin-bottom: 10%;
    color: #007bff;
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
    background-color: #0004ff;
    color: white;
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
    background-color: #292929;
    box-shadow: 0 0 40px blue;
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
  