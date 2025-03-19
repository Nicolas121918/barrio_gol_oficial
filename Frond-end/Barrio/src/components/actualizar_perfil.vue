<template>
 
  <header>
    <headerapp></headerapp>

  </header>

  <div class="actualizar_caja">

  <section v-if="mostrar" class="Actualizar_contenedor">
    <h1>{{ movistore.usuario.documento }}</h1>
    <h1>{{ movistore.usuario.equipo_tiene }}</h1>
    <h1>{{ movistore.usuario.Edad }}</h1>
    <router-link class="volver_actualizar" to="/Perfil">volver</router-link>
    <h1 class="actualizar_h1">¿Qué desea actualizar?</h1>
    <button @click="cambiar_foto" class="Actualizar_button">Cambiar Foto de Perfil</button>
    <br /><br />
    <button @click="cambiar_nombre" class="Actualizar_button">Cambiar Nombre</button>
    <br /><br />
    <button @click="cambiar_ciudad" class="Actualizar_button">Cambiar Ciudad</button>
    <br /><br />
    <button @click="cambiar_descripcion" class="Actualizar_button">Cambiar Descripción</button>
    <br /><br />
  </section>


  <!-- Formulario para cambiar foto -->
  <section v-if="foto" class="nombre">
    <button @click="volver"><img class="salir" src="../assets/iconos header/emblemunreadable_93487 (1).png" alt="Salir" /></button>
    <form @submit.prevent="actualizarFoto">
      <label>Seleccione foto de perfil:</label>
      <input type="file" @change="onFileChange" accept="image/*" />
      <button class="boton_actu1" type="submit">Actualizar Foto</button>
    </form>
  </section>

  <!-- Formulario para cambiar nombre -->
  <section v-if="nombre" class="nombre">
    <button @click="volver"><img class="salir" src="../assets/iconos header/emblemunreadable_93487 (1).png" alt="Salir" /></button>
    <form @submit.prevent="actualizarNombre">
      <label>Nuevo Nombre:</label>
      <input class="lineal" v-model="nuevoNombre" type="text" />
      <br>
      <button class="boton_actu" type="submit">Actualizar Nombre</button>
    </form>
  </section>

  <!-- Formulario para cambiar ciudad -->
<section v-if="ciudad" class="nombre">
  <button @click="volver"><img class="salir" src="../assets/iconos header/emblemunreadable_93487 (1).png" alt="Salir" /></button>
  <form @submit.prevent="actualizarCiudad">
    <label>Nueva Ciudad:</label>
    <input v-model="nuevaCiudad" class="lineal" type="text" />
    <br>
    <button class="boton_actu" type="submit">Actualizar Ciudad</button>
  </form>
</section>

  <!-- Formulario para cambiar descripción -->
<section v-if="descripcion" class="nombre">
  <button @click="volver"><img class="salir" src="../assets/iconos header/emblemunreadable_93487 (1).png" alt="Salir" /></button>
  <form @submit.prevent="actualizarDescripcion">
    <label>Descripción:</label>
    <textarea class="lineal" v-model="nuevaDescripcion" type="text"></textarea>
    <button class="boton_actu" type="submit">Actualizar Descripción</button>
  </form>
</section>
</div>

</template>

<script setup>
import { ref } from "vue";
import axios from "axios";
import Swal from 'sweetalert2';
import Headerapp from "./Headerapp.vue";
import { useUsuarios } from "@/stores/usuario";

const movistore = useUsuarios();
const mostrar = ref(true);
const nombre = ref(false);
const ciudad = ref(false);
const descripcion = ref(false);
const foto = ref(false);
const actualizar = useUsuarios();

const nuevoNombre = ref("");
const nuevaCiudad = ref("");
const nuevaDescripcion = ref("");
const archivoSeleccionado = ref(null);


// Definir las variables reactivas
const fileInput = ref('');  // Para almacenar la URL de la imagen

const onFileChange = (e) => {
  archivoSeleccionado.value = e.target.files[0]; // Captura el primer archivo seleccionado
};

const cambiar_foto = () => {
  mostrar.value = false;
  foto.value = true;
};
const cambiar_nombre = () => {
  mostrar.value = false;
  nombre.value = true;
};
const cambiar_ciudad = () => {
  mostrar.value = false;
  ciudad.value = true;
};
const cambiar_descripcion = () => {
  mostrar.value = false;
  descripcion.value = true;
};
const volver = () => {
  mostrar.value = true;
  nombre.value = false;
  ciudad.value = false;
  descripcion.value = false;
  foto.value = false;
};

// Función para actualizar la foto de perfil
const actualizarFoto = async () => {
  const correo = movistore.usuario?.correo;
  console.log("correo" + movistore.usuario.correo)

  if (!correo) {
    console.error("Correo no encontrado.");
    return;
  }

  // Verificar que un archivo haya sido seleccionado
  if (!archivoSeleccionado.value) {
    console.error("No se ha seleccionado una imagen.");
    return;
  }

  // Crear un FormData para enviar el archivo
  const formData = new FormData();
  formData.append('file', archivoSeleccionado.value);  // Asegúrate de pasar el archivo correctamente

  try {
    // Enviar el archivo al servidor para actualizar la foto
    const response = await axios.put(`http://127.0.0.1:8000/usuario/actualizar-foto?correo=${correo}`, formData);
    

    // Verificar que la respuesta sea exitosa
    if (response.status === 200) {
      Swal.fire({
        icon: 'success',
        title: '¡Foto actualizada correctamente!',
        text: 'Tu foto de perfil se ha actualizado exitosamente.',
        confirmButtonText: 'Aceptar',
      });

      // Obtener la nueva ruta de la imagen desde la respuesta del backend
      const nuevaRuta = response.data.ruta;  // Ahora estamos usando "ruta" en lugar de "fileInput"

      // Actualizar el objeto usuario en localStorage con la nueva ruta
      const updatedUser = { ...movistore.usuario, fileInput: nuevaRuta };  // Usamos "fileInput" en lugar de "imagen"
      actualizar.setUsuario(updatedUser);

      // Actualizar la imagen de perfil en la interfaz de usuario
      fileInput.value = nuevaRuta;  // Actualizamos la imagen reactiva

      // También actualizar el valor de fileInput en el objeto del usuario para evitar desincronización
      movistore.usuario.fileInput = nuevaRuta;  // Asegurando que el estado local también se actualice
    }
  } catch (error) {
    console.error('Error al actualizar la foto:', error);
    console.log(error)
    Swal.fire({
      icon: 'error',
      title: 'Error al actualizar la foto',
      text: 'Hubo un problema al actualizar tu foto. Inténtalo de nuevo.',
      confirmButtonText: 'Aceptar',
    });
  }
};


const actualizarNombre = async () => {
  try {
    // Verificar que se haya ingresado un nuevo nombre
    if (!nuevoNombre.value.trim()) {
      Swal.fire({
        icon: "warning",
        title: "Nombre vacío",
        text: "Por favor, ingresa un nuevo nombre.",
      });
      return;
    }

    // Obtener el correo desde localStorage
    const usuario = movistore.usuario.correo
    
    // Verificar si el objeto 'usuario' es válido
    console.log(usuario);  // Aquí verificamos el contenido de 'usuario'

    if (!usuario) {
      Swal.fire({
        icon: "error",
        title: "Usuario no encontrado",
        text: "No se encontró el usuario en el sistema.",
      });
      return;
    }

    const correo = movistore.usuario.correo
    if (!correo) {
      Swal.fire({
        icon: "error",
        title: "Correo no encontrado",
        text: "No se encontró el correo del usuario.",
      });
      return;
    }

    // Crear el cuerpo de la solicitud utilizando URLSearchParams
    const formData = new URLSearchParams();
    formData.append('nombre', nuevoNombre.value);  // Agregar el nuevo nombre

    // Verificar que la URL y los parámetros están correctos
    console.log(`Enviando correo: ${correo}`);
    console.log(`Nuevo nombre: ${nuevoNombre.value}`);

    // Realizar la solicitud PUT al backend
    const response = await axios.put(
      `http://127.0.0.1:8000/usuario/actualizar-nombre?correo=${correo}`,  // Correo en la URL
      formData,  // Enviar el FormData con el nombre
      {
        headers: {
          "Content-Type": "application/x-www-form-urlencoded", // Aseguramos que se envíe como formulario
        },
      }
    );

    // Verificar que la respuesta sea exitosa
    if (response.status === 200) {
      Swal.fire({
        icon: "success",
        title: "Nombre actualizado",
        text: response.data.message || "El nombre se actualizó correctamente.",
      });

      // Aquí actualizamos el atributo 'nombreUsuario' en lugar de agregar uno nuevo
      movistore.usuario.nombreUsuario = nuevoNombre.value;

      // Volver a la vista principal o realizar cualquier acción que necesites
      volver();
    }
  } catch (error) {
    // Manejar errores del backend o de red
    Swal.fire({
      icon: "error",
      title: "Error al actualizar",
      text: error.response?.data?.detail || "Ocurrió un error al actualizar el nombre.",
    });
    console.error("Error al actualizar el nombre:", error);
  }
};


const actualizarCiudad = async () => {
  try {
    // Verificar que se haya ingresado una nueva ciudad
    if (!nuevaCiudad.value.trim()) {
      Swal.fire({
        icon: "warning",
        title: "Ciudad vacía",
        text: "Por favor, ingresa una nueva ciudad.",
      });
      return;
    }

    // Obtener el usuario desde localStorage
    const usuario = movistore.usuario.correo;
    
    // Verificar si el objeto 'usuario' es válido
    if (!usuario) {
      Swal.fire({
        icon: "error",
        title: "Usuario no encontrado",
        text: "No se encontró el usuario en el sistema.",
      });
      return;
    }

    const correo = movistore.usuario.correo;
    if (!correo) {
      Swal.fire({
        icon: "error",
        title: "Correo no encontrado",
        text: "No se encontró el correo del usuario.",
      });
      return;
    }

    // Crear el cuerpo de la solicitud utilizando URLSearchParams
    const formData = new URLSearchParams();
    formData.append('ciudad', nuevaCiudad.value);  // Agregar la nueva ciudad

    // Realizar la solicitud PUT al backend para actualizar la ciudad
    const response = await axios.put(
      `http://127.0.0.1:8000/usuario/actualizar-ciudad?correo=${correo}`,  // Correo en la URL
      formData,  // Enviar el FormData con la ciudad
      {
        headers: {
          "Content-Type": "application/x-www-form-urlencoded", // Aseguramos que se envíe como formulario
        },
      }
    );

    // Verificar que la respuesta sea exitosa
    if (response.status === 200) {
      Swal.fire({
        icon: "success",
        title: "Ciudad actualizada",
        text: response.data.message || "La ciudad se actualizó correctamente.",
      });

      // Actualizar la ciudad en el objeto usuario
      movistore.usuario.ciudad = nuevaCiudad.value;

      // Volver a la vista principal o realizar cualquier acción que necesites
      volver();
    }
  } catch (error) {
    // Manejar errores del backend o de red
    console.error("Error al actualizar la ciudad:", error);
    Swal.fire({
      icon: "error",
      title: "Error al actualizar la ciudad",
      text: "Hubo un problema al actualizar tu ciudad. Inténtalo de nuevo.",
      confirmButtonText: 'Aceptar',
    });
  }
};


const actualizarDescripcion = async () => {
  try {
    // Verificar que se haya ingresado una nueva descripción
    if (!nuevaDescripcion.value.trim()) {
      Swal.fire({
        icon: "warning",
        title: "Descripción vacía",
        text: "Por favor, ingresa una nueva descripción.",
      });
      return;
    }

    // Obtener el usuario desde localStorage
    const usuario = movistore.usuario.correo;
    
    // Verificar si el objeto 'usuario' es válido
    if (!usuario) {
      Swal.fire({
        icon: "error",
        title: "Usuario no encontrado",
        text: "No se encontró el usuario en el sistema.",
      });
      return;
    }

    const correo = movistore.usuario.correo;
    if (!correo) {
      Swal.fire({
        icon: "error",
        title: "Correo no encontrado",
        text: "No se encontró el correo del usuario.",
      });
      return;
    }

    // Crear el cuerpo de la solicitud utilizando URLSearchParams
    const formData = new URLSearchParams();
    formData.append('descripcion', nuevaDescripcion.value);  // Agregar la nueva descripción

    // Realizar la solicitud PUT al backend para actualizar la descripción
    const response = await axios.put(
      `http://127.0.0.1:8000/usuario/actualizar-descripcion?correo=${correo}`,  // Correo en la URL
      formData,  // Enviar el FormData con la descripción
      {
        headers: {
          "Content-Type": "application/x-www-form-urlencoded", // Aseguramos que se envíe como formulario
        },
      }
    );

    // Verificar que la respuesta sea exitosa
    if (response.status === 200) {
      Swal.fire({
        icon: "success",
        title: "Descripción actualizada",
        text: response.data.message || "La descripción se actualizó correctamente.",
      });

      // Actualizar la descripción en el objeto usuario
      movistore.usuario.descripcion = nuevaDescripcion.value;

      // Volver a la vista principal o realizar cualquier acción que necesites
      volver();
    }
  } catch (error) {
    // Manejar errores del backend o de red
    console.error("Error al actualizar la descripción:", error);
    Swal.fire({
      icon: "error",
      title: "Error al actualizar la descripción",
      text: "Hubo un problema al actualizar tu descripción. Inténtalo de nuevo.",
      confirmButtonText: 'Aceptar',
    });
  }
};


</script>

  

<style scoped>
.lineal{
  font-size: 50%;
  background-color: rgb(255, 255, 255);
  text-align: center;
  color: rgb(58, 58, 58);
  text-shadow: 0  2px rgb(238, 255, 0) ;
}
.lineal:hover{
  font-size: 55%;
  background-color: rgb(255, 255, 255);
  text-align: center;
  color: rgb(58, 58, 58);
  text-shadow: 0  2px rgb(238, 255, 0) ;
}
.actualizar_caja{
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  margin-top: 20%;
  margin-left: 25%;
  
  
}
.boton_actu{
  background: rgb(0, 0, 0);
  border: solid white;
  color: white;
  font-size: 50%;
  font-family:Georgia, 'Times New Roman', Times, serif;
}
.boton_actu1{
  background: rgb(0, 0, 0);
  border: solid white;
  color: white;
  font-size: 50%;
  font-family:Georgia, 'Times New Roman', Times, serif;
}
.boton_actu:hover{
  
  border: solid rgb(247, 227, 0);
  color: rgb(230, 242, 2);
  font-size: 60%;
  font-family:Georgia, 'Times New Roman', Times, serif;
}
.volver_actualizar{
  font-size: 200%;
  font-family: Cambria, Cochin, Georgia, Times, 'Times New Roman', serif;
  color: rgb(255, 0, 0);
  border-style: solid;
  text-shadow: 0 0 2px rgb(214, 178, 178);
  background-color: rgb(255, 240, 244);
}
.volver_actualizar:hover{
  color: rgb(0, 0, 0);
  background-color: beige;
  text-shadow: 0 0 2px rgb(0, 238, 255);
}
.salir{
  height: 50px;
  width: 50px;
  margin-left: 90%;

}
.salir:hover{
  transform: scale(1.1);
}
 
.nombre{
  background-color: black;
  font-size: 300%;
  text-align: center;
  font-family: 'Times New Roman', Times, serif;
  border: 10px;
  border-style: solid;
  text-decoration:underline;
  box-shadow: 0 0 10px rgb(251, 255, 255);
  display: flex;
  flex-direction: column;
  width: 80%;
}
.cambiar_nombre{
  background-image: url('');
  font-size: 100%;
  text-shadow: 0 0 5px rgb(3, 73, 100);
  box-shadow: 0 0 10px rgb(4, 95, 131);
  text-align: center;
}
.espacio_nombre{
  font-size: 50%;
  text-align: center;
}
.formulario_nombre{
  margin: 5%;
}
.Actualizar_contenedor{
  background-color: rgb(0, 0, 0);
  height: auto;
  left: 0%;
  width: 150%;
  text-align: center;
  border: 2%;
  margin-left: -40%;
  border-style: solid;
  border-color: aliceblue;
}
.Actualizar_button{
  border: none;
  background-color: none;
  font-size: 200%;
  text-align:left;
  font-family:Cambria, Cochin, Georgia, Times, 'Times New Roman', serif;
  text-decoration:double;
  background-color: rgb(0, 0, 0);
  color: aliceblue;
  width: 100%;
  border-bottom: rgb(253, 253, 253);
  border-left: none;
  border: solid;
  width: 50%;
  text-align: center;
}
.Actualizar_button:hover{
  text-shadow: 1px rgb(56, 56, 56);
  color: rgb(0, 183, 255);
  transform: scale(1.1);
  
}
.actualizar_h1{
  background-color: rgb(255, 255, 255);
  border: 1px;
  border-color: rgb(255, 255, 255);
  border-style: solid;
  text-shadow: 0 0 2px black;
  margin-bottom: 2%;
  width: 100%;
  font-size: 200%;
  left: -5%;
  color: rgb(0, 0, 0);
  font-family:'Lucida Sans', 'Lucida Sans Regular', 'Lucida Grande', 'Lucida Sans Unicode', Geneva, Verdana, sans-serif;
}


@media (max-width: 480px) {
  /* Estilos para pantallas con un ancho máximo de 480px */
  .actualizar_caja{
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  margin-top:100%;
  margin-left: 0%;
  width: 120%
  
}

.Actualizar_contenedor{
  background-color: rgb(0, 0, 0);
  height: auto;
  left: 0%;
  width: 100%;
  text-align: center;
  border: 2%;
  margin-left: 0%;
  font-size: 8px;
  border-style: solid;
  border-color: aliceblue;
}
}


@media (min-width: 481px) and (max-width: 600px) {
  /* Estilos para pantallas entre 481px y 600px */
  .actualizar_caja{
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  margin-top: 50%;
  margin-left: 0%;
  
}

.Actualizar_contenedor{
  background-color: rgb(0, 0, 0);
  height: auto;
  left: 0%;
  width: 120%;
  text-align: center;
  border: 2%;
  margin-left: 35%;
  font-size: 10px;
  border-style: solid;
  border-color: aliceblue;
}
}


@media (min-width: 601px) and (max-width: 768px) {
  /* Estilos para pantallas entre 601px y 768px */
  .actualizar_caja{
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  margin-top: 20%;
  margin-left: 0%;
  
}

.Actualizar_contenedor{
  background-color: rgb(0, 0, 0);
  height: auto;
  left: 0%;
  width: 150%;
  text-align: center;
  border: 2%;
  margin-left: 20%;
  font-size: 10px;
  border-style: solid;
  border-color: aliceblue;
}
}


@media (min-width: 769px) and (max-width: 1024px) {
  /* Estilos para pantallas entre 769px y 1024px */
  .actualizar_caja{
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  margin-top: 10%;
  margin-left: 0%;
  
}

.Actualizar_contenedor{
  background-color: rgb(0, 0, 0);
  height: auto;
  left: 0%;
  width: 120%;
  text-align: center;
  border: 2%;
  margin-left: 0%;
  font-size: 15px;
  border-style: solid;
  border-color: aliceblue;
}
}


@media (min-width: 1025px) and (max-width: 1280px) {
  /* Estilos para pantallas entre 1025px y 1280px */
  .actualizar_caja{
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  margin-top: 10%;
  margin-left: 0%;
  
}

.Actualizar_contenedor{
  background-color: rgb(0, 0, 0);
  height: auto;
  left: 0%;
  width: 120%;
  text-align: center;
  border: 2%;
  margin-left: 0%;
  font-size: 15px;
  border-style: solid;
  border-color: aliceblue;
}
}

@media (min-width: 1281px) and (max-width: 1440px) {
  /* Estilos para pantallas entre 1281px y 1440px */
  .actualizar_caja{
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  margin-top: 20%;
  margin-left: 0%;
  
}

.Actualizar_contenedor{
  background-color: rgb(0, 0, 0);
  height: auto;
  left: 0%;
  width: 120%;
  text-align: center;
  border: 2%;
  margin-left: 0%;
  font-size: 15px;
  border-style: solid;
  border-color: aliceblue;
}
}



@media (min-width: 1441px) and (max-width: 1920px) {
  /* Estilos para pantallas entre 1441px y 1920px */
}

@media (min-width: 1921px) and (max-width: 2560px) {
  /* Estilos para pantallas entre 1921px y 2560px */
}

@media (min-width: 2561px) and (max-width: 3840px) {
  /* Estilos para pantallas entre 2561px y 3840px */
}


@media (min-width: 3841px) and (max-width: 5120px) {
  /* Estilos para pantallas entre 3841px y 5120px */
}





</style>