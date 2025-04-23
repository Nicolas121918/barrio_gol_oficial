<template>
    <header>
        <Headerapp></Headerapp>
    
    </header>
    <div class="container">
    <button @click="$router.go(-1)" class="volver">⬅ Volver</button>
    <h1>Lista de Jugadores equipo...</h1>

    <!-- Buscador -->
    <div class="buscador">
      <input
        type="text"
        v-model="searchQuery"
        placeholder="Buscar por nombre, número o causa de tarjeta"
        @input="filtrarJugadores"
      />
    </div>
  
    <!-- Lista de Jugadores -->
    <div class="jugadores">
      <div v-for="jugador in jugadoresFiltrados" :key="jugador.id" class="jugador">
        <img :src="jugador.foto" alt="Foto del jugador" class="foto" />
        <div class="info">
          <p>{{ jugador.nombre }} (#{{ jugador.numero }})</p>
          <div class="acciones">
            <button @click="asignarTarjeta(jugador, 'Amarilla')" class="amarilla">.</button>
            <button @click="asignarTarjeta(jugador, 'Roja')" class="roja">.</button>
            <button @click="asignarTarjeta(jugador, 'Azul')" class="azul">.</button>
          </div>
        </div>
        <div class="tarjetas">
          <button @click="jugador.mostrarHistorial = !jugador.mostrarHistorial" class="historial-btn">📌 Historial</button>
          <div v-if="jugador.mostrarHistorial" class="historial">
            <h3>Historial de Tarjetas</h3>
            <ul>
              <li v-for="(tarjeta, index) in jugador.tarjetas" :key="index">
                {{ tarjeta.tipo }} - {{ tarjeta.motivo }}
                <span :class="{ pagado: tarjeta.pagado, pendiente: !tarjeta.pagado }">
                  {{ tarjeta.pagado ? '✅ Pagado' : '❌ Pendiente' }}
                </span>
                <button @click="mostrarOpciones(jugador, index)" class="opciones-btn">...</button>
                <div v-if="tarjeta.mostrarOpciones" class="opciones">
                  <button @click="eliminarTarjeta(jugador, index)">Cancelar Tarjeta</button>
                </div>
              </li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  
    <div v-if="showModal" class="modal">
      <div class="modal-content">
        <h2>Asignar Tarjeta {{ tarjetaModal.tipo }}</h2>
        <textarea v-model="tarjetaModal.motivo" placeholder="Motivo de la tarjeta"></textarea>
        <label>
          <input type="checkbox" v-model="tarjetaModal.pagado" /> Pagado
        </label>
        <button @click="confirmarTarjeta">Confirmar</button>
        <button @click="showModal = false">Cancelar</button>
      </div>
    </div>
  </div>
  </template>
  
  <script>
import Headerapp from './Headerapp.vue';
  export default {
    components : {
        Headerapp

    },
  data() {
    return {
      searchQuery: '',
      jugadores: [
        { id: 1, foto: 'https://img.freepik.com/vector-gratis/logotipo-juegos-diseno-plano_23-2150747166.jpg', nombre: 'Juan Pérez', numero: 10, tarjetas: [], mostrarHistorial: false },
        { id: 2, foto: 'https://via.placeholder.com/50', nombre: 'Carlos Gómez', numero: 7, tarjetas: [], mostrarHistorial: false },
        { id: 3, foto: 'https://via.placeholder.com/50', nombre: 'Ana Martínez', numero: 5, tarjetas: [], mostrarHistorial: false },
        // Agrega más jugadores según sea necesario
      ],
      tarjetaModal: { jugador: null, tipo: '', motivo: '', pagado: false },
      showModal: false,
      jugadoresFiltrados: [],
    };
  },
  watch: {
    // Cuando cambia el searchQuery, se actualiza la lista filtrada
    searchQuery() {
      this.filtrarJugadores();
    },
  },
  methods: {
    asignarTarjeta(jugador, tipo) {
      if (tipo === 'Amarilla') {
        const amarillas = jugador.tarjetas.filter(t => t.tipo === 'Amarilla').length;
        if (amarillas === 1) {
          jugador.tarjetas = jugador.tarjetas.filter(t => t.tipo !== 'Amarilla');
          tipo = 'Roja';
        }
      }
      this.tarjetaModal.jugador = jugador;
      this.tarjetaModal.tipo = tipo;
      this.tarjetaModal.motivo = '';
      this.tarjetaModal.pagado = false;
      this.showModal = true;
    },
    confirmarTarjeta() {
      if (this.tarjetaModal.jugador) {
        this.tarjetaModal.jugador.tarjetas.push({ tipo: this.tarjetaModal.tipo, motivo: this.tarjetaModal.motivo, pagado: this.tarjetaModal.pagado });
        this.showModal = false;
      }
    },
    mostrarOpciones(jugador, index) {
      jugador.tarjetas[index].mostrarOpciones = !jugador.tarjetas[index].mostrarOpciones;
    },
    eliminarTarjeta(jugador, index) {
      jugador.tarjetas.splice(index, 1);
    },
    filtrarJugadores() {
      const query = this.searchQuery.toLowerCase();
      this.jugadoresFiltrados = this.jugadores.filter(jugador => {
        // Filtra por nombre, número o causa de tarjeta
        const tarjetasMotivo = jugador.tarjetas.map(t => t.motivo).join(' ').toLowerCase();
        return (
          jugador.nombre.toLowerCase().includes(query) ||
          jugador.numero.toString().includes(query) ||
          tarjetasMotivo.includes(query)
        );
      });
    },
  },
  created() {
    // Inicializa la lista filtrada con todos los jugadores al principio
    this.jugadoresFiltrados = this.jugadores;
  },
  };
  </script>
  
  
  <style scoped>
  /* Estilos para el buscador */
  .buscador {
  margin-bottom: 20px;
  color: white;
  }
  
  .buscador input {
  width: 100%;
  padding: 8px;
  font-size: 16px;
  background-color: rgb(0, 0, 0);
  color: white;
  text-align: center;
  
  }
  /* Estilo general para el contenedor */
  .container {
  background: #270f0f;
  background: linear-gradient(to right, #525151, #242323);
  color: #dcdfe1;
  border-radius: 20px;
  padding: 40px;
  max-width: 1000px;
  margin: auto;
  box-shadow: 0 0 50px rgba(0, 0, 0, 0.8);
  font-family: 'Orbitron', sans-serif;
  animation: fadeIn 1s ease-out;
  margin-top: 20%;
  }
  
  /* Animación de entrada del contenedor */
  @keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
  }
  
  /* Estilo para el botón Volver */
  .volver {
  background: #00b894;
  color: #ecf0f1;
  padding: 15px 30px;
  border-radius: 12px;
  border: none;
  font-size: 15px;
  font-weight: bold;
  text-transform: uppercase;
  letter-spacing: 1px;
  cursor: pointer;
  transition: all 0.3s ease;
  transform: scale(1);
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
  display: inline-block;
  text-align: center;
  outline: none;
  }
  
  .volver:hover {
  border: solid white 2px;
  background: #00cec9;
  transform: scale(1.05);
  box-shadow: 0px 8px 25px rgba(0, 0, 0, 0.5);
  color: #2d3436;
  text-shadow: 1px 1px 5px rgba(0, 0, 0, 0.2);
  }
  
  .volver:active {
  background: #00a8b9;
  transform: scale(0.98);
  box-shadow: 0px 4px 15px rgba(0, 0, 0, 0.3);
  }
  
  .volver:focus {
  outline: none;
  box-shadow: 0 0 10px rgba(0, 200, 200, 0.6);
  }
  
  /* Título */
  h1 {
  font-size: 42px;
  margin-bottom: 30px;
  font-weight: bold;
  text-align: center;
  color: #ebae06;
  text-shadow: 4px 4px 8px rgba(0, 0, 0, 0.7);
  text-transform: uppercase;
  letter-spacing: 4px;
  }
  
  /* Sección de jugadores */
  .jugadores {
  display: flex;
  flex-direction: column;
  gap: 25px;
  }
  
  /* Card de cada jugador */
  .jugador {
  background: #000000;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 25px;
  border-radius: 15px;
  box-shadow: 0px 20px 40px rgba(109, 109, 109, 0.8);
  transition: 0.3s ease;
  cursor: pointer;
  border: 2px solid #adadad;
  position: relative;
  }
  
  .jugador:hover {
  background: #061e36;
  transform: scale(1.05);
  box-shadow: 0px 30px 60px rgba(0, 0, 0, 0.9);
  }
  
  .foto {
  width: 80px;
  height: 75px;
  border-radius: 50%;
  border: 4px solid #ecf0f1;
  transition: all 0.3s ease;
  box-shadow: 0 0 10px white;
  }
  
  .foto:hover {
  transform: rotate(360deg);
  box-shadow: 0px 0px 15px rgba(0, 0, 0, 0.7);
  border-color: #f39c12;
  box-shadow: 0 0 10px rgb(240, 145, 2);
  }
  
  /* Información del jugador */
  .info {
  display: flex;
  flex-direction: column;
  gap: 20px;
  font-size: 130%;
  }
  
  /* Botones de acciones */
  .amarilla {
  margin: 10px;
  padding: 12px 22px;
  border-radius: 12px;
  border: none;
  color: white;
  font-size: 20px;
  cursor: pointer;
  transition: 0.3s ease;
  background-color: #ffee00;
  transform: scale(1);
  }
  
  .amarilla:hover {
  background-color: #eeff00;
  transform: scale(1.1);
  box-shadow: 0px 6px 18px rgba(0, 0, 0, 0.3);
  box-shadow: 0 0 10px white;
  }
  
  /* Tarjetas de acción */
  
  .roja {
  margin: 10px;
  padding: 12px 22px;
  border-radius: 12px;
  border: none;
  color: white;
  font-size: 20px;
  cursor: pointer;
  transition: 0.3s ease;
  background-color: #ff0000;
  transform: scale(1);
  }
  
  .roja:hover {
  background-color: #ff0000;
  transform: scale(1.1);
  box-shadow: 0px 6px 18px rgba(0, 0, 0, 0.3);
  box-shadow: 0 0 10px white;
  }
  .azul{
  margin: 10px;
  padding: 12px 22px;
  border-radius: 12px;
  border: none;
  color: white;
  font-size: 20px;
  cursor: pointer;
  transition: 0.3s ease;
  background-color: #0026ff;
  transform: scale(1);
  }
  
  .azul:hover {
  background-color: #0400ff;
  transform: scale(1.1);
  box-shadow: 0px 6px 18px rgba(0, 0, 0, 0.3);
  box-shadow: 0 0 10px white;
  }
  /* Efectos de resplandor */
  @keyframes glowingYellow {
  0% { box-shadow: 0 0 10px rgba(241, 196, 15, 0.6); }
  100% { box-shadow: 0 0 25px rgba(241, 196, 15, 1); }
  }
  @keyframes glowingRed {
  0% { box-shadow: 0 0 10px rgba(231, 76, 60, 0.6); }
  100% { box-shadow: 0 0 25px rgba(231, 76, 60, 1); }
  }
  @keyframes glowingBlue {
  0% { box-shadow: 0 0 10px rgba(41, 128, 185, 0.6); }
  100% { box-shadow: 0 0 25px rgba(41, 128, 185, 1); }
  }
  
  /* Opciones de tarjeta */
  .opciones-btn {
  background: transparent;
  border: none;
  color: #ecf0f1;
  font-size: 28px;
  cursor: pointer;
  transition: 0.3s ease;
  }
  
  .opciones-btn:hover {
  color: #f39c12;
  transform: rotate(180deg);
  }
  
  /* Opciones (eliminar tarjeta) */
  .opciones {
  margin-top: 15px;
  }
  
  .opciones button {
  background: #e74c3c;
  color: white;
  padding: 12px 18px;
  border-radius: 12px;
  border: none;
  cursor: pointer;
  transition: 0.3s ease;
  }
  .opciones button:hover {
  background: #c0392b;
  box-shadow: 0px 6px 15px rgba(0, 0, 0, 0.3);
  }
  
  /* Modal de tarjeta */
  .modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.7);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 9999;
  animation: modalFadeIn 0.5s ease-out;
  }
  
  @keyframes modalFadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
  }
  
  .modal-content {
  background: #2c3e50;
  padding: 40px;
  border-radius: 15px;
  width: 500px;
  box-shadow: 0px 25px 55px rgba(0, 0, 0, 0.8);
  animation: modalZoomIn 0.5s ease-in-out;
  border: solid white;
  }
  
  @keyframes modalZoomIn {
  from { transform: scale(0.8); }
  to { transform: scale(1); }
  }
  
  .modal-content h2 {
  color: #ecf0f1;
  margin-bottom: 25px;
  font-size: 30px;
  text-align: center;
  text-transform: uppercase;
  letter-spacing: 2px;
  }
  
  textarea {
  width: 100%;
  height: 100px;
  margin-top: 20px;
  border-radius: 10px;
  border: 2px solid #7f8c8d;
  background: #34495e;
  color: white;
  font-size: 16px;
  padding: 12px;
  transition: 0.3s ease;
  }
  
  textarea:focus {
  border-color: #1abc9c;
  background: #2c3e50;
  }
  
  label {
  color: #ecf0f1;
  margin-top: 12px;
  font-size: 16px;
  }
  
  button {
  background-color: #0075b8;
  color: white;
  padding: 12px 25px;
  border-radius: 12px;
  border: none;
  cursor: pointer;
  transition: 0.3s ease;
  margin-top: 20px;
  font-size: 18px;
  transform: scale(1);
  border: solid white 1px;
  margin-right: 10px;
  }
  
  button:hover {
  background: #00cec9;
  transform: scale(1.1);
  box-shadow: 0px 5px 15px rgba(0, 0, 0, 0.3);
  color: black;
  }
  
  
  </style>