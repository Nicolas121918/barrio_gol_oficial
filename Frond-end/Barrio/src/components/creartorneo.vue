<template>
  <header>
    <Headerapp></Headerapp>
  </header>
  <div class="form-container">
    <form @submit.prevent="crearEvento">
      <h1>Crear Torneo</h1>

      <div class="form-group">
        <label for="nombre">Nombre:</label>
        <input type="text" id="nombre" v-model="form.nombre" placeholder="Nombre del torneo" required />
      </div>

      <div class="form-group">
        <label for="tipo">Tipo de Torneo:</label>
        <input type="text" id="tipo" v-model="form.tipo" placeholder="Ej: Microfútbol, Penales, 1 vs 1" required />
      </div>

      <div class="form-group">
        <label for="categoria">Categoría:</label>
        <select id="categoria" v-model="form.categoria" required>
          <option disabled value="">Selecciona una categoría</option>
          <option>Libre</option>
          <option>Juvenil</option>
          <option>Infantil</option>
          <option>Mixto</option>
          <option>Femenino</option>
          <option>Senior</option>
        </select>
      </div>

      <div class="form-group">
        <label for="formato">Formato:</label>
        <select id="formato" v-model="form.formato" required>
          <option disabled value="">Selecciona un formato</option>
          <option>Eliminación directa</option>
          <option>Todos contra todos</option>
          <option>Grupos + Eliminación</option>
          <option>Llave ida y vuelta</option>
        </select>
      </div>

      <div class="form-group">
        <label for="fecha_inicio">Fecha de Inicio:</label>
        <input type="date" id="fecha_inicio" v-model="form.fecha_inicio" required />
      </div>

      <div class="form-group">
        <label for="fecha_final">Fecha Final:</label>
        <input type="date" id="fecha_final" v-model="form.fecha_final" required />
      </div>

      <div class="form-group">
        <label for="fecha_limite_inscripcion">Fecha Límite de Inscripción:</label>
        <input type="date" id="fecha_limite_inscripcion" v-model="form.fecha_limite_inscripcion" required />
      </div>

      <div class="form-group">
        <label for="descripcion_reglas">Descripción de Reglas:</label>
        <textarea id="descripcion_reglas" v-model="form.descripcion_reglas" rows="4" placeholder="Reglas generales del torneo" required></textarea>
      </div>

      <div class="form-group">
        <label for="cantidad_participantes">Cantidad de Participantes:</label>
        <input type="number" id="cantidad_participantes" v-model="form.cantidad_participantes" min="2" required />
      </div>

      <div class="form-group">
        <label for="requiere_uniforme">¿Requiere uniforme? (Especifique):</label>
        <input type="text" id="requiere_uniforme" v-model="form.requiere_uniforme" placeholder="Ej: Camiseta y pantaloneta del mismo color" />
      </div>

      <div class="form-group">
        <label for="duracion_partido">Duración de Partido:</label>
        <input type="text" id="duracion_partido" v-model="form.duracion_partido" placeholder="Ej: 2 tiempos de 20 min" required />
      </div>

      <div class="form-group">
        <label for="direccion">Dirección del Torneo:</label>
        <input type="text" id="direccion" v-model="form.direccion" placeholder="Dirección del evento" required />
      </div>

      <div class="form-group">
        <label for="descripcion_llegada">Descripción para llegar:</label>
        <textarea id="descripcion_llegada" v-model="form.descripcion_llegada" rows="3" placeholder="Punto de referencia o cómo llegar al sitio"></textarea>
      </div>

      <div class="form-group">
        <label for="foto_cancha">Foto de la Cancha:</label>
        <input type="file" @change="onFileChangeCancha" accept="image/jpeg, image/png" />
      </div>

      <div class="form-group">
        <label for="imagen_torneo">Imagen Representativa del Torneo:</label>
        <input type="file" @change="onFileChangeTorneo" accept="image/jpeg, image/png" />
      </div>

      <div class="form-group">
        <label for="premio_principal">Premio Principal:</label>
        <input type="text" id="premio_principal" v-model="form.premio_principal" placeholder="Premio principal del torneo" required />
      </div>

      <div class="form-group">
        <label for="premios_adicionales">Premios Adicionales (Opcional):</label>
        <input type="text" id="premios_adicionales" v-model="form.premios_adicionales" placeholder="Ej: Trofeos, medallas, etc." />
      </div>

      <div class="form-group">
        <label for="precio_arbitraje">Precio de Arbitraje ($):</label>
        <input type="number" id="precio_arbitraje" v-model="form.precio_arbitraje" min="1" required />
      </div>

      <div class="form-group">
        <label for="precio_inscripcion">Precio de Inscripción ($):</label>
        <input type="number" id="precio_inscripcion" v-model="form.precio_inscripcion" min="1" required />
      </div>

      <input type="hidden" v-model="form.correo_usuario" />

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
        tipo: '',
        categoria: '',
        formato: '',
        fecha_inicio: '',
        fecha_final: '',
        fecha_limite_inscripcion: '',
        descripcion_reglas: '',
        cantidad_participantes: '',
        requiere_uniforme: '',
        duracion_partido: '',
        direccion: '',
        descripcion_llegada: '',
        premio_principal: '',
        premios_adicionales: '',
        precio_arbitraje: '',
        precio_inscripcion: '',
        correo_usuario: '',
        foto_cancha: null,
        imagen_torneo: null,
      },
    };
  },
  methods: {
    onFileChangeCancha(event) {
      this.form.foto_cancha = event.target.files[0];
    },
    onFileChangeTorneo(event) {
      this.form.imagen_torneo = event.target.files[0];
    },
    async crearEvento() {
      const datosenviar = new FormData();
      const campos = [
        'nombre', 'tipo', 'categoria', 'formato',
        'fecha_inicio', 'fecha_final', 'fecha_limite_inscripcion',
        'descripcion_reglas', 'cantidad_participantes', 'requiere_uniforme',
        'duracion_partido', 'direccion', 'descripcion_llegada',
        'premio_principal', 'premios_adicionales',
        'precio_arbitraje', 'precio_inscripcion',
      ];

      campos.forEach(campo => {
        datosenviar.append(campo, this.form[campo]);
      });

      datosenviar.append('correo_usuario', this.datos.usuario?.correo || '');

      if (this.form.foto_cancha) {
        datosenviar.append('foto_cancha', this.form.foto_cancha);
      }

      if (this.form.imagen_torneo) {
        datosenviar.append('imagen_torneo', this.form.imagen_torneo);
      }

      try {
        const response = await axios.post('http://localhost:8000/crearTorneo', datosenviar, {
          headers: { 'Content-Type': 'multipart/form-data' },
        });

        alert('Torneo creado con éxito!');
        console.log(response.data);

        // Reset del formulario
        this.form = {
          nombre: '',
          tipo: '',
          categoria: '',
          formato: '',
          fecha_inicio: '',
          fecha_final: '',
          fecha_limite_inscripcion: '',
          descripcion_reglas: '',
          cantidad_participantes: '',
          requiere_uniforme: '',
          duracion_partido: '',
          direccion: '',
          descripcion_llegada: '',
          premio_principal: '',
          premios_adicionales: '',
          precio_arbitraje: '',
          precio_inscripcion: '',
          correo_usuario: '',
          foto_cancha: null,
          imagen_torneo: null,
        };
      } catch (error) {
        console.error('Error al crear el torneo:', error);
        console.log('Detalles del error:', error.response?.data);
        alert('Ocurrió un error al crear el torneo.');
      }
    },
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
  