
<template>
  <header>
    <!-- Header de escritorio -->
    <div class="d-none d-md-block">
      <Headerapp></Headerapp>
    </div>

    <!-- Header para móviles -->
    <div class="d-block d-md-none">
      <headermobile></headermobile>
    </div>
  </header>

  <!-- Forzar actualización del contenido principal cuando cambia equipo_tiene -->
  <div :key="movistore.usuario.equipo_tiene">
    <!-- Mostrar botón y Equipos_container si el usuario no tiene equipo -->
    <div v-if="!movistore.usuario.equipo_tiene">
      <div class="crear-equipo-container">
        <router-link to="/creacionequipo" class="boton-crear">
          + CREA TU EQUIPO
        </router-link>
        <router-link to="/solicitud_teams" class="boton-crear2">
          solicitudes
        </router-link>

      </div>
      <Equipos_container />
    </div>

    <!-- Mostrar equipo_lider si el usuario es líder -->
    <Equipo_lider v-else-if="movistore.usuario.esLider" />

    <!-- Mostrar equipo_miembro si el usuario no es líder pero tiene equipo -->
    <Equipo_miembro v-else />
  </div>
</template>

<script>
import { watch, onMounted, onBeforeUnmount } from "vue";
import { useUsuarios } from "@/stores/usuario";
import Headerapp from "./Headerapp.vue";
import headermobile from "./headermobile.vue";
import Equipo_lider from "./equipo_lider.vue";
import Equipo_miembro from "./equipo_miembro.vue";
import Equipos_container from "./equipos_container.vue";
import axios from "axios";
import { io } from "socket.io-client";
import { useRouter, useRoute } from "vue-router";

export default {
  components: {
    Headerapp,
    headermobile,
    Equipo_lider,
    Equipo_miembro,
    Equipos_container,
  },
  setup() {
    const movistore = useUsuarios();
    const router = useRouter();
    const route = useRoute();

    // --- WebSocket para expulsión ---
    let socket = null;

    onMounted(() => {
      socket = io("http://localhost:9000");
      // Unirse a la sala personal del usuario
      socket.emit("joinRoom", movistore.usuario.documento);
      console.log("Uniéndose a la sala:", movistore.usuario.documento);

      // Listener de expulsión
      socket.on("expulsion", (data) => {
        if (data.documento === movistore.usuario.documento) {
          console.log("Evento de expulsión recibido en equipo.vue:", data);
          movistore.actualizarEquipo(0);
          alert(data.mensaje);
          // Si no está en /equipo, redirige
          if (route.name !== "equipos") {
            router.replace({ name: "equipos" });
          }
        }
      });
    });

    onBeforeUnmount(() => {
      if (socket) socket.disconnect();
    });

    // --- Lógica de líder y watcher original ---
    const verificarLider = async () => {
      if (movistore.usuario.equipo_tiene !== 0) {
        try {
          const response = await axios.get(
            `http://localhost:8000/es_lider/${movistore.usuario.documento}`
          );
          movistore.setUsuario({
            ...movistore.usuario,
            esLider: response.data.esLider,
          });
        } catch (error) {
          console.error("❌ Error al verificar si el usuario es líder:", error);
        }
      }
    };

    verificarLider();

    watch(
  () => movistore.usuario.equipo_tiene,
  (nuevoValor, valorAnterior) => {
    console.log("Watcher equipo_tiene:", valorAnterior, "->", nuevoValor);
  },
  { immediate: true }
);

    return {
      movistore,
    };
  },
};
</script>

<style scoped>
.crear-equipo-container {
  text-align: center;
  margin-bottom: 2rem;
  margin-top: 10rem;
}

.boton-crear,
.boton-crear2 {
  display: inline-block;
  color: black;
  font-weight: bold;
  padding: 1rem 1.5rem;
  border-radius: 12px;
  text-decoration: none;
  font-size: 1rem;
  transition: background 0.3s, transform 0.2s, box-shadow 0.3s;
  border: 2px solid black;
  text-transform: uppercase;
  font-family: 'Audiowide', cursive;
  position: relative;
  overflow: hidden;
  margin-top: 10%;
  max-width: 90%;
  box-sizing: border-box;
  word-wrap: break-word;
}

/* Estilo botón dorado */
.boton-crear {
  background-color: gold;
  box-shadow: 0 4px 10px rgba(255, 215, 0, 0.3);
}

.boton-crear:hover {
  background-color: #d4af37;
  transform: scale(1.1) rotate(-2deg);
  box-shadow: 0 6px 15px rgba(255, 215, 0, 0.7);
}

/* Estilo botón azul */
.boton-crear2 {
  background-color: rgb(0, 213, 255);
  font-size: 0.9rem;
  margin-left: 5%;
  box-shadow: 0 4px 10px rgba(0, 213, 255, 0.3);
}

.boton-crear2:hover {
  background-color: #6137d4;
  transform: scale(1.1) rotate(-2deg);
  box-shadow: 0 6px 15px rgba(0, 213, 255, 0.7);
}

/* Efecto brillo animado */
.boton-crear::before,
.boton-crear2::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: rgba(255, 255, 255, 0.3);
  transform: skewX(-45deg);
  transition: left 0.5s;
}

.boton-crear:hover::before,
.boton-crear2:hover::before {
  left: 100%;
}

/* Contenedor de búsqueda */
.busqueda-container {
  display: flex;
  justify-content: center;
  flex-wrap: wrap;
  margin-bottom: 1rem;
}

/* Responsivo */
@media (max-width: 768px) {
  .boton-crear,
  .boton-crear2 {
    padding: 0.8rem 1.2rem;
    font-size: 0.95rem;
    margin-top: 10%;
    margin-left: 0;
  }

  .crear-equipo-container {
    margin-bottom: 1.5rem;
  }
}

@media (max-width: 480px) {
  .boton-crear,
  .boton-crear2 {
    width: 90%;
    font-size: 0.85rem;
    padding: 0.7rem 1rem;
    margin-top: 1rem;
  }

  .busqueda-container {
    flex-direction: column;
    align-items: center;
  }
}
</style>
