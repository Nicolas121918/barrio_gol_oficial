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
    
    <form @submit.prevent="enviarFormulario" enctype="multipart/form-data" class="formulario">
      <div class="volver">
  <router-link to="/torneos" class="btn-volver">
    Volver
  </router-link>
</div>

      <h2 class="tiit">Crear Torneo</h2>

      <label>Nombre del torneo:</label>
      <input v-model="form.nombre" type="text" required />

      <div>
        <br>
        <label>Tipo de torneo:</label>
        <br>

<select v-model="form.tipo_torneo" required>
  <option  value="">Seleccione una opción</option>
  <option value="personalizado">Personalizado</option>
  <option   value="relampago">Relámpago</option>
  <option  value="todos">Todos contra todos</option>
  
</select>

    <div v-if="form.tipo_torneo">
      <p v-if="form.tipo_torneo === 'relampago'">
        Torneo rápido donde los jugadores se eliminan en rondas directas.
      </p>
      <p v-else-if="form.tipo_torneo === 'todos'">
        Cada jugador compite contra todos los demás. Gana quien tenga más victorias.
      </p>
      <p v-else-if="form.tipo_torneo === 'personalizado'">
        Tú defines las reglas del torneo: rondas, puntos, enfrentamientos, etc.
      </p>
    </div>
  </div>


  <label>Tipo de fútbol:</label>
<select v-model="form.tp_futbol" required>
  <option disabled value="">Seleccione un tipo de fútbol</option>
  <option value="Fútbol 11">Fútbol 11 (cancha grande)</option>
  <option value="Fútbol 7">Fútbol 7 (cancha mediana)</option>
  <option value="Fútbol 5">Fútbol 5 (cancha pequeña)</option>
  <option value="Fútbol Sala">Fútbol Sala (interior, reglamento FIFA)</option>
  <option value="Playa">Fútbol Playa (arena)</option>
</select>

  


      <label>Fecha de inicio:</label>
      <input v-model="form.fecha_inicio" type="date" required
      :min="fecha"  max="2026-01-01"/>

    

      <label>Ubicación:</label>
<div style="display: flex; gap: 8px;">
  <input
  v-model="form.ubicacion"
  type="text"
  required
  style="flex: 1;"
  readonly
/>
</div>
<button type="button" @click="usarUbicacionActual">Obtener ubicación actual</button>

      <label>¿Cómo llegar?:</label>
      <input v-model="form.como_llegar" type="text" required />

      <label>Lugar:</label>
<input
  v-model="form.lugar"
  type="text"
  list="ciudades"
  required
  @change="validarCiudad"
/>

<datalist id="ciudades">
  <option v-for="ciudad in listaCiudades" :key="ciudad" :value="ciudad" />
</datalist>

<label>Número de participantes:</label>
<input
  v-model.number="form.numero_participantes"
  type="number"
  min="3"
  required
/>
<p v-if="form.numero_participantes > 0 && form.numero_participantes < 3" style="color: red;">
  El número mínimo de participantes es 3.
</p>


      <label>Premiación:</label>
      <input v-model="form.premiacion" type="text" required />
      <label for="reglas">Reglas:</label>
<textarea
  id="reglas"
  v-model="form.reglas"
  required
  rows="6"
  placeholder="Escribe aquí todas las reglas del torneo..."
  style="
    width: 100%;
    resize: none;
    padding: 10px;
    font-size: 1rem;
    border-radius: 8px;
    border: 1px solid #ccc;
    outline: none;
    transition: border-color 0.3s ease;
    box-shadow: 2px 2px 5px rgba(0,0,0,0.05);
  "
  @focus="(e) => e.target.style.borderColor = '#3b82f6'"
  @blur="(e) => e.target.style.borderColor = '#ccc'"
></textarea>


      <label>Categorías:</label>
<select v-model="form.categorias" required>
  <option disabled value="">Seleccione una categoría</option>
  <option value="Niños">Niños (menores de 13 años)</option>
  <option value="Adolescentes">Adolescentes (14 a 18 años)</option>
  <option value="Adultos">Adultos (mayores de 19 años)</option>
  <option value="Mixto">Mixto (todas las edades)</option>
</select>


<label>Costo de inscripción:</label>
<input
  :value="formatearPesos(form.costo_inscripcion)"
  @input="actualizarCosto($event)"
  type="text"
  inputmode="numeric"
  required
/><label>Imagen de la cancha:</label>
<input type="file" @change="mostrarVistaPrevia1" />
<img v-if="imagenPrevia1" :src="imagenPrevia1" style="width: 150px;height: 150px; margin-top: 10px;border: solid white 1px;" />

<label>Logo del torneo:</label>
<input type="file" @change="mostrarVistaPrevia2" />
<img v-if="imagenPrevia2" :src="imagenPrevia2" style="width: 150px;height: 150px;border: solid white 1px; margin-top: 10px;" />

<div  style="display: flex; align-items: center; gap: 12px; margin-top: 16px;">


  <button type="submit">Crear Torneo</button>


  <div class="vamiss" style="font-size: 0.9rem; margin-top: 10px;">
  <strong class="verde">¡Accede gratis por tiempo limitado!</strong><br>
  <span style="display: block; margin-top: 4px;">
    Sé parte de los primeros creadores de torneos <strong class="num">${{ comisionEstimado.toLocaleString() }} COP</strong> <br>
    <em style="font-size: 0.8rem;">(Precio estimado en el futuro)</em>
  </span>
</div>

</div>


      <transition name="fade">
  <div v-if="mensaje === '¡Torneo creado exitosamente!'" class="modal">
    <div class="modal-contenido">
      <svg xmlns="http://www.w3.org/2000/svg" class="icono-check" fill="none" viewBox="0 0 24 24" stroke="green" stroke-width="2">
        <path stroke-linecap="round" stroke-linejoin="round" d="M5 13l4 4L19 7" />
      </svg>
      <h3>{{ mensaje }}</h3>
      <button class="btn-aceptar" @click="cerrarModal">Aceptar</button>
    </div>
  </div>
</transition>
    </form>
  </template>
  <script setup>
  const fecha = ref('');
  import { onBeforeUnmount } from 'vue';
  import { computed } from 'vue';
  import 'leaflet/dist/leaflet.css';
  import { ref } from 'vue';
  import axios from 'axios';
  import { useUsuarios } from '@/stores/usuario';
  import { useRouter } from 'vue-router';
  import listaCiudadesJson from '../assets/ciudades.json'
  import Headerapp from './Headerapp.vue';
  import headermobile from '@/components/headermobile.vue';
const listaCiudades = ref(listaCiudadesJson)
  const imagenPrevia1 = ref("");
const imagenPrevia2 = ref("");
const mostrarVistaPrevia1 = (event) => {
  const archivo = event.target.files[0];
  if (archivo && archivo.type.startsWith('image/')) {
    const lector = new FileReader();
    lector.onload = () => {
      imagenPrevia1.value = lector.result;
    };
    lector.readAsDataURL(archivo);
    form.value.imagen_cancha = archivo; // <-- Aquí se guarda en el formulario
  } else {
    imagenPrevia1.value = null;
    form.value.imagen_cancha = null;
  }
};

const mostrarVistaPrevia2 = (event) => {
  const archivo = event.target.files[0];
  if (archivo && archivo.type.startsWith('image/')) {
    const lector = new FileReader();
    lector.onload = () => {
      imagenPrevia2.value = lector.result;
    };
    lector.readAsDataURL(archivo);
    form.value.torneo_logo = archivo; // <-- Aquí también
  } else {
    imagenPrevia2.value = null;
    form.value.torneo_logo = null;
  }
};
 // Actualiza la fecha cada segundo
 const interval = setInterval(() => {
  const now = new Date();
  // Formateamos a YYYY-MM-DD
  const año = now.getFullYear();
  const mes = String(now.getMonth() + 1).padStart(2, '0');
  const dia = String(now.getDate()).padStart(2, '0');
  fecha.value = `${año}-${mes}-${dia}`;
}, 1000);

onBeforeUnmount(() => {
  clearInterval(interval);
});

  const router = useRouter();
  const usuariosStore = useUsuarios();
function validarCiudad() {
  if (!listaCiudades.value.includes(form.value.lugar)) {
    alert("Por favor selecciona una ciudad válida de la lista.")
    form.value.lugar = ''
  }
}
  const form = ref({
    nombre: '',
    tipo_torneo: '',
    tp_futbol: '',
    fecha_inicio: '',
    ubicacion: '',
    como_llegar: '',
    lugar: '',
    numero_participantes: 0,
    premiacion: '',
    reglas: '',
    categorias: '',
    costo_inscripcion: 0.0,
    imagen_cancha: null,
    torneo_logo: null,
  });

  const mensaje = ref('');

  const handleFileChange = (event, tipo) => {
    const file = event.target.files[0];
    form.value[tipo] = file;
  };
  const cerrarModal = () => {
    router.push('/torneos'); // Redirigir a la página de torneos
  };
function usarUbicacionActual() {
  if (!navigator.geolocation) {
    alert("La geolocalización no es compatible con este navegador.");
    return;
  }

  navigator.geolocation.getCurrentPosition(
    (position) => {
      const lat = position.coords.latitude.toFixed(6);
      const lon = position.coords.longitude.toFixed(6);
      form.value.ubicacion = `${lat}, ${lon}`; // <- Aquí está el cambio
    },
    (error) => {
      console.error("Error obteniendo ubicación:", error);
      alert("No se pudo obtener la ubicación. Asegúrate de permitir el acceso.");
    }
  );
}
const formatearPesos = (valor) => {
  if (!valor) return '';
  return new Intl.NumberFormat('es-CO').format(valor);
};
const comisionEstimado = computed(() => {
  const total = form.value.costo_inscripcion * form.value.numero_participantes;
  return Math.floor(total * 0.01); // 1% del total
});


// Convertir string con puntos a número real
const actualizarCosto = (event) => {
  const soloNumeros = event.target.value.replace(/\D/g, ''); // Quita todo menos dígitos
  const numero = parseInt(soloNumeros, 10);
  form.value.costo_inscripcion = isNaN(numero) ? 0 : numero;
};

// endpoint para crear torneo   
const enviarFormulario = async () => {
  console.log("🟡 Función enviarFormulario ejecutada");

  const formData = new FormData();
  for (const key in form.value) {
    if (form.value[key] !== null) {
      formData.append(key, form.value[key]);
    }
  }
  formData.append("documento_creador", usuariosStore.usuario.documento);

  try {
    const response = await axios.post("http://127.0.0.1:8000/crearTorneo", formData);
    console.log("🟢 Formulario enviado correctamente:", response);
    mensaje.value = "¡Torneo creado exitosamente!";
  } catch (error) {
    console.log("🔴 Error al enviar el formulario:", error);
    mensaje.value = "Hubo un error al crear el torneo.";
  }
};

  
  
  </script>

<style scoped>
select {
  padding: 10px;
  border-radius: 8px;
  border: 1px solid #ccc;
  font-size: 16px;
  background-color: #000 ;
  color: white;
  margin-bottom: 15px;
}
.formulario {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  background-color: #121212;
  color: #fff;
  padding: 2rem;
  border-radius: 12px;
  max-width: 500px;
  margin: 30% auto ;
  box-shadow: 0 0 20px rgba(218, 165, 32, 0.3);
}

h2 {
  color: gold;
  text-align: center;
  font-size: 2rem;
  margin-bottom: 1rem;
  text-shadow: 1px 1px #000;
}

label {
  color: #ccc;
  font-weight: 600;
}

input[type="text"],
input[type="date"],
input[type="number"],
input[type="file"] {
  padding: 0.6rem;
  border-radius: 8px;
  border: 1px solid #333;
  background-color: #1f1f1f;
  color: white;
  transition: border 0.2s, background-color 0.2s;
}

input:focus {
  border-color: gold;
  outline: none;
  background-color: #2a2a2a;
}

button {
  background-color: gold;
  color: black;
  font-weight: bold;
  padding: 0.7rem;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: background-color 0.3s, transform 0.2s;
}

button:hover {
  background-color: #d4af37;
  transform: scale(1.05);
}

.mensaje {
  color: #00ff99;
  font-weight: bold;
  text-align: center;
}

fade-enter-active, .fade-leave-active {
  transition: opacity 0.5s ease;
}
.fade-enter-from, .fade-leave-to {
  opacity: 0;
}
.fade-enter-to, .fade-leave-from {
  opacity: 1;
}

.modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.6);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-contenido {
  background: #fff;
  padding: 30px 40px;
  border-radius: 20px;
  text-align: center;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.25);
  max-width: 400px;
  animation: slideIn 0.4s ease;
}

@keyframes slideIn {
  from {
    transform: translateY(-30px);
    opacity: 0;
  }
  to {
    transform: translateY(0);
    opacity: 1;
  }
}

.modal-contenido h3 {
  font-size: 20px;
  margin-bottom: 20px;
  color: #333;
}

.btn-aceptar {
  padding: 10px 20px;
  background-color: #4caf50;
  border: none;
  border-radius: 8px;
  color: white;
  font-weight: bold;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.btn-aceptar:hover {
  background-color: #45a049;
}

.icono-check {
  width: 50px;
  height: 50px;
  margin-bottom: 15px;
}
.volver {
  text-align: center;
  margin-top: 20px;
  display: flex;
  align-items: end;
}

.btn-volver {
  display: inline-block;
  background-color: #000000; /* Negro */
  color: #FFD700; /* Dorado */
  font-size: 16px;
  padding: 10px 20px;
  border: 2px solid #FFD700; /* Borde dorado */
  border-radius: 5px;
  cursor: pointer;
  text-decoration: none; /* Elimina el subrayado */
  transition: background-color 0.3s, color 0.3s, border-color 0.3s; /* Transiciones suaves */
}

.btn-volver:hover {
  background-color: #FFD700; /* Fondo dorado al pasar el mouse */
  color: #000000; /* Texto negro al pasar el mouse */
  border-color: #000000; /* Borde negro al pasar el mouse */
}

.btn-volver:focus {
  outline: none; /* Elimina el borde al hacer foco */
}
.verde {
  color: #fffb00;
  font-weight: bold;
}

.num {
  text-decoration: line-through;
  color: #ff7f50;
  font-weight: bold;
}

.vamiss{
  max-width: 300px;
}
.tiit{
  color: #d4af37;
  font-family:Georgia, 'Times New Roman', Times, serif;
}

</style>