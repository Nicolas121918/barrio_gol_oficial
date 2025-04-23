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
    <link href="https://fonts.googleapis.com/css2?family=Press+Start+2P&display=swap" rel="stylesheet">
    <div class="torneo-container">
      <!-- Parte 1: Equipos -->
       
      <!-- Parte 4: VS (Equipos enfrentados) -->
      <div v-if="!finalizarTorneo" class="vs-section">
        <h2 class="titulo">COMPETIDORES </h2>
        <h4>selecciona dos competidores</h4>
        <div class="enfrentamiento">
          
          <div v-for="(equipo, index) in enfrentamientos" :key="index" class="equipo-vs">
            <img :src="equipo.logo" alt="logo" class="equipo-logo" />
            <p class="equipo-nombre">{{ equipo.nombre }}</p>
            
            
            <button @click="eliminarDeEnfrentamiento(equipo)" class="btn eliminar-vs-btn">-</button>
          </div>
          
        </div>
      </div>
      <div class="divisor">
        <input type="datetime-local" v-model="fecha" class="fecha-input" />
        <button @click="agendarPartido" class="btn agendar-btn">Agendar</button>
      </div>
    </div>

    <h2 class="titulo">Equipos</h2>
    <div v-if="!finalizarTorneo" class="equipos-section">
      <div class="equipos-container">
        <div v-for="(equipo, index) in equipos" :key="index" class="equipo-item">
          <img :src="getImagenUrl(equipo.logoTeam)" alt="logo" class="equipo-logo" />
          <p class="equipo-nombre">{{ equipo.nombre }}</p>
          <div class="acciones">
            <button @click="agregarAEnfrentamiento(equipo)" class="btn agregar-btn">+</button>
            <button @click="eliminarEquipo(index)" class="btn eliminar-btn">Eliminar</button>
          </div>
        </div>
      </div>
    </div>

    <!-- Parte 5: Partidos Programados (con logos) -->
    <h2 class="titulo">Partidos Programados</h2>
    <div v-if="partidosProgramados.length && !finalizarTorneo" class="partidos-section">
      <div v-for="(partido, index) in partidosProgramados" :key="index" class="partido-item">
        <div class="equipo-vs">
          <img :src="partido.equipo1.logo" alt="logo" class="equipo-logo" />
          <p class="partido-nombres">{{ partido.equipo1.nombre }} vs {{ partido.equipo2.nombre }}</p>
          <img :src="partido.equipo2.logo" alt="logo" class="equipo-logo" />
        </div>
        <p class="partido-fecha">Fecha: {{ partido.fecha }}</p>
        <div class="acciones">
          <button @click="cancelarPartido(index)" class="btn-cancelar-btn">Cancelar Encuentro</button>
          <router-link to="/jugadorestorneo"><button class="btn-iniciar-btn">Iniciar</button></router-link>
        </div>
      </div>
    </div>

    <!-- Parte 6: Equipos Eliminados -->
    <h2 class="titulo">Equipos Eliminados</h2>
    <div v-if="eliminados.length && !finalizarTorneo" class="eliminados-section">
      <div v-for="(equipo, index) in eliminados" :key="index" class="equipo-eliminado">
        <p class="equipo-nombre">{{ equipo.nombre }}</p>
        <img :src="equipo.logo" alt="logo" class="equipo-logo" />
        <button @click="repetirEquipo(index)" class="btn repichaje-btn">Repichaje</button>
      </div>
    </div>

    <br>

    <!-- Parte 7: Finalizar Torneo -->
    <div class="CAJA">
      <div v-if="!finalizarTorneo" class="terminar-torneo">
        <router-link to="/gana"><button @click="finalizarTorneoAccion" class="finalizar-torneo-btn">Finalizar Torneo</button></router-link>
      </div>
    </div>

</template>

<script>
import axios from 'axios';
import Headerapp from './Headerapp.vue';
import headermobile from './headermobile.vue';
import { useRoute } from 'vue-router';
const route = useRoute();
export default {
  components: {
    Headerapp,
    headermobile
  },
  data() {
    return {
      equipos: [],
      enfrentamientos: [],
      partidosProgramados: [],
      eliminados: [],
      fecha: '',
      equipoGanador: null,
      finalizarTorneo: false,
      
    };
  },
  mounted() {
    this.getequipos();
  },
  methods: {
    getImagenUrl : (path) => {
  return path ? `http://127.0.0.1:8000/${path}` : '';
},
    
    async getequipos() {
      const idEquipo = route.params.id_Equipo; // Obtener el ID del torneo de la ruta
      try {
        const response = await axios.get(`http://localhost:8000/equiposensorteo/${idEquipo}`);
        this.equipos = response.data.equipos;
      } catch (error) {
        console.error("Error al obtener los equipos:", error);
      }
    },
    data() {
      return {
        equipos: [],
        enfrentamientos: [],
        partidosProgramados: [],
        eliminados: [],
        fecha: '',
        equipoGanador: null,
        finalizarTorneo: false,
      };
    },

    async mounted() {
    // Suponiendo que el id del torneo viene por params
    const idTorneo = this.$route.params.id_torneo;
    await this.cargarEquiposAceptados(idTorneo);
  },

    methods: {
      async cargarEquiposAceptados(idTorneo) {
    try {
      const response = await fetch(`http://localhost:8000/solicitudes_aceptadas/${idTorneo}`);
      const data = await response.json();
      if (Array.isArray(data)) {
        this.equipos = data.map(eq => ({
          id: eq.id_equipo,
          nombre: eq.nombre_equipo,
          // Convierte la ruta relativa en URL absoluta
          logo: eq.logo_equipo ? `http://localhost:8000/${eq.logo_equipo}` : null
        }));
      } else {
        this.equipos = [];
      }
    } catch (error) {
      console.error("Error al cargar equipos aceptados:", error);
      this.equipos = [];
    }
  },

      agregarAEnfrentamiento(equipo) {
        if (this.enfrentamientos.length < 2 && !this.enfrentamientos.includes(equipo)) {
          this.enfrentamientos.push(equipo);
        }
      },
      eliminarEquipo(index) {
        const equipoEliminado = this.equipos.splice(index, 1)[0];
        this.eliminados.push(equipoEliminado);
      },
      eliminarDeEnfrentamiento(equipo) {
        const index = this.enfrentamientos.indexOf(equipo);
        if (index > -1) {
          this.enfrentamientos.splice(index, 1); // Eliminar del "VS"
          // Solo agregar a "equipos" si no está ya presente
          if (!this.equipos.includes(equipo)) {
            this.equipos.push(equipo);
          }
        }
      },
      agendarPartido() {
        if (this.enfrentamientos.length === 2 && this.fecha) {
          this.partidosProgramados.push({
            equipo1: this.enfrentamientos[0],
            equipo2: this.enfrentamientos[1],
            fecha: this.fecha
          });
          this.enfrentamientos = [];
          this.fecha = '';
        }
      },
      cancelarPartido(index) {
        this.partidosProgramados.splice(index, 1);
      },
      repetirEquipo(index) {
        const equipo = this.eliminados.splice(index, 1)[0];
        this.equipos.push(equipo);
      },
      finalizarTorneo() {
        this.finalizarTorneo = true;
        if (this.equipos.length === 1) {
          this.equipoGanador = this.equipos[0].nombre;
        }
      },
      confirmarGanador() {
        if (this.equipoGanador) {
          alert('El ganador es: ${this.equipoGanador');
          this.equipos = [];
          this.partidosProgramados = [];
          this.eliminados = [];
        }
      }
    },
    agendarPartido() {
      if (this.enfrentamientos.length === 2 && this.fecha) {
        this.partidosProgramados.push({
          equipo1: this.enfrentamientos[0],
          equipo2: this.enfrentamientos[1],
          fecha: this.fecha
        });
        this.enfrentamientos = [];
        this.fecha = '';
      }
    },
    cancelarPartido(index) {
      this.partidosProgramados.splice(index, 1);
    },
    repetirEquipo(index) {
      const equipo = this.eliminados.splice(index, 1)[0];
      this.equipos.push(equipo);
    },
    finalizarTorneoAccion() {
      this.finalizarTorneo = true;
      if (this.equipos.length === 1) {
        this.equipoGanador = this.equipos[0].nombre;
      }
    },
    confirmarGanador() {
      if (this.equipoGanador) {
        alert(`El ganador es: ${this.equipoGanador}`);
        this.equipos = [];
        this.partidosProgramados = [];
        this.eliminados = [];
      }
    }
  }
};
</script>

  <style scoped>
  /* Estilos generales para el torneo */
  .torneo-container {
    font-family: Arial, sans-serif;
    background-color: #000000;
    padding: 50px;
    border-radius: 8px;
    color: black;
    box-shadow: 0 0 10px white;
    margin-top: 25%;
  }
  
  /* Botón de Finalizar Torneo */
  .finalizar-torneo-btn {
    background: linear-gradient(45deg, #ff0000, #ff8800); /* Degradado llamativo */
    color: white;
    padding: 12px 24px;
    border: 2px solid #ff4500;
    border-radius: 10px;
    cursor: pointer;
    font-size: 18px;
    font-weight: bold;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    box-shadow: 0 4px 15px rgba(255, 0, 0, 0.6); /* Sombra con un toque de neón */
    transition: all 0.3s ease;
    position: relative;
    overflow: hidden;
  }
  
  .finalizar-torneo-btn:hover {
    background: linear-gradient(45deg, #ff4500, #ff0000);
    transform: scale(1.1);
    box-shadow: 0 6px 20px rgba(255, 0, 0, 0.8);
  }
  
  .finalizar-torneo-btn:active {
    transform: scale(0.95);
    box-shadow: 0 2px 8px rgba(255, 0, 0, 0.5);
  }
  
  /* Estilos para la parte de equipos */
  .equipos-section {
    display: flex;
    flex-wrap: nowrap; /* Evita que los equipos se ajusten a la siguiente fila */
    justify-content: flex-start; /* Alinea los equipos a la izquierda */
    gap: 20px; /* Espacio entre los elementos */
    border: solid rgb(255, 255, 255) 1px; /* Para ver el borde */
    overflow-x: auto; /* Permite desplazarse horizontalmente si los equipos no caben */
    padding: 5%;
    background-color: rgba(48, 47, 47, 0.295);
    color: white;
  }
  
  .equipo-item {
    display: flex;
    flex-direction: column;
    align-items: center;
    min-width: 25vw;
    background-color: rgb(0, 0, 0);
    margin: 2rem;
    padding: 2rem;
    box-shadow: white 0 0 8px;
    border: solid white 1px;
  
  }
  .equipo-item:hover{
    transform: scale(1.1);
    box-shadow: 0 0px 20px rgba(255, 196, 0, 0.7);
    color: #f7b500;
    
  }
  
  .equipo-logo {
    width: 50px;
    height: 50px;
    border: solid black 1px;
    border-radius: 50%;
    box-shadow: white 0 0 8px;
  }
  
  .equipo-nombre {
    margin-top: 10px;
    font-family: 'Lucida Sans', 'Lucida Sans Regular', 'Lucida Grande', 'Lucida Sans Unicode', Geneva, Verdana, sans-serif;
  }
  
  /* Botones para agregar y eliminar equipos */
  .btn {
    padding: 8px 15px;
    border-radius: 5px;
    border: none;
    cursor: pointer;
    transition: background-color 0.3s ease;
  }
  .btn:hover{
    transform: scale(1.1);
    text-shadow: 0 0 10px rgba(0, 255, 255, 1), 0 0 15px rgba(0, 255, 255, 1), 0 0 20px rgba(0, 255, 255, 1); /* Aumenta la sombra para el hover */
    box-shadow: 0 8px 12px rgba(0, 0, 0, 0.7);
  }
  .agregar-btn {
    background-color: #12b612;
    border: sol;
    color: rgb(0, 0, 0);
    text-shadow: 0 0 60px white;
    font-size: 100%;
    border: solid white 0.2px;
  }
  
  .agregar-btn:hover {
    background-color: #45fa0d;
    border: solid white 3px;
  }
  
  .eliminar-btn {
    background-color: #f44336;
    color: white;
    margin-top: 10px;
    border: solid white 0.2px;
  }
  
  .eliminar-btn:hover {
    background-color: #d32f2f;
    border: solid white 3px;
  }
  
  /* Estilos para la sección de VS */
  .vs-section {
    display: flex;
    flex-direction: column;
    justify-content: center; /* Centra los elementos verticalmente */
    align-items: center; /* Centra los elementos horizontalmente */
    margin-top: 10px;
    text-align: center;
    padding: 5%;
    background-image: url("https://www.unicef.org/venezuela/sites/unicef.org.venezuela/files/styles/hero_desktop/public/JV_UNICEF_MISERICORDIA%20FC_SUCRE-6.webp?itok=KHTjiGPG");
    background-size: cover; /* Hace que la imagen cubra todo el área */
    background-position: center; /* Centra la imagen en el contenedor */
    background-repeat: no-repeat; /* Evita que la imagen se repita */
    border: solid 2px rgb(255, 255, 255); /* Ajuste de borde */
    border-radius: 10px; /* Bordes redondeados */
    color: rgb(0, 0, 0); /* Asegura que el texto sea blanco para destacar sobre el fondo */
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.3); /* Sombra suave para darle profundidad */
    max-width: 100%; /* Limita el ancho máximo del contenedor */
  /* Centra el contenedor horizontalmente */
  }
  
  .vs-section h1 {
    margin-bottom: 10px; /* Espacio debajo del título */
    font-size: 2rem; /* Tamaño adecuado para títulos */
  }
  
  .vs-section p {
    font-size: 1rem; /* Tamaño de fuente más pequeño para el texto */
    line-height: 1.5; /* Mejora la legibilidad del texto */
    max-width: 600px; /* Limita el ancho del texto para evitar que se estire demasiado */
  }
  h4{
    background-color: #0000008e;
    color: white;
    padding: 1%;
    margin-bottom: 7%;
  }
  
  
  .enfrentamiento {
    display: flex;
    gap: 20px;
    flex-wrap: wrap;
  }
  
  .equipo-vs {
    background-color: #fff;
    border: solid rgb(0, 0, 0);
    padding: 15px;
    border-radius: 8px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    text-align: center;
    width: 150px;
    color: #d9dd04;
    box-shadow: 0 0 7px yellow;
    transition: all 0.3s ease; /* Agrega una transición suave */
    text-shadow: 1px 1px 2px black, -1px -1px 2px black, 1px -1px 2px black, -1px 1px 2px black; /* Contorno negro alrededor del texto */
  }
  
  .equipo-vs:hover {
    transform: scale(1.1); /* Hace que el contenedor crezca un poco */
    box-shadow: 0 0 15px 3px rgba(255, 255, 0, 0.8); /* Aumenta la sombra y cambia su color al pasar el mouse */
    background-color: #f4f4f4; /* Cambia el color de fondo cuando se pasa el mouse */
    cursor: pointer; /* Cambia el cursor para indicar que es interactivo */
    color: #fabb0d;
    text-shadow: 1px 1px 2px black, -1px -1px 2px black, 1px -1px 2px black, -1px 1px 2px black; /* Contorno negro alrededor del texto */
  }
  
  
  
  .eliminar-vs-btn {
    background-color: #f44336;
    color: white;
    padding: 5px 10px;
    border-radius: 10px;
    border: none;
    cursor: pointer;
    font-family:Impact, Haettenschweiler, 'Arial Narrow Bold', sans-serif;
    font-size: 16px;
    border: solid rgb(0, 0, 0) 1px;
  }
  
  .eliminar-vs-btn:hover {
    background-color: #d32f2f;
  }
  
  /* Estilos para la sección de partidos programados */
  .partidos-section {
    margin-top: 30px;
    background-color: rgb(37, 37, 37);
    padding: 20px;
    border: solid rgb(255, 255, 255);
    box-shadow: 0 0 10px rgb(247, 210, 1);
  }
  
  .partido-item {
    display: flex;
    flex-direction: column;
    align-items: center;
    background-color: #ffffff;
    padding: 15px;
    border-radius: 8px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    margin-bottom: 20px;
    width: 200px;
    border: solid rgb(31, 31, 31);
    box-shadow: white 0 0 5px;
  }
  
  .partido-nombres {
    font-size: 16px;
    font-weight: bold;
    color: rgb(190, 190, 190);
  }
  
  .fecha-input {
    margin-top: 10px;
    padding: 5px;
    border-radius: 5px;
    border: 1px solid #000000;
    width: 110%;
    color: rgb(255, 255, 255);
    background-color: #000000;
    border: solid white 3px;
  }
  .caja{
    display: flex;
    width: 100%;
    justify-content: center;
  }
  .agendar-btn {
    border-radius: 5px;
    cursor: pointer;
    margin-top: 10px;
    width: 30%;
    height: 20%;
  background-image: url("https://thumbs.dreamstime.com/b/textura-de-color-dorado-brillante-para-la-ilustraci%C3%B3n-fondo-158084362.jpg");
  border: solid white 1px;
  color: white;
  text-shadow: 1px 1px 2px black, -1px -1px 2px black, 1px -1px 2px black, -1px 1px 2px black; 
  font-size: 110%;
  margin-left: 10%;
  }
  .titulo {
    font-family: 'Press Start 2P', cursive; /* Fuente tipo retro pixelada */
    color: #fff; /* Blanco */
    text-align: center;
    font-size: 20px; /* Tamaño grande para resaltar */
    letter-spacing: 2px; /* Espaciado entre letras */
    text-shadow: 0 0 5px rgba(255, 187, 0, 0.8), 0 0 10px rgba(251, 255, 0, 0.8), 0 0 15px rgba(252, 255, 57, 0.8); /* Efecto de sombra pixelada */
    padding: 20px;
    border-radius: 10px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.5); /* Sombra suave alrededor */
    text-align: center;
  }
  .terminar-torneo{
    display: flex;
    justify-content: center;
  }
  
  
  /* Estilos para la sección de eliminados */
  .eliminados-section {
    display: flex;
    flex-wrap: wrap;
    margin-top: 30px;
    background-color: rgb(0, 0, 0);
    border: solid rgb(255, 6, 6);
    box-shadow: 0 0 20px rgb(247, 114, 114);
  }
  
  .equipo-eliminado {
    background-color: #000000; /* Color de fondo oscuro */
    padding: 20px;
    border-radius: 12px; /* Bordes más redondeados */
    box-shadow: 0 4px 10px rgba(255, 0, 0, 0.7); /* Sombra roja más suave */
    border: 2px solid red; /* Borde rojo */
    text-align: center;
    width: 180px; /* Un poco más grande */
    margin-bottom: 25px;
    color: rgb(255, 13, 13); /* Color del texto blanco para un buen contraste */
    font-weight: bold; /* Hace el texto un poco más fuerte */
    transition: all 0.3s ease; /* Añade transición suave para los efectos */
    margin: 2%;
  }
  
  .equipo-eliminado:hover {
    box-shadow: 0 0 15px rgba(255, 0, 0, 1); /* Sombra más intensa */
    transform: scale(1.05); /* Hace que el contenedor crezca un poco */
    color: #ff3300; /* Cambia el color del texto a un rojo brillante */
    cursor: pointer; /* Cambia el cursor a mano para indicar interacción */
  }
  
  
  .repichaje-btn {
    background-color: #f32121;
    color: white;
    padding: 8px 15px;
    border-radius: 5px;
    border: none;
    cursor: pointer;
    transition: background-color 0.3s ease;
  }
  
  .repichaje-btn:hover {
    background-color: #ffffff;
    color: #000;
  }
  
  /* Estilos para el ganador */
  
  .divisor{
    display: flex;
  
  }
  .btn-cancelar-btn {
    background-color: #5f5f5f; /* Rojo fuerte para indicar cancelación */
    color: white; /* Texto blanco para buen contraste */
    font-size: 16px; /* Tamaño de letra adecuado */
    padding: 5px 5px; /* Espaciado interno para hacerlo más grande */
    border: none; /* Sin borde */
    border-radius: 5px; /* Bordes redondeados */
    cursor: pointer; /* Cursor de mano para indicar interactividad */
    transition: all 0.3s ease; /* Transición suave */
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); /* Sombra sutil */
    margin-bottom: 10%;
  }
  
  .btn-cancelar-btn:hover {
    background-color: #000000; /* Rojo más oscuro al pasar el ratón */
    transform: scale(1.05); /* Aumenta ligeramente el tamaño al hacer hover */
    box-shadow: 0 6px 8px rgba(1, 83, 116, 0.2); /* Sombra más fuerte en hover */
  }
  
  .btn-cancelar-btn:active {
    background-color: #1c93b7; /* Rojo aún más oscuro cuando se hace clic */
    transform: scale(0.98); /* Efecto de "presionar" el botón */
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); /* Vuelve la sombra al estado original */
  }
  
  
  .btn-iniciar-btn {
    background-color: #00ffff; /* Verde fuerte para indicar acción positiva */
    color: rgb(0, 0, 0); /* Texto blanco para contraste */
    font-size: 16px; /* Tamaño de letra adecuado */
    padding: 10px 20px; /* Espaciado interno */
    border: none; /* Sin borde */
    border-radius: 5px; /* Bordes redondeados */
    cursor: pointer; /* Cursor de mano para indicar interactividad */
    transition: all 0.3s ease; /* Transición suave */
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.76); /* Sombra ligera */
  }
  
  .btn-iniciar-btn:hover {
    background-color: #2943b6; /* Verde más oscuro al pasar el ratón */
    transform: scale(1.05); /* Efecto de crecimiento al hacer hover */
    box-shadow: 0 6px 8px rgba(0, 0, 0, 0.2); /* Aumenta la sombra */
    color: white;
    border: solid black 2px;
  }
  
  .btn-iniciar-btn:active {
    background-color: #2E7D32; /* Verde más oscuro cuando se presiona */
    transform: scale(0.98); /* Efecto de "presionar" el botón */
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); /* Reduce la sombra */
  }
  
  </style>