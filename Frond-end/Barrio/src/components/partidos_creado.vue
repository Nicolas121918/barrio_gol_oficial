
<template>
  <button @click="$router.push({ name: 'torneos' })" class="boton-volver">Volver</button>
  <div class="container">
    
    <!-- PARTIDOS EN ESPERA -->
    <div class="partidos-section">
      <h2 class="title">Partidos en Espera</h2>
      <div v-if="partidosEnEspera.length">
        <div v-for="partido in partidosEnEspera" :key="partido.id" class="card">
          <img
            :src="partido.logomatch || 'https://via.placeholder.com/100x100?text=Sin+Logo'"
            alt="logo"
            class="logo"
            @click="ampliarLogo(partido.logomatch || 'https://via.placeholder.com/100x100?text=Sin+Logo')"
          />
          <div class="info">
            <h3 class="tit">{{ partido.name }}</h3>
            <p>{{ partido.tipo_futbol }}</p>
            <p>{{ partido.dia }} - {{ partido.hora }}</p>
            <p>Apuesta: {{ formatoPesos(partido.apuesta) }}</p>
          </div>
          <div class="acciones">
            <button @click="verDetalle(partido)" class="btn-detalle">Ver Contenido</button>
            <button class="btn-detalle2" @click="irAComponente(partido.id_Partido)">Ingresar</button>
          </div>
        </div>
      </div>
      <p v-else class="sin-partidos">No hay partidos en espera disponibles.</p>
    </div>

    <!-- PARTIDOS FINALIZADOS -->
    <div class="partidos-section">
      <h2 class="title">Partidos Finalizados</h2>
      <div v-if="partidosFinalizados.length">
        <div v-for="partido in partidosFinalizados" :key="partido.id" class="card">
          <img
            :src="partido.logo || partido.logomatch || 'https://via.placeholder.com/100x100?text=Sin+Logo'"
            alt="logo"
            class="logo"
            @click="ampliarLogo(partido.logo || partido.logomatch || 'https://via.placeholder.com/100x100?text=Sin+Logo')"
          />
          <div class="info">
            <h3 class="tit">{{ partido.name }}</h3>
            <p>{{ partido.tipo_futbol }}</p>
            <p>{{ partido.dia }} - {{ partido.hora }}</p>
            <p>Apuesta: {{ formatoPesos(partido.apuesta) }}</p>
          </div>
          <div class="acciones">
            <button @click="verDetalle(partido)" class="btn-detalle">Ver Contenido</button>
            <button class="btn-detalle2" @click="irAComponente3(partido.id_Partido)">Ver Resultado</button>
            
          </div>
        </div>
      </div>
      <p v-else class="sin-partidos">No hay partidos finalizados disponibles.</p>
    </div>

    <!-- MODAL LOGO AMPLIADO -->
    <div v-if="logoAmpliado" class="modal-img" @click="logoAmpliado = false">
      <img :src="logoSrc" alt="Logo grande" />
    </div>

    <!-- MODAL DETALLE -->
    <div v-if="modalActivo" class="modal-overlay" @click.self="modalActivo = false">
      <div class="modal">
        <button class="cerrar" @click="modalActivo = false">X</button>
        <h2>{{ partidoSeleccionado.name }}</h2>
        <p><strong>Fecha y Hora:</strong> {{ partidoSeleccionado.dia }} - {{ partidoSeleccionado.hora }}</p>
        <p><strong>Apuesta:</strong> {{ formatoPesos(partidoSeleccionado.apuesta) }}</p>
        <p><strong>Modalidad:</strong> {{ partidoSeleccionado.tipo_futbol || 'Fútbol 11' }}</p>
        <p><strong>Reglas:</strong> {{ partidoSeleccionado.reglas || 'Reglas estándar del torneo' }}</p>
        <p><strong>Cómo llegar:</strong> {{ partidoSeleccionado.como_llegar || 'Dirección no especificada' }}</p>

        <img
          v-if="partidoSeleccionado.imagenCancha"
          :src="partidoSeleccionado.imagenCancha"
          alt="Cancha"
          class="imagen-cancha"
          @click="imagenAmpliada = true"
        />

        <div v-if="imagenAmpliada" class="modal-img" @click="imagenAmpliada = false">
          <img
            v-if="partidoSeleccionado.imagenCancha"
            :src="partidoSeleccionado.imagenCancha || 'https://via.placeholder.com/300x200?text=Sin+Imagen'"
            alt="Cancha"
            class="imagen-cancha"
          />
        </div>

        <p><strong>Ubicación:</strong> {{ partidoSeleccionado.ubicacionpartido || 'Disponible en Google Maps' }}</p>
        <a
          class="btn-detalle2"
          :href="`https://www.google.com/maps/search/?api=1&query=${encodeURIComponent(partidoSeleccionado.ubicacion)}`"
          target="_blank"
          v-if="partidoSeleccionado.ubicacion"
        >
          Ir a ubicación
        </a>
      </div>
    </div>
  </div>
</template>

<script>
import { onMounted, ref } from 'vue';
import axios from 'axios';
import { useUsuarios } from '@/stores/usuario';
import { useRouter } from 'vue-router';

export default {
  setup() {
    const router = useRouter();
    const usuariosStore = useUsuarios();
    const partidosEnEspera = ref([]);
    const partidosFinalizados = ref([]);
    const modalActivo = ref(false);
    const partidoSeleccionado = ref(null);
    const imagenAmpliada = ref(false);
    const logoAmpliado = ref(false);
const logoSrc = ref('');

    const URL_BASE = "http://127.0.0.1:8000/";

    // Agrega el prefijo de URL si existe la imagen
    const agregarURL = (ruta) => ruta ? `${URL_BASE}${ruta}` : null;

    const verDetalle = (partido) => {
      partidoSeleccionado.value = partido;
      modalActivo.value = true;
    };
    const ampliarLogo = (src) => {
  logoSrc.value = src;
  logoAmpliado.value = true;
};

const irAComponente = (idPartido) => {
  router.push({ name: 'sala_partidos', params: { id: idPartido } });
};
const irAComponente3 = (idPartido) => {
  router.push({ name: 'ganador_partido', params: { id: idPartido } });
};

    const irAComponente2 = () => {
      window.location.href = "/ganador_partido";
    };
    const formatoPesos = (valor) => {
  if (!valor) return '0';
  return new Intl.NumberFormat('es-CO').format(valor);
};

    onMounted(async () => {
      const documento = usuariosStore.usuario?.documento;
      if (!documento) {
        console.warn("No se encontró el documento del usuario.");
        return;
      }

      try {
        const resEspera = await axios.get(`${URL_BASE}partidos_en_espera/${documento}`);
        partidosEnEspera.value = resEspera.data.map(partido => ({
          ...partido,
          logomatch: agregarURL(partido.logomatch),
          imagenCancha: agregarURL(partido.imagenCancha),
        }));
      } catch (error) {
        console.error("Error cargando partidos en espera:", error);
      }

      try {
        const resFinalizados = await axios.get(`${URL_BASE}partidos_finalizados/${documento}`);
        partidosFinalizados.value = resFinalizados.data.map(partido => {
  const logoFinal = agregarURL(partido.logo) || agregarURL(partido.logomatch);
  return {
    ...partido,
    logo: logoFinal,
    imagenCancha: agregarURL(partido.imagenCancha),
  };
});
      } catch (error) {
        console.error("Error cargando partidos finalizados:", error);
      }
    });

    return {
      partidosEnEspera,
      partidosFinalizados,
      modalActivo,
      ampliarLogo,
      partidoSeleccionado,
      imagenAmpliada,
      verDetalle,
      irAComponente,
      formatoPesos,
      irAComponente2,
      irAComponente3,
      logoSrc,
    };
  },
};
</script>

 <style scoped>
 .container {
   display: flex;
   flex-direction: column;
   gap: 20px;
   padding: 20px;
   background-color: #1c1c1c;
   color: #ffffff;
   font-family: 'Segoe UI', sans-serif;
   border: solid white 1px;
 }
 
 .partidos-section {
   background: #000000;
   padding: 20px;
   border-radius: 12px;
   box-shadow: 0 4px 10px rgba(0, 0, 0, 0.3);
   border-left: 6px solid gold;
   transition: transform 0.3s ease;
   border-bottom: 2px white solid;
   box-shadow: 0 0 10px;
   min-height: 250px;
 }
 
 .partidos-section:hover {
   transform: scale(1.01);
   box-shadow: 0 0 10px orange;
 }
 
 .card {
   display: flex;
   align-items: center;
   justify-content: space-between;
   background: #1a1a1a; /* Negro suave */
   color: #f5f5f5; /* Blanco grisáceo para texto */
   padding: 20px;
   margin: 20px 0;
   border-radius: 16px;
   border: 1px solid #333;
   box-shadow: 0 4px 12px rgba(255, 215, 0, 0.2);
   transition: transform 0.3s ease, box-shadow 0.3s ease;
   backdrop-filter: blur(3px);
   position: relative;
   overflow: hidden;
   font-family: Verdana, Geneva, Tahoma, sans-serif;
   border: 1px solid rgb(70, 70, 70);
 }
 
 .card::before {
   content: '';
   position: absolute;
   top: 0;
   left: -100%;
   width: 100%;
   height: 100%;
   background: linear-gradient(
     120deg,
     transparent,
     rgba(255, 215, 0, 0.1),
     transparent
   );
   transition: all 0.6s ease-in-out;
 }
 
 .card:hover::before {
   left: 100%;
 }
 
 .card:hover {
   transform: translateY(-6px);
   box-shadow: 0 8px 20px rgba(255, 215, 0, 0.3);
 }
 
 
 .logo {
   width: 60px;
   height: 60px;
   border-radius: 50%;
   border: 2px solid gold;
   object-fit: cover;
   transition: transform 0.3s ease;
 }
 
 .logo:hover {
   transform: rotate(5deg) scale(1.1);
 }
 
 .info {
   flex-grow: 1;
   margin-left: 15px;
 }
 
 .btn-detalle {
   background: linear-gradient(135deg, #6d6d6d, #000000); /* Dorado degradado */
   color: #ffffff;
   padding: 5px 5px;
   border: 2px solid #ffcc00;
   border-radius: 10px;
   font-weight: 100px;
   letter-spacing: 1px;
   text-transform: uppercase;
   cursor: pointer;
   transition: all 0.3s ease;
   margin-right: 5px;
   box-shadow: 0 4px 10px rgba(255, 215, 0, 0.3);
 }
 
 .btn-detalle:hover {
   background: #525252;
   color: #ffcc00;
   transform: scale(1.08);
   box-shadow: 0 6px 18px rgba(255, 255, 255, 0.4);
 }
 .btn-detalle2 {
   background: linear-gradient(135deg, #ffcc00, #b8860b); /* Dorado degradado */
   color: #000;
   padding: 5px 5px;
   border: 2px solid #ffcc00;
   border-radius: 10px;
   font-weight: 100px;
   letter-spacing: 1px;
   text-transform: uppercase;
   cursor: pointer;
   transition: all 0.3s ease;
   box-shadow: 0 4px 10px rgba(255, 215, 0, 0.3);
 }
 
 .btn-detalle2:hover {
   background: #5d5d5d;
   color: #ffcc00;
   transform: scale(1.08);
   box-shadow: 0 6px 18px rgba(255, 255, 255, 0.4);
 }
 
 .modal-overlay {
   position: fixed;
   top: 0;
   left: 0;
   right: 0;
   bottom: 0;
   background: rgba(0, 0, 0, 0.7);
   display: flex;
   justify-content: center;
   align-items: center;
   z-index: 1000;
   animation: fadeIn 0.3s ease;
 }
 
 .modal {
   background: #f0f0f0;
   color: #000;
   padding: 25px;
   border-radius: 12px;
   max-width: 550px;
   width: 95%;
   position: relative;
   box-shadow: 0 4px 20px rgba(0, 0, 0, 0.4);
   animation: slideUp 0.4s ease;
 }
 
 .cerrar {
   position: absolute;
   top: 10px;
   right: 10px;
   border: none;
   background: crimson;
   color: white;
   border-radius: 50%;
   width: 30px;
   height: 30px;
   font-weight: bold;
   cursor: pointer;
   transition: transform 0.2s ease;
 }
 
 .cerrar:hover {
   transform: rotate(90deg);
 }
 
 @keyframes fadeIn {
   from { opacity: 0; }
   to { opacity: 1; }
 }
 
 @keyframes slideUp {
   from {
     transform: translateY(30px);
     opacity: 0;
   }
   to {
     transform: translateY(0);
     opacity: 1;
   }
 }
 .modal-overlay {
   position: fixed;
   top: 0;
   left: 0;
   right: 0;
   bottom: 0;
   background: rgba(0, 0, 0, 0.85);
   backdrop-filter: blur(6px);
   display: flex;
   align-items: center;
   justify-content: center;
   z-index: 999;
   animation: overlayFade 0.4s ease-in-out;
 }
 
 .modal {
   background: linear-gradient(145deg, #1a1a1a, #2c2c2c);
   color: #f2f2f2;
   padding: 35px;
   border-radius: 20px;
   max-width: 600px;
   width: 92%;
   position: relative;
   box-shadow: 0 0 30px rgba(255, 215, 0, 0.2),
               0 0 8px rgba(255, 255, 255, 0.05);
   border: 1px solid #444;
   animation: modalPop 0.4s ease;
 }
 .modal h2 {
   font-size: 30px;
   color: #000000;
   margin-bottom: 20px;
   text-align: center;
   text-shadow: 1px 1px 3px #000;
   border-bottom: 2px solid #ffcc00;
   padding-bottom: 12px;
   letter-spacing: 1px;
   font-family: Georgia, 'Times New Roman', Times, serif;
   position: relative;
 
   /* Borde blanco fino */
   -webkit-text-stroke: 0.5px #ffffff;
 }
 
 
 .modal p {
   font-size: 17px;
   color: #d0d0d0;
   margin: 14px 0;
   line-height: 1.7;
   font-family: Cambria, Cochin, Georgia, Times, 'Times New Roman', serif;
 }
 
 .modal p strong {
   color: #ffd500;
   -webkit-text-stroke: 0.5px #ffffff;
   font-size: 20px;
 }
 
 .imagen-cancha {
   width: 20%;
   margin: 20px 0;
   border-radius: 12px;
   border: 3px solid #ffd700;
   box-shadow: 0 0 20px rgba(255, 215, 0, 0.3);
   cursor: pointer;
   transition: transform 0.3s ease, box-shadow 0.3s ease;
 }
 
 .imagen-cancha:hover {
   transform: scale(1.05);
   box-shadow: 0 0 30px rgba(255, 215, 0, 0.5);
 }
 
 .modal-img {
   position: fixed;
   top: 0;
   left: 0;
   width: 100vw;
   height: 100vh;
   background: rgba(0, 0, 0, 0.85);
   display: flex;
   justify-content: center;
   align-items: center;
   z-index: 9999;
 }
 
 .modal-img img {
   width: 600px;
   height: 500px;
   border: 5px solid #ffd700;
   border-radius: 16px;
   box-shadow: 0 0 50px rgba(255, 215, 0, 0.6);
   transition: transform 0.3s ease;
 }
 
 
 .imagen-cancha:hover {
   transform: scale(1.05);
   box-shadow: 0 0 30px rgba(255, 215, 0, 0.5);
 }
 
 .cerrar {
   position: absolute;
   top: 12px;
   right: 12px;
   background: #ff1a1a;
   color: white;
   border: none;
   border-radius: 50%;
   width: 34px;
   height: 34px;
   font-size: 18px;
   font-weight: bold;
   cursor: pointer;
   box-shadow: 0 0 8px rgba(255, 0, 0, 0.4);
   transition: background 0.3s ease, transform 0.3s ease;
 }
 
 .cerrar:hover {
   background: #cc0000;
   transform: scale(1.2) rotate(15deg);
 }
 
 @keyframes modalPop {
   from {
     opacity: 0;
     transform: scale(0.8) translateY(-20px);
   }
   to {
     opacity: 1;
     transform: scale(1) translateY(0);
   }
 }
 
 @keyframes overlayFade {
   from {
     background: rgba(0, 0, 0, 0);
   }
   to {
     background: rgba(0, 0, 0, 0.85);
   }
 }
 
 @keyframes fadeIn {
   from {
     transform: scale(0.8);
     opacity: 0;
   }
   to {
     transform: scale(1);
     opacity: 1;
   }
 }
 .title {
   font-size: 28px;
   font-weight: 900;
   color: #000000; /* Dorado elegante */
   text-align: center;
   text-transform: uppercase;
   letter-spacing: 2.5px;
   margin-bottom: 15px;
   position: relative;
   padding-bottom: 10px;
 
   /* Borde negro al texto */
   text-shadow: 
     -1px -1px 0 #ffffff,  
      1px -1px 0 #ffffff,
     -1px  1px 0 #ffffff,
      1px  1px 0 #ffffff;
 }
 
 .title::after {
   content: "";
   display: block;
   width: 60px;
   height: 3px;
   background: #ffbf00;
   margin: 5px auto 0;
   border-radius: 5px;
   transition: width 0.3s ease-in-out;
 }
 
 .title:hover::after {
   width: 100px;
 }
 .boton-volver {
   padding: 10px 25px;
   background-color: black;
   color: gold;
   border: 2px solid gold;
   font-size: 16px;
   font-weight: bold;
   border-radius: 12px;
   cursor: pointer;
   transition: all 0.3s ease;
   box-shadow: 0 4px 10px rgba(255, 215, 0, 0.3);
 }
 .sin-partidos {
  text-align: center;
  font-style: italic;
  color: gray;
  margin-top: 1rem;
}
 .boton-volver:hover {
   background-color: gold;
   color: black;
   border: 2px solid white;
   box-shadow: 0 6px 15px rgba(255, 255, 255, 0.4);
 }
 .tit {
   font-size: 22px;
   font-weight: 700;
   color: #000000; /* Dorado intenso */
   margin: 0 0 10px 0;
   text-transform: uppercase;
   letter-spacing: 1.5px;
   text-shadow: 
     -1px -1px 0 #abaaaa, 
      1px -1px 0 #565656, 
     -1px  1px 0 #000, 
      1px  1px 0 #000; /* Contorno negro */
   transition: color 0.3s ease;
 }
 
 .tit:hover {
   color: #ffffff; /* Cambia a blanco al pasar el mouse */
 }
 .modal-img {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.8);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 9999;
}

.modal-img img {
  max-width: 90%;
  max-height: 90%;
  border-radius: 10px;
}

.logo {
  cursor: pointer;
}
.buscador {
  width: 100%;
  max-width: 400px;
  margin: 10px auto 30px;
  padding: 10px;
  font-size: 16px;
  display: block;
  border: 1px solid #ccc;
  border-radius: 10px;
}
 </style>