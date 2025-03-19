<template>
    <div class="bota">
      <!-- Botón para mostrar el formulario -->
       <div class="caja">
        <button @click="mostrarFormulario">
        Programar Entrenamiento
      </button>
      <button class="volver">
        volver
      </button>
      
    </div>
      <!-- Formulario de programación de entrenamiento -->
      <div v-if="showForm">
        <form @submit.prevent="crearEntrenamiento">
          <button  type="button" @click="cancelarFormulario">Cancelar</button>
          <div>
            <label for="lugar">Lugar:</label>
            <input type="text" v-model="nuevoEntrenamiento.lugar" required />
          </div>
          <div>
            <label for="horaInicio">Hora de inicio:</label>
            <input type="time" v-model="nuevoEntrenamiento.horaInicio" required />
          </div>
          <div>
            <label for="duracion">Duración (en horas):</label>
            <input type="number" v-model="nuevoEntrenamiento.duracion" required min="1" />
          </div>
          <div>
            <label for="descripcion">Descripción:</label>
            <textarea v-model="nuevoEntrenamiento.descripcion"></textarea>
          </div>
          <div>
            <label for="horaFinalizacion">Hora de finalización:</label>
            <input type="time" :value="calcularHoraFinalizacion()" readonly />
          </div>
  
          <!-- Foto de la cancha (opcional) -->
          <div v-if="nuevoEntrenamiento.fotoCancha === null">
            <label for="fotoCancha">Foto de la cancha (opcional):</label>
            <input type="file" @change="handleFileChange" />
          </div>
          <!-- Mostrar la foto solo si se seleccionó una -->
          <div v-if="nuevoEntrenamiento.fotoCancha">
            <strong>Foto de la cancha:</strong><br />
            <img :src="nuevoEntrenamiento.fotoCancha" alt="Foto de la cancha" width="100" />
          </div>
  
          <div>
            <label>¿Es para hoy?</label>
            <!-- Botones circulares para elegir si es para hoy o para otro día -->
            <button type="button" :class="{'selected': esParaHoy}" @click="esParaHoy = true">
              Hoy
            </button>
            <button type="button" :class="{'selected': !esParaHoy}" @click="esParaHoy = false">
              Otro día
            </button>
          </div>
          <div v-if="!esParaHoy">
            <label for="fecha">Seleccionar fecha:</label>
            <input type="date" v-model="nuevoEntrenamiento.fecha" required />
          </div>
  
          <button class="volver" type="submit">Crear Entrenamiento</button>
          <div v-if="error" class="error">
        Ya hay un entrenamiento programado a esa hora.
      </div>
           <!-- Botón de Cancelar -->
        </form>
      </div>
  
      <!-- Mensaje de error si ya existe un entrenamiento en el mismo horario -->
      
  
      <!-- Lista de entrenamientos programados (solo visible si no se está mostrando el formulario) -->
      <div v-if="!showForm && entrenamientos.length > 0">
        <h3>Entrenamientos Programados</h3>
        <ul>
          <li v-for="(entrenamiento, index) in entrenamientos" :key="index">
            <strong>Lugar:</strong> {{ entrenamiento.lugar }}<br />
            <strong>Hora de inicio:</strong> <p>{{ convertirAHora12(entrenamiento.horaInicio) }}</p>
            <strong>Duración:</strong> {{ entrenamiento.duracion }} horas<br />
            <strong>Descripción:</strong> {{ entrenamiento.descripcion }}<br />
            <strong>Hora de finalización:</strong> {{ entrenamiento.horaFinalizacion }}<br />
            <strong>Fecha:</strong> {{ mostrarFecha(entrenamiento.fecha) }}<br />
            <strong>Foto de la cancha:</strong><br />
            <img v-if="entrenamiento.fotoCancha" :src="entrenamiento.fotoCancha" alt="Foto de la cancha" width="100" />
            <br />
            <!-- Botón para eliminar el entrenamiento -->
            <button @click="eliminarEntrenamiento(index)">cancelar</button>
          </li>
        </ul>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        showForm: false,
        esParaHoy: true,
        nuevoEntrenamiento: {
          lugar: "",
          horaInicio: "",  // Se asegura que este campo esté vacío inicialmente
          duracion: 1,
          descripcion: "",
          horaFinalizacion: "",
          fotoCancha: null,
          fecha: new Date().toISOString().split("T")[0], // Por defecto, la fecha es hoy
        },
        entrenamientos: [],
        error: false,
      };
    },
    methods: {
      // Convertir la hora a formato de 12 horas
      convertirAHora12(hora) {
        let [h, m] = hora.split(":").map(Number);
        const ampm = h >= 12 ? "PM" : "AM";
        h = h % 12;
        h = h ? h : 12; // El 0 debe convertirse en 12
        return `${h}:${String(m).padStart(2, "0")} ${ampm}`;
      },
  
      // Calcular la hora de finalización automáticamente
      calcularHoraFinalizacion() {
        if (this.nuevoEntrenamiento.horaInicio && this.nuevoEntrenamiento.duracion) {
          let [hora, minutos] = this.nuevoEntrenamiento.horaInicio.split(":").map(Number);
          hora += Number(this.nuevoEntrenamiento.duracion);
          const horaFinal = `${String(hora).padStart(2, "0")}:${String(minutos).padStart(2, "0")}`;
          return this.convertirAHora12(horaFinal); // Convertir al formato de 12 horas
        }
        return "";
      },
  
      // Crear un nuevo entrenamiento
      crearEntrenamiento() {
        const horaFinalizacion = this.calcularHoraFinalizacion();
        const nuevoEntrenamiento = {
          ...this.nuevoEntrenamiento,
          horaFinalizacion,
        };
  
        // Verificar conflictos de horario solo si es la misma fecha
        const existeConflicto = this.entrenamientos.some((entrenamiento) => {
          return (
            entrenamiento.fecha === nuevoEntrenamiento.fecha && // Misma fecha
            !(
              nuevoEntrenamiento.horaInicio >= entrenamiento.horaFinalizacion || // Nuevo después del existente
              nuevoEntrenamiento.horaFinalizacion <= entrenamiento.horaInicio // Nuevo antes del existente
            )
          );
        });
  
        if (existeConflicto) {
          this.error = true;
        } else {
          this.entrenamientos.push(nuevoEntrenamiento); // Agregar a la lista
          this.cancelarFormulario(); // Limpiar el formulario
        }
      },
  
      // Función para mostrar "Hoy" en lugar de la fecha actual
      mostrarFecha(fecha) {
        const hoy = new Date().toISOString().split("T")[0];
        return fecha === hoy ? "Hoy" : fecha;
      },
  
      // Manejar selección de foto
      handleFileChange(event) {
        const file = event.target.files[0];
        if (file) {
          this.nuevoEntrenamiento.fotoCancha = URL.createObjectURL(file);
        }
      },
  
      // Cancelar el formulario y limpiar datos
      cancelarFormulario() {
        this.showForm = false;
        this.error = false;
        this.nuevoEntrenamiento = {
          lugar: "",
          horaInicio: "",
          duracion: 1,
          descripcion: "",
          horaFinalizacion: "",
          fotoCancha: null,
          fecha: new Date().toISOString().split("T")[0],
        };
      },
  
      // Eliminar entrenamiento por índice
      eliminarEntrenamiento(index) {
        this.entrenamientos.splice(index, 1);
      },
  
      // Mostrar la hora de inicio en formato 12 horas
      mostrarHoraInicio() {
        if (this.nuevoEntrenamiento.horaInicio) {
          return this.convertirAHora12(this.nuevoEntrenamiento.horaInicio);
        }
        return ""; // Si no hay hora de inicio, retorna vacío
      },
  
      mostrarFormulario() {
        this.showForm = true;
      },
    },
  };
  </script>
  
  
  <style scoped>
  /* Contenedor principal */
  .bota{
    background-color: rgba(0, 0, 0, 0.575);
  }
  div {
    font-family: Arial, sans-serif;
    color: #333;
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 20px;
    
  }
  .caja{
    display: flex;
    flex-direction: row;
    gap: 100%;
    
  }
  
  /* Botón principal */
  button {
    background-color: #0cb4a6;
    color: white;
    border: none;
    padding: 10px 20px;
    border-radius: 20px;
    cursor: pointer;
    font-size: 15px;
    transition: background-color 0.3s ease;
    margin: 10px 0;
    /* Agregar box-shadow para darle un efecto de profundidad */
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2); /* Desenfoque y sombra suave */
    /* Agregar text-shadow para darle un efecto al texto */
    text-shadow: 1px 1px 3px rgba(0, 0, 0, 0.2); /* Sombra suave en el texto */
  }
  
  button:hover {
    background-color: #45a098;
    transform: scale(1.05);
    /* Añadir un efecto de sombra más grande cuando el botón está en hover */
    box-shadow: 0 6px 12px rgba(0, 0, 0, 0.3); /* Sombra más intensa en hover */
    color: rgb(5, 5, 5);
    text-shadow: white 0 0 5px;
  }
  
  button.selected {
    background-color: #007BFF;
    color: rgb(0, 0, 0);
    /* Cambiar sombra también cuando el botón está seleccionado */
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.589); /* Sombra más pronunciada cuando se selecciona */
    border: 3px solid black;
  }
  
  /* Formulario */
  form {
    background: #f9f9f9;
    padding: 20px;
    border-radius: 10px;
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
    max-width: 600px;
    width: 100%;
    display: flex;
    flex-direction: column;
    gap: 15px;
    
  }
  
  form div {
    display: flex;
    flex-direction: column;
    
  }
  
  label {
    font-weight: bold;
    margin-bottom: 5px;
  }
  
  input,
  textarea {
    width: 100%;
    padding: 10px;
    border: 1px solid #ccc;
    border-radius: 5px;
    font-size: 14px;
  }
  
  input:focus,
  textarea:focus {
    outline: none;
    border-color: #007BFF;
  }
  
  /* Botones del formulario */
  form button {
    align-self: flex-start;
  }
  
  /* Foto de la cancha */
  img {
    border-radius: 5px;
    margin-top: 10px;
  }
  
  /* Lista de entrenamientos */
  
  
  li {
    background: #fff;
    padding: 15px;
    border: 1px solid #ddd;
    border-radius: 5px;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
    display: flex;
    flex-direction: column;
    gap: 10px;
    
  }
  
  li strong {
    display: inline-block;
    
  }
  
  .error {
    color: red;
    font-weight: bold;
    margin: 10px 0;
  }
  
  /* Alinear botones dentro de cada tarjeta */
  li button {
    align-self: flex-end;
    
  }
  /* Lista de entrenamientos */
  ul{
    padding: 0;
    margin-top: 20px;
    list-style: none;
    display: flex;
    flex-wrap: wrap;
    gap: 20px;
    justify-content: center;
    flex-direction: row;
    justify-content: flex-start;
  }
  
  li {
    background: linear-gradient(135deg, #feffff, #f4f800b7);
    border-radius: 15px;
    box-shadow: 0 6px 10px rgb(255, 255, 255);
    padding: 20px;
    width: 280px;
    display: flex;
    flex-direction: column;
    gap: 10px;
    position: relative;
    transition: transform 0.3s ease, box-shadow 0.3s ease;
    border: 2px solid black;
  
  }
  li:hover {
    transform: scale(1.05);
    box-shadow: 0 6px 30px rgb(255, 255, 255);
    background: linear-gradient(135deg, #feffff, #b8bb06de);
  }
  
  li strong {
    font-size: 16px;
    color: #024b9e;
    font-weight: bold;
    text-transform: uppercase;
    letter-spacing: 1px;
  }
  
  li img {
    border-radius: 12px;
    max-width: 100%;
    height: auto;
    transition: transform 0.3s ease;
  }
  
  li img:hover {
    transform: scale(1.1);
  }
  
  li p {
    font-size: 14px;
    color: #555;
    line-height: 1.5;
  }
  
  li button {
    background-color: #ef5350;
    color: white;
    border: none;
    padding: 8px 12px;
    border-radius: 10px;
    font-size: 14px;
    cursor: pointer;
    align-self: flex-end;
    transition: background-color 0.3s ease, transform 0.2s ease;
  }
  
  li button:hover {
    background-color: #e53935;
    transform: translateY(-2px);
  }
  
  /* Encabezado de la sección */
  h3 {
    color: #ffffff;
    font-size: 26px;
    margin-bottom: 15px;
    text-decoration: underline white;
    text-align: center;
    font-weight: bold;
    text-transform: uppercase;
    letter-spacing: 2px;
    text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.2);
    /* Borde negro alrededor de la letra */
    -webkit-text-stroke: 1.3px black; /* Borde negro con grosor de 1px */
    text-stroke: 4px black; /* Para compatibilidad con otros navegadores */
  }
  
  /* Centrado de la lista */
  div > h3 {
    display: flex;
    flex-direction: column;
    align-items: center;
  }
  
  /* Animaciones sutiles */
  @keyframes fadeIn {
    from {
      opacity: 0;
      transform: translateY(10px);
    }
    to {
      opacity: 1;
      transform: translateY(0);
    }
  }
  
  li {
    animation: fadeIn 0.5s ease-in-out;
  }
  
  .volver{
    background-image: url("https://i.pinimg.com/736x/82/77/8d/82778d6d72c05cf2808e3bd2bcaeb823.jpg");
    color: black;
    box-shadow: rgb(255, 255, 255) 0 0 40%;
    font-size: 120%;
  }
  .volver:hover{
    color: rgb(255, 255, 255);
    box-shadow: rgb(255, 255, 255) 0 0 40%;
    font-size: 120%;
  }
  </style>