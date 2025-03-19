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
  margin-top: 50%;
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
</style>