
<template>
  <div class="flexjustify-center">
    <!-- Botón para abrir el modal -->
    <button
      @click="abrirModal"
      class="hola"
    >
      <img class="tamaño_img" src="https://cdn-icons-png.flaticon.com/512/1636/1636054.png" alt="">
    </button>

    <!-- Modal -->
    <transition name="modal">
      <div
        v-if="modalAbierto"
        class="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50 backdrop-blur-md z-50"
      >
        <div class="bg-white p-6 rounded-2xl shadow-2xl w-[400px] flex flex-col border border-gray-200 scale-in">
          <h2 class="txt">
            <span class="text-red-600text-3xl">⚠</span> Reportar Usuario
          </h2>

          <!-- Selección de motivo -->
          <label class="text-gray-700 font-medium mb-2">Motivo del reporte:</label>
          <select
            v-model="motivoSeleccionado"
            class="p-2 border rounded-xl focus:ring-4 focus:ring-red-500 transition-all duration-300 outline-none"
          >
            <option value="">Seleccione un motivo...</option>
            <option v-for="(opcion, index) in opcionesReporte" :key="index" :value="opcion">
              {{ opcion }}
            </option>
          </select>

          <!-- Campo de descripción con animación -->
          <transition name="fade">
            <div v-if="motivoSeleccionado" class="mt-4">
              <label class="">Motivo:</label>
              <textarea
                v-model="descripcion"
                placeholder="Explica qué sucedió..."
                class="w-full p-2 border rounded-xl resize-none h-24 focus:ring-4 focus:ring-red-500 transition-all duration-300 outline-none"
              ></textarea>
            </div>
          </transition>

          <!-- Botones -->
          <div class="flex justify-between items-center mt-6">
            <button
              @click="cerrarModal"
              class="px-4 py-2 bg-gray-300 text-gray-800 rounded-full hover:bg-gray-400 hover:scale-105 transition-all duration-300"
            >
              Cancelar
            </button>
            <button
              @click="enviarReporte"
              class="px-6 py-2 bg-red-600 text-white rounded-full shadow-md hover:bg-red-700 hover:scale-105 transition-all duration-300 disabled:opacity-50 disabled:cursor-not-allowed"
              :disabled="!motivoSeleccionado || !descripcion"
            >
              Enviar Reporte
            </button>
          </div>
        </div>
      </div>
    </transition>
  </div>
</template>

<script>
import { useUsuarios } from '@/stores/usuario';// 👈 Asegúrate de que la ruta sea correcta

export default {
  props: {
    documentoReportado: {
      type: String,
      required: true
    }
  },
  data() {
    return {
      modalAbierto: false,
      motivoSeleccionado: "",
      descripcion: "",
      opcionesReporte: [
        "Nombre inapropiado",
        "Foto de perfil inapropiada",
        "Descripción inapropiada",
        "Comportamiento tóxico",
        "Spam o publicidad no deseada",
        "Acoso o intimidación",
        "Contenido ofensivo o violento",
        "Suplantación de identidad",
        "Otro",
      ],
    };
  },
  methods: {
    abrirModal() {
      this.modalAbierto = true;
    },
    cerrarModal() {
      this.modalAbierto = false;
      this.motivoSeleccionado = "";
      this.descripcion = "";
    },
    enviarReporte() {
      if (this.motivoSeleccionado && this.descripcion) {
        const usuariosStore = useUsuarios(); // ✅ Ya funciona porque está importado arriba
        const documentoReportante = usuariosStore.usuario.documento;

        const reporte = {
          documento_reportado: this.documentoReportado,
          documento_reportante: documentoReportante,
          motivo: this.motivoSeleccionado,
          descripcion: this.descripcion,
          fecha_reporte: new Date().toISOString()
        };

        fetch('http://127.0.0.1:8000/reportar_usuario/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(reporte)
        })
        .then(res => {
          if (!res.ok) throw new Error('Error al enviar el reporte');
          return res.json();
        })
        .then(data => {
          alert("✅ Tu reporte ha sido enviado correctamente.");
          console.log("Reporte registrado con ID:", data.reporte_id);
          this.cerrarModal();
        })
        .catch(error => {
          console.error("❌ Error al enviar reporte:", error);
          alert("❌ Ocurrió un error al enviar el reporte.");
        });
      } else {
        alert("⚠️ Por favor selecciona un motivo y escribe una descripción.");
      }
    }
  },
};
</script>

<style scoped>
.flexjustify-center{
  font-family: Verdana, Geneva, Tahoma, sans-serif;
  display: flex;
  justify-content:flex-start;
}
/* Animación de entrada y salida del modal */
.modal-enter-active,
.modal-leave-active {
  transition: opacity 0.3s ease-in-out, transform 0.3s ease-in-out;
}
.modal-enter,
.modal-leave-to {
  opacity: 0;
  transform: scale(0.9);
}

/* Fondo del modal con efecto de desenfoque */
.bg-black {
  backdrop-filter: blur(8px);
}

/* Estilo del contenedor del modal */
.scale-in {
  animation: scaleIn 0.3s ease-in-out;
}

@keyframes scaleIn {
  from {
    transform: scale(0.8);
    opacity: 0;
  }
  to {
    transform: scale(1);
    opacity: 1;
  }
}

/* Diseño del modal */
.bg-white {
  background: linear-gradient(to bottom, #5b5b5b, #393939);
  border-radius: 18px;
  padding: 24px;
  box-shadow: 0px 15px 30px rgba(0, 0, 0, 0.15);
  border: 1px solid #e0e0e0;
  max-width: 420px;
  color: white;
  width: 90%;
}

/* Botón de reportar */
.bg-gradient-to-r {
  transition: all 0.3s ease-in-out;
  padding: 12px 18px;
  border-radius: 25px;
  font-weight: bold;
  text-transform: uppercase;
  font-size: 14px;
}
.bg-gradient-to-r:hover {
  transform: scale(1.08);
  box-shadow: 0px 8px 16px rgba(255, 0, 0, 0.5);
}
.txt {
  color: #d90429; /* Rojo intenso */
  font-weight: bold;
  font-size: 18px;
  text-transform: uppercase;
  letter-spacing: 1px;
  text-shadow: 2px 2px 5px rgba(255, 0, 0, 0.5); /* Brillo rojo */
  animation: parpadeo 1.5s infinite alternate;
  margin-bottom: 5%;
  text-align: center;
}

/* Efecto de parpadeo para más impacto */
@keyframes parpadeo {
  from {
    opacity: 0.1;
  }
  to {
    opacity: 1;
  }
}

/* Select y textarea */
select,
textarea {
  width: 100%;
  padding: 12px;
  border-radius: 12px;
  border: 1px solid #d1d1d1;
  transition: all 0.3s ease-in-out;
  font-size: 15px;
  background: #f5f5f5;
  outline: none;
}
select:focus,
textarea:focus {
  border-color: #ff4d4d;
  box-shadow: 0px 0px 12px rgba(255, 77, 77, 0.3);
  
}

/* Animación del campo de descripción */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease-in-out, transform 0.2s ease-in-out;
}
.fade-enter,
.fade-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}

/* Estilos de los botones */
button {
  transition: all 0.3s ease-in-out;
  border-radius: 20px;
  padding: 10px 16px;
  font-size: 14px;
  font-weight: bold;
}

/* Botón de cancelar */
.bg-gray-300 {
  background: #f0f0f0;
}
.bg-gray-300:hover {
  background: #282323;
  color: white;
}

/* Botón de enviar */
.bg-red-600 {
  background: linear-gradient(to right, #ff4d4d, #cc0000);
  color: white;
}
.bg-red-600:hover {
  background: linear-gradient(to right, #cc0000, #990000);
  color: #9a9a9a;
}

/* Deshabilitar botón */
.disabled {
  opacity: 0.5;
  cursor: not-allowed;
}
.hola {
  background-color: transparent;
  border: none;
  width: 80px; /* Tamaño fijo */
  height: 80px;
  cursor: pointer;
  transition: transform 0.2s ease-in-out;
}

.hola:hover {
  transform: scale(1.1);
}

.tamaño_img {
  width: 100%;
  height: 100%;
  object-fit: contain; /* Mantiene la proporción */
  transition: box-shadow 0.3s ease-in-out, border 0.3s ease-in-out;
  
}

.hola:hover .tamaño_img {

  box-shadow: 0px 4px 10px rgba(255, 0, 0, 0.5); /* Sombra roja */
  border-radius: 10px; /* Esquinas redondeadas */
  background-color: #ff000056;

}


</style>