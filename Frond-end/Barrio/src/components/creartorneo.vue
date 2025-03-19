<template>
  <header>
    <Headerapp></Headerapp>
  </header>
  <div class="form-container">
    <form @submit.prevent="crearEvento">
      <h1>Crear Torneo</h1>

      <div class="form-group">
        <label for="nombre">Nombre:</label>
        <input type="text" id="nombre" v-model="form.nombre" placeholder="Nombre del evento" required />
      </div>

      <div class="form-group">
        <label for="fecha">Fecha:</label>
        <input type="date" id="fecha" v-model="form.fecha" required />
      </div>

      <div class="form-group">
        <label for="mapa">Ubicación:</label>
        <div id="map" class="map"></div>
        <input type="text" v-model="form.ubicacion" readonly placeholder="Ubicación seleccionada" />
      </div>

      <div class="form-group">
        <button type="button" class="centered-button" @click="obtenerUbicacionActual">Usar Mi Ubicación</button>
      </div>

      <div class="form-group">
        <label for="numPartidos">Número de Partidos:</label>
        <input type="number" id="numPartidos" v-model="form.numPartidos" min="1" required placeholder="Número de partidos del torneo" />
      </div>

      <div class="form-group">
        <label for="numParticipantes">Número de Participantes:</label>
        <input type="number" id="numParticipantes" v-model="form.numeroparticipantes" min="2" required placeholder="Número de participantes del torneo" />
      </div>

      <div class="form-group">
        <label for="apuestaTorneo">Apuesta por Torneo ($):</label>
        <input type="number" id="apuestaTorneo" v-model="form.apuestaTorneo" min="1" required placeholder="Monto de apuesta por torneo" />
      </div>

      <div class="form-group">
        <label for="precioArbitrajeTorneo">Precio de Arbitraje por Torneo ($):</label>
        <input type="number" id="precioArbitrajeTorneo" v-model="form.precioArbitrajeTorneo" min="1" required placeholder="Precio de arbitraje por torneo" />
      </div>

      <div class="form-group">
        <label for="precioInscripcion">Precio de Inscripción ($):</label>
        <input type="number" id="precioInscripcion" v-model="form.precioInscripcion" min="1" required placeholder="Precio de inscripción al torneo" />
      </div>

      <div class="form-group">
        <label for="reglasTorneo">Reglas del Torneo:</label>
        <textarea id="reglasTorneo" v-model="form.reglasTorneo" rows="4" placeholder="Escribe las reglas del torneo aquí"></textarea>
      </div>

      <input type="hidden" v-model="form.correo_usuario" />

      <div class="form-group">
        <label class="logotext">Logo del torneo</label>
        <input type="file" @change="onFileChange" accept="image/jpeg, image/png" />
      </div>

      <div class="form-group">
        <button type="submit" class="centered-button">Crear</button>
      </div>
    </form>
  </div>
</template>

<script>
import L from 'leaflet';
import Headerapp from './Headerapp.vue';
import axios from 'axios';
import { useUsuarios } from '@/stores/usuario';

export default {
  components: {
    Headerapp,
  },
  data() {
    return {
      datos: useUsuarios(),
      form: {
        nombre: '',
        fecha: '',
        ubicacion: '',
        numPartidos: '',
        apuestaTorneo: '',
        precioArbitrajeTorneo: '',
        precioInscripcion: '',
        reglasTorneo: '',
        numeroparticipantes: '',
        logoTeam: null,
        correo_usuario: '',
      },
    };
  },
  methods: {
    onFileChange(event) {
      this.form.logoTeam = event.target.files[0];
    },
    async crearEvento() {
      const datosenviar = new FormData();
      datosenviar.append('nombre', this.form.nombre);
      datosenviar.append('fecha', this.form.fecha);
      datosenviar.append('ubicacion', this.form.ubicacion);
      datosenviar.append('numPartidos', this.form.numPartidos);
      datosenviar.append('apuestaTorneo', this.form.apuestaTorneo);
      datosenviar.append('precioArbitrajeTorneo', this.form.precioArbitrajeTorneo);
      datosenviar.append('precioInscripcion', this.form.precioInscripcion);
      datosenviar.append('reglasTorneo', this.form.reglasTorneo);
      datosenviar.append('numeroparticipantes', this.form.numeroparticipantes);
      datosenviar.append('correo_usuario', this.datos.usuario?.correo); 

      if (this.form.logoTeam) {
        datosenviar.append('logoTeam', this.form.logoTeam);
      }

      try {
        const response = await axios.post('http://localhost:8000/crearTorneo', datosenviar, {
          headers: { 'Content-Type': 'multipart/form-data' },
        });

        console.log('Evento creado con éxito:', response.data);
        alert('Torneo creado con éxito!');

        this.form = {
          nombre: '',
          fecha: '',
          ubicacion: '',
          numPartidos: '',
          apuestaTorneo: '',
          precioArbitrajeTorneo: '',
          precioInscripcion: '',
          reglasTorneo: '',
          numeroparticipantes: '',
          logoTeam: null,
          correo_usuario: '',
        };
      } catch (error) {
        console.error('Error al crear el evento:', error);
        console.log('Detalles del error:', error.response?.data);
      }
    },
    obtenerUbicacionActual() {
      if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(
          (position) => {
            const { latitude, longitude } = position.coords;
            this.obtenerNombreUbicacion(latitude, longitude);
          },
          () => {
            alert('No se pudo obtener la ubicación');
          }
        );
      } else {
        alert('Geolocalización no es compatible con este navegador.');
      }
    },
    obtenerNombreUbicacion(lat, lng) {
      const url = `https://nominatim.openstreetmap.org/reverse?lat=${lat}&lon=${lng}&format=json&addressdetails=1&lang=es`;
      fetch(url)
        .then((response) => response.json())
        .then((data) => {
          this.form.ubicacion = data.address.city || data.address.town || data.address.village || 'Ubicación desconocida';
        })
        .catch((error) => {
          console.error('Error al obtener la ubicación:', error);
          this.form.ubicacion = 'Error al obtener la ubicación';
        });
    },
    initMap() {
      const map = L.map('map').setView([4.5709, -74.2973], 6);
      L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png').addTo(map);
      map.on('click', (e) => this.obtenerNombreUbicacion(e.latlng.lat, e.latlng.lng));
    },
  },
  mounted() {
    this.initMap();
  },
};
</script>

  <style scoped>
  .form-container {
    width: 500px;
    max-width: 600px;
    margin-top: 200px;
    padding: 20px;
    border-radius: 30px;
    border: 4px solid rgb(4, 3, 2); /* Borde negro */
    background: linear-gradient(to bottom, #514e4290, #8c8b8584); /* Fondo degradado */
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    margin-bottom: 100px;
}

  h1{
    font-weight: bold;
    color: black;
  }
  
  .form-group {
    display: flex;
    flex-direction: column;
    margin-bottom: 15px;
    color: black;
  }
  
  label {
    font-weight: bold;
    margin-bottom: 5px;
  }
  
  input,
  select,
  textarea {
    padding: 8px;
    font-size: 16px;
    border-radius: 5px;
    border: 1px solid #ccc;
    
  }

  #tipo{
    color: black;
  }
  
  button {
    background: url('https://i.pinimg.com/736x/82/77/8d/82778d6d72c05cf2808e3bd2bcaeb823.jpg') no-repeat center center; /* Imagen de fondo */
    background-size: cover; /* Ajusta la imagen para cubrir todo el botón */
    color: rgb(0, 0, 0); /* Color del texto */
    font-size: 17px;
    padding: 10px 20px; /* Espaciado interno */
    border: solid 2px black; /* Borde */
    border-radius: 5px; /* Bordes redondeados */
    width: 250px; /* Ancho del botón */
    cursor: pointer; /* Cursor interactivo */
    text-shadow: 1px 1px 2px black; /* Sombra para que el texto sea más legible */
}


button:hover {
    background-color: gray; /* Fondo gris */

    transform: scale(1.1); /* Aumenta el tamaño del botón un 10% */
}

  
  .map {
    height: 200px;
    margin-top: 20px;
    z-index: 0;
  }
  
  h1 {
    text-align: center;
    font-size: 24px;
  }
  
  textarea {
    resize: vertical;
  }

  .centered-button{
    display: block;
  margin: 10px auto;
  text-align: center;
  }

  @media (max-width: 320px) {
    .form-container {
    width: 120px;
    max-width: 150px;
    margin-top: 200px;
    padding: 20px;
    border-radius: 30px;
    border: 4px solid rgb(4, 3, 2); /* Borde negro */
    background: linear-gradient(to bottom, #514e4290, #8c8b8584); /* Fondo degradado */
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    margin-bottom: 100px;
}
}


@media (max-width: 480px) {
    .form-container {
    width: 300px;
    max-width: 400px;
    margin-top: 200px;
    padding: 20px;
    border-radius: 30px;
    border: 4px solid rgb(4, 3, 2); /* Borde negro */
    background: linear-gradient(to bottom, #514e4290, #8c8b8584); /* Fondo degradado */
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    margin-bottom: 100px;
}
}


@media (min-width: 481px) and (max-width: 600px) {
    .form-container {
    width: 400px;
    max-width: 600px;
    margin-top: 200px;
    padding: 20px;
    border-radius: 30px;
    border: 4px solid rgb(4, 3, 2); /* Borde negro */
    background: linear-gradient(to bottom, #514e4290, #8c8b8584); /* Fondo degradado */
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    margin-bottom: 100px;
}
}


  </style>
  