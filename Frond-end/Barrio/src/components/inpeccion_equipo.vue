<template>
  <div class="contenedor-equipo">
    <button class="boton-volver" @click="$router.go(-1)">Volver</button>

    <!-- Encabezado del equipo -->
    <div class="encabezado-equipo" v-if="equipo">
      <img
        :src="getImagenUrl(equipo.logoTeam)"
        alt="Logo equipo"
        class="logo-equipo"
        @click="abrirModalLogo"
      />
      <div>
        <h1 class="titulo-equipo">{{ equipo.nombreteam }}</h1>
        <p class="descripcion-equipo">{{ equipo.Descripcion }}</p>
        <p class="descripcion-equipo">Miembros: {{ cantidadIntegrantes }}</p>
        <button class="boton-galeria" @click="verGaleria(equipo.Id_team)">Ver Galería</button>
      </div>
    </div>

    <!-- Lista de miembros -->
    <div class="lista-miembros" v-if="equipo">
      <!-- Líder -->
      <div class="tarjeta-miembro" v-if="lider" @click="irADetalleMiembro(lider)">
        <img :src="getImagenUrl(lider.logo)" class="imagen-miembro" />
        <p class="nombre-miembro">{{ lider.nombre }}</p>
        <p class="rol-lider">Líder</p>
      </div>

      <!-- Integrantes -->
      <div v-for="(miembro, index) in miembros" :key="index" class="tarjeta-miembro" @click="irADetalleMiembro(miembro)">
        <img :src="getImagenUrl(miembro.logo)" class="imagen-miembro" />
        <p class="nombre-miembro">{{ miembro.nombre }}</p>
        <p class="rol-lider2">Miembro</p>
      </div>
    </div>

    <!-- Modal del Logo -->
   
  </div>
  <div v-if="mostrarModal" class="modal-fondo" @click="cerrarModal">
      <div class="modal-contenido" @click.stop>
        <img v-if="mostrarLogoGrande" :src="getImagenUrl(equipo.logoTeam)" class="imagen-logo-grande" />
      </div>
    </div>
</template>

<script>
import axios from "axios";

export default {
  name: "InspeccionarEquipo",
  data() {
    return {
      equipo: null,
      lider: null,
      miembros: [],
      cantidadIntegrantes: 0,
      mostrarModal: false,
      mostrarLogoGrande: false,
    };
  },
  async mounted() {
    this.obtenerEquipo();
  },
  methods: {
    async obtenerEquipo() {
      try {
        const idEquipo = this.$route.params.id;
        const response = await axios.get(`http://127.0.0.1:8000/equipos/${idEquipo}/info`);
        console.log("Datos recibidos:", response.data);

        this.equipo = response.data.equipo;
        this.lider = response.data.lider || null;
        this.miembros = response.data.miembros || [];
        this.cantidadIntegrantes = response.data.cantidad_integrantes || (this.miembros.length + (this.lider ? 1 : 0));
      } catch (error) {
        console.error("Error obteniendo equipo:", error);
      }
    },
    verGaleria(id) {
    this.$router.push({ name: 'galeria-inspeccionar', params: { id } });
  },
    getImagenUrl(path) {
      return path ? `http://127.0.0.1:8000/${path}` : "https://via.placeholder.com/150";
    },
    abrirModalLogo() {
      this.mostrarLogoGrande = true;
      this.mostrarModal = true;
    },
    cerrarModal() {
      this.mostrarModal = false;
    },
    irADetalleMiembro(miembro) {
      if (!miembro || !miembro.documento) {
        console.warn("El miembro no tiene documento:", miembro);
        return;
      }

      this.$router.push({
        name: "perfiles",
        params: {
          documento: miembro.documento, // Asegúrate de que la API devuelva este campo
        },
      });
    },
  },
};
</script>

<style scoped>
.contenedor-equipo {
  padding: 2rem 3rem;
  background: linear-gradient(135deg, #1a1a1a, #2c2c2c);
  color: #fff;
  max-width: 1000px;
  min-width: 1000px;
  margin: 2rem auto;
  border: 2px solid rgb(255, 255, 255);
  border-radius: 20px;
  box-shadow: 0 0 20px rgba(246, 246, 246, 0.4);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  margin-top: 10%;
}

.contenedor-equipo:hover {
  transform: scale(1.02);
  box-shadow: 0 0 30px rgba(0, 0, 0, 0.6);
}

/* Encabezado del equipo */
.encabezado-equipo {
  display: flex;
  gap: 1.5rem;
  align-items: center;
  border-bottom: 1px solid #444;
  padding-bottom: 1.5rem;
  justify-content: center;
}

.logo-equipo {
  width: 150px;
  height: 150px;
  border-radius: 50%;
  object-fit: cover;
  border: 4px solid gold;
  cursor: pointer;
  box-shadow: 0 0 15px rgba(255, 215, 0, 0.6);
  transition: transform 0.4s ease-in-out;
  animation: pulseBorder 2s infinite;
  position: relative;
  z-index: 1;
}

.logo-equipo::after {
  content: "";
  position: absolute;
  top: -8px;
  left: -8px;
  width: 116px;
  height: 116px;
  border-radius: 50%;
  background: radial-gradient(rgba(255, 215, 0, 0.3), transparent);
  z-index: -1;
  animation: glow 2s infinite ease-in-out;
  opacity: 0.7;
}

.logo-equipo:hover {
  transform: scale(1.15) rotate(3deg);
  box-shadow: 0 0 25px rgba(255, 215, 0, 1), 0 0 45px rgba(255, 223, 0, 0.6);
}

/* Animaciones */
@keyframes pulseBorder {
  0%, 100% {
    border-color: gold;
    box-shadow: 0 0 15px rgba(255, 215, 0, 0.6);
  }
  50% {
    border-color: #ffd700;
    box-shadow: 0 0 25px rgba(255, 215, 0, 0.9);
  }
}

@keyframes glow {
  0%, 100% {
    transform: scale(1);
    opacity: 0.6;
  }
  50% {
    transform: scale(1.2);
    opacity: 1;
  }
}


.titulo-equipo {
  font-size: 2.5rem;
  margin: 0;
  font-weight: bold;
  color: rgb(255, 255, 255);
  padding: 0.5rem 1.5rem;
  border-radius: 12px;
  text-align: center;
  letter-spacing: 1.5px;
  text-shadow: 2px 2px 4px rgba(255, 255, 255, 0.8);
  transition: all 0.4s ease;
  display: inline-block;
  position: relative;
  overflow: hidden;
  -webkit-text-stroke: 1px rgb(8, 8, 8);
  text-shadow: 0 0 10px rgb(255, 208, 0);
}

.titulo-equipo:hover {
  transform: scale(1.05);
  text-shadow: 0 0 10px orange;
}

.titulo-equipo::after {
  content: "";
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(
    120deg,
    rgba(255, 255, 255, 0.2) 0%,
    rgba(255, 255, 255, 0.1) 50%,
    rgba(255, 255, 255, 0.2) 100%
  );
  transition: left 0.8s ease;
  pointer-events: none;
}

.titulo-equipo:hover::after {
  left: 100%;
}


.descripcion-equipo {
  font-size: 1rem;
  margin: 0.2rem 0;
  color: #ccc;
}

.boton-galeria {
  margin-top: 1rem;
  background: linear-gradient(145deg, #1a1a1a, #2e2e2e); /* negro + gris oscuro */
  color: gold;
  font-weight: bold;
  padding: 0.6rem 1.5rem;
  border: 2px solid gold;
  border-radius: 8px;
  cursor: pointer;
  box-shadow: 0 0 10px rgba(255, 215, 0, 0.3);
  transition: all 0.3s ease;
  text-transform: uppercase;
  letter-spacing: 1px;
}

.boton-galeria:hover {
  background: gold;
  color: black;
  box-shadow: 0 0 20px rgba(255, 215, 0, 0.7);
  transform: scale(1.05);
}


/* Lista de miembros */
.lista-miembros {
  display: flex;
  flex-wrap: wrap;
  gap: 1.5rem;
  margin-top: 2rem;
  justify-content: center;
}

.tarjeta-miembro {
  width: 150px;
  background: linear-gradient(160deg, #1a1a1a, #2e2e2e); /* Fondo negro/gris con profundidad */
  padding: 1rem;
  border-radius: 16px;
  text-align: center;
  cursor: pointer;
  transition: all 0.4s ease;
  color: white;
  border: 2px solid rgba(255, 215, 0, 0.4); /* dorado tenue */
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.8);
  position: relative;
  overflow: hidden;
  font-weight: bold;
  letter-spacing: 1px;
  backdrop-filter: blur(2px);
}

.tarjeta-miembro::before {
  content: "";
  position: absolute;
  top: -50%;
  left: -50%;
  width: 200%;
  height: 200%;
  background: radial-gradient(circle, rgba(255, 215, 0, 0.15), transparent 70%);
  transform: rotate(25deg);
  transition: all 0.5s ease;
  z-index: 0;
}

.tarjeta-miembro:hover::before {
  top: -30%;
  left: -30%;
  background: radial-gradient(circle, rgba(255, 215, 0, 0.3), transparent 80%);
}

.tarjeta-miembro:hover {
  transform: scale(1.1);
  border-color: gold;
  box-shadow: 0 0 25px rgba(255, 215, 0, 0.6), 0 0 10px rgba(255, 255, 255, 0.1);
}

.tarjeta-miembro > * {
  position: relative;
  z-index: 1;
}


.imagen-miembro {
  width: 70px;
  height: 70px;
  border-radius: 50%;
  object-fit: cover;
  margin-bottom: 0.5rem;
  border: 3px solid gold;
  box-shadow: 0 0 10px rgba(255, 215, 0, 0.5), 0 0 3px white;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  cursor: pointer;
}

.imagen-miembro:hover {
  transform: scale(1.1);
  box-shadow: 0 0 15px gold, 0 0 5px white;
}

.nombre-miembro {
  font-weight: bold;
  margin: 0;
  color: white;
  font-size: 1.1rem;
  letter-spacing: 0.5px;
  text-transform: uppercase;
  text-shadow: 
    -1px -1px 0 black,
     1px -1px 0 rgb(150, 150, 150),
    -1px  1px 0 black,
     1px  1px 0 black,
     0 0 6px gold;
  background: linear-gradient(to right, #ffffff, #ffd700);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  transition: transform 0.3s ease, text-shadow 0.3s ease;
  white-space: nowrap; /* Evita que el texto se divida en varias líneas */
  overflow: hidden; /* Oculta el texto que no cabe */
  text-overflow: ellipsis; /* Agrega los tres puntos (...) cuando el texto es muy largo */
  max-width: 150px; /* Ajusta el ancho máximo según necesites */
  display: block;
}

.nombre-miembro:hover {
  transform: scale(1.05);
  text-shadow: 
    -1px -1px 0 black,
     1px -1px 0 black,
    -1px  1px 0 black,
     1px  1px 0 black,
     0 0 10px gold,
     0 0 20px #f5c400;
}


.rol-lider {
  font-size: 0.85rem;
  color: black;
  background: linear-gradient(145deg, gold, #f5c400);
  padding: 0.2rem 0.5rem;
  border-radius: 9999px;
  margin-top: 0.4rem;
  font-weight: bold;
  box-shadow: 0 2px 6px rgba(255, 215, 0, 0.4);
  text-transform: uppercase;
  letter-spacing: 0.5px;
  display: inline-block;
  transition: transform 0.3s ease;
}

.rol-lider:hover {
  transform: scale(1.1);
  box-shadow: 0 0 10px rgba(255, 215, 0, 0.6);
}
.rol-lider2{
  font-size: 0.85rem;
  color: rgb(255, 255, 255);
  background: linear-gradient(145deg, rgb(74, 74, 74), #353535);
  padding: 0.2rem 0.5rem;
  border-radius: 9999px;
  margin-top: 0.4rem;
  font-weight: bold;
  box-shadow: 0 2px 6px rgba(119, 119, 119, 0.4);
  text-transform: uppercase;
  letter-spacing: 0.5px;
  display: inline-block;
  transition: transform 0.3s ease;
}

.rol-lider2:hover {
  transform: scale(1.1);
  box-shadow: 0 0 10px rgba(98, 98, 98, 0.6);
}


/* Modal */
.modal-fondo {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.85);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 999;
}

.modal-contenido {
  padding: 2rem;
  border-radius: 10px;
  text-align: center;
  color: white;
  max-width: 90%;
}

.imagen-logo-grande {
  max-width: 400px;
  width: 500px;
  height: 500px;
  border-radius: 1rem;
  border: 3px solid gold;
  box-shadow: 0 0 10px white;
  margin-bottom: 1rem;
}

.boton-volver {
  background-color: black;
  color: gold;
  border: 2px solid gold;
  padding: 0.6rem 1.2rem;
  border-radius: 8px;
  font-weight: bold;
  cursor: pointer;
  font-size: 1rem;
  transition: all 0.3s ease;
  box-shadow: 0 0 8px rgba(255, 215, 0, 0.4);
}

.boton-volver:hover {
  background-color: gold;
  color: black;
  box-shadow: 0 0 12px rgba(255, 215, 0, 0.8);
  transform: scale(1.05);
}

</style>
