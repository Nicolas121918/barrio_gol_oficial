<template>  
<header>
  <Headerapp></Headerapp>

</header>
  <div class="game-container">
    <h2 class="game-title">Escoger Ganador</h2>
    <div class="team-list">
      <div 
        v-for="equipo in equipos" 
        :key="equipo.id" 
        @click="seleccionarEquipo(equipo.id)"
        class="team-card"
        :class="{'selected': equipoSeleccionado === equipo.id}"
      >
        <img :src="equipo.logo" alt="Logo" class="team-logo" />
        <span class="team-name">{{ equipo.nombre }}</span>
      </div>
    </div>
    <div class="buttons-container">
      <button class="back-button" @click="$emit('volver')">Volver</button>
      <button 
        class="choose-button" 
        :class="{'disabled': !equipoSeleccionado}"
        :disabled="!equipoSeleccionado"
        @click="confirmacion = true"
      >
        Escoger Ganador
      </button>
    </div>

    <div v-if="confirmacion" class="modal-overlay">
      <div class="modal">
        <h3 class="modal-title">Confirmación</h3>
        <p class="modal-text">¿Estás seguro de que deseas elegir a <span class="highlight">{{ getEquipoSeleccionado.nombre }}</span> como ganador?</p>
        <button class="confirm-button" @click="mostrarConfirmacion = true; confirmacion = false">Sí</button>
        <button class="cancel-button" @click="confirmacion = false">No</button>
      </div>
    </div>

    <div v-if="mostrarConfirmacion" class="modal-overlay">
      <div class="modal">
        <h3 class="modal-title">¡Ganador Confirmado!</h3>
        <p class="modal-text">El equipo ganador es <span class="highlight">{{ getEquipoSeleccionado.nombre }}</span></p>
        <button class="confirm-button" @click="mostrarConfirmacion = false">Aceptar</button>
      </div>
    </div>
  </div>
</template>

<script>
import Headerapp from './Headerapp.vue';

export default {
  components:{
    Headerapp

  },
  props: {
    equipos: {
      type: Array,
      default: () => [
        { id: 1, nombre: "Equipo A", logo: "https://img.freepik.com/vector-gratis/logotipo-juegos-diseno-plano_23-2150747166.jpg" },
        { id: 2, nombre: "Equipo B", logo: "https://via.placeholder.com/50" },
        { id: 4, nombre: "Equipo c", logo: "https://via.placeholder.com/50" },
        { id: 5, nombre: "Equipo e", logo: "https://via.placeholder.com/50" },
        { id: 6, nombre: "Equipo f", logo: "https://via.placeholder.com/50" },
        { id: 7, nombre: "Equipo g", logo: "https://via.placeholder.com/50" },
      ]
    }
  },
  data() {
    return {
      equipoSeleccionado: null,
      confirmacion: false,
      mostrarConfirmacion: false
    };
  },
  computed: {
    getEquipoSeleccionado() {
      return this.equipos.find(equipo => equipo.id === this.equipoSeleccionado) || {};
    }
  },
  methods: {
    seleccionarEquipo(id) {
      this.equipoSeleccionado = id;
    }
  }
};
</script>
<style scoped>
.game-container {
  background: radial-gradient(circle, #01011859, #000424);
  color: #fff;
  padding: 40px;
  border-radius: 15px;
  text-align: center;
  max-width: 900px;
  margin: auto;
  font-family: 'Press Start 2P', cursive;
  box-shadow: 0 0 40px rgba(230, 196, 3, 0.781); /* Efecto de neón */
  border: solid white;
  margin-top: 20%;
}

.game-title {
  font-size: 40px; /* Título más grande */
  margin-bottom: 20px;
  color: #ffec9e;
  text-shadow: 0 0 10px #ffcc00, 0 0 20px #ffcc00; /* Efecto de neón */
}

.team-list {
  display: flex;
  flex-wrap: wrap; /* Para que las tarjetas se ajusten cuando haya más espacio */
  gap: 20px; /* Más espacio entre las tarjetas */
  justify-content: center; /* Centrar las tarjetas en el contenedor */

}

.team-card {
  display: flex;
  align-items: center;
  justify-content: center; /* Centrar el contenido dentro de la tarjeta */
  padding: 20px;
  border: 3px solid #ffcc00; /* Borde más grueso */
  border-radius: 10px;
  cursor: pointer;
  transition: all 0.3s ease-in-out;
  background: #000000;
  font-size: 20px; /* Fuente más grande */
  box-shadow: 0 0 15px rgba(255, 204, 0, 0.5); /* Efecto de neón en el borde */
  width: 200px; /* Ancho fijo para las tarjetas */
  height: 250px; /* Altura fija para las tarjetas */
  flex-direction: column; /* Asegura que el logo esté encima del nombre */
  text-align: center; /* Alinear el texto al centro */
}

.team-card:hover, .selected {
  background-image: url("https://img.freepik.com/fotos-premium/fondo-dorado-textura-dorado-que-dice-palabra-el_662214-601359.jpg?w=360"); /* Fondo verde brillante */
  color: #000; /* Texto negro */
  box-shadow: 0 0 25px rgba(255, 255, 255, 0.7), 0 0 35px rgba(0, 255, 0, 0.5); /* Efecto de neón */
  transform: scale(1.05); /* Agrandar ligeramente la tarjeta */
}


.team-logo {
  width: 80px; /* Logo más grande */
  height: 80px;
  margin-bottom: 10px;
  border-radius: 50%;
  border: solid white 1px;
  box-shadow: rgb(255, 253, 253) 0 0 2px;
}

.team-name {
  text-decoration: overline white;
  font-size: 24px; /* Texto más grande */
  font-weight: bold;
  text-shadow: 0 0 10px rgba(255, 255, 255, 0.5); 
 
}

.buttons-container {
  display: flex;
  justify-content: space-between;
  margin-top: 30px;
}

.back-button, .choose-button {
  padding: 15px 25px;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-size: 20px; /* Botones más grandes */
  font-weight: bold;
  text-transform: uppercase;
  transition: all 0.3s ease;
}

.back-button {
  background: #ff4444; /* Fondo rojo brillante */
  color: white; /* Texto blanco */
  padding: 15px 25px; /* Espaciado en los lados y arriba/abajo */
  border: 2px solid #ff2222; /* Borde de color rojo oscuro */
  border-radius: 12px; /* Bordes redondeados */
  font-size: 20px; /* Tamaño de la fuente */
  font-weight: bold; /* Texto en negrita */
  text-transform: uppercase; /* Convertir texto a mayúsculas */
  cursor: pointer; /* Cambiar el cursor a puntero al pasar sobre el botón */
  box-shadow: 0 0 15px rgba(255, 68, 68, 0.7); /* Sombra difusa en tonos rojos */
  transition: all 0.3s ease-in-out; /* Transición suave para los cambios */
}

/* Efecto cuando el usuario pasa el mouse sobre el botón */
.back-button:hover {
  background: #ff3333; /* Fondo más oscuro cuando pasa el mouse */
  border-color: #ff1111; /* Borde más oscuro */
  transform: scale(1.05); /* Agrandar ligeramente el botón */
  box-shadow: 0 0 25px rgba(255, 51, 51, 0.9); /* Resplandor más intenso cuando se hace hover */
}

/* Efecto cuando el botón es presionado */
.back-button:active {
  background: #cc3333; /* Fondo aún más oscuro cuando se presiona */
  box-shadow: 0 0 20px rgba(255, 51, 51, 0.6); /* Sombra más suave */
  transform: scale(0.98); /* Efecto de reducción cuando se presiona */
}


.choose-button {
  background-image: url("https://static.vecteezy.com/system/resources/thumbnails/000/549/015/small/vector-apr-2018-19.jpg"); /* Fondo azul brillante */
  color: rgb(0, 0, 0); /* Texto blanco */
  padding: 15px 25px; /* Espaciado en los lados y arriba/abajo */
  border: 2px solid #ffffff; /* Borde de color azul oscuro */
  border-radius: 12px; /* Bordes redondeados */
  font-size: 20px; /* Tamaño de la fuente */
  font-weight: bold; /* Texto en negrita */
  text-transform: uppercase; /* Convertir texto a mayúsculas */
  cursor: pointer; /* Cambiar el cursor a puntero al pasar sobre el botón */
  box-shadow: 0 0 15px rgba(255, 255, 255, 0.7); /* Sombra difusa en tonos azules */
  transition: all 0.3s ease-in-out; /* Transición suave para los cambios */
}

/* Efecto cuando el usuario pasa el mouse sobre el botón */
.choose-button:hover {
   /* Fondo más oscuro cuando pasa el mouse */
  border-color: #000000; /* Borde más oscuro */
  transform: scale(1.05); /* Agrandar ligeramente el botón */
  box-shadow: 0 0 25px rgba(0, 0, 0, 0.9); /* Resplandor más intenso cuando se hace hover */
}

/* Efecto cuando el botón es presionado */
.choose-button:active {
  background: #003e7e; /* Fondo aún más oscuro cuando se presiona */
  box-shadow: 0 0 20px rgba(0, 95, 200, 0.6); /* Sombra más suave */
  transform: scale(0.98); /* Efecto de reducción cuando se presiona */
}

/* Efecto cuando el botón está deshabilitado */
.choose-button.disabled {
  background: #4a90e2; /* Fondo más claro cuando está deshabilitado */
  cursor: not-allowed; /* Cambiar el cursor para indicar que está deshabilitado */
  opacity: 0.6; /* Reducir la opacidad para darle un aspecto apagado */
}


.choose-button.disabled {
  background: gray;
  cursor: not-allowed;
}

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background:  rgba(0, 0, 0, 0.8);
  display: flex;
  align-items: center;
  justify-content: center;
}

.modal {
  background: #302f2f;
  padding: 30px;
  border-radius: 15px;
  text-align: center;
  max-width: 400px;
  box-shadow: 0 0 25px rgba(255, 196, 0, 0.7); /* Efecto de neón en la modal */
}

.modal-title {
  font-size: 30px;
  color: #ffffff;
  text-shadow: 0 0 10px #ffcc00, 0 0 20px #ffcc00; /* Efecto de neón */
}

.modal-text {
  margin-top: 20px;
  font-size: 20px; /* Texto más grande */
}

.highlight {
  color: transparent; /* Hacer el texto transparente para que se vea solo el fondo */
  font-weight: bold;
  font-size: 24px; /* Texto más grande */
  background: url('https://static.vecteezy.com/system/resources/thumbnails/000/549/015/small/vector-apr-2018-19.jpg') no-repeat center center; /* Usar la imagen como fondo */
  background-size: cover; /* Asegurarse de que la imagen cubra todo el texto */
  -webkit-background-clip: text; /* Aplicar el fondo solo al texto */
  background-clip: text; /* Compatibilidad para otros navegadores */
  transition: background 0.3s ease-in-out, transform 0.3s ease; /* Transiciones para el fondo y el tamaño */
  animation: animarTexto 1.5s ease-in-out infinite; /* Animación inicial */
}

@keyframes animarTexto {
  0% {
    transform: scale(1); /* Tamaño normal al inicio */
    opacity: 0.8; /* Opacidad ligeramente más baja */
  }
  50% {
    transform: scale(1.1); /* Aumenta el tamaño a 1.1 */
    opacity: 1; /* Opacidad normal */
  }
  100% {
    transform: scale(1); /* Vuelve al tamaño normal */
    opacity: 0.8; /* Opacidad ligeramente más baja */
  }
}

.highlight:hover {
  background-size: cover; /* Asegurarse de que la imagen cubra todo el texto */
  transform: scale(1.2); /* Aumentar ligeramente el tamaño del texto al pasar el ratón */
  opacity: 1; /* Opacidad al pasar el ratón */
  animation: none; /* Desactivar la animación en hover */
}

.confirm-button, .cancel-button {
  margin-top: 20px;
  padding: 12px 18px;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-size: 18px; /* Botones más grandes */
  font-weight: bold;
  text-transform: uppercase;
  transition: all 0.3s ease;
}

.confirm-button {
  background: #44ff44; /* Color de fondo verde brillante */
  color: #000; /* Color del texto en negro */
  padding: 12px 24px; /* Espaciado interno para hacerlo más grande y cómodo de hacer clic */
  border-radius: 8px; /* Bordes redondeados para un diseño más suave */
  font-weight: bold; /* Resaltar el texto */
  font-size: 16px; /* Tamaño del texto adecuado */
  transition: transform 0.3s ease, background 0.3s ease; /* Transiciones suaves para el cambio de tamaño y fondo */
  cursor: pointer; /* Apunta a la mano al pasar el cursor sobre el botón */
  border: 2px solid transparent; /* Inicialmente sin borde visible */
  margin-right: 10px; /* Separación a la derecha del botón */
}

.confirm-button:hover {
  background: #36cc36; /* Cambia a un verde más oscuro cuando se pasa el cursor */
  transform: scale(1.05); /* Aumenta ligeramente el tamaño para dar un efecto de "toque" */
  border-color: #28a728; /* Aparece un borde verde oscuro cuando se pasa el cursor */
  color: white;
}

.confirm-button:active {
  background: #28a728; /* Fondo verde oscuro cuando el botón está siendo presionado */
  transform: scale(0.98); /* El botón se reduce ligeramente al presionarlo */
}

.cancel-button {
  background: #ff4444; /* Color de fondo rojo brillante */
  color: white; /* Color del texto en blanco */
  padding: 12px 24px; /* Espaciado interno para hacerlo más grande y cómodo de hacer clic */
  border-radius: 8px; /* Bordes redondeados para un diseño más suave */
  font-weight: bold; /* Resaltar el texto */
  font-size: 16px; /* Tamaño del texto adecuado */
  transition: transform 0.3s ease, background 0.3s ease; /* Transiciones suaves para el cambio de tamaño y fondo */
  cursor: pointer; /* Apunta a la mano al pasar el cursor sobre el botón */
  border: 2px solid transparent; /* Inicialmente sin borde visible */
}

.cancel-button:hover {
  color: #000;
  background: #e63946; /* Cambia a un rojo más oscuro cuando se pasa el cursor */
  transform: scale(1.05); /* Aumenta ligeramente el tamaño para dar un efecto de "toque" */
  border-color: #d32f2f; /* Aparece un borde rojo oscuro cuando se pasa el cursor */
}

.cancel-button:active {
  background: #d32f2f; /* Fondo rojo oscuro cuando el botón está siendo presionado */
  transform: scale(0.98); /* El botón se reduce ligeramente al presionarlo */
}


</style>