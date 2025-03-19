<template>


<header>
  <headerapp></headerapp>

</header>



  <section class="formulario_join">
    <div class="form-card1">
  <div class="form-card2">
    <form @submit.prevent="enviarFormulario" class="form">
      <h1 id="equipo_titulo"> Únete a Nuestro Equipo de Fútbol</h1>
      <p class="form-heading"></p>

      <div class="form-field">
        <input
          required
          placeholder="Digite su nombre"
          class="input-field"
          v-model="insertar.nombre"
          type="text"
        />
      </div>

      <div class="form-field">
        <input
          required
          placeholder="Digite su edad"
          class="input-field"
          v-model="insertar.Edad"
          type="number"
        />
      </div>
      <div class="form-field">
    <select v-model="insertar.posicion" required class="input-field">
      <option class="options_var" disabled value="">Seleccione una posición de juego</option>
      <option class="options_var" value="Delantero">Delantero</option>
      <option class="options_var" value="Defensa">Defensa</option>
      <option class="options_var" value="Centrocampista">Centrocampista</option>
      <option class="options_var" value="Portero">Portero</option>
      <option class="options_var" value="Lateral Derecho">Lateral Derecho</option>
      <option class="options_var" value="Lateral Izquierdo">Lateral Izquierdo</option>
      <option class="options_var" value="Extremo Derecho">Extremo Derecho</option>
      <option class="options_var" value="Extremo Izquierdo">Extremo Izquierdo</option>
      <option class="options_var" value="Mediocentro Defensivo">Mediocentro Defensivo</option>
    </select>
  </div>

      <div class="form-field">
        <input
          required
          placeholder="Digite su Correo electrónico"
          class="input-field"
          v-model="insertar.email"
          type="email"
        />
      </div>

      <div class="form-field">
        <input
          required
          placeholder="Digite su celular"
          class="input-field"
          v-model="insertar.celular"
          type="text"
        />
      </div>

      <div class="form-field">
        <select v-model="insertar.equipo" class="input-field" required>
          <option class="options_var" disabled value="">Seleccione un equipo</option>
          <option class="options_var" v-for="equipo in equipos" :key="equipo">{{ equipo }}</option>
        </select>
      </div>

      <div >
        <button
          id="enviar-boton"
          @click="cargarDatosDesdeStorage"
          class="sendMessage-btn"
          type="button">
        </button>
      </div>
      <button class="sendMessage-btn" type="submit">Enviar Solicitud</button>
    </form>
  </div>
</div>
  </section>
</template>

<script>
import axios from 'axios';
import { ref, onMounted } from 'vue';
import Swal from 'sweetalert2';
import Headerapp from './Headerapp.vue';

export default {
  components : {
    Headerapp

  },
  setup() {
    const insertar = ref({
      nombre: '',
      posicion: '',
      email: '',
      celular: '',
      Edad : '',
      equipo: ''
    });

    const equipos = ref([]);
    const obtenerEquipos = async () => {
      try {
        const response = await axios.get('http://localhost:8000/equipo/lista');
        equipos.value = response.data;
      } catch (error) {
        console.error('Error al obtener los equipos:', error);
        Swal.fire({
          icon: 'error',
          title: 'Error',
          text: 'No se pudieron cargar los equipos. Intenta de nuevo más tarde.',
        });
      }
    };

    const cargarDatosDesdeStorage = () => {
      const datosusuario = JSON.parse(localStorage.getItem('usuario'));
      if (datosusuario) {
        insertar.value = {
          nombre: datosusuario.nombreUsuario || '',
          posicion: datosusuario.posicion || '',
          email: datosusuario.correo || '',
          celular: datosusuario.celular || '',
          Edad : datosusuario.Edad || '',
          posicion : datosusuario.posicion || '',
          Equipo: datosusuario.equipo || '',
        };
        Swal.fire({
          icon: 'success',
          title: 'Datos cargados',
          text: 'Los datos del usuario se han cargado correctamente .',
          timer:2000,
        });
      } else {
        Swal.fire({
          icon: 'warning',
          title: 'Sin datos',
          text: 'No se encontraron datos del usuario.',
        });
      }
    };

    const enviarFormulario = async () => {
      const result = await Swal.fire({
        title: '¿Estás seguro?',
        text: `¿Quieres enviar tu solicitud para unirte al equipo ${insertar.value.equipo}?`,
        icon: 'warning',
        showCancelButton: true,
        confirmButtonText: 'Sí, enviar',
        cancelButtonText: 'No, cancelar',
      });

      if (result.isConfirmed) {
        try {
          const response = await axios.post('http://localhost:8000/jugadores', insertar.value);

          if (response.status === 200) {
            Swal.fire({
              icon: 'success',
              title: 'Solicitud enviada',
              text: 'Tu solicitud para unirte al equipo ha sido enviada correctamente.',
            });

            insertar.value = {
              nombre: '',
              posicion: '',
              email: '',
              celular: '',
              Edad : '',
              equipo: ''
            };
          } else {
            Swal.fire({
              icon: 'error',
              title: 'Error',
              text: 'Hubo un problema al enviar tu solicitud. Inténtalo de nuevo.',
            });
          }
        } catch (error) {
          Swal.fire({
            icon: 'error',
            title: 'Error',
            text: 'Hubo un problema al enviar tu solicitud. Inténtalo de nuevo.',
          });
          console.error('Error al enviar la solicitud:', error);
        }
      }
    };

    onMounted(obtenerEquipos,cargarDatosDesdeStorage());

    return {
      insertar,
      equipos,
      enviarFormulario,
      cargarDatosDesdeStorage,
    };
  },
};
</script>


<style scoped>

.form {
  display: flex;
  flex-direction: column;
  align-self: center;
  font-family: inherit;
  gap: 20px;
  padding-inline: 2em;
  padding-bottom: 0.4em;
  background-color: #000000;
  background-color: #0a192f;
  border-radius: 20px;

}
.formulario_join {
  display: inline-block;
  transform: translate(15%, 15%); /* Mueve verticalmente */
}

.options_var{
  background-color: #ffffff;
  color: black;
}



.form-heading {
  text-align: center;
  margin: 2em;
  color: #FFD700;
  font-size: 1.2em;
  background-color: transparent;
  align-self: center;
}

.form-field {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5em;
  border-radius: 10px;
  padding: 0.6em;
  border: none;
  outline: none;
  color: white;
  background-color: #171717;
  box-shadow: inset 2px 5px 10px rgb(5, 5, 5);
}

.input-field {
  background: none;
  border: none;
  outline: none;
  width: 100%;
  color: #ccd6f6;
  padding-inline: 1em;
  
}

.sendMessage-btn {
  cursor: pointer;
  margin-bottom: 3em;
  padding: 1em;
  border-radius: 10px;
  border: none;
  outline: none;
  background-color: transparent;
  color: white;
  font-weight: bold;
  outline: 1px solid #FFD700;
  transition: all ease-in-out 0.3s;
}

.sendMessage-btn:hover {
  transition: all ease-in-out 0.3s;
  background-color: #FFD700;
  color: #000;
  cursor: pointer;
  box-shadow: inset 2px 5px 10px rgb(5, 5, 5);
}

.form-card1 {
  background-image: linear-gradient(163deg, #ffd900 0%, #000000 100%);
  border-radius: 22px;
  transition: all 0.3s;
}

.form-card1:hover {
  box-shadow: 0px 0px 30px 1px rgba(100, 255, 218, 0.3);
}

.form-card2 {
  border-radius: 0;
  transition: all 0.2s;
  
}

.form-card2:hover {
  transform: scale(0.98);
  border-radius: 20px;
}


#enviar-boton{
  display: none;
}
@media (max-width: 480px) {
  .formulario_join {
    padding: 8px;
    max-width: 100%;
  }

  #equipo_titulo {
    font-size: 0.95rem;
  }

  .Form_input,
  select {
    font-size: 0.85rem;
    padding: 5px;
  }

  button.formulario_boton {
    font-size: 0.85rem;
    padding: 7px;
  }
}

</style>

