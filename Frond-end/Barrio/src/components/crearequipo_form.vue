<template>
  <header>
    <headerapp></headerapp>
  </header>
  <form @submit.prevent="Insertar_team" class="crear_equipo_form">
    <div class="crear_equipo_form-title"><span>CREA TU PRIMER EQUIPO AQUI</span></div>

    <div class="crear_equipo_input-container">
      <p class="arrina">Nombre:</p>
      <input v-model="nombreteam" class="crear_equipo_input" type="text" placeholder="Nombre del equipo" required />
    </div>

    <div class="crear_equipo_input-container">
      <p class="arrina">Descripción:</p>
      <textarea v-model="Descripcion" class="crear_equipo_input" placeholder="Descripción del equipo" required></textarea>
    </div>

    <div class="crear_equipo_input-container">
      <p class="arrina">Cantidad De Integrantes:</p>
      <input v-model="numeropeople" class="crear_equipo_input" type="number" required placeholder="Cantidad de Integrantes" />
    </div>

    <div class="crear_equipo_input-container">
      <p class="arrina">Futuro Capitán:</p>
      <input v-model="capitanteam" class="crear_equipo_input" type="text" readonly required placeholder="Capitán Del equipo" />
    </div>

    <div class="crear_equipo_input-container">
      <input v-model="documento_cap" class="crear_equipo_input" type="hidden" />
    </div>

    <div class="crear_equipo_input-container">
      <p class="arrina">Requisitos De Equipo:</p>
      <input v-model="requisitos_join" class="crear_equipo_input" type="text" required placeholder="Requisitos del equipo" />
    </div>

    <div class="crear_equipo_input-container">
      <p class="arrina">Ciudad Del Equipo:</p>
      <input v-model="location" class="crear_equipo_input" type="text" placeholder="Ciudad del equipo" required />
    </div>

    <div class="crear_equipo_input-container">
      <label class="logotext">Logo del equipo</label>
      <input type="file" @change="onFileChange" accept="image/jpeg, image/png" />

      <!-- Vista previa de la imagen -->
      <div v-if="logoPreview" class="logo-preview">
        <img :src="logoPreview" alt="Vista previa del logo">
      </div>
    </div>
    <button class="contacto_boton" type="submit">Enviar</button>
  </form>
</template>
<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';
import Swal from 'sweetalert2';
import Headerapp from './Headerapp.vue';
import router from '@/rutas/rutas';
import { useUsuarios } from '@/stores/usuario';

// Variables reactivas
const nombreteam = ref('');
const Descripcion = ref('');
const numeropeople = ref('');
const capitanteam = ref('');
const requisitos_join = ref('');
const location = ref('');
const logoTeam = ref('');
const documento_cap = ref(0);
const movistore = useUsuarios();
const logoPreview = ref('');
const id_team = ref('');

// Obtener los datos del usuario desde localStorage al cargar el componente
onMounted(() => {
  const datosusuario = movistore.usuario.nombreUsuario;
  const document_cap = movistore.usuario.documento
  console.log(datosusuario);
  if (datosusuario && document_cap) {
    capitanteam.value = movistore.usuario.nombreUsuario; 
    documento_cap.value = movistore.usuario.documento
  }
});
console.log(capitanteam);



const onFileChange = (event) => {
  const file = event.target.files[0];
  if (file) {
    logoTeam.value = file;
    logoPreview.value = URL.createObjectURL(file);
  }
};
const Insertar_team = async () => {
  const formData = new FormData();
  formData.append('nombreteam', nombreteam.value);
  formData.append('Descripcion', Descripcion.value);
  formData.append('numeropeople', numeropeople.value);
  formData.append('requisitos_join', requisitos_join.value);
  formData.append('location', location.value);
  formData.append('documento_cap',documento_cap.value)
  formData.append('capitanteam',capitanteam.value)

  if (logoTeam.value) {
    formData.append('logoteam', logoTeam.value);
  }
    if (!nombreteam.value || !Descripcion.value || !numeropeople.value || numeropeople<1 || numeropeople>12  || !requisitos_join.value || !location.value) {
      Swal.fire({
        icon: 'error',
        title: 'Error',
        text: 'Por favor, completa todos los campos antes de enviar.',
      });
      return;
    }

  try {
    const insertar = await axios.post('http://localhost:8000/Teams', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    console.log(movistore.usuario.equipo_tiene)

    const Equipos = {
      nombreteam: insertar.data.nombreteam,
      Descripcion: insertar.data.Descripcion,
      numeropeople: insertar.data.numeropeople,
      requisitos_join: insertar.data.requisitos_join,
      location: insertar.data.location,
      logoTeam: insertar.data.logoTeam,
      capitanteam: insertar.data.capitanteam,
      documento_cap : insertar.data.documento_cap
    };

   
    console.log('Respuesta del servidor:', insertar);
    localStorage.setItem('Equipos', JSON.stringify(Equipos));

    if (insertar.status == 200) {
      const movistore = useUsuarios();
    
    // Obtener el ID del equipo a eliminar
    const response = await axios.get(`http://127.0.0.1:8000/id_equipo/${movistore.usuario.documento}`);
    const id_delete = response.data.Id_team;

      movistore.setUsuario({
        ...movistore.usuario,
        equipo_tiene: id_delete, // Asigna el ID del equipo recién creado
        esLider: true, // El usuario ahora es líder
      });
      Swal.fire({
        timer: 2000,
        icon: 'success',
        title: 'PERFECTO',
        text: 'Tu Equipo Se ha Creado Correctamente',
      });
      router.push('/equipos');
      console.log(movistore.usuario.equipo_tiene)
    }

    // Limpiar los campos después de enviar el formulario
    nombreteam.value = '';
    Descripcion.value = '';
    numeropeople.value = '';
    capitanteam.value = '';
    requisitos_join.value = '';
    location.value = '';
    logoTeam.value = '';
  } catch (error) {
    console.error(error);
  }
};
</script>


<style scoped>
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

@keyframes bounceClick {
  0% { transform: scale(1); }
  50% { transform: scale(1.1); }
  100% { transform: scale(1); }
}

.crear_equipo_form {
  font-family: 'Trebuchet MS', Arial, sans-serif;
  padding: 1.5rem;
  max-width: 400px;
  background: linear-gradient(135deg, rgba(51, 51, 51, 0.9) 0%, rgba(26, 26, 26, 0.95) 100%);
  border-radius: 12px;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.4);
  text-align: center;
  color: #fff;
  backdrop-filter: blur(6px);
  margin: 10% auto;
  position: relative;
  animation: fadeIn 0.8s ease-out;
}

.crear_equipo_form-title {
  font-size: 26px;
  font-weight: bold;
  margin-bottom: 15px;
  color: #d4af37;
  text-shadow: 0 0 10px rgba(255, 215, 0, 0.8);
}

.crear_equipo_input-container {
  margin-bottom: 15px;
  text-align: left;
}

.crear_equipo_input {
  width: 100%;
  padding: 10px;
  border: 2px solid #d4af37;
  border-radius: 6px;
  font-size: 1rem;
  background: #fff;
  color: #333;
  transition: 0.3s ease-in-out;
}

.crear_equipo_input:focus {
  border-color: #ffd700;
  box-shadow: 0 0 15px rgba(255, 215, 0, 0.8);
  transform: scale(1.02);
}

.contacto_boton {
  background: #d4af37;
  color: #000;
  padding: 12px;
  border: none;
  border-radius: 6px;
  font-size: 1rem;
  font-weight: bold;
  width: 100%;
  cursor: pointer;
  transition: 0.3s ease-in-out;
}

.contacto_boton:hover {
  background: #b8860b;
  box-shadow: 0 0 10px rgba(255, 215, 0, 0.8);
  transform: translateY(-2px);
}

.contacto_boton:active {
  background: #8b6508;
  animation: bounceClick 0.3s ease-in-out;
}

.crear_equipo_input[type="file"] {
  background: transparent;
  border: none;
  padding: 5px;
}

.crear_equipo_input-container label {
  color: #d4af37;
  font-weight: 600;
  display: block;
  margin-bottom: 5px;
}

/* Animación de la vista previa del logo */
@keyframes fadeInScale {
  from {
    opacity: 0;
    transform: scale(0.8);
  }
  to {
    opacity: 1;
    transform: scale(1);
  }
}

.logo-preview {
  text-align: center;
  margin-top: 15px;
}

.logo-preview img {
  max-width: 120px;
  max-height: 120px;
  border-radius: 10px;
  border: 2px solid #d4af37;
  box-shadow: 0 0 15px rgba(218, 165, 32, 0.8);
  animation: fadeInScale 0.5s ease-out;
}
</style>