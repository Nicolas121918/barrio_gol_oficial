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
  <div class="solicitudes-container">
    <!-- Botón de Volver -->
    <router-link to="/equipos" class="btn-volver">
      Volver
    </router-link>

    <h2 class="titulo-solicitudes">Solicitudes de Invitación</h2>
    <small>Las solicitudes enviadas hace más de un mes serán eliminadas automáticamente por el sistema.</small>

    <!-- Si no hay solicitudes -->
    <div v-if="solicitudes.length === 0" class="sin-solicitudes">
      <p>No tienes solicitudes pendientes.</p>
    </div>

    <!-- Lista de solicitudes -->
    <div v-else class="lista-solicitudes">
      <div
        v-for="(solicitud, index) in solicitudes"
        :key="index"
        class="solicitud-card"
      >
        <img :src="solicitud.logo" alt="Logo del equipo" class="logo-equipo" />
        <div class="info-equipo">
          <h3>{{ solicitud.nombreEquipo }}</h3>
          <p>Fecha de envío: {{ solicitud.fecha }}</p>
        </div>
        <div class="acciones-solicitud">
          <button @click="verEquipo(solicitud)">Ver equipo</button>
          <button class="btn-aceptar" @click="aceptarSolicitud(solicitud)">Aceptar</button>
          <button class="btn-rechazar" @click="rechazarSolicitud(solicitud)">Rechazar</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import Headerapp from "./Headerapp.vue";
import headermobile from "./headermobile.vue";
export default {
  components: {
    Headerapp,
    headermobile,
  },
  name: "SolicitudesInvitacion",
  data() {
    return {
      solicitudes: [
        {
          nombreEquipo: "Los Titanes",
          fecha: "2025-04-18",
          logo: "https://via.placeholder.com/60",
        },
        {
          nombreEquipo: "Dragones FC",
          fecha: "2025-04-17",
          logo: "https://via.placeholder.com/60",
        },
      ],
    };
  },
  methods: {
    verEquipo(solicitud) {
      console.log("Ver equipo:", solicitud);
      // Aquí puedes redirigir al perfil del equipo
    },
    aceptarSolicitud(solicitud) {
      console.log("Aceptada:", solicitud);
      // Lógica para aceptar
    },
    rechazarSolicitud(solicitud) {
      console.log("Rechazada:", solicitud);
      // Lógica para rechazar
    },
  },
};
</script>


<style scoped>


.solicitudes-container {
  font-family: 'Arial', sans-serif;
  padding: 20px;
  background-color: #141414;
  color: #fff;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
  margin-top: 30%;
}

.titulo-solicitudes {
  text-align: center;
  font-size: 1.8rem;
  color: #d4af37; /* Dorado suave */
  margin-bottom: 25px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 1px;
}

.btn-volver {
  display: inline-block;
  background-color: #d4af37; /* Dorado */
  color: #1f1f1f;
  padding: 8px 16px;
  text-decoration: none;
  border-radius: 4px;
  margin-bottom: 20px;
  font-size: 1rem;
  font-weight: 600;
  transition: background-color 0.4s ease, transform 0.3s ease, box-shadow 0.3s ease;
}

.btn-volver:hover {
  background-color: #b58c2c;
  transform: translateY(-4px);
  box-shadow: 0 8px 15px rgba(0, 0, 0, 0.2);
}

.sin-solicitudes {
  text-align: center;
  color: #ccc;
}

.sin-solicitudes p {
  font-size: 1rem;
}

.lista-solicitudes {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.solicitud-card {
  background-color: #333;
  border-radius: 8px;
  padding: 12px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  transition: transform 0.3s ease, box-shadow 0.4s ease, background-color 0.3s ease;
}

.solicitud-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 12px 25px rgba(0, 0, 0, 0.3);
  background-color: #444; /* Fondo ligeramente más claro al hacer hover */
  border: solid 1px;
}

.logo-equipo {
  width: 45px;
  height: 45px;
  border-radius: 50%;
  margin-right: 15px;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.logo-equipo:hover {
  transform: scale(1.2); /* Aumento más notorio */
  box-shadow: 0 0 10px 2px #d4af37; /* Brillo dorado al hacer hover */
}

.info-equipo {
  flex-grow: 1;
}

.info-equipo h3 {
  color: #fff;
  font-size: 1.1rem;
  margin-bottom: 5px;
  font-weight: 600;
}

.info-equipo p {
  color: #bbb;
  font-size: 1rem;
}

.acciones-solicitud {
  display: flex;
  gap: 10px;
}

.acciones-solicitud button {
  padding: 8px 14px;
  border-radius: 4px;
  border: none;
  cursor: pointer;
  font-size: 1rem;
  transition: all 0.4s ease;
  font-weight: 600;
}

.btn-aceptar {
  background-color: #28a745;
  color: #fff;
  border: 2px solid #28a745;
}

.btn-aceptar:hover {
  background-color: #218838;
  border-color: #218838;
  transform: scale(1.1);
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.3);
}

.btn-rechazar {
  background-color: #dc3545;
  color: #fff;
  border: 2px solid #dc3545;
}

.btn-rechazar:hover {
  background-color: #c82333;
  border-color: #c82333;
  transform: scale(1.1);
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.3);
}

.acciones-solicitud button:active {
  transform: scale(0.98); /* Efecto de presionar el botón */
}




/* Dispositivos móviles pequeños (teléfonos) */
@media (max-width: 576px) {
  .solicitudes-container {
    margin-top: 20%;
    padding: 15px;
  }

  .titulo-solicitudes {
    font-size: 1.4rem;
  }

  .btn-volver {
    width: 100%;
    text-align: center;
    padding: 10px;
  }

  .solicitud-card {
    flex-direction: column;
    align-items: flex-start;
  }

  .logo-equipo {
    width: 40px;
    height: 40px;
  }

  .info-equipo h3 {
    font-size: 1rem;
  }

  .info-equipo p {
    font-size: 0.9rem;
  }

  .acciones-solicitud {
    width: 100%;
    justify-content: space-between;
  }

  .acciones-solicitud button {
    flex: 1;
    font-size: 0.9rem;
    padding: 8px;
  }
}

/* Tablets y móviles grandes */
@media (min-width: 577px) and (max-width: 768px) {
  .solicitudes-container {
    margin-top: 15%;
    padding: 18px;
  }

  .titulo-solicitudes {
    font-size: 1.6rem;
  }

  .solicitud-card {
    flex-direction: column;
    align-items: flex-start;
  }

  .acciones-solicitud {
    justify-content: flex-start;
    flex-wrap: wrap;
    gap: 10px;
  }

  .acciones-solicitud button {
    font-size: 0.95rem;
  }
}

/* Pantallas medianas (laptops pequeñas) */
@media (min-width: 769px) and (max-width: 1024px) {
  .solicitudes-container {
    margin-top: 30%;
  }

  .titulo-solicitudes {
    font-size: 1.8rem;
  }

  .logo-equipo {
    width: 45px;
    height: 45px;
  }
}


</style>
