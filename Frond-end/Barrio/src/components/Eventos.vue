<template>
  <header>
    <headerapp></headerapp>
  </header>
  <h1 class="titulo_torneo">Lista de Torneos y Partidos</h1>
  <div class="main-container">
    <div class="buscador_torneo">
      <div class="search-container">
        <input v-model="searchQuery" type="text" placeholder="Buscar torneos o partidos..." class="search-input" />
        <div class="crear-dropdown relative">
          <button @click="mostrarOpciones = true" class="crear-btn">
            Crear ➕
          </button>
          <div v-if="mostrarOpciones" class="modal-overlay" @click.self="mostrarOpciones = false">
            <div class="modal-menu">
              <router-link to="/creartorneo" class="dropdown-option" @click="mostrarOpciones = false">
                ➕ Crear Torneo
              </router-link>
              <router-link to="/crearpartido" class="dropdown-option" @click="mostrarOpciones = false">
                ⚽ Crear Partido
              </router-link>
            </div>
          </div>
        </div>
        <div class="relative inline-block text-left">
          <button @click="mostrarMenu = !mostrarMenu" class="boton-creados">
            Creados▼
          </button>
          <div v-if="mostrarMenu" class="menu-creados absolute right-0 mt-2 w-48 bg-black text-white border border-gold rounded shadow-lg z-50">
            <div @click="irATorneos" class="opcion-menu">Torneos Creados</div>
            <hr class="border-gold my-1" />
            <div @click="irAPartidos" class="opcion-menu">Partidos Creados</div>
          </div>
        </div>
        <div class="relative inline-block text-left" @mouseleave="mostrarMenu2 = false">
          <button @click="mostrarMenu2 = !mostrarMenu2" class="boton-creados">
            Eventos  finalizados▼
          </button>
          <div v-if="mostrarMenu2" class="menu-creados absolute right-0 mt-2 w-48 bg-black text-white border border-gold rounded shadow-lg z-50">
            <hr class="border-gold my-1" />
            <div @click="irATorneos2" class="opcion-menu">Torneos Finalizados</div>
            <hr class="border-gold my-1" />
            <div @click="irAFinalizados" class="opcion-menu"> Partidos Finalizados</div>
          </div>
        </div>
      </div>
    </div>
    <div>
      <div v-for="(item, index) in filteredTorneos" :key="index" class="card3">
        <div class="card-header-tor">
          <img :src="getImagenUrl(item.logoTeam)" alt="Logo del Torneo" class="logo-img" />
          <div class="card-info-tor">
            <h2 class="titu">Nombre Torneo: {{ item.nombre }}</h2>
            <p>Participantes Torneo: {{ item.numeroparticipantes }}</p>
            <p>Precio de Inscripción Torneo: ${{ item.precioInscripcion }}</p>
            <p>Precio de Arbitraje por partido: ${{ item.precioArbitrajeTorneo }}</p>
          </div>
        </div>
        <div class="uno_solo">
          <div class="rules-container">
            <button @mouseover="showRules('torneo', index)" @mouseleave="hideRules('torneo', index)" class="torn_boton">Ver Reglas</button>
            <div v-if="activeRules.torneo === index" class="rules-info-tor">
              <p class="reglas">Reglas del Torneo: {{ item.reglasTorneo }}</p>
            </div>
          </div>
          <button class="action-button-tor" @click="inscribirTorneo(item)">Inscribir</button>
        </div>
      </div>
    </div>
    <div>
      <div v-for="(item, index) in filteredPartidos" :key="index" class="card3">
        <div class="card-header-tor">
          <img :src="getImagenUrl(item.logomatch)" alt="Logo del partido" class="logo-img" />
          <div class="card-info-tor">
            <h2 class="titu">Partido: {{ item.name }}</h2>
            <span class="letra-tit">Creador:</span> 
            <div class="creador-info">
              <img :src="getImagenUrl(item.creador.nombre)" alt="Logo del Creador" class="logo-pequeno" />
              <p class="letrass">{{ item.creador.logo }}</p>
            </div>
            <p class="letrass"> <span class="letra-tit"> Partido:</span>{{ item.hora }}</p>
            <p class="letrass"> <span class="letra-tit"> Tipo:</span>{{ item.tipo_futbol}}</p>
            <p class="letrass"> <span class="letra-tit"> Apuesta: $</span> {{ item.apuesta }}</p>
            <p class="letrass"> <span class="letra-tit"> Ubicación:</span>  {{ item.ubicacionpartido }}</p>
            <span class="letra-tit">equipo local:</span> 
            <div class="equipo-info">
              <img :src="getImagenUrl(item.equipo_local.logo)" alt="Logo del Equipo" class="logo-pequeno" />
              <p class="letrass">{{ item.equipo_local.nombre }}</p>
            </div>
            
          </div>
          <button class="action-button-tor2" @click="verDetalles(item)">Ver Detalles</button>
          <button class="action-button-tor" @click="unirsePartido(item.id_Partido)">Unirse</button>
          
    
        </div>
       
      </div>
    </div>

    <!-- Modal para detalles del partido -->
    <div v-if="mostrarModal" class="modal-overlay2" @click.self="cerrarModal">
    <div class="modal-content2">
      <h2 class="dettt">Detalles del Partido</h2>
      
      <!-- Logo y nombre del partido -->
      <div class="modal-section">
        <strong class="let">partido:</strong>
        <img :src="getImagenUrl(partidoSeleccionado.logomatch)" alt="Logo del Partido" class="logo-modal" />
        <p class="dettt">{{ partidoSeleccionado.name }}</p>
      </div>
      <!-- Creador -->
      <div class="modal-section">
        <span><strong class="let">creador:</strong></span>
        <img :src="getImagenUrl(partidoSeleccionado.creador.nombre)" alt="Logo del Creador" class="logo-modal" />
        <button class="inspect-button"  @click="irACreador(partidoSeleccionado.creador.documento)"  @mouseover="tooltipCreador = true" @mouseleave="tooltipCreador = false">
          {{ partidoSeleccionado.creador.logo }}
        </button>
        <span v-if="tooltipCreador" class="tooltip">Inspeccionar</span>
      </div>
      <div class="modal-section">
        <strong class="let">equipo local:</strong>
        <img :src="getImagenUrl(partidoSeleccionado.equipo_local.logo)" alt="Logo del Equipo Local" class="logo-modal" />
        <button class="inspect-button"   @click="irAEquipo(partidoSeleccionado.equipo_local.id)" @mouseover="tooltipEquipo = true" @mouseleave="tooltipEquipo = false">
          <strong class="nombre-partido">{{ partidoSeleccionado.equipo_local.nombre }} </strong>
        </button>
        <span v-if="tooltipEquipo" class="tooltip">Inspeccionar</span>
      </div>
      
      <!-- Datos del partido -->
      <div class="modal-section2">
  <strong class="titulo-detalle">Detalles del Partido:</strong>
  <p><strong>Hora:</strong> <span class="detalle-texto">{{ partidoSeleccionado.hora }}</span></p>
  <p><strong>Dia:</strong> <span class="detalle-texto">{{ partidoSeleccionado.dia }}</span></p>
  <p><strong>Apuesta:</strong> <span class="detalle-texto">${{ partidoSeleccionado.apuesta }}</span></p>
  <p><strong>Tipo:</strong> <span class="detalle-texto">{{ partidoSeleccionado.tipo_futbol }}</span></p>
  <p><strong>Reglas:</strong> <span class="detalle-texto">{{ partidoSeleccionado.reglas }}</span></p>
  <div class="modal-section">
    <strong class="let">Cancha:</strong>
<img :src="getImagenUrl(partidoSeleccionado.imagen_cancha)" alt="Imagen de la Cancha" class="imagen-cancha-modal" />
  </div>
  <p><strong>Como llegar:</strong> <span class="detalle-texto">{{ partidoSeleccionado.como_llegar }}</span></p>
  <p><strong>Ubicación:</strong> <span class="detalle-texto">{{ partidoSeleccionado.ubicacionpartido }}</span></p>
  <button class="map-button" @click="verEnMapa(partidoSeleccionado.ubicacionpartido)">
    📍 Ver ubicación en mapa
  </button>
  
</div>
      <!-- Equipo local -->
       <div>
        <button class="action-button-tor3" @click="unirsePartido(partidoSeleccionado.idPartido)">Unirse</button>
       </div>
     
      <button class="close-button2" @click="cerrarModal">Cerrar</button>
    </div>
    
  </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import axios from 'axios';  
import { useUsuarios } from '@/stores/usuario';
import { useRouter } from 'vue-router';
import Headerapp from './Headerapp.vue';

const documento_equipo = ref("");
const router = useRouter();
const mostrarMenu2 = ref(false);
const torneos = ref([]);
const partidos = ref([]);
const searchQuery = ref('');
const activeRules = ref({ torneo: null, partido: null });
const datos = useUsuarios();
const nombre = computed(() => datos.usuario?.nombreUsuario);
const nombrew = computed(() => datos.usuario?.nombreUsuario);
const mostrarOpciones = ref(false);
const mostrarMenu = ref(false);
const mostrarModal = ref(false);
const partidoSeleccionado = ref(null);
const tooltipCreador = ref(false);
const tooltipEquipo = ref(false);


const irACreador = (documentoCreador) => {
  router.push(`/perfiles/${documentoCreador}`);
};


const irAEquipo = (documentoEquipo) => {
  router.push(`/inspeccion_equipo/${documentoEquipo}`);
};



const verDetalles = (item) => {
  partidoSeleccionado.value = item;
  mostrarModal.value = true;
};
const cerrarModal = () => {
  mostrarModal.value = false;
  partidoSeleccionado.value = null;
};
const irAPartidos2 = () => {
  router.push('/partidos_creados');
  mostrarMenu2.value = false;
};

const irATorneos2 = () => {
  router.push('/torneos_finalizados');
  mostrarMenu2.value = false;
};


const irAFinalizados = () => {
  router.push('/partido_finalizados');
  mostrarMenu2.value = false;
};

const getImagenUrl = (path) => {
  return path ? `http://127.0.0.1:8000/${path}` : '';
};

const irATorneos = () => {
  router.push('/torneo_creados');
};

const irAPartidos = () => {
  router.push('/partidos_creados');
};
const getTorneos = async () => {
  try {
    const idUsuario = datos.usuario.documento;
    const response = await axios.get(`http://localhost:8000/torneosDisponibles/${idUsuario}`);
    torneos.value = response.data.torneos; // Asumiendo que la respuesta tiene una propiedad 'torneos'
  } catch (error) {
    console.error('Error al obtener los torneos:', error);
  }
};


const getPartidos = async () => {
  try {
    const idUsuario = datos.usuario.documento;
    const idEquipo = datos.usuario.equipo_tiene; 

    const response = await axios.get(`http://localhost:8000/listar_partidos_filtrados/${idUsuario}/${idEquipo}`);
    partidos.value = response.data;
  } catch (error) {
    console.error('Error al obtener los partidos:', error);
  }
};

const verEnMapa = (ubicacion) => {
  const url = `https://www.google.com/maps/search/?api=1&query=${encodeURIComponent(ubicacion)}`;
  window.open(url, "_blank");
};
const showRules = (type, index) => {
  activeRules.value[type] = index;
};

const hideRules = (type, index) => {
  if (activeRules.value[type] === index) {
    activeRules.value[type] = null;
  }
};

// Función para unirse a un partido
const unirsePartido = async (idPartido) => {
  const idUsuario = datos.usuario.documento;
  const idEquipo = datos.usuario.equipo_tiene; // Usamos el equipo del usuario

  try {
    const solicitud = {
      id_usuario: idUsuario,
      id_equipo: idEquipo,
      id_partido: idPartido, // Aseguramos que se incluya el id_partido
    };

    const response = await axios.post(`http://localhost:8000/solicitar_unirse/`, solicitud);
    alert(response.data.mensaje); // Muestra el mensaje del backend
  } catch (error) {
    console.error('Error al unirse al partido:', error);
    alert('tu equipo ya envio solicitud a este partido.');
  }
};
const inscribirTorneo = async (torneo) => {
  const idTorneo = torneo.id_torneo;
  const idEquipo = datos.usuario.equipo_tiene;

  try {
    const response = await axios.post(`http://localhost:8000/enviarSolicitud/${idTorneo}`, null, {
      params: {
        id_equipo: idEquipo,
      },
    });

    alert(response.data.mensaje);
  } catch (error) {
    if (error.response && error.response.data && error.response.data.detail) {
      alert("❌ " + error.response.data.detail);
    } else {
      alert("el equipo ya envio solicitud.");
    }
    console.error(error);
  }
};
const filteredTorneos = computed(() => {
  return torneos.value.filter(torneo =>
    torneo.nombre.toLowerCase().includes(searchQuery.value.toLowerCase())
  );
});

const filteredPartidos = computed(() => {
  return partidos.value.filter(partido =>
    partido.name.toLowerCase().includes(searchQuery.value.toLowerCase())
  );
});

onMounted(() => {
  getTorneos();
  getPartidos();
});
</script>

  
  <style scoped>
.letrass {
  font-family:'Times New Roman', Times, serif;
  color: rgb(173, 173, 173);
}

  .letra-tit{
    color: #ffffff;
    text-shadow: #ffe100 0 0 5px;
    font-family:Cambria, Cochin, Georgia, Times, 'Times New Roman', serif;
    font-size: 21px
  }
  .creador-info{
    display: flex;
  align-items: center;
  border-bottom: 2px white solid;
 
  }
  .search-container{
    display: flex;
    flex-direction: row;
    width: 100%;
    align-content: space-between;
  
    justify-content: space-between;
  }

.uno_solo{
  display: flex;
  flex-direction: row;
  justify-content: flex-end;
}
  .main-container {
  padding: 20px;
  text-align: center;
  display: flex;
  flex-direction: column;
  justify-content: center;
  margin-top: 2%;
  margin-left: -10%;
  width: 100%;
  text-align: center;
  gap: 50px;

}

.buscador_torneo{
  display: flex;
  flex-direction: row;
  margin-bottom: 2%;
}

.header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 20px;
  
}

.search-bar {
  width: 40%;
  padding: 10px;
  font-size: 16px;
  position: relative;
  left: 100%;
}

.view-games-button {
  
  background-color: #0c0452;
  color: white;
  padding: 10px 20px;
  font-size: 16px;
  border: none;
  cursor: pointer;
  transition: background-color 0.3s ease;
  border: 2px solid white;

}


.card-list {
  display: flex;
  flex-direction: column; /* Mostrar en vertical */
  gap: 20px;
}

.card3 {
  color: white;
  width: 60vw; /* 60% del ancho de la vista del usuario */
  min-height: 100%;
  min-width: 150%;
  background-color: #000000;
  padding: 15px;
  box-shadow: 0px 4px 2px rgb(255, 255, 255);
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  border: none; /* Sin bordes redondeados */
  box-sizing: border-box; /* Asegura que el padding no aumente el ancho total */
  overflow: hidden; /* Asegura que no haya bordes redondeados */
  position: relative;
  right: 10%;
  gap: 50px;
  border: solid rgb(108, 107, 107);
  margin-bottom: 30px;
}

.card-header-tor, .card-header-match {
  display: flex;
  align-items: center;
  gap: 50px;
}

.logo-img {
  width: 15%;
  height: 15%;
  object-fit: cover;
  
  border: solid white;
}

.card-info-tor, .card-info-match {
  flex-grow: 1;
  
  text-align: left;
  font-size: 120%;
  width: 10%;
  display: inline;
}

.rules-container {
  margin-right: 35%;
  height: auto;
  font-size: 90%;
}

.card-info-tor, .card-info-match {
  flex-grow: 0; /* Elimina el crecimiento del elemento */
  text-align: left;
  font-size: 120%;
  width: auto; /* Elimina la ocupación total del ancho */
  display: inline-block; /* Solo ocupa el ancho del contenido */
}

.titulo_torneo {
margin-top: 20%;
text-align: center;
  text-shadow: 0 0 6px rgb(255, 255, 255);
  color: #ffffff;
  font-size: 250%;
}

.action-button-tor, .action-button-match {
  margin-top: 10px;
  background-image: url("https://static.vecteezy.com/system/resources/thumbnails/000/549/015/small/vector-apr-2018-19.jpg");
  height: auto;
  color: white;
  padding: 10px;
  font-size: 300%;
  cursor: pointer;
  border-radius: 20px;
  margin-left: 13%;
  bottom: 35%;
  font-family: 'Times New Roman', Times, serif;
  text-shadow: 0 0 5px black;
  font-weight: bold;
  transition: all 0.3s ease; /* Transición suave */
  box-shadow: 0 8px 15px rgba(0, 0, 0, 0.1);
}
.action-button-tor2 {
  margin-top: 2px;
  background-color: #989898;
  height: auto;
  color: white;
  padding: 10px;
  font-size: 150%;
  cursor: pointer;
  font-family: 'Times New Roman', Times, serif;
  text-shadow: 0 0 5px black;
  font-weight: bold;
  transition: all 0.3s ease;
  box-shadow: 0 8px 15px rgba(0, 0, 0, 0.1);
  border-radius: 5px; /* Bordes redondeados */
}

.action-button-tor2:hover {
  background-color: #7a7a7a; /* Color más oscuro al pasar el cursor */
  box-shadow: 0 12px 20px rgba(0, 0, 0, 0.3); /* Sombra más intensa */
  transform: scale(1.05); /* Aumenta ligeramente el tamaño */
}

.action-button-tor3 {
  margin-top: 5px;
  background-image: url("https://static.vecteezy.com/system/resources/thumbnails/000/549/015/small/vector-apr-2018-19.jpg");
  height: auto;
  color: white;
  padding: 5px;
  font-size: 200%;
  cursor: pointer;
  margin-bottom: 10px;
  bottom: 35%;
  font-family: 'Times New Roman', Times, serif;
  text-shadow: 0 0 5px black;
  font-weight: bold;
  transition: all 0.3s ease; /* Transición suave */
  border-radius: 20px;
  box-shadow: 0 8px 15px rgba(0, 0, 0, 0.1);
}

/* Hover */
.action-button-tor3 {
  margin-top: 5px;
  background-image: url("https://static.vecteezy.com/system/resources/thumbnails/000/549/015/small/vector-apr-2018-19.jpg");
  height: auto;
  color: white;
  padding: 5px;
  font-size: 200%;
  cursor: pointer;
  margin-bottom: 10px;
  bottom: 35%;
  font-family: 'Times New Roman', Times, serif;
  text-shadow: 0 0 5px black;
  font-weight: bold;
  transition: transform 0.3s ease, box-shadow 0.3s ease; /* Transición suave */
  border-radius: 20px;
  box-shadow: 0 8px 15px rgba(0, 0, 0, 0.1);
}

/* Hover mejorado */
.action-button-tor:hover {
  transform: translateY(-3px); /* Efecto de elevación */
  box-shadow: 0 12px 20px rgba(255, 255, 255, 0.3); /* Sombra más brillante */
  text-shadow: 0 0 10px rgba(255, 255, 255, 0.8); /* Brillo sutil en el texto */
}
.action-button-tor3:hover {
  transform: translateY(-3px); /* Efecto de elevación */
  box-shadow: 0 12px 20px rgba(255, 255, 255, 0.3); /* Sombra más brillante */
  text-shadow: 0 0 10px rgba(255, 255, 255, 0.8); /* Brillo sutil en el texto */
}


.torn_boton {
  color: rgb(0, 0, 0);
  position: relative;
  border-radius: 10px;
  font-size: 150%;
  font-family: Cambria, Cochin, Georgia, Times, 'Times New Roman', serif;

}

.reglas {
  background-color: rgb(90, 90, 90);
  width: 15%;
  height: auto;
  position: absolute;
}

.titu {
  font-size: 170%;
  font-weight: bold;
  text-align: center;
  
  background-image: url("https://static.vecteezy.com/system/resources/thumbnails/000/549/015/small/vector-apr-2018-19.jpg");
  background-size: cover; /* Ajusta el tamaño de la imagen para que cubra todo el texto */
  background-clip: text;
  -webkit-background-clip: text; /* Para navegadores que requieren prefijo */
  color: transparent; /* Hace el texto transparente para mostrar el fondo */
  text-shadow: none; /* Elimina sombras en el texto si hay */
}
.search-input{
  font-size: 140%;
  border: 2px solid transparent;
  width: 15em;
  height: 2.5em;
  padding-left: 0.8em;
  outline: none;
  overflow: hidden;
  background-color: #f3f3f3;
  border-radius: 10px;
  transition: all 0.5s;
}

.search-input:hover,
.search-input:focus {
  border: 2px solid #4a9dec;
  box-shadow: 0px 0px 0px 7px rgb(74, 157, 236, 20%);
  background-color: white;
}

.titu2 {
  font-size: 170%;
  font-weight: bold;

  left: 300%;
  background-image: url("https://static.vecteezy.com/system/resources/thumbnails/000/549/015/small/vector-apr-2018-19.jpg");
  background-size: cover; /* Ajusta el tamaño de la imagen para que cubra todo el texto */
  background-clip: text;
  -webkit-background-clip: text; /* Para navegadores que requieren prefijo */
  color: transparent; /* Hace el texto transparente para mostrar el fondo */
  text-shadow: none;
}

@media (max-width: 320px) {
  /* Estilos para pantallas con un ancho máximo de 320px */
  .titulo_torneo {
margin-top: 20%;
text-align: center;
  text-shadow: 0 0 6px rgb(255, 255, 255);
  color: #ffffff;
  font-size: 160%;
  width: 100%;
  margin-left: 20%;
}
.main-container {
  padding: 20px;
  text-align: center;
  display: flex;
  flex-direction: column;
  justify-content: center;
  margin-top: 2%;
  margin-left: 33%;
  width: 65%;
  gap: 50px;
  text-align: center;

}
  
}


@media (min-width: 321px) and (max-width:480px) {
  /* Estilos para pantallas con un ancho máximo de 320px */
  .titulo_torneo {
margin-top: 20%;
text-align: center;
  text-shadow: 0 0 6px rgb(255, 255, 255);
  color: #ffffff;
  font-size: 160%;
  width: 100%;
  margin-left: 20%;
}
.main-container {
  padding: 20px;
  text-align: center;
  display: flex;
  flex-direction: column;
  justify-content: center;
  margin-top: 2%;
  margin-left: 28%;
  width: 70%;
  text-align: center;
  gap: 50px;
}
  
}




@media (min-width: 481px) and (max-width: 600px) {
  /* Estilos para pantallas entre 481px y 600px */
  .titulo_torneo {
margin-top: 20%;
  text-shadow: 0 0 6px rgb(255, 255, 255);
  color: #000000;
  font-size: 160%;
  margin-left: 40%;
}
.main-container {
  padding: 20px;
  text-align: center;
  display: flex;
  flex-direction: column;
  justify-content: center;
  margin-top: 2%;
  margin-left: 17%;
  width: 60%;
  text-align: center;
  gap: 50px;
}
}







@media (min-width: 601px) and (max-width: 768px) {
  /* Estilos para pantallas entre 601px y 768px */
  .titulo_torneo {
margin-top: 20%;
  text-shadow: 0 0 6px rgb(255, 255, 255);
  color: #000000;
  font-size: 160%;
  margin-left: 40%;
}
.main-container {
  padding: 20px;
  text-align: center;
  display: flex;
  flex-direction: column;
  justify-content: center;
  margin-top: 2%;
  margin-left: 6%;
  width: 70%;
  text-align: center;
  gap: 50px;
}
}


@media (min-width: 769px) and (max-width: 1024px) {
  /* Estilos para pantallas entre 769px y 1024px */
  .titulo_torneo {
margin-top: 20%;
  text-shadow: 0 0 6px rgb(255, 255, 255);
  color: #000000;
  font-size: 205%;
  margin-left: 20%;
}
.main-container {
  padding: 20px;
  text-align: center;
  display: flex;
  flex-direction: column;
  justify-content: center;
  margin-top: 2%;
  margin-left: 5%;
  width: 100%;
  text-align: center;
  gap: 50px;
}
}


@media (min-width: 1025px) and (max-width: 1280px) {
  /* Estilos para pantallas entre 1025px y 1280px */
  .titulo_torneo {
margin-top: 20%;
  text-shadow: 0 0 6px rgb(255, 255, 255);
  color: #000000;
  font-size: 205%;
  margin-left: 20%;
}
.main-container {
  padding: 20px;
  text-align: center;
  display: flex;
  flex-direction: column;
  justify-content: center;
  margin-top: 2%;
  margin-right: 0%;
  width: 100%;
  text-align: center;
  gap: 50px;
}
}

@media (min-width: 1281px) and (max-width: 1440px) {
  /* Estilos para pantallas entre 1281px y 1440px */
  .titulo_torneo {
margin-top: 20%;
  text-shadow: 0 0 6px rgb(255, 255, 255);
  color: #000000;
  font-size: 205%;
  margin-left: 20%;
}
.main-container {
  padding: 20px;
  text-align: center;
  display: flex;
  flex-direction: column;
  justify-content: center;
  margin-top: 2%;
  margin-right: 0%;
  width: 100%;
  gap: 50px;
  text-align: center;
}
}



@media (min-width: 1441px) and (max-width: 1920px) {
  /* Estilos para pantallas entre 1441px y 1920px */
}

@media (min-width: 1921px) and (max-width: 2560px) {
  /* Estilos para pantallas entre 1921px y 2560px */
}

@media (min-width: 2561px) and (max-width: 3840px) {
  /* Estilos para pantallas entre 2561px y 3840px */
}


@media (min-width: 3841px) and (max-width: 5120px) {
  /* Estilos para pantallas entre 3841px y 5120px */
}


.crear-btn {
  background-color: black;
  color: gold;
  padding: 10px 25px;
  border: 2px solid gold;
  border-radius: 10px;
  font-weight: bold;
  cursor: pointer;
  transition: background 0.3s, color 0.3s;
  z-index: 10;
  font-size: 16px;
}

.crear-btn:hover {
  background-color: gold;
  color: black;
}

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.7); /* fondo oscuro translúcido */
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 100;
}

.modal-menu {
  background-color: white;
  border-radius: 12px;
  padding: 30px 20px;
  min-width: 280px;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.4);
  text-align: center;
  position: relative;
}

.dropdown-option {
  display: block;
  padding: 15px 10px;
  color: black;
  text-decoration: none;
  font-weight: 600;
  font-size: 16px;
  transition: background-color 0.2s, color 0.2s;
  border: #989898 solid;
}

.dropdown-option:hover {
  background-color: rgba(255, 217, 0, 0.489);
  color: black;
  border: solid black;
  border-radius: 6px;
}

.separator {
  height: 2px;
  background-color: gold;
  margin: 10px 0;
  border-radius: 2px;
}

/* Estilo para Torneos */
.boton-torneos:hover {
  transform: scale(1.05);
  box-shadow: 0 6px 14px rgba(212, 175, 55, 0.6);
}

/* Estilo para Partidos */
.boton-partidos {
  background-color: black;
  color: white;
  padding: 12px 28px;
  border: 2px solid gold;
  border-radius: 15px;
  font-weight: 600;
  font-size: 16px;
  margin: 10px;
  cursor: pointer;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.3);
  transition: background-color 0.3s ease, transform 0.2s ease;
}

.boton-partidos:hover {
  background-color: gold;
  color: black;
  transform: scale(1.05);
}

.boton-creados {
  background-color: black;
  color: gold;
  padding: 10px 20px;
  border: 2px solid gold;
  border-radius: 8px;
  cursor: pointer;
  font-weight: bold;
  transition: 0.3s;
  margin-left: 40px;
}

.boton-creados:hover {
  background-color: gold;
  color: black;
}

.menu-creados {
  border-radius: 10px;
  overflow: hidden;
}

.opcion-menu {
  padding: 12px 16px;
  cursor: pointer;
  transition: background-color 0.3s;
  background-color: black;
  color: white;
}

.opcion-menu:hover {
  color: orange;
  border: 1px solid rgb(255, 255, 255);
  box-shadow: 0 0 10px white;
}

.border-gold {
  border-color: gold;
}
.logo-pequeno{
  width: 50px;
  height: 50px;
  border-radius: 50px;
  border: solid rgb(255, 200, 0);
  margin-right: 10px;
  margin-bottom: 10px;
}
.equipo-info{
  display: flex;
  justify-content: center;
  align-items: center;
}
.modal-overlay2 {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.6);
  display: flex;
  align-items: center;
  justify-content: center;
  backdrop-filter: blur(8px);
}

.modal-content2 {
  margin-top: 125px;
  background: linear-gradient(135deg, #1c1c1c, #444);
  color: #fff;
  padding: 20px;
  border-radius: 10px;
  width: 400px;
  max-height: 80vh; /* Limita la altura del modal */
  overflow-y: auto; /* Agrega barra de desplazamiento vertical */
  text-align: center;
  box-shadow: 0 0 15px rgba(255, 215, 0, 0.5);
  border: 1px solid #FFD700;
}


.modal-section {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  margin: 10px 0;
  padding: 10px;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 8px;
}
.modal-section2 {
  display: flex;
  flex-direction: column;
  gap: 12px;
  margin: 10px 0;
  padding: 15px;
  background: rgba(255, 255, 255, 0.15);
  border-radius: 10px;
  box-shadow: 0 0 10px rgba(255, 215, 0, 0.3);
  text-align: left;
} 
.logo-modal {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  border: 2px solid #FFD700;
}

.inspect-button {
  background: none;
  color: #FFD700;
  border: 1px solid #FFD700;
  padding: 5px 10px;
  border-radius: 5px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.inspect-button:hover {
  background: #FFD700;
  color: #000;
  box-shadow: 0 0 10px #FFD700;
}

.tooltip {
  background: #333;
  color: #fff;
  padding: 5px;
  border-radius: 5px;
  font-size: 12px;
  position: absolute;
  transform: translateY(-150%);
}

.close-button2 {
  background: #FFD700;
  color: #000;
  border: none;
  padding: 10px 15px;
  border-radius: 5px;
  cursor: pointer;
  font-weight: bold;
  transition: 0.3s;
}

.close-button2:hover {
  background: #fff;
  color: #000;
  box-shadow: 0 0 10px #FFD700;
}
.titulo-detalle {
  font-size: 1.4rem;
  color: #FFD700;
  text-transform: uppercase;
  text-align: center;
  font-weight: bold;
  border-bottom: 2px solid #FFD700;
  padding-bottom: 5px;
  margin-bottom: 8px;
  letter-spacing: 1px;
}
.detalle-texto {
  font-weight: bold;
  color: #fff;
  font-size: 1rem;
}
.modal-section2 p {
  display: flex;
  justify-content: space-between;
  background: rgba(0, 0, 0, 0.3);
  padding: 8px;
  border-radius: 5px;
  box-shadow: inset 0 0 5px rgba(255, 215, 0, 0.4);
}

.modal-section2 p strong {
  color: #FFD700;
  font-size: 1rem;
  font-weight: bold;
}


.map-button {
  background: linear-gradient(45deg, #FFD700, #FFB800);
  color: #000;
  padding: 10px;
  font-size: 1rem;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-weight: bold;
  margin-top: 10px;
  transition: 0.3s ease-in-out;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
}
.map-button:hover {
  background: linear-gradient(45deg, #FFB800, #FFD700);
  transform: scale(1.05);
  box-shadow: 0 0 10px rgba(255, 215, 0, 0.6);
}
.let {
  color: rgb(255, 255, 255);
  font-size: 1.1rem; /* Tamaño de letra más grande */
  font-weight: bold; /* Negrita */
  text-transform: uppercase; /* Convertir el texto en mayúsculas */
  text-shadow: 2px 2px 5px rgba(255, 242, 0, 0.5); /* Sombra roja suave */
  letter-spacing: 1px; /* Espaciado entre letras */
  font-family: 'Poppins', sans-serif; /* Fuente moderna */
}

.dettt{

  color: #ffffff; /* Dorado */
  font-size: 1.1rem; /* Más grande que los demás textos */
  font-weight: bold; /* Negrita */
  text-transform: uppercase; /* Convertir en mayúsculas */
  text-shadow: 3px 3px 8px rgba(255, 215, 0, 0.8); /* Sombra más fuerte */
  font-family: 'Poppins', sans-serif; /* Fuente elegante */
  text-align: center; /* Centrado */
  display: block; /* Para ocupar toda la línea */
  margin-bottom: 10px; /* Espaciado debajo */
  border-radius: 8px; /* Bordes redondeados */


}
.imagen-cancha-modal {
  width: 100%;
  max-height: 250px;
  object-fit: cover;
  border-radius: 10px;
  margin-top: 10px;
}

  </style>
  