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

    <div
      v-if="mostrarMenu"
      class="menu-creados absolute right-0 mt-2 w-48 bg-black text-white border border-gold rounded shadow-lg z-50"
    >
      <div @click="irATorneos" class="opcion-menu">Torneos Creados</div>
      <hr class="border-gold my-1" />
      <div @click="irAPartidos" class="opcion-menu">Partidos Creados</div>
    </div>
  </div>
  <div class="relative inline-block text-left" @mouseleave="mostrarMenu2 = false">
  <button @click="mostrarMenu2 = !mostrarMenu2" class="boton-creados">
    Eventos ▼
  </button>

  <div
    v-if="mostrarMenu2"
    class="menu-creados absolute right-0 mt-2 w-48 bg-black text-white border border-gold rounded shadow-lg z-50"
  >
    <div @click="irAPartidos2" class="opcion-menu">Partidos en juego</div>
    <hr class="border-gold my-1" />
    <div @click="irATorneos2" class="opcion-menu">Torneos en juego</div>
    <hr class="border-gold my-1" />
    <div @click="irAFinalizados" class="opcion-menu">Finalizados</div>
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
          <button class="action-button-tor" @click="inscribirTorneo(index)">Inscribir</button>
        </div>
      </div>
    </div>
    <div>
      <div v-for="(item, index) in filteredPartidos" :key="index" class="card3">
        <div class="card-header-tor">
          <img :src="getImagenUrl(item.logomatch)" alt="Logo del partido" class="logo-img" />
          <div class="card-info-tor">
            <h2 class="titu">Nombre Partido: {{ item.name }}</h2>
            <p>Hora Partido: {{ item.hora }}</p>
            <p>Apuesta: ${{ item.apuesta }}</p>
            <p>Ubicación: {{ item.ubicacionpartido }}</p>
          </div>
        </div>
        <div class="uno_solo">
          <button class="action-button-tor" @click="inscribirTorneo(index)">Jugar</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import axios from 'axios';
import Headerapp from './Headerapp.vue';
import { useUsuarios } from '@/stores/usuario';
import { useRouter } from 'vue-router';

const router = useRouter();
const mostrarMenu2 = ref(false)


const torneos = ref([]);
const partidos = ref([]);
const searchQuery = ref('');
const activeRules = ref({ torneo: null, partido: null });
const datos = useUsuarios();
const nombre = computed(() => datos.usuario?.nombreUsuario);
const nombrew = computed(() => datos.usuario?.nombreUsuario);
const mostrarOpciones = ref(false);
const mostrarMenu = ref(false);


console.log( nombre.value)
console.log(nombrew.value)

const irAPartidos2 = () => {
  router.push('/partidos_creados')
  mostrarMenu2.value = false
}
const irATorneos2 = () => {
  router.push('/torneos_en_juego')
  mostrarMenu2.value = false
}
const irAFinalizados = () => {
  router.push('/finalizados')
  mostrarMenu2.value = false
}
const getImagenUrl = (path) => {
  return path ? `http://127.0.0.1:8000/${path}` : '';
};
const irATorneos = () => {
  router.push('/ganador'); // asegúrate de que la ruta exista
};

const irAPartidos = () => {
  router.push('/partidos_creados'); // asegúrate de que esta ruta esté bien escrita
};



const getTorneos = async () => {
  try {
    const response = await axios.get(`http://localhost:8000/listartorneos/${nombre.value}`); 
    torneos.value = response.data;
  } catch (error) {
    console.error('Error al obtener los torneos:', error);
  }
};
    
const getPartidos = async () => {
  try {
    const response = await axios.get(`http://localhost:8000/listarpartidos/${nombrew.value}`);
    partidos.value = response.data;
  } catch (error) {
    console.error('Error al obtener los partidos:', error);
  }
};



const showRules = (type, index) => {
  activeRules.value[type] = index;
};

const hideRules = (type, index) => {
  if (activeRules.value[type] === index) {
    activeRules.value[type] = null;
  }
};

const inscribirTorneo = (index) => {
  alert(`Inscripción al torneo ${index + 1}`);
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

  left: 70%;
  bottom: 35%;
  font-family: 'Times New Roman', Times, serif;
  text-shadow: 0 0 5px black;
  font-weight: bold;
  transition: all 0.3s ease; /* Transición suave */
  box-shadow: 0 8px 15px rgba(0, 0, 0, 0.1);
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
  </style>
  