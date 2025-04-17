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
  <div class="pantalla bg-black flex items-center justify-center">
    <div class="contenedor-principal animacion-entrada">
      <h1 class="titulo mb-6">⚽✨ Emprende con nosotros. El barrio es de los que sueñan. Muy pronto: Barrio Store.</h1>
      <p class="subtitulo mb-8">
        "¡Sé de los primeros vendedores en Barrio Gol y hagamos historia en el barrio!"
      </p>
      <button @click="showModal = true" class="boton-principal">
        🚀 Enviar solicitud para ser vendedor
      </button>
    </div>

    <!-- Modal -->
    <div v-if="showModal" class="modal-fondo">
  <div class="modal-caja animacion-entrada">
    <button @click="showModal = false" class="modal-cerrar">✕</button>
    <h2 class="modal-titulo">Formulario de solicitud</h2>

    <form @submit.prevent="handleSubmit" class="space-y-4">
      <label>
        Nombre completo:
        <input v-model="form.nombre" type="text" placeholder="Nombre completo" class="input-elegante" required />
      </label>

      <label>
        Documento de identidad:
        <input v-model="form.documento" type="text" placeholder="Número de documento" class="input-elegante" required />
      </label>

      <label>
        Empresa o marca:
        <input v-model="form.empresa" type="text" placeholder="Empresa o marca" class="input-elegante" />
      </label>

      <label>
        Correo electrónico:
        <input v-model="form.correo" type="email" placeholder="Correo electrónico" class="input-elegante" required />
      </label>

      <label>
        Número de contacto:
        <input v-model="form.telefono" type="text" placeholder="Número de contacto" class="input-elegante" required />
      </label>

      <label>
        Redes sociales o página web:
        <input v-model="form.redes" type="text" placeholder="Redes sociales o página web" class="input-elegante" />
      </label>

      <label>
        Descripción:
        <textarea v-model="form.descripcion" placeholder="Cuéntanos un poco sobre tu solicitud" class="input-elegante" rows="3"></textarea>
      </label>

      <button type="submit" class="boton-principal w-full">📨 Enviar</button>
    </form>
  </div>
</div>
  </div>
</template>

<script>
import headermobile from './headermobile.vue';
import headerapp from './headerapp.vue';
export default {
  components: {
    headerapp,
    headermobile,
  },
  data() {
    return {
      showModal: false,
      showSuccess: false,
      form: {
        nombre: '',
        empresa: '',
        correo: '',
        telefono: '',
        redes: '',
        descripcion: '',
        documento: '',
      },
    };
  },
  methods: {
    handleSubmit() {
      this.showModal = false;
      this.showSuccess = true;
      setTimeout(() => {
        this.showSuccess = false;
      }, 5000);
      // Aquí podrías enviar los datos a tu backend o Firebase
    },
  },
};
</script>
<style scoped>
/* Fondo principal */
.pantalla {
  all: unset; /* Esto borra casi todo el estilo heredado de Boostrap */
  min-height: 100vh;
}

/* Contenedor principal con efecto de vidrio */
.contenedor-principal {
  background-color: rgba(20, 20, 20, 0.9);
  padding: 3rem;
  border-radius: 2rem;
  border: 1px solid #DAA520;
  box-shadow: 0 0 50px rgba(218, 165, 32, 0.2);
  backdrop-filter: blur(10px);
  text-align: center;
  width: 100%;
  max-width: 800px;
  margin-top: 20%;
}

/* Animación de entrada */
.animacion-entrada {
  animation: fadeIn 1s ease-out both;
}
@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(-20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* Título brillante */
.titulo {
  font-size: 2.2rem;
  font-weight: 900;
  color: #dddddd;
  text-shadow: 0 0 10px #DAA520, 0 0 30px #FFD700;
  animation: resplandor 3s ease-in-out infinite;
}
@keyframes resplandor {
  0%, 100% {
    text-shadow: 0 0 10px #DAA520, 0 0 30px #FFD700;
  }
  50% {
    text-shadow: 0 0 30px #DAA520, 0 0 60px #FFD700;
  }
}

/* Subtítulo */
.subtitulo {
  margin-top: 50px;
  font-size: 1.25rem;
  color: #d1d5db;
}

/* Botón dorado */
.boton-principal {
  background-color: #DAA520;
  color: black;
  margin-top: 50px;
  font-weight: bold;
  padding: 0.75rem 2rem;
  border-radius: 9999px;
  box-shadow: 0 0 10px rgba(218, 165, 32, 0.5);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}
.boton-principal:hover {
  transform: scale(1.05);
  box-shadow: 0 0 20px rgba(218, 165, 32, 0.8);
}

/* Modal */
.modal-fondo {
  position: fixed;
  inset: 0;
  background-color: rgba(0, 0, 0, 0.85);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 50;
}

.modal-caja {
  background-color:   #1f2937;
  border: 2px solid #DAA520;
  border-radius: 1.5rem;
  padding: 2rem;
  width: 100%;
  max-width: 600px;
  box-shadow: 0 0 30px rgba(218, 165, 32, 0.4);
  position: relative;
}

/* Botón de cerrar modal */
.modal-cerrar {
  position: absolute;
  top: 1rem;
  right: 1rem;
  color: #DAA520;
  font-size: 1.5rem;
  font-weight: bold;
  transition: color 0.3s ease;
}
.modal-cerrar:hover {
  color: white;
}

/* Título modal */
.modal-titulo {
  font-size: 2rem;
  font-weight: 600;
  color: #DAA520;
  text-align: center;
  margin-bottom: 1.5rem;
}

/* Inputs */
.input-elegante {
  width: 100%;
  padding: 0.75rem 1rem;
  border: 1px solid #444;
  background-color: #111;
  color: #fff;
  border-radius: 0.75rem;
  transition: border 0.3s ease, box-shadow 0.3s ease;
}
.input-elegante:focus {
  border-color: #DAA520;
  box-shadow: 0 0 10px rgba(218, 165, 32, 0.4);
  outline: none;
}

.modal-fondo {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.7); /* fondo oscuro translúcido */
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: 1rem;
  overflow-y: auto;
}

.modal-caja {
  background: linear-gradient(145deg, #1f2937, #111827); /* fondo degradado oscuro */
  border: 2px solid #DAA520;
  border-radius: 1.5rem;
  padding: 2rem;
  width: 100%;
  max-width: 600px;
  box-shadow: 0 0 30px rgba(218, 165, 32, 0.4);
  position: relative;
  max-height: 90vh; /* para que no se salga de la pantalla */
  overflow-y: auto; /* permite scroll dentro del modal */
}

/* Opcional: hacer el scroll dentro del modal más elegante */
.modal-caja::-webkit-scrollbar {
  width: 8px;
}
.modal-caja::-webkit-scrollbar-thumb {
  background-color: #DAA520;
  border-radius: 4px;
}
.modal-caja::-webkit-scrollbar-track {
  background: transparent;
}

.modal-cerrar {
  position: absolute;
  top: 1rem;
  right: 1rem;
  background: none;
  border: none;
  color: #DAA520;
  font-size: 1.5rem;
  cursor: pointer;
}

.modal-titulo {
  color: #DAA520;
  font-size: 1.8rem;
  margin-bottom: 1rem;
  text-align: center;
}

.input-elegante {
  width: 100%;
  padding: 0.75rem 1rem;
  background-color: #111827;
  border: 1px solid #DAA520;
  border-radius: 0.75rem;
  color: #fff;
  font-size: 1rem;
  margin-top: 0.25rem;
  margin-bottom: 0.75rem;
}

.input-elegante::placeholder {
  color: #c2c2c2;
}

.boton-principal {
  background-color: #DAA520;
  color: #111827;
  font-weight: bold;
  padding: 0.75rem;
  border-radius: 1rem;
  border: none;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.boton-principal:hover {
  background-color: #ffcf40;
}
label{
  color: white  ;
}
</style>