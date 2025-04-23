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

    <div class="contenedor">
      <router-link to="/torneos" class="btn-volver">
    Volver
  </router-link>
  
      <!-- Título -->
      <h1 class="titulo">Torneos Finalizados</h1>
  
      <!-- Buscador y filtros -->
      <div class="filtros">
        <input
          v-model="search"
          type="text"
          placeholder="Buscar torneo o creador"
        />
  
        <div class="fecha">
          <select v-model="selectedDay">
            <option value="">Día</option>
            <option v-for="d in 31" :key="d" :value="d">{{ d }}</option>
          </select>
  
          <select v-model="selectedMonth">
            <option value="">Mes</option>
            <option v-for="(m, index) in months" :key="index" :value="index + 1">{{ m }}</option>
          </select>
  
          <select v-model="selectedYear">
            <option value="">Año</option>
            <option v-for="y in years" :key="y" :value="y">{{ y }}</option>
          </select>
        </div>
      </div>
  
      <!-- Cards -->
      <div class="cards">
        <div v-for="t in filteredTournaments" :key="t.id" class="card">
          <div class="card-header">
            <img :src="t.logoTorneo" alt="logo torneo" class="logo" />
            <h3>{{ t.nombreTorneo }}</h3>
          </div>
  
          <p class="fecha-texto">Fecha: {{ t.fecha }}</p>
  
          <div class="creador">
            <img :src="t.logoCreador" alt="logo creador" class="logo" />
            <span>{{ t.creador }}</span>
          </div>
  
          <p>Participantes: {{ t.participantes }}</p>
          <p>Lugar: {{ t.lugar }}</p>
  
          <button @click="verResultado(t.id)">Ver resultado</button>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import Headerapp from './Headerapp.vue';
  import headermobile from './headermobile.vue';
  export default {
    components: {
      Headerapp,
      headermobile
    },
    data() {
      return {
        search: '',
        selectedDay: '',
        selectedMonth: '',
        selectedYear: '',
        months: ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'],
        years: [2023, 2024, 2025],
        torneos: [
          {
            id: 1,
            nombreTorneo: 'Copa Elite',
            logoTorneo: 'https://via.placeholder.com/50',
            fecha: '2024-04-01',
            creador: 'Carlos',
            logoCreador: 'https://via.placeholder.com/40',
            participantes: 16,
            lugar: 'Bogotá'
          },
          {
            id: 2,
            nombreTorneo: 'Liga Dorada',
            logoTorneo: 'https://via.placeholder.com/50',
            fecha: '2024-03-15',
            creador: 'Andrea',
            logoCreador: 'https://via.placeholder.com/40',
            participantes: 8,
            lugar: 'Medellín'
          }
        ]
      }
    },
    computed: {
      filteredTournaments() {
        return this.torneos.filter((t) => {
          const searchMatch =
            t.nombreTorneo.toLowerCase().includes(this.search.toLowerCase()) ||
            t.creador.toLowerCase().includes(this.search.toLowerCase());
  
          const [anio, mes, dia] = t.fecha.split("-").map(Number);
  
          const diaMatch = this.selectedDay ? dia === Number(this.selectedDay) : true;
          const mesMatch = this.selectedMonth ? mes === Number(this.selectedMonth) : true;
          const anioMatch = this.selectedYear ? anio === Number(this.selectedYear) : true;
  
          return searchMatch && diaMatch && mesMatch && anioMatch;
        });
      }
    },
    methods: {
      verResultado(id) {
        alert(`Mostrando resultados del torneo con ID: ${id}`);
      }
    }
  }
  </script>
  <style scoped>
  /* Fondo general y tipografía */
  .contenedor {
    background-color: #0a0a0a;
    color: #ffffff;
    padding: 2rem;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    margin-top: 30%;
  }
  
  /* Título principal */
  .titulo {
    font-size: 2rem;
    font-weight: bold;
    margin-bottom: 1.5rem;
    color: #d4af37; /* dorado */
    border-bottom: 2px solid #444;
    padding-bottom: 0.5rem;
  }
  
  /* Filtros */
  .filtros {
    display: flex;
    flex-wrap: wrap;
    gap: 1rem;
    margin-bottom: 2rem;
  }
  
  .filtros input,
  .filtros select {
    background-color: #1a1a1a;
    border: 1px solid #444;
    color: white;
    padding: 0.5rem 1rem;
    border-radius: 8px;
    outline: none;
    transition: border 0.3s;
  }
  
  .filtros input::placeholder {
    color: #888;
  }
  
  .filtros input:focus,
  .filtros select:focus {
    border-color: #d4af37;
  }
  
  /* Fecha filtros */
  .fecha {
    display: flex;
    gap: 0.5rem;
  }
  
  /* Cards */
  .cards {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
    gap: 1.5rem;
  }
  
  .card {
    background: linear-gradient(145deg, #1a1a1a, #111111);
    border: 1px solid rgba(212, 175, 55, 0.2); /* dorado con transparencia */
    border-radius: 16px;
    padding: 1.5rem;
    backdrop-filter: blur(2px);
    transition: transform 0.2s, box-shadow 0.3s, border-color 0.3s;
    box-shadow: 0 8px 16px rgba(0, 0, 0, 0.6);
  } 
  .card:hover {
    transform: scale(1.015);
    border-color: #d4af37;
    box-shadow: 0 10px 25px rgba(212, 175, 55, 0.3);
  }
  
  /* Encabezado de la card */
  .card-header {
    display: flex;
    align-items: center;
    gap: 1rem;
    margin-bottom: 1rem;
    border-bottom: white solid 1px;
  }
  .card-header h3 {
    font-size: 1.2rem;
    font-weight: 700;
    color: #d4af37; /* dorado/amarillo */
    -webkit-text-stroke: 1px #000000; /* borde negro */
    text-shadow: 0px 0px 5px #ffffffaa; /* sombra blanca suave */
  }
  
  
  .logo {
    width: 40px;
    height: 40px;
    object-fit: cover;
    border-radius: 50%;
    border: 1px solid #444;
  }
  
  /* Info adicional */
  .fecha-texto {
    color: #aaa;
    margin-bottom: 0.5rem;
  }
  
  
  .creador {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    margin: 0.5rem 0;
    font-style: italic;
    color: #ccc;
  }
  
  
  /* Botón */
  button {
    background-color: #d4af37;
    color: #0a0a0a;
    border: none;
    padding: 0.5rem 1rem;
    border-radius: 8px;
    cursor: pointer;
    font-weight: bold;
    transition: background-color 0.3s;
  }
  
  button:hover {
    background-color: #b8962d;
  }
  .card button {
    background-color: transparent;
    color: #d4af37;
    border: 1px solid #d4af37;
    padding: 0.5rem 1rem;
    border-radius: 8px;
    cursor: pointer;
    transition: background-color 0.3s;
    margin-top: 1rem;
  }
  
  .card button:hover {
    background-color: #d4af37;
    color: #0a0a0a;
  } 
  .btn-volver {
    display: inline-block;
    margin-bottom: 1rem;
    padding: 0.4rem 1rem;
    background-color: transparent;
    border: 1px solid #d4af37;
    color: #d4af37;
    text-decoration: none;
    border-radius: 8px;
    font-weight: bold;
    transition: background-color 0.3s, color 0.3s;
  }
  
  .btn-volver:hover {
    background-color: #d4af37;
    color: #0a0a0a;
  }
  
  </style>
  