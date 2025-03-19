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
            <li v-for="(i, index) in filtradordeequipos" :key="index" class="tarjeta-equipo">
              <div class="contenido-tarjeta">
                <img :src="getImagenUrl(i.logoTeam)" class="logo-equipo" alt="Logo del equipo" />
                <div class="info-equipo">
                  <h3 class="nombre-equipo">{{ i.nombreteam }}</h3>
                  <p class="texto-secundario"><strong>Capitán:</strong> {{ i.capitanteam }}</p>
                  <p class="texto-secundario"><strong>Ubicación:</strong> {{ i.location }}</p>
                  <p class="texto-secundario descripcion">
                    <strong>Descripción:</strong> {{ i.Descripcion }}
                  </p>
                  <p class="texto-secundario"><strong>Integrantes:</strong> {{ i.numeropeople }}</p>
                  <button @click="unirseEquipo(i.Id_team)">Unirse</button>

                </div>
              </div>
            </li>
          </ul>
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
          console.error("Error al obtener los equipos", error);
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
}

.crear-equipo-container {
  text-align: center;

}

.boton-crear {
  display: inline-block;
  background-color: #4a90e2;
  color: white;
  font-weight: bold;
  padding: 12px 20px;
  border-radius: 8px;
  text-decoration: none;
  transition: 0.3s;
}

.boton-crear:hover {
  background-color: #357abd;
}


.busqueda-container {
  display: flex;
  justify-content: center;
  margin-bottom: 15px;
}

.input-busqueda {
  width: 100%;
  max-width: 400px;
  padding: 10px;
  border-radius: 8px;
  border: 1px solid #ccc;
  outline: none;
  transition: 0.3s;
}

.input-busqueda:focus {
  border-color: #4a90e2;
}

.lista-equipos {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 20px;
  justify-content: center;
  padding: 10px;
}


.tarjeta-equipo {
  background-color: #1e1e1e;
  border-radius: 30px;
  box-shadow: 0 4px 12px rgba(255, 255, 255, 0.15);
  padding: 50px;
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  transition: 0.3s;
  width: 100%;
  margin-top: 5%;
}

.tarjeta-equipo:hover {
  transform: translateY(-5px);
  box-shadow: 0 6px 16px rgba(255, 255, 255, 0.3);
}

.logo-equipo {
  width: 100px;
  height: 100px;
  object-fit: cover;
  border-radius: 50%;
  margin-bottom: 10px;
  border: 3px solid #4a90e2;
}


.info-equipo {
  width: 100%;
}

.nombre-equipo {
  font-size: 1.4rem;
  font-weight: bold;
  color: #ffffff;
  margin-bottom: 5px;
}

.texto-secundario {
  color: #b0b0b0;
  font-size: 0.95rem;
  margin-bottom: 5px;
}

.descripcion {
  font-size: 0.9rem;
  line-height: 1.4;
  color: #d0d0d0;
}

.boton-unirse {
  margin-top: 10px;
  background-color: #38a169;
  color: white;
  font-weight: bold;
  padding: 12px 18px;
  border-radius: 8px;
  border: none;
  cursor: pointer;
  transition: background 0.3s;
  width: 100%;
  max-width: 220px;
}

.boton-unirse:hover {
  background-color: #2f855a;
}


@media (max-width: 768px) {
  .lista-equipos {
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  }
}
</style>