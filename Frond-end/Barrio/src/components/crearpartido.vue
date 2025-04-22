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
  <div class="crear-partido-container">

    <div class="volver-btn">
  <button @click="volver" class="btn-volver">
    Volver
  </button>
</div>
    <div class="formulario">
      <h2>Crear Partido</h2>
      <form @submit.prevent="crearPartido">
        <div class="campo">
          <label for="name">Nombre del Partido:</label>
          <input type="text" id="name" v-model="form.name" required />
        </div>
        <div class="campo">
          <label for="hora">Hora:</label>
          <input type="time" id="hora" v-model="form.hora" required />
        </div>
        <div class="campo">
          <label for="dia">Fecha:</label>
          <input type="date" id="dia" v-model="form.dia" required />
        </div>
        <div class="campo">
  <label for="apuesta">Apuesta total de dinero:// {{ apuestaFormateada }}</label>
  <input
    type="number"
    id="apuesta"
    v-model.number="form.apuesta"
    min="100"
    step="100"
    @input="formatearApuesta"
    required
  />
  <small class="texto-apuesta">{{ apuestaFormateada }}</small>
</div>

<div class="campo">
  <label for="tipo_futbol">Modalidad:</label>
  <select id="tipo_futbol" v-model="form.tipo_futbol" required>
    <option disabled value="">Seleccione</option>
    <option value="futbol 11" title="11 jugadores por equipo, cancha grande">Fútbol 11</option>
<option value="Fútbol Sala (Futsal)" title="5 jugadores por equipo, cancha pequeña o cubierta">Fútbol Sala (Futsal)</option>
<option value="Fútbol 7" title="7 jugadores por equipo, cancha mediana">Fútbol 7</option>
<option value="Fútbol Playa" title="5 jugadores por equipo, se juega en arena, cancha pequeña">Fútbol Playa</option>
<option value="Fútbol Indoor" title="5 jugadores por equipo, cancha cubierta o sintética">Fútbol Indoor</option>
  </select>
  <!-- ✅ Texto explicativo según selección -->
  <p v-if="descripcionModalidad()" class="descripcion-modalidad">
  {{ descripcionModalidad() }}
</p>

</div>
        <div class="campo">
  <label for="reglas">Reglas del Partido:</label>
  <textarea id="reglas" v-model="form.reglas" rows="3"  required ></textarea>
</div>
<div class="campo">
  <label for="como_llegar">Cómo llegar:</label>
  <textarea id="como_llegar" v-model="form.como_llegar" rows="3"  required ></textarea>
</div>
<div class="campo">
  <label for="logo_partido">Logo del Partido:</label>
  <input type="file" id="logo_partido" @change="onFileChangeLogo" required  />
  <div v-if="logoPartidoPreview" class="preview-img">
    <img :src="logoPartidoPreview" alt="Vista previa del logo" />
  </div>
</div>
<div class="campo">
  <label for="imagen_cancha">Imagen de la Cancha:</label>
  <input type="file" id="imagen_cancha" @change="onFileChangeCancha"  required />
  <div v-if="imagenCanchaPreview" class="preview-img">
    <img :src="imagenCanchaPreview" alt="Vista previa de la cancha" />
  </div>
</div>
        <div class="campo">
          <label for="ubicacionpartido"  required >Ubicación:</label>
          <input
            type="text"
            id="ubicacionpartido"
            v-model="form.ubicacionpartido"
            readonly
            required
          />
          <button type="button" @click="obtenerUbicacionActual" >
            Obtener ubicación
          </button>
        </div>
        <div class="acciones">
          <button type="submit">Crear Partido</button>
        </div>
      </form>
    </div>
  </div>
</template>
<script>

import Headerapp from "@/components/Headerapp.vue";
import Headermobile from "@/components/Headermobile.vue"; 
import { useUsuarios } from "@/stores/usuario";

export default {
  name: "CrearPartido",
  components: {
    Headerapp,
  },
  setup() {
    const usuariosStore = useUsuarios();
    return {
      usuariosStore,
    };
  },
  data() {
    return {
      logoPartidoPreview: null,
      imagenCanchaPreview: null,
      apuestaFormateada: "",
      form: {
        name: "",
        hora: "",
        dia: "",
        apuesta: null,
        tipo_futbol: "",
        estado_partido: "pendiente",
        ganador: "",
        ubicacionpartido: "",
        equipo_local: "",
        reglas: "",         
        como_llegar: ""     
      },
      logoPartido: null,
      imagenCancha: null,
    };
  },
  methods: {
    onFileChangeLogo(event) {
      const file = event.target.files[0];
      this.logoPartido = file;
      if (file) {
        this.logoPartidoPreview = URL.createObjectURL(file);
      }
    },
    onFileChangeCancha(event) {
      const file = event.target.files[0];
      this.imagenCancha = file;
      if (file) {
        this.imagenCanchaPreview = URL.createObjectURL(file);
      }
    },
    formatearApuesta() {
      const valor = this.form.apuesta;
      if (valor >= 100) {
        this.apuestaFormateada = `$ ${valor.toLocaleString("es-CO")}`;
      } else {
        this.apuestaFormateada = "";
      }
    },
    descripcionModalidad() {
  switch (this.form.tipo_futbol) {
    case "futbol 11":
      return "Fútbol 11: 11 jugadores por equipo, se juega en cancha grande.";
    case "Fútbol Sala (Futsal)":
      return "Fútbol Sala (Futsal): 5 jugadores por equipo, cancha pequeña o cubierta.";
    case "Fútbol 7":
      return "Fútbol 7: 7 jugadores por equipo, cancha mediana.";
    case "Fútbol Playa":
      return "Fútbol Playa: 5 jugadores por equipo, se juega en arena.";
    case "Fútbol Indoor":
      return "Fútbol Indoor: 5 jugadores por equipo, cancha cubierta o sintética.";
    default:
      return "";
  }
},
    obtenerUbicacionActual() {
      if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(
          (position) => {
            const { latitude, longitude } = position.coords;
            this.form.ubicacionpartido = `${latitude}, ${longitude}`;
          },
          (error) => {
            alert("Error al obtener la ubicación: " + error.message);
          }
        );
      } else {
        alert("La geolocalización no es compatible con este navegador.");
      }
    },
    volver() {
      this.$router.back();
    },
    async crearPartido() {
      try {
        const formData = new FormData();
        this.form.equipo_local = this.usuariosStore.usuario.equipo_tiene;
        for (const key in this.form) {
          formData.append(key, this.form[key]);
        }
        formData.append("Documento_Creador_P", this.usuariosStore.usuario.documento);
        formData.append("correo_usuario", this.usuariosStore.usuario.correo);
        if (this.logoPartido) {
          formData.append("logomatch", this.logoPartido);
        }
        if (this.imagenCancha) {
          formData.append("imagen_cancha", this.imagenCancha);
        }
        const response = await fetch("http://localhost:8000/crearPartido", {
          method: "POST",
          body: formData,
        });
        const data = await response.json();
        if (response.ok) {
          alert("¡Partido creado exitosamente!");
          this.$router.push("/partidos_creados");
        } else {
          alert("Error al crear el partido: " + JSON.stringify(data.detail || "Desconocido"));
        }
      } catch (error) {
        alert("Error de red: " + error.message);
      }
    },
  },
};
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600&display=swap');

.crear-partido-container {
  margin-top: 30%;
  background-color: #000;
  color: #fff;
  min-height: 100vh;
  padding: 2rem;
  font-family:Georgia, 'Times New Roman', Times, serif;
}

.formulario {
  background-color: #1a1a1a;
  border: 1px solid #444;
  border-radius: 12px;
  padding: 2rem;
  max-width: 600px;
  margin: 2rem auto;
  box-shadow: 0 0 15px rgba(218, 165, 32, 0.25);
  transition: transform 0.3s ease;
}

.formulario:hover {
  transform: scale(1.01);
}

h2 {
  text-align: center;
  color: #daa520;
  margin-bottom: 1.5rem;
  font-weight: 600;
}

.campo {
  margin-bottom: 1.2rem;
  display: flex;
  flex-direction: column;
}

label {
  margin-bottom: 0.4rem;
  font-weight: 600;
  color: #ccc;
}

input[type="text"],
input[type="time"],
input[type="date"],
input[type="number"],
input[type="file"],
select,
textarea {
  padding: 0.6rem;
  border-radius: 6px;
  border: 1px solid #555;
  background-color: #2a2a2a;
  color: #fff;
  transition: border-color 0.3s, box-shadow 0.3s;
}

input:hover,
select:hover,
textarea:hover {
  border-color: #daa520;
  box-shadow: 0 0 5px rgba(218, 165, 32, 0.3);
}

input:focus,
select:focus,
textarea:focus {
  outline: none;
  border-color: #daa520;
  box-shadow: 0 0 8px #daa520;
}

textarea {
  resize: none;
}

button {
  background-color: #daa520;
  color: #000;
  border: none;
  padding: 0.6rem 1.2rem;
  border-radius: 6px;
  font-weight: bold;
  cursor: pointer;
  transition: 0.3s;
}

button:hover {
  background-color: #ffc107;
  transform: scale(1.03);
  box-shadow: 0 0 10px rgba(218, 165, 32, 0.4);
}

.acciones {
  text-align: center;
  margin-top: 1.5rem;
}

/* Estilo especial para el botón de ubicación */
#ubicacionpartido + button {
  margin-top: 0.5rem;
  background-color: transparent;
  border: 1px solid #daa520;
  color: #daa520;
  padding: 0.4rem 0.8rem;
  font-size: 0.9rem;
  display: inline-flex;
  align-items: center;
  gap: 0.4rem;
  border-radius: 6px;
  transition: 0.3s;
}

#ubicacionpartido + button:hover {
  background-color: #daa520;
  color: #000;
  transform: scale(1.02);
}
.preview-img img {
  max-width: 200px;
  margin-top: 10px;
  border-radius: 8px;
  box-shadow: 0 2px 6px rgba(0,0,0,0.2);
}
.btn-volver {
  background-color: #000;
  color: #FFD700; /* dorado */
  border: 2px solid #FFD700;
  padding: 10px 18px;
  border-radius: 10px;
  cursor: pointer;
  font-weight: bold;
  font-size: 16px;
  transition: all 0.3s ease;
}

.btn-volver:hover {
  background-color: #FFD700;
  color: #000;
  border-color: #000;
  transform: scale(1.05);
}

.descripcion-modalidad {
  margin-top: 5px;
  font-size: 0.9em;
  color: #555;
  font-style: italic;
}

</style>
