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

    <div class="torneo-container">
      <router-link to="/torneo_creados" class="btn-volver">
  Volver
</router-link>
<br>
<br>  
    <!-- Nombre y Logo -->
    <div class="torneo-header">
      <img :src="getImagenUrl(torneo.torneo_logo
      )" alt="Logo Torneo" class="torneo-logo" />
      <h1>{{ torneo.nombre }}</h1>
    </div>
    <!-- Creador -->
    <div class="creador-box">
      <div class="creador-info">
        <img :src="getImagenUrl(movistore.usuario.fileInput)" alt="Logo Creador" class="creador-logo" />
        <p>{{ torneo.creador.nombre }}</p>
      </div>
      <button class="boton" @click="verCreador">Ver perfil</button>
    </div>
    <!-- Equipos Aceptados -->
    <div>
      <h2 class="titulo-seccion">Equipos Aceptados ({{ equiposAceptados.length }}/{{ torneo.numero_participantes }})</h2>
      <div class="equipos-grid">
        <div
          v-for="equipo in equiposAceptados"
          :key="equipo.id"
          class="equipo-box"
          @click="verEquipo(equipo.id_equipo)"
        >
        <img :src="getLogoEquipoUrl(equipo.logo_equipo)" class="equipo-logo" />
          <p>{{ equipo.nombre_equipo}}</p>
        </div>
      </div>
    </div>
    <div class="boton-continuar">
    <button class="boton-iniciar" @click="iniciarTorneo">Continuar</button>
  </div>
  <div v-if="cuposLlenos" class="mensaje-cupos-llenos">
    ¡Cupos del torneo llenos! 
  </div>
    <!-- Buzón de solicitudes -->
    <div>
      <h2 class="titulo-seccion">Solicitudes</h2>
      <div
        v-for="solicitud in solicitudes"
        :key="solicitud.id"
        class="solicitud-box"
      >
        <div class="solicitud-info">
          <img :src="getLogoEquipoUrl(solicitud.logo_equipo)" class="equipo-logo" />
<p>{{ solicitud.nombre_equipo }}</p>

        </div>
        <div>
          <button class="boton" @click="verEquipo(solicitud.id_equipo)">Ver</button>
      
  <button class="boton aceptar" @click="gestionarSolicitud(solicitud.id_solicitud, 'aceptado')">Aceptar</button>
<button class="boton rechazar" @click="gestionarSolicitud(solicitud.id_solicitud, 'rechazado')">Rechazar</button>
        </div>
      </div>
      
      <div>
        <h2
        class="titulo-seccion"
        :style="{ color: mostrarRechazadas ? 'red' : '' }"
        @click="mostrarRechazadas = !mostrarRechazadas"
        style="cursor: pointer"
      >
      ⬇ Solicitudes Rechazadas ({{ solicitudes_rechazadas.length }})
      </h2>
      <div v-if="mostrarRechazadas">
        <div
          v-for="solicitud in solicitudes_rechazadas"
          :key="solicitud.id"
          class="solicitud-box"
        >
          <div class="solicitud-info">
            <img :src="getLogoEquipoUrl(solicitud.logo_equipo)" class="equipo-logo" />
            <p>{{ solicitud.nombre_equipo }}</p>
            <button class="boton" @click="verEquipo(solicitud.id_equipo)">Ver</button>
          </div>
        </div>
      </div>
        </div>
        
     
    </div>
    <!-- Especificaciones -->
    <div class="especificaciones">
    <h2 class="titulo-seccion">Información del Torneo</h2>
    <div class="info-linea"><strong>Tipo torneo:</strong> {{ torneo.tipo_torneo }}</div>
    <div class="info-linea"><strong>Tipo fútbol:</strong> {{ torneo.tp_futbol }}</div>
    <div class="info-linea"><strong>Fecha inicio:</strong> {{ torneo.fecha_inicio }}</div>
    <div class="info-linea"><strong>Categorías:</strong> {{ torneo.categorias }}</div>
    <div class="info-linea"><strong>Número participantes:</strong> {{ torneo.numero_participantes }}</div>
    <h2 class="titulo-seccion">Ubicación</h2>
    <div class="info-linea"><strong>Ubicación:</strong> {{ torneo.ubicacion }}</div>
    <a :href="mapsUrl" target="_blank" class="boton maps-btn">📍 Ver en Google Maps</a>
    <div class="info-linea"><strong>Cómo llegar:</strong> {{ torneo.como_llegar }}</div>
    <img :src="getImagenUrl(torneo.imagen_cancha)" alt="Cancha" class="cancha-img" />
    <h2 class="titulo-seccion">Reglas y Premios</h2>
    <div class="info-linea"><strong>Premiación:</strong> {{ torneo.premiacion }}</div>
    <div class="info-linea"><strong>Reglas:</strong> {{ torneo.reglas }}</div>
    <div class="info-linea"><strong>Costo inscripción:</strong> {{ torneo.costo_inscripcion }}</div>
  </div>
  </div>
  </template>
  <script>
  import axios from 'axios';
  import Headerapp from './Headerapp.vue';
  import headermobile from './headermobile.vue';
  import { useUsuarios } from '@/stores/usuario';
  
  export default {
    components: {
      Headerapp,
      headermobile,
      
    
    },  
    data() {
      return {
        mostrarRechazadas: false,
        movistore: useUsuarios(),
        torneo: {
          creador: {}
        },
        equiposAceptados: [],
        solicitudes: [],
        solicitudes_rechazadas: [],
      };
    },
    mounted() {
      const idTorneo = this.$route.params.id_torneo;
  this.obtenerTorneo(idTorneo);
  this.cargarSolicitudes(idTorneo);
  this.aceptadas(idTorneo);
  this.rechazadas(idTorneo);
    },
    methods: {
      async obtenerTorneo(id) {
        try {
          const response = await axios.get(`http://localhost:8000/listar_torneo/${id}`);
          this.torneo = response.data;
        } catch (error) {
          console.error("Error al obtener el torneo:", error);
        }
      },
      async gestionarSolicitud(id, estado) {
    try {
      const response = await axios.put(`http://localhost:8000/gestionarSolicitud/${id}?estado=${estado}`);
      alert(response.data.mensaje);
      // Actualiza la lista local eliminando la solicitud procesada
      this.solicitudes = this.solicitudes.filter(s => s.id !== id);
    } catch (error) {
      console.error(error);
      alert("Error al gestionar la solicitud.");
    }
  }, 
      verCreador() {
  this.$router.push({ name: 'perfiles', params: { documento: this.torneo.creador.documento } });
},

getImagenUrl(path) {
      return path ? `http://127.0.0.1:8000/${path}` : '';
    },
      verEquipo(id) {
        this.$router.push({ name: 'inspeccion_equipo', params: { id } });
      },
      iniciarTorneo() {
        if (this.equiposAceptados.length < this.torneo.numero_participantes) {
          if (confirm("¿Estás seguro de iniciar sin los cupos llenos?")) {
            this.enviarInicioTorneo()
          }
        } else {
          this.enviarInicioTorneo()
        }
      },
      async cargarSolicitudes(idTorneo) {
  try {
    const response = await fetch(`http://localhost:8000/solicitudes_pendientestorneo/${idTorneo}`);
    const data = await response.json();
    if (Array.isArray(data)) {
      this.solicitudes = data;
    } else {
      this.solicitudes = [];
      console.log(data.mensaje);
    }
  } catch (error) {
    console.error("Error al cargar solicitudes:", error);
  }
},

async aceptadas(idTorneo) {
  try {
    const response = await fetch(`http://localhost:8000/solicitudes_aceptadas/${idTorneo}`);
    const data = await response.json();
    if (Array.isArray(data)) {
      this.equiposAceptados= data;
    } else {
      this.equiposAceptados = [];
      console.log(data.mensaje);
    }
  } catch (error) {
    console.error("Error al cargar aceptadas:", error);
  }
},
async rechazadas(idTorneo) {
  try {
    const response = await fetch(`http://localhost:8000/solicitudes_rechazadas/${idTorneo}`);
    const data = await response.json();
    if (Array.isArray(data)) {
      this.solicitudes_rechazadas= data;
    } else {
      this.solicitudes_rechazadas = [];
      console.log(data.mensaje);
    }
  } catch (error) {
    console.error("Error al cargar aceptadas:", error);
  }
}, 
getLogoUrl(nombreArchivo) {
    return new URL(`@/assets/${nombreArchivo}`, import.meta.url).href;
  },

  getLogoEquipoUrl(logoEquipo) {
  if (!logoEquipo) return '';
  // Si ya es una URL absoluta, la retorna tal cual
  if (logoEquipo.startsWith('http')) return logoEquipo;
  // Si es relativa, la convierte a absoluta
  return `http://localhost:8000/${logoEquipo}`;
},

  async enviarInicioTorneo() {
  try {
    // Usamos el endpoint de gestionarSolicitud, pero mandamos el id del torneo y estado=iniciar
    const response = await axios.put(`http://localhost:8000/gestionarSolicitud/${this.torneo.id_torneo}?estado=iniciar`);
    alert(response.data.mensaje);
    // Redirige incluyendo el id_torneo como parámetro
    this.$router.push({ name: 'torneoscreador', params: { id_torneo: this.torneo.id_torneo } });
  } catch (error) {
    alert("No se pudo iniciar el torneo");
    console.error(error);
  }
}
    }
  };
  </script>
  
  <style scoped>
  @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600&family=Roboto&display=swap');
  
  * {
    font-family: 'Roboto', sans-serif;
    transition: all 0.3s ease-in-out;
    box-sizing: border-box;
  }
  
  .torneo-container {
    background-color: #121212;
    color: white;
    padding: 2rem;
    border-radius: 1.5rem;
    box-shadow: 0 0 20px rgba(212, 175, 55, 0.2);
    min-width: 50vw;
    max-width: 100vw;
    margin-top: 20%;
  }
  
  h1, h2 {
    font-family: 'Playfair Display', serif;
    color: #d4af37;
    margin-bottom: 1rem;
  }
  
  .torneo-header {
    display: flex;
    align-items: center;
    gap: 1rem;
    margin-bottom: 2rem;
  }
  
  .torneo-logo {
    width: 70px;
    height: 70px;
    border-radius: 50%;
    border: 2px solid #d4af37;
    box-shadow: 0 0 10px rgba(212, 175, 55, 0.4);
  }
  
  .creador-box {
    background-color: #1f1f1f;
    padding: 1rem 1.5rem;
    border-radius: 1rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 2rem;
    box-shadow: 0 2px 10px rgba(255, 255, 255, 0.05);
  }
  
  .creador-info {
    display: flex;
    align-items: center;
    gap: 1rem;
  }
  
  .creador-logo {
    width: 50px;
    height: 50px;
    border-radius: 50%;
    border: 1px solid #d4af37;
  }
  .boton {
    background: linear-gradient(145deg, #111, #1a1a1a); /* Negro con profundidad */
    color: #f5d66b; /* Dorado suave */
    border: 1px solid #f5d66b;
    padding: 0.5rem 1rem;
    border-radius: 12px;
    font-family: 'Poppins', sans-serif;
    font-weight: 600;
    transition: all 0.3s ease;
    cursor: pointer;
    box-shadow: 0 4px 8px rgba(0,0,0,0.3);
    margin: 0.3rem;
  }
  .boton:hover {
    background-color: #f5d66b;
    color: #111;
    transform: scale(1.05);
    box-shadow: 0 6px 12px rgba(0,0,0,0.5);
  }
  
  .maps-btn {
    display: inline-block;
    margin-top: 0.5rem;
    background: transparent;
    border: 1px solid #aaa;
    color: #ccc;
    font-size: 0.95rem;
  }
  
  .maps-btn:hover {
    background: #f5d66b;
    color: #111;
    border-color: #f5d66b;
  }
  .titulo-seccion {
    margin-top: 2rem;
    color: #d4af37;
    font-size: 1.4rem;
    border-left: 4px solid #d4af37;
    padding-left: 0.5rem;
  }
  
  .equipos-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
    gap: 1rem;
    border: solid rgb(255, 255, 255);
    padding: 20px;
    min-height: 200px;
    margin-top: 1rem;
  }
  
  .equipo-box {
    background-color: #1e1e1e;
    border-radius: 1rem;
    padding: 1rem;
    text-align: center;
    cursor: pointer;
    box-shadow: 0 0 8px rgba(255, 255, 255, 0.05);
    transition: transform 0.3s ease, box-shadow 0.3s ease;
  }
  
  .equipo-box:hover {
    transform: translateY(-5px);
    box-shadow: 0 0 12px rgba(212, 175, 55, 0.3);
  }
  
  .equipo-logo {
    width: 50px;
    height: 50px;
    border-radius: 50%;
    margin-bottom: 0.5rem;
    border: 1px solid #d4af37;
  }
  
  .solicitud-box {
    background-color: #2a2a2a;
    padding: 1rem;
    border-radius: 1rem;
    margin-top: 1rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
    box-shadow: 0 0 10px rgba(255, 255, 255, 0.03);
  }
  
  .solicitud-info {
    display: flex;
    align-items: center;
    gap: 1rem;
  }
  .especificaciones {
    background-color: #1e1e1e;
    padding: 2rem;
    border-radius: 1rem;
    margin-top: 2rem;
    box-shadow: 0 0 15px rgba(255, 255, 255, 0.05);
    animation: fadeInUp 0.6s ease;
  }
  
  .titulo-seccion {
    font-family: 'Playfair Display', serif;
    color: #d4af37;
    margin-top: 1.5rem;
    margin-bottom: 1rem;
    font-size: 1.4rem;
  }
  
  .info-linea {
    margin-bottom: 0.75rem;
    color: #ccc;
    font-size: 1rem;
  }
  
  .info-linea strong {
    color: #d4af37;
  }
  
  
  .cancha-img {
    width: 30%;
    max-width: 60vw;
    border-radius: 0.75rem;
    margin-top: 1rem;
    border: 2px solid #333;
    box-shadow: 0 0 10px rgba(255, 255, 255, 0.05);
  }
  
  @keyframes fadeInUp {
    0% {
      opacity: 0;
      transform: translateY(15px);
    }
    100% {
      opacity: 1;
      transform: translateY(0);
    }
  }
  .boton.aceptar {
    background: linear-gradient(145deg, #f5d66b, #eac94f);
    color: #111;
    border: 1px solid #d4af37;
    box-shadow: 0 4px 8px rgba(255, 215, 0, 0.3);
  }
  
  .boton.aceptar:hover {
    background: #fff1b8;
    transform: scale(1.05);
  }
  
  .boton.rechazar {
    background: linear-gradient(145deg, #3a3a3a, #2a2a2a);
    color: #f88f8f;
    border: 1px solid #f88f8f;
    box-shadow: 0 4px 8px rgba(255, 0, 0, 0.2);
  }
  
  .boton.rechazar:hover {
    background: #ff4d4d;
    color: white;
    transform: scale(1.05);
  }
  .boton-continuar {
    margin-top: 20px;
    text-align: center;
  }
  .boton-iniciar {
    background-color: #4CAF50;
    color: white;
    font-weight: bold;
    padding: 10px 20px;
    border: none;
    border-radius: 8px;
    cursor: pointer;
  }
  .boton-iniciar:hover {
    background-color: #45a049;
  }
  
  .mensaje-cupos-llenos {
    color: red;
    font-weight: bold;
    text-align: center;
    margin-top: 10px;
  }
  .btn-volver {
 
  color: rgb(255, 255, 255);
  padding: 10px 16px;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-weight: bold;
  margin: 20px 0;
  display: inline-block;
  text-align: center;
  text-decoration: none;
  border: solid rgb(255, 255, 255);
  transition: background-color 0.3s ease;
}

.btn-volver:hover {
  background-color: #ffd900;
  border: solid white;
}

  </style>
  