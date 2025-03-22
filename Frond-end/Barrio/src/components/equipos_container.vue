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
                </p>
                <button @click="unirseEquipo(i.Id_team)">Unirse</button>
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

      const getImagenUrl = (path) => `http://127.0.0.1:8000/${path}`;

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
      };
    },
  };
  </script>
  <style scoped> 
  .container {
    display: flex;
    justify-content: center;
    padding: 5%;
  
  }
  
  .contenido {
    width: 100%;
    max-width: 1200px;
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
    gap: 20px;
   
  }
  
  .busqueda-container {
    display: flex;
    justify-content: center;
    margin-bottom: 20px;
    width: 100%;
  }
  
  .input-busqueda {
    width: 100%;
    max-width: 400px;
    padding: 12px;
    border-radius: 8px;
    border: 2px solid gold;
    background-color: #1e1e1e;
    color: white;
    outline: none;
    transition: border-color 0.3s, box-shadow 0.3s;
  }
  
  .input-busqueda:focus {
    border-color: #d4af37;
    box-shadow: 0 0 10px rgba(255, 215, 0, 0.5);
  }
  
  .lista-equipos {
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
    gap: 20px;
    width: 100%;
  }
  
  .tarjeta-equipo {
    background-color: #1e1e1e;
    border-radius: 20px;
    box-shadow: 0 4px 12px rgba(255, 215, 0, 0.2);
    padding: 30px;
    display: flex;
    flex-direction: column;
    align-items: center;
    text-align: center;
    transition: transform 0.3s, box-shadow 0.3s;
    width: 320px;
    border: 3px solid gold;
    margin-bottom: 10%;
  }
  
  .tarjeta-equipo:hover {
    transform: translateY(-8px);
    box-shadow: 0 0 20px white;
  }
  
  .logo-equipo {
    width: 120px;
    height: 120px;
    object-fit: cover;
    border-radius: 50%;
    margin-bottom: 15px;
    border: 4px solid gold;
  }
  
  .nombre-equipo {
    font-size: 1.6rem;
    font-weight: bold;
    color: gold;
    margin-bottom: 10px;
  }
  
  .texto-secundario {
    color: #b0b0b0;
    font-size: 1rem;
    margin-bottom: 8px;
  }
  
  .descripcion {
    font-size: 0.95rem;
    line-height: 1.5;
    color: #d0d0d0;
  }
  
  button {
    margin-top: 15px;
    background-color: gold;
    color: black;
    font-weight: bold;
    padding: 12px 20px;
    border-radius: 10px;
    border: none;
    cursor: pointer;
    transition: background 0.3s, transform 0.2s;
    width: 100%;
    max-width: 240px;
  }
  
  button:hover {
    background-color: #d4af37;
    transform: scale(1.05);
  }
  
  @media (max-width: 768px) {
    .lista-equipos {
      flex-direction: column;
      align-items: center;
    }
  }
  
  .mensaje-sin-equipos {
  text-align: center;
  margin-top: 30px;
  color: #777;
  font-size: 1.2rem;
}

  </style>