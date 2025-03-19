<template>
  <header>
    <Headerapp></Headerapp>
  </header>
  <div class="form-container">
    <h2>Crear Partido</h2>

    <form @submit.prevent="crearPartido">

      <!-- Nombre:  -->
      <label>Nombre Partido :</label>
      <input type="text" v-model="form.name" required />



      <input type="hidden" v-model="form.correo_usuario" />

      <!-- Hora -->
      <label>Hora:</label>
      <input type="time" v-model="form.hora" required />

      <!-- Apuesta -->
      <label>Apuesta:</label>
      <input type="number" v-model="form.apuesta" required />

      <!-- Ubicación -->
      <label>Ubicación:</label>
      <input type="text" v-model="form.ubicacionpartido" placeholder="Seleccione una ubicación"  />
      <button type="button" class="ubicacion-btn" @click="obtenerUbicacionActual">
        Obtener Ubicación Actual
      </button>
     

      <!-- Logo del Partido -->
      <div class="form_group">
        <label class="logotext">Logo del Partido</label>
        <input type="file" @change="onFileChange" accept="image/jpeg, image/png" />
      </div>

      <!-- Mapa -->
      <div id="map"></div>

      <!-- Botón de envío -->
      <button type="submit" class="submit-btn">Crear Partido</button>
    </form>
  </div>
</template>

<script>
import Headerapp from "./Headerapp.vue";
import axios from "axios";
import { useUsuarios } from "@/stores/usuario";

export default {
  components:{
    Headerapp

  },
  data() {
    
    return {
      movistore : useUsuarios(),
      form: {
        hora: "",
        name: "",
        apuesta: null,
        ubicacionpartido: "",
        logomatch : null,
        correo_usuario :"",
      },
    };
  },
  methods: {
    onFileChange(event) {
  this.form.logomatch = event.target.files[0];
},
    async crearPartido() {
      const datosenviar = new FormData();
      datosenviar.append("hora", this.form.hora);
      datosenviar.append("name", this.form.name);
      datosenviar.append("apuesta", this.form.apuesta);
      datosenviar.append("ubicacionpartido", this.form.ubicacionpartido);
      datosenviar.append("logomatch", this.form.logomatch);
      datosenviar.append("correo_usuario",this.movistore.usuario?.correo)

      try {
        const response = await axios.post("http://localhost:8000/crearPartidos", datosenviar, {
          headers: { "Content-Type": "multipart/form-data" },
        });
        console.log("Este es el corro: "+this.movistore.usuario.correo)



        console.log("Evento creado con éxito:", response.data);
        alert(`Torneo creado con éxito!`);
        
        // Limpiar el formulario después de enviar los datos
        this.form = {
        hora: "",
        name:"",
        apuesta: null,
        ubicacionpartido: "",
        logomatch : null,
        correo_usuario : ""
        };

      } catch (error) {
        console.error("Error al crear el evento:", error);
        console.log("Detalles del error:", error.response?.data);
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
          if (data && data.address) {
            const city = data.address.city || data.address.town || data.address.village || 'Ubicación desconocida';
            this.form.ubicacionpartido = city;
          } else {
            this.form.ubicacionpartido = 'Ubicación no encontrada';
          }
        })
        .catch((error) => {
          console.error('Error al obtener la ubicación:', error);
          this.form.ubicacion = 'Error al obtener la ubicación';
        });
    },
    initMap() {
      // Crear un mapa centrado en Colombia
      const map = L.map('map').setView([4.5709, -74.2973], 6); // Coordenadas de Colombia

      // Añadir capa de mapa (OpenStreetMap)
      L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
      }).addTo(map);

      // Manejar clics en el mapa para seleccionar ubicación
      map.on('click', (e) => {
        const { lat, lng } = e.latlng;
        this.obtenerNombreUbicacion(lat, lng); // Obtener el nombre de la ubicación
      });
    },
  },

  mounted() {
    this.initMap();
      const usuarios = this.movistore.usuario
      if (usuarios) {
      this.form.correo_usuario = this.movistore.usuario.correo;
  } else {
    console.error('No se encontró usuario en localStorage');
  }

  },
  
};
</script>

<style scoped>
/* Contenedor del formulario */
.form-container {
  width: 90%;
  max-width: 450px;
  margin: auto;
  padding: 25px;
  border-radius: 12px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
  background: #f0f8ff; /* Azul muy claro */
  font-family: Arial, sans-serif;
  margin-top: 40%;
}

/* Título */
h2 {
  text-align: center;
  color: #064789; /* Azul oscuro */
}

/* Etiquetas */
label {
  display: block;
  margin-top: 12px;
  color: #064789;
  font-weight: bold;
}

/* Campos de entrada */
input {
  width: 100%;
  padding: 10px;
  margin-top: 6px;
  border: 2px solid #5aa469; /* Verde suave */
  border-radius: 6px;
  font-size: 16px;
}

/* Botón para obtener ubicación */
.ubicacion-btn {
  width: 100%;
  padding: 10px;
  margin-top: 12px;
  background: #f4a261; /* Naranja */
  color: white;
  font-size: 16px;
  border: none;
  cursor: pointer;
  border-radius: 6px;
  transition: 0.3s;
}

.ubicacion-btn:hover {
  background: #e76f51; /* Naranja oscuro */
}

/* Mapa */
#map {
  width: 100%;
  height: 200px;
  margin-top: 12px;
  border-radius: 6px;
  border: 2px solid #5aa469;
}

/* Botón de envío */
.submit-btn {
  width: 100%;
  padding: 12px;
  margin-top: 16px;
  background: #064789; /* Azul oscuro */
  color: white;
  font-size: 18px;
  border: none;
  cursor: pointer;
  border-radius: 8px;
  transition: 0.3s;
}

.submit-btn:hover {
  background: #042c5c; /* Azul más oscuro */
}
</style>
