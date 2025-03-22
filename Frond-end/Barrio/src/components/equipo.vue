<template>
  <header>
    <headerapp></headerapp>
  </header>
 
  <!-- Fase 1: No tiene equipo -->
  <div v-if="movistore.usuario.equipo_tiene === 0">
    <div class="crear-equipo-container">
      <router-link to="/creacionequipo" class="boton-crear">+ CREA TU EQUIPO</router-link>
    </div>
    <div>
      <Equipos_container></Equipos_container>
    </div>
  </div>

  <!-- Fase 2: Es líder -->
  <div v-else-if="movistore.usuario.esLider">
    <equipo_lider></equipo_lider>
  </div>

  <!-- Fase 3: Es miembro -->
  <div v-else>
    <equipo_miembro></equipo_miembro>
  </div>
</template>

<script>

import { useUsuarios } from '@/stores/usuario';
import Headerapp from './Headerapp.vue';
import Equipo_lider from './equipo_lider.vue';
import Equipo_miembro from './equipo_miembro.vue';
import axios from 'axios';
import Equipos_container from './equipos_container.vue';

export default {
  components: {
    Headerapp,
    Equipo_lider,
    Equipo_miembro,
    Equipos_container,
  },
  setup() {
    const movistore = useUsuarios();

    console.log("✅ Usuario encontrado:", movistore.usuario);

    // Si el usuario tiene equipo, verificar si es líder
    if (movistore.usuario.equipo_tiene !== 0) {
      axios.get(`http://localhost:8000/es_lider/${movistore.usuario.documento}`)
        .then(response => {
          movistore.setUsuario({
            ...movistore.usuario,
            esLider: response.data.esLider  // ✅ Se actualiza con la acción
          });
        })
        .catch(error => {
          console.error("❌ Error al verificar si el usuario es líder:", error);
        });
    }

    return {
      movistore,
    };
  }
};
</script>


<style scoped>
.crear-equipo-container {
  text-align: center;
  margin-bottom: 20px;
}

.boton-crear {
  display: inline-block;
  background-color: gold;
  color: black;
  font-weight: bold;
  padding: 15px 25px;
  border-radius: 12px;
  text-decoration: none;
  font-size: 1.2rem;
  transition: background 0.3s, transform 0.2s, box-shadow 0.3s;
  border: 2px solid black;
  box-shadow: 0 4px 10px rgba(255, 215, 0, 0.3);
  text-transform: uppercase;
  font-family: 'Audiowide', cursive;
  position: relative;
  overflow: hidden;
  margin-top: 30%;
}

.boton-crear::before {
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

.boton-crear:hover::before {
  left: 100%;
}

.boton-crear:hover {
  background-color: #d4af37;
  transform: scale(1.1) rotate(-2deg);
  box-shadow: 0 6px 15px rgba(255, 215, 0, 0.7);
}

.busqueda-container {
  display: flex;
  justify-content: center;
  margin-bottom: 15px;
}

</style>