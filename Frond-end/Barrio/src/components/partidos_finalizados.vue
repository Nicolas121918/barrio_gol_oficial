<template>
    <div>
      <h1 class="titulo">Todos los Partidos Jugados</h1>
  
      <!-- Buscador de equipo -->
      <input v-model="busqueda" type="text" placeholder="Buscar equipo..." class="buscador" />
  
      <!-- Botón para mostrar el filtro de fecha -->
      <button @click="mostrarFiltroFecha = !mostrarFiltroFecha" class="boton2">
        Filtrar por Fecha
      </button>
  
      <!-- Si mostrarFiltroFecha es true, se muestran los selects para día, mes y año -->
      <div v-if="mostrarFiltroFecha" class="filtro-fecha">
        <select v-model="busquedaDia" class="buscador">
          <option value="">Seleccionar Día</option>
          <option v-for="n in 31" :key="n" :value="n">{{ n < 10 ? '0' + n : n }}</option>
        </select>
  
        <select v-model="busquedaMes" class="buscador">
          <option value="">Seleccionar Mes</option>
          <option v-for="(mes, index) in meses" :key="index" :value="index + 1">{{ mes }}</option>
        </select>
  
        <select v-model="busquedaAño" class="buscador">
          <option value="">Seleccionar Año</option>
          <option v-for="n in 5" :key="n" :value="new Date().getFullYear() - (5 - n)">
            {{ new Date().getFullYear() - (5 - n) }}
          </option>
        </select>
      </div>
  
      <!-- Lista de partidos -->    
      <div class="container">
        <div v-for="partido in partidosFiltrados" :key="partido.id_partido" class="card">
          <!-- Nombre y logo del partido -->
          <div class="partido">
            <img :src="getImagenUrl(partido.logo_partido)" alt="Logo del partido" class="logo-partido" />
            <h3 class="nombre-partido">{{ partido.nombre_partido }}</h3>
          </div>
  
          <div class="equipos">
            <div class="equipo">
              <img :src="getImagenUrl(partido.equipos[0].logo)" alt="Logo" class="logo" />
              <span class="nombre">{{ partido.equipos[0].nombre }}</span>
            </div>
            <span class="vs">VS</span>
            <div class="equipo">
              <img :src="getImagenUrl(partido.equipos[1].logo)" alt="Logo" class="logo" />
              <span class="nombre">{{ partido.equipos[1].nombre }}</span>
            </div>
          </div>
  
          <!-- Fecha formateada -->
          <p class="fecha">{{ formatFecha(partido.fecha) }}</p>
          <button class="boton" @click="verResultado(partido.id_partido)">Ver Resultado</button>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  import { useRouter } from 'vue-router';
  
  export default {
    data() {
      return {
        busqueda: "", // Búsqueda de equipos
        busquedaDia: "", // Búsqueda de día
        busquedaMes: "", // Búsqueda de mes
        busquedaAño: "", // Búsqueda de año
        partidos: [], // Lista de partidos
        mostrarFiltroFecha: false, // Para mostrar u ocultar el filtro de fecha
        meses: ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
      };
    },
    computed: {
      // Filtro de partidos basado en búsqueda de equipos y fecha
      partidosFiltrados() {
        return this.partidos.filter(partido => {
          const partidoFecha = new Date(partido.fecha); // Fecha en formato 'YYYY-MM-DD'
  
          // Filtramos por equipo, día, mes o año
          return (
            // Filtrar por equipo
            (partido.equipos[0].nombre.toLowerCase().includes(this.busqueda.toLowerCase()) ||
              partido.equipos[1].nombre.toLowerCase().includes(this.busqueda.toLowerCase())) &&
  
            // Filtrar por día
            (this.busquedaDia ? partidoFecha.getDate() === parseInt(this.busquedaDia) : true) &&
  
            // Filtrar por mes
            (this.busquedaMes ? partidoFecha.getMonth() + 1 === parseInt(this.busquedaMes) : true) &&
  
            // Filtrar por año
            (this.busquedaAño ? partidoFecha.getFullYear() === parseInt(this.busquedaAño) : true)
          );
        });
      }
    },
    methods: {
      // Método para obtener los partidos finalizados desde el backend
      async obtenerPartidos() {
        try {
          const response = await axios.get('http://localhost:8000/partidos_finalizados');
          this.partidos = response.data;
        } catch (error) {
          console.error('Error al obtener los partidos:', error);
        }
      },
      // Método para navegar al componente de resultado
      verResultado(id) {
        this.$router.push({ name: 'ganador_partido', params: { id: id } });
      },
      // Método para obtener la URL de las imágenes
      getImagenUrl(path) {
        return path ? `http://127.0.0.1:8000/${path}` : '';
      },
      // Formato de fecha 'DD/MM/YYYY'
      formatFecha(fecha) {
        const date = new Date(fecha);
        const dia = String(date.getDate()).padStart(2, '0'); // Obtener día
        const mes = this.meses[date.getMonth()]; // Obtener mes en texto
        const año = date.getFullYear(); // Obtener año
        return `${dia} - ${mes} - ${año}`;
      }
    },
    mounted() {
      this.obtenerPartidos(); // Obtener los partidos al montar el componente
    }
  };
  </script>
  
  
  
<style scoped>
/* Reset de márgenes y padding */
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: 'Arial', sans-serif;
  background-color: #111;
  color: white;
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  padding: 20px;
  flex-direction: column;
  
}

/* Título de la sección */
.titulo {
  text-align: center;
  font-size: 2rem;
  text-shadow: 0 0 10px orange;
  color: rgb(255, 255, 255);
  text-transform: uppercase;
  margin-bottom: 40px;
  letter-spacing: 2px;
  font-weight: 700;
  animation: fadeIn 1s ease-out;
}

/* Buscador */
.buscador {

  width: 20%;
  margin: 20px auto;
  padding: 10px;
  font-size: 1.1rem;
  border: 2px solid #555;
  border-radius: 8px;
  background-color: #222;
  color: white;
  font-family: 'Arial', sans-serif;
  transition: border-color 0.3s ease;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.5);
}

.buscador:focus {
  border-color: gold;
  box-shadow: 0 4px 15px rgba(255, 215, 0, 0.6);
}

.buscador.fecha {
  width: 20%;
  margin-top: 10px;
}

.container {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 20px;
  width: 100%;
  max-width: 1200px;
  
}

.card {
  background-color: #000000;
  color: white;
  padding: 24px;
  border-radius: 16px;
  text-align: center;
  box-shadow: 0 8px 20px rgba(255, 215, 0, 0.3);
  border: 2px solid #555;
  transition: transform 0.3s ease-in-out, box-shadow 0.3s;
  position: relative;
  overflow: hidden;
  justify-content: center;
  align-items: center;
  z-index: 0;
}

.card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease-in-out;
  z-index: -1;
}

.card:hover {
  transform: scale(1.05);
  box-shadow: 0 10px 25px rgba(255, 215, 0, 0.5);
}

.card:hover::before {
  background: rgba(108, 108, 108, 0.3);
}

.equipos {
  display: flex;
  justify-content: space-between;
  align-items: center;
  text-align: center;
  margin-bottom: 16px;
  transition: all 0.3s ease;
}
.partido{
    display: flex;
    margin-bottom: 20px;
    border-bottom: solid;
    align-items: center;

}

.equipo {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
}

.logo {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  border: 3px solid gold;
  transition: transform 0.3s, border-color 0.3s;
}

.logo:hover {
  transform: scale(1.15);
  border-color: white;
}

.nombre {
  font-size: 1.3rem;
  font-weight: bold;
  text-transform: uppercase;
  letter-spacing: 1px;
  color: white;
}

.vs {
  font-size: 2rem;
  color: gold;
  font-weight: bold;
}

.fecha {
  font-size: 1.1rem;
  color: gray;
  margin-bottom: 10px;
}

.boton {
  background: rgba(255, 217, 0, 0.793);
  color: black;
  padding: 14px 24px;
  font-size: 1.2rem;
  font-weight: bold;
  text-transform: uppercase;
  border: none;
  border-radius: 12px;
  cursor: pointer;
  transition: background 0.3s, transform 0.3s, box-shadow 0.3s ease-in-out;
  font-family: 'Arial', sans-serif;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.4);
}
.boton2 {
  background: rgb(110, 110, 110);
  color: rgb(192, 192, 192);
  padding: 10px 10px;
  font-size: 1em;
  font-weight: bold;
  text-transform: uppercase;
  border: none;
  border-radius: 12px;
  cursor: pointer;
  transition: background 0.3s, transform 0.3s, box-shadow 0.3s ease-in-out;
  font-family: 'Arial', sans-serif;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.4);
  margin-left: 10px;
}

.boton2:hover {
  background: #505050d9;
  color: white;
  transform: scale(1.1);
  box-shadow: 0 8px 15px rgba(255, 253, 253, 0.6);
}


.boton:hover {
  background: #ffd700d9;
  transform: scale(1.1);
  box-shadow: 0 8px 15px rgba(255, 215, 0, 0.6);
}

.boton:active {
  background: #d4af37;
  box-shadow: 0 4px 8px rgba(255, 215, 0, 0.6);
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(-20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
.logo-partido{
    width: 60px;
    height:60px;
    border-radius: 50px;
    border: solid white 2px;
    margin-bottom: 15px;
}
.nombre-partido{
    margin-left: 13px;
    font-size: 20px;
    padding: 0;
    font-family: Arial, Helvetica, sans-serif;
    color: #ffffff;
    text-shadow: 0 0 5px white;
}
</style>