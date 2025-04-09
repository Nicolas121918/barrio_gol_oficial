<template>
  <div class="container">
    <div class="contenido">
      <!-- Barra de búsqueda -->
      <div class="busqueda-container" v-if="teams.length > 0">
        <input
          v-model="buscadorteams"
          type="text"
          placeholder="Buscar equipo..."
          class="input-busqueda"
        />
      </div>

      <!-- Lista de equipos -->
      <div class="lista-equipos">
        <ul>
          <li
            v-for="(i, index) in filtradordeequipos"
            :key="index"
            class="tarjeta-equipo"
          >
            <div class="contenido-tarjeta">
              <img
                :src="getImagenUrl(i.logoTeam)"
                class="logo-equipo"
                alt="Logo del equipo"
              />
              <div class="info-equipo">
                <h3 class="nombre-equipo">{{ i.nombreteam }}</h3>
                <p class="texto-secundario">
                  <strong>Capitán:</strong> {{ i.capitanteam }}
                </p>
                <p class="texto-secundario">
                  <strong>Ubicación:</strong> {{ i.location }}
                </p>
                <p class="texto-secundario descripcion">
                  <strong>Descripción:</strong> {{ i.Descripcion }}
                </p>
                <p class="texto-secundario">
                  <strong>Integrantes:</strong> {{ i.numeropeople }}
                  <strong>id:</strong> {{ i.Id_team }}
                </p>
                <button @click="enviarSolicitud(i.Id_team)" class="boton-solicitud">
  Unirse al equipo
</button>
                <button >ver equipo</button>
              </div>
            </div>
          </li>
        </ul>
        <!-- Mensaje si no hay equipos -->
        <div v-if="teams.length === 0" class="mensaje-sin-equipos">
          <p>No hay equipos disponibles aún.</p>
        </div>
      </div>
    </div>
  </div>
</template>
<script>
import { ref, onMounted, computed } from 'vue';
import Swal from 'sweetalert2';
import axios from 'axios';
import { useUsuarios } from '@/stores/usuario';
import Headerapp from './Headerapp.vue';
import Componente from './equipo_lider.vue';

export default {
  components: {
    Headerapp,
    Componente,
  },
  setup() {
    const teams = ref([]);
    const buscadorteams = ref('');
    const usuarios = useUsuarios(); // Usa el store de Pinia
    const movistore = useUsuarios();

    const getImagenUrl = (path) => `http://127.0.0.1:8000/${path}`;
    const enviarSolicitud = async (id_equipo) => {
  try {
    const documento_usuario = movistore.usuario.documento;

    const response = await axios.post(`http://localhost:8000/equipos/${id_equipo}/solicitar_union`, null, {
      params: {
        documento_usuario: documento_usuario
      }
    });

    alert(response.data.mensaje);
  } catch (error) {
    alert("Ocurrió un error al enviar la solicitud.");
    console.error(error);
  }
};
    const fetchTeams = async () => {
      try {
        const response = await axios.get('http://localhost:8000/listarteams');
        teams.value = response.data;
      } catch (error) {
console.error("Error al obtener los equipos:", error);
if (error.response) {
  console.error("Respuesta del servidor:", error.response.data);
  console.error("Código de estado:", error.response.status);
} else if (error.request) { 
  console.error("No hubo respuesta del servidor:", error.request);
} else {
  console.error("Error desconocido:", error.message);
}
}
    };

    const unirseEquipo = async (idEquipo) => {
console.log("ID del equipo recibido:", idEquipo);

if (!idEquipo) {
  Swal.fire("Error", "ID de equipo no válido.", "error");
  return;
}

if (!usuarios.usuario.documento) {
  Swal.fire("Error", "No se encontró el usuario. Inicia sesión.", "error");
  return;
}

try {
  const formData = new FormData();
  formData.append("documento_user", usuarios.usuario.documento);
  formData.append("id_equipo", idEquipo);

  console.log("Datos enviados:", {
    documento_user: usuarios.usuario.documento,
    id_equipo: idEquipo,
  });

  const response = await axios.post("http://localhost:8000/equipos/unirse", formData);

  Swal.fire("¡Éxito!", response.data.mensaje, "success");

  // 🔄 **Actualizar la información del usuario en el store**
  usuarios.setUsuario({
    ...usuarios.usuario,
    equipo_tiene: idEquipo, // Asignar el nuevo equipo
  });

  // 🚀 **Actualizar la lista de equipos sin recargar la página**
  await fetchTeams(); 

} catch (error) {
  console.error("Error en la solicitud:", error.response?.data);
  Swal.fire("Error", error.response?.data?.detail || "No se pudo unir al equipo.", "error");
}
};

    onMounted(fetchTeams);

    const filtradordeequipos = computed(() => {
      if (buscadorteams.value.trim() === "") return teams.value;
      return teams.value.filter(equipo =>
        equipo.nombreteam.toLowerCase().includes(buscadorteams.value.toLowerCase())
      );
    });

    return {
      teams,
      buscadorteams,
      getImagenUrl,
      filtradordeequipos,
      unirseEquipo,
      enviarSolicitud, 
    };
  },
};
</script>
<style scoped>
.container {
  display: flex;
  justify-content: center;
  padding: 2rem;

  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  color: #fff;
  min-width: 1000px;
}

.contenido {
  width: 100%;
  max-width: 1200px;
}

.busqueda-container {
  margin-bottom: 1.5rem;
  text-align: center;
}

.input-busqueda {
  padding: 0.8rem 1.2rem;
  width: 100%;
  max-width: 400px;
  border: 2px solid #aaa;
  border-radius: 1rem;
  outline: none;
  font-size: 1rem;
  background-color: #2b2b2b;
  color: #fff;
  transition: all 0.3s ease;
}

.input-busqueda::placeholder {
  color: #ccc;
}

.input-busqueda:focus {
  border-color: #d4af37;
  box-shadow: 0 0 10px rgba(212, 175, 55, 0.3);
}

.lista-equipos ul {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 1.5rem;
  padding: 0;
  list-style: none;
}

.tarjeta-equipo {
  background: #000000;
  border-radius: 1rem;
  padding: 1.2rem;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
  transition: transform 0.2s ease, box-shadow 0.2s ease;
  border: 1px solid #444;
  border: solid white;
  
}

.tarjeta-equipo:hover {
  transform: translateY(-6px);
  box-shadow: 0 8px 20px rgba(212, 175, 55, 0.3);
  border-color: #d4af37;
}

.contenido-tarjeta {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
}

.logo-equipo {
  width: 90px;
  height: 90px;
  object-fit: cover;
  border-radius: 50%;
  border: 3px solid #d4af37;
  margin-bottom: 1rem;
}

.nombre-equipo {
  font-size: 1.2rem;
  color: #d4af37;
  margin-bottom: 0.5rem;
}

.texto-secundario {
  font-size: 0.9rem;
  color: #ccc;
  margin-bottom: 0.3rem;
}

.descripcion {
  font-style: italic;
  color: #aaa;
}

button {
  background-color: #d4af37;
  border: none;
  color: #000;
  padding: 0.5rem 1rem;
  border-radius: 1rem;
  margin: 0.3rem;
  font-weight: bold;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

button:hover {
  background-color: #b8972d;
}

.mensaje-sin-equipos {
  text-align: center;
  color: #ccc;
  margin-top: 2rem;
}
</style>
