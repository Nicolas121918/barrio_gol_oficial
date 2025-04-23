<script setup>
import { ref } from "vue";
import Headerapp from "./Headerapp.vue";

// Estado de la cuenta
const saldoDisponible = ref(100); // Saldo inicial
const recarga = ref(0);
const mensaje = ref("");
const servicios = ref([
  { id: 1, nombre: "Tarjeta Amarilla", precio: 10, pagado: false },
  { id: 2, nombre: "Tarjeta Roja", precio: 20, pagado: false },
  { id: 3, nombre: "Arbitraje", precio: 50, pagado: false },
]);

// Función para recargar saldo
const recargarSaldo = () => {
  if (recarga.value > 0) {
    saldoDisponible.value += parseFloat(recarga.value);
    mensaje.value = `Saldo recargado: $${recarga.value.toFixed(2)}`;
    recarga.value = 0;
  } else {
    mensaje.value = "Por favor, ingrese un monto válido.";
  }
};

// Función para pagar servicio
const pagarServicio = (servicio) => {
  if (saldoDisponible.value >= servicio.precio) {
    saldoDisponible.value -= servicio.precio;
    servicio.pagado = true;
    mensaje.value = `Has pagado: ${servicio.nombre}.`;
  } else {
    mensaje.value = `No tienes suficiente saldo para pagar ${servicio.nombre}.`;
  }
};

// Función para pagar torneo
const pagarTorneo = () => {
  if (saldoDisponible.value >= 50) {
    saldoDisponible.value -= 50;
    mensaje.value = "¡Has pagado el torneo con éxito!";
  } else {
    mensaje.value = "No tienes suficiente saldo para pagar el torneo.";
  }
};
</script>

<template>
    <header>
        <Headerapp></Headerapp>

    </header>
  <div class="min-h-screen bg-gradient-to-br from-black to-gray-900 flex items-center justify-center p-6">
    <div class="max-w-4xl w-full bg-gradient-to-br from-gray-900 to-black rounded-3xl shadow-xl overflow-hidden border border-gray-700">
      <!-- Encabezado -->
      <div class="p-8 bg-gradient-to-r from-indigo-500 to-purple-600 text-white text-center rounded-t-3xl">
        <h1 class="text-5xl font-extrabold tracking-wider">Billetera Deportiva</h1>
        <p class="text-lg mt-2 font-light opacity-80">
          Administra tus pagos de forma rápida y segura ⚡️
        </p>
      </div>

      <!-- Saldo Disponible -->
      <div class="p-6 text-center">
        <h2 class="text-3xl font-semibold text-white mb-4">Saldo Disponible</h2>
        <p class="text-6xl font-bold text-green-500 mt-2">
          ${{ saldoDisponible.toFixed(2) }}
        </p>
      </div>

      <!-- Recargar Saldo -->
      <div class="p-6 border-t border-gray-700 bg-gray-800">
        <h3 class="text-2xl font-bold text-white mb-4">Recargar Saldo</h3>
        <div class="flex flex-wrap items-center gap-6">
          <input
            type="number"
            v-model="recarga"
            placeholder="Monto a recargar"
            class="w-full sm:w-auto p-4 border-2 border-indigo-600 rounded-x  l bg-gray-900 text-white placeholder-gray-400 focus:ring-4 focus:ring-indigo-500 transition-all"
          />
          <button
            @click="recargarSaldo"
            class="bg-indigo-600 text-white py-3 px-8 rounded-xl hover:bg-indigo-700 transition-all transform hover:scale-105"
          >
            Recargar
          </button>
        </div>
        <p v-if="mensaje" class="text-sm text-gray-400 mt-3 font-light italic">{{ mensaje }}</p>
      </div>

      <!-- Servicios Disponibles -->
      <div class="p-6 border-t border-gray-700 bg-gray-800">
        <h3 class="text-2xl font-bold text-white mb-4">Pendientes Por Pagar</h3>
        <ul class="space-y-6">
          <li
            v-for="servicio in servicios"
            :key="servicio.id"
            class="flex items-center justify-between p-6 rounded-xl shadow-2xl transition-all transform hover:scale-105 hover:shadow-lg"
            :class="{
              'bg-gradient-to-r from-green-500 to-green-600': servicio.pagado,
              'bg-gradient-to-r from-red-500 to-red-600': !servicio.pagado && saldoDisponible < servicio.precio,
              'bg-gradient-to-r from-blue-500 to-blue-600': !servicio.pagado && saldoDisponible >= servicio.precio,
            }"
          >
            <div>
              <p class="text-xl font-semibold text-white">{{ servicio.nombre }}</p>
              <p class="text-sm text-gray-300">Precio: ${{ servicio.precio }}</p>
              <p v-if="servicio.pagado" class="text-green-400 text-sm font-bold">Pagado</p>
            </div>
            <button
              @click="pagarServicio(servicio)"
              :disabled="servicio.pagado || saldoDisponible < servicio.precio"
              class="py-3 px-6 rounded-xl font-bold transition-all transform hover:scale-105"
              :class="{
                'bg-gray-600 text-gray-400 cursor-not-allowed': servicio.pagado || saldoDisponible < servicio.precio,
                'bg-indigo-600 hover:bg-indigo-700 text-white': !servicio.pagado && saldoDisponible >= servicio.precio,
              }"
            >
              {{ servicio.pagado ? "Pagado" : "Pagar" }}
            </button>
          </li>
        </ul>
      </div>

      <!-- Pagar Torneo -->
      <div class="p-6 border-t border-gray-700 bg-gray-800">
        <h3 class="text-2xl font-bold text-white mb-4">Pagar Torneo</h3>
        <button
          @click="pagarTorneo"
          :disabled="saldoDisponible < 50"
          class="py-3 px-8 bg-red-500 text-white rounded-xl hover:bg-red-600 transition-all transform hover:scale-105"
        >
          Pagar Torneo
        </button>
        <p v-if="mensaje" class="text-sm text-gray-400 mt-3 font-light italic">{{ mensaje }}</p>
      </div>

      <!-- Pie de página -->
      <div class="p-4 bg-gray-800 text-center border-t border-gray-700 rounded-b-3xl">
        <p class="text-sm text-gray-400 font-light">Diseñado para jugadores de fútbol. ⚽️ Futuro en tus manos.</p>
      </div>
    </div>
  </div>
</template>

<style scoped>
/* Fondo general */
.min-h-screen {
  display: flex;
  align-items: center;
  justify-content: center;
  background: #1a120b; /* Fondo oscuro cálido */
  padding: 1rem 2rem;
  margin-top: 21%;
}

/* Contenedor principal */
.max-w-4xl {
  background: #3e2c1c; /* Fondo marrón oscuro */
  border-radius: 6rem;
  box-shadow: 0 12px 30px rgba(255, 215, 0, 0.2);
  border: 1px solid #a67c00;
  padding: 2rem;
  max-width: 90%;
}

/* Encabezado */
.p-8.bg-gradient-to-r {
  background: linear-gradient(45deg, #d4af37, #b8860b);
  text-align: center;
  color: #fff;
  border-top-left-radius: 2rem;
  border-top-right-radius: 2rem;
  padding: 1.5rem;
}

.p-8.bg-gradient-to-r h1 {
  font-size: 3rem;
  font-weight: 800;
  letter-spacing: 0.1rem;
  margin-bottom: 1rem;
  text-shadow: 2px 2px 10px rgba(255, 215, 0, 0.6);
}

.p-8.bg-gradient-to-r p {
  font-size: 1.2rem;
  opacity: 0.9;
}

/* Saldo disponible */
.text-green-500 {
  color: #ffcc00;
  font-size: 2.5rem;
  font-weight: 800;
  margin-top: 1rem;
}

/* Inputs */
input {
  width: 100%;
  padding: 1rem;
  border: 2px solid #ffcc00;
  border-radius: 1rem;
  background: #4a3625;
  color: #fff6d5;
  font-size: 1rem;
  outline: none;
  transition: border-color 0.3s ease, background 0.3s ease;
}

input:focus {
  border-color: #ffd700;
  background: #5c432f;
}

/* Botones */
button {
  padding: 1rem 2rem;
  border-radius: 1rem;
  font-size: 1.2rem;
  font-weight: 700;
  text-transform: uppercase;
  transition: background-color 0.3s ease, transform 0.3s ease;
  cursor: pointer;
  border: none;
  background: #d4af37;
  color: #1a120b;
}

button:hover {
  transform: scale(1.1);
  background: #b8860b;
}

button:disabled {
  background-color: #a67c00;
  color: #5c432f;
  cursor: not-allowed;
}

/* Servicios */
li {
  background: #4a3625;
  padding: 1.5rem;
  border-radius: 1rem;
  box-shadow: 0 10px 30px rgba(255, 215, 0, 0.15);
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
  transition: background 0.3s ease, transform 0.3s ease;
}

li:hover {
  background: #5c432f;
  transform: scale(1.05);
}

li p {
  margin: 0;
  color: #fff6d5;
}

/* Pie de página */
.p-4 {
  background: #3e2c1c;
  text-align: center;
  font-size: 0.9rem;
  color: #caa472;
  border-bottom-left-radius: 2rem;
  border-bottom-right-radius: 2rem;
  padding: 1rem;
}

/* Responsive Design */
@media (max-width: 768px) {
  .max-w-4xl {
    border-radius: 3rem;
    padding: 1.5rem;
  }
  
  .p-8.bg-gradient-to-r h1 {
    font-size: 2.5rem;
  }
  
  .text-green-500 {
    font-size: 2rem;
  }
}
@media (max-width: 480px) {
  /* Fondo general */
.min-h-screen {
  margin-top: 45%;
}

}


</style>