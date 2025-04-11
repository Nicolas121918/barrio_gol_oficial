<template>
  <div class="inicio_sesion_contenedor">
    <div v-if="isLogin">
      <div class="inicio_sesion_container_titulo">
      <h1 class="inicio_sesion_titulo">Iniciar sesión</h1>
    </div>
      <form class="inicio_sesion_form" @submit.prevent="iniciarSesion">
        <br>

        <div class="frminput">
          <label class="pa" for="correo">Correo electrónico:</label>
          <br>
          <input class="inicio_sesion_cont" placeholder="correo electronico" type="email" id="correo" v-model="correo" required />
          <br>
        </div>
        <div class="frminput">
  <label class="pa" for="password">Contraseña:</label>
  <br>
  <div style="position: relative; display: inline-block;">
    <input 
      class="inicio_sesion_cont" 
      placeholder="contraseña" 
      :type="showPassword ? 'text' : 'password'" 
      id="password" 
      v-model="password" 
      required 
    />
    <button @click="togglePassword" type="button" class="password-toggle">
      <img 
        :src="showPassword ? nover : verimg"
        alt="Toggle password visibility" 
        class="password-icon"
      />
    </button>
  </div>
  <br>
</div>

        <button class="inicio_sesion_boton" type="submit">Iniciar sesión</button>
        <p class="inicio_sesion_letra">
  ¿No tienes cuenta?
  <a href="#" @click.prevent="toggleForm" class="registro-link">Regístrate</a>
</p>
      </form>

    </div>   
    <div  v-else>
      <div class="registro_contenedor">
      <h1 class="registro_titulo">Crear una cuenta</h1>
      </div>
      <form class="registro_form" @submit.prevent="registrarUsuario">
        <div class="frminput">
          <label for="nombre">Nombre</label>
          <input class="registro_cont" type="text" id="nombre" v-model="nombre" required />
        </div>
        <div class="frminput">
          <label for="telefono">Ciudad</label>
          <input class="registro_cont" type="text" id="ciudad" v-model="ciudad" required />
        </div>
        <div class="frminput">
          <label for="telefono">Descripcion</label>
          <input class="registro_cont" type="text" id="Descripcion" v-model="descripcion" required placeholder="Descripcion minimo 50 caracteres" />
        </div>

        <div class="frminput">
          <label for="correo">Correo electrónico</label>
          <input class="registro_cont" type="email" id="correo" v-model="correo" required />
        </div>

        <div class="frminput">
    <label for="documento">Documento</label>
    <input 
        class="registro_cont" 
        type="text" 
        id="documento" 
        v-model="documento" 
        required 
        pattern="[0-9]*" 
        inputmode="numeric"
        title="Solo se permiten números."
    />
</div>


<div class="frminput">
    <label for="telefono">Teléfono</label>
    <input 
        class="registro_cont" 
        type="text" 
        id="telefono" 
        v-model="celular" 
        required 
        pattern="[0-9]*" 
        inputmode="numeric" 
        title="Solo se permiten números."
    />
</div>

<div class="frminput">
<label for="fecha_nacimiento">Fecha de nacimiento</label>
<br />
<input
    type="date"
    id="fecha_nacimiento"
    v-model="fechaNacimiento"
    @change="calcularedad"
    required
    min="1925-01-01"
    :max="fecha"
    title="La fecha de nacimiento no puede ser mayor que hoy"
    class="input-fecha"
  />
</div>

<div class="frminput">
  <label for="password">Contraseña</label>
  <div style="position: relative; display: inline-block; width: 100%;">
    <input 
      class="registro_cont" 
      :type="showPassword ? 'text' : 'password'" 
      id="password" 
      v-model="password" 
      required 
      pattern="^(?=.*[A-Z])(?=.*).{8,}$" 
      title="La contraseña debe tener al menos 8 caracteres, al menos una letra mayúscula."
    />
    <button @click="togglePassword" type="button" class="password-toggle">
      <img 
        :src="showPassword ? nover : verimg"
        alt="Toggle password visibility" 
        class="password-icon"
      />
    </button>
  </div>
</div>


<div class="frminput">
          <br>
          <input type="hidden" id="Edad" v-model="Edad" required /> 
        </div>


        <div class="frminput">
  <select v-model="posicion" required class="select-posicion">
    <option disabled value="">Seleccione una posición de juego</option>
    <option value="Delantero">Delantero</option>
    <option value="Defensa">Defensa</option>
    <option value="Centrocampista">Centrocampista</option>
    <option value="Portero">Portero</option>
    <option value="Lateral Derecho">Lateral Derecho</option>
    <option value="Lateral Izquierdo">Lateral Izquierdo</option>
    <option value="Extremo Derecho">Extremo Derecho</option>
    <option value="Extremo Izquierdo">Extremo Izquierdo</option>
    <option value="Mediocentro Defensivo">Mediocentro Defensivo</option>
  </select>
</div>



<div class="form-imagen">
  <label for="imagen">Imagen</label>
  <input
    type="file"
    id="imagen"
    @change="onFileChange"
    accept="image/jpeg, image/png"
    class="input-imagen"
  />

  <div v-if="imageUrl" class="logo-preview">
    <img :src="imageUrl" alt="Vista previa de la imagen" />
  </div>
</div>
  <br>
  <br>  
  <br> 
        <button class="inicio_sesion_boton" type="submit">Registrar</button>
        <p class="inicio_sesion_letra">
  ¿Ya tienes cuenta?
  <a href="#" @click.prevent="toggleForm" class="inicia-sesion-link">Inicia sesión</a>
</p>

        <div v-if="menError" class="error-message">{{ menError }}</div>
      </form>
    </div>
  </div>
</template>


<script setup>
import { ref, onBeforeUnmount } from 'vue';
import axios from 'axios';
import Swal from 'sweetalert2';
import { useRouter } from 'vue-router';
import { useUsuarios } from '@/stores/usuario';
import verimg from '@/assets/imagenes/ojo.png'
import nover from '@/assets/imagenes/ojos.png'

const router = useRouter();
const isLogin = ref(true);
const nombre = ref('');
const correo = ref('');
const documento = ref('');
const celular = ref('');
const fechaNacimiento = ref('');
const password = ref('');
const menError = ref('');
const ciudad = ref('');
const descripcion = ref('');
const fileInput = ref('');
const Edad = ref(0);
const posicion = ref('');
const fecha = ref('');
const usuariosStore = useUsuarios();
const showPassword = ref(false); // Estado para mostrar/ocultar contraseña

// Cálculo de la fecha mínima para usuarios menores de edad
const calcularedadmenor = setInterval(() => {
  const hoy = new Date();
  hoy.setFullYear(hoy.getFullYear() - 18);
  fecha.value = hoy.toISOString().split('T')[0];
}, 1000);

onBeforeUnmount(() => {
  clearInterval(calcularedadmenor);
});

const toggleForm = () => {
  isLogin.value = !isLogin.value;
};

const imageUrl = ref(""); // Variable correctamente referenciada

const onFileChange = (event) => {
  const file = event.target.files[0];
  if (file) {
    imageUrl.value = URL.createObjectURL(file);
    fileInput.value = file; // Guardar el archivo seleccionado
  }
};


const calcularedad = () => {
  if (!fechaNacimiento.value) {
    Edad.value = '';
    return;
  }

  const nacimiento = new Date(fechaNacimiento.value);
  const hoy = new Date();
  let años = hoy.getFullYear() - nacimiento.getFullYear();

  const mesHoy = hoy.getMonth();
  const mesNacimiento = nacimiento.getMonth();
  const diaHoy = hoy.getDate();
  const diaNacimiento = nacimiento.getDate();

  if (mesHoy < mesNacimiento || (mesHoy === mesNacimiento && diaHoy < diaNacimiento)) {
    años--;
  }

  Edad.value = años;
};

// Función para alternar la visibilidad de la contraseña
const togglePassword = () => {
  showPassword.value = !showPassword.value;
};

const iniciarSesion = async () => {
  try {
    const iniciar = await axios.post("http://127.0.0.1:8000/iniciar", {
      correo: correo.value,
      contraseña: password.value,
    });

    if (iniciar.data) {
      const userData = {
        correo: iniciar.data.correo,
        id: iniciar.data.id,
        nombreUsuario: iniciar.data.nombreUsuario,
        ciudad: iniciar.data.ciudad,
        descripcion: iniciar.data.descripcion,
        fechaNacimiento: iniciar.data.fechaNacimiento,
        celular: iniciar.data.celular,
        Edad: iniciar.data.Edad,
        posicion: iniciar.data.posicion,
        fileInput: iniciar.data.imagen,
        documento: iniciar.data.documento,
        equipo_tiene: iniciar.data.equiposTiene,
      };

      await usuariosStore.setUsuario(userData); // Esperar a que se actualice el estado

      router.push("/Perfil").then(() => {
        Swal.fire({
          icon: "success",
          title: "¡Inicio de sesión exitoso!",
          text: "Bienvenido de nuevo",
          confirmButtonText: "Aceptar",
        });
      });
    }
  } catch (error) {
    alert("⚠️ Correo o contraseña incorrectos. ⚠️");
    console.error("Error al iniciar sesión:", error);
  }
};


const registrarUsuario = async () => {
  const { value: passwordConfirmation } = await Swal.fire({
    title: 'Confirmar contraseña',
    input: 'password',
    inputLabel: 'Por favor, confirma tu contraseña',
    inputPlaceholder: 'Introduce tu contraseña',
    showCancelButton: true,
    confirmButtonText: 'Confirmar',
    cancelButtonText: 'Cancelar',
  });

  if (passwordConfirmation) {
    if (passwordConfirmation === password.value) {
      const formData = new FormData();
      formData.append('nombre', nombre.value);
      formData.append('correo', correo.value);
      formData.append('documento', documento.value);
      formData.append('celular', celular.value);
      formData.append('fecha_nacimiento', fechaNacimiento.value);
      formData.append('contraseña', password.value);
      formData.append('ciudad', ciudad.value);
      formData.append('descripcion', descripcion.value);
      formData.append('Edad', Edad.value);
      formData.append('posicion', posicion.value);

      if (fileInput.value) {
        formData.append('file', fileInput.value);
      }

      try {
        const insertar = await axios.post('http://127.0.0.1:8000/insertarc', formData, {
          headers: { 'Content-Type': 'multipart/form-data' },
        });

        const userData = {
          id: insertar.data.documento,
          nombreUsuario: insertar.data.nombre,
          correo: insertar.data.correo,
          ciudad: insertar.data.ciudad,
          descripcion: insertar.data.descripcion,
          fecha_nacimiento: insertar.data.fechaNacimiento,
          celular: insertar.data.celular,
          Edad: insertar.data.Edad,
          posicion: insertar.data.posicion,
          fileInput: insertar.data.imagen,
          documento: insertar.data.documento,
          equipo_tiene: insertar.data.equiposTiene,
        };
        usuariosStore.setUsuario(userData);

        if (insertar.status === 200) {
          Swal.fire({
            title: 'ADVERTENCIA LEGAL',
            html: `
    <div style="text-align: center;">
      <span style="font-size: 2.5rem; color: #d90000;">⚠</span>
      <h2 style="color: #d90000; font-size: 1.8rem; font-weight: bold;">¡ATENCIÓN!</h2>
      <p style="font-size: 1.2rem; color: #222; line-height: 1.6;">
        <strong>¡ATENCIÓN!</strong> Si eres menor de edad, debes estar bajo la supervisión de tus padres o tutores legales mientras usas este servicio. 
        De acuerdo con la <strong>Ley de Protección a Menores (Ley 12345/2024)</strong>, es <u>estrictamente obligatorio</u> que los menores de 18 años estén acompañados por un adulto responsable durante la utilización de servicios en línea. 
        El incumplimiento de esta ley puede acarrear consecuencias legales.
      </p>
    </div>
  `,
  confirmButtonText: 'ACEPTAR',
  confirmButtonColor: '#d90000',
          }).then(() => {
            Swal.fire({
              icon: 'success',
              title: 'Cuenta creada exitosamente',
              text: 'Ahora puedes iniciar sesión',
            });

            isLogin.value = true;
          });
        }
      } catch (error) {
        const errorMessage = error.response?.data?.detail || 'Error al registrar';
        menError.value = errorMessage;
        Swal.fire({
          icon: 'error',
          title: 'Error',
          text: errorMessage,
        });
      }
    } else {
      Swal.fire({
        icon: 'error',
        title: 'Error',
        text: 'Las contraseñas no coinciden.',
      });
    }
  }
};
</script>


<style scoped>
.inicio_sesion_form{
background-color: rgb(0, 0, 0);
border: 5px solid rgb(255, 255, 255);
padding: 20px;
border-radius: 8px;
box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.5);
display: flex;
flex-direction: column;
gap: 20px; 
width: 100%; 
max-width: 400px;
margin-left: 10%;
transition: initial;
}
.inicio_sesion_form:hover{
border-color: #FFD700;
}
.password-icon {
  width: 24px;
  height: 24px;
  cursor: pointer;
}

.inicio_sesion_container_titulo{
position: absolute;
background-color: rgb(0, 0, 0);
width: 60%;
top: -5%;
left:30%;
box-shadow: 0 0 6px rgb(255, 255, 255);
border: solid;
border: 50px;
border-color: antiquewhite;
}
.registro_titulo{
margin-left: 10%;
margin-right: 10%;
position: relative;
font-family: Impact, Haettenschweiler, 'Arial Narrow Bold', sans-serif;
font-size: 25px;
background-image: url('https://static.vecteezy.com/system/resources/thumbnails/000/549/015/small/vector-apr-2018-19.jpg');
background-size: cover;
color: transparent;
background-clip: text;
text-shadow: 2px 2px 2px rgba(0, 0, 0, 0.158);
width: 200px;

}
.registro_contenedor{
position: absolute;
background-color: rgb(0, 0, 0);
width: 60%;
top: 0%;
left:35%;
box-shadow: 0 0 6px rgb(255, 255, 255);
border: solid;
border: 50px;
border-color: antiquewhite;

}
.pa{
  color: white;
}
.logos3{
  margin-left: 100px;
  position: relative;
  top: 20px;
  left: 500px;
  width: 70px;
  height: 50px;
  cursor: pointer;
}
.registro_form{
  overflow: hidden;   
  color: white;
background-color: rgb(0, 0, 0);
border: 5px solid rgb(255, 255, 255);
padding: 20px;
border-radius: 8px;
box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.5);
display: flex;
flex-direction: column;
gap: 10px; 
width: 100%; 
max-width: 400px; 
font-size: 50%;
margin-left: 15%;
margin-top: 30px;

}

#animal{
  position: relative;
  height: 150px;
  width: 1500px;
  top: 495px;
  left: -143px;
  position: absolute;
  top: 800px;
  width: 1640px;
  height: 100px;
  background-color: rgba(255, 255, 255, 0.199);
  
  
}
.inicio_sesion_titulo{
margin-left: 10%;
margin-right: 10%;
position: relative;
font-family: Impact, Haettenschweiler, 'Arial Narrow Bold', sans-serif;
font-size: 25px;
background-image: url('https://static.vecteezy.com/system/resources/thumbnails/000/549/015/small/vector-apr-2018-19.jpg');
background-size: cover;
color: transparent;
background-clip: text;
text-shadow: 2px 2px 2px rgba(0, 0, 0, 0.158);
}
.inicio_sesion_contenedor{
font-size: 25px;
text-align: center;
font-family:'Lucida Sans', 'Lucida Sans Regular', 'Lucida Grande', 'Lucida Sans Unicode', Geneva, Verdana, sans-serif;
position: relative;
left: 36%;
margin-top: 70px;

}
.inicio_sesion_cont{
background-color: black;
font-size: 20px;
text-align: center;
width: 90%;
font-family: 'Trebuchet MS', 'Lucida Sans Unicode', 'Lucida Grande', 'Lucida Sans', Arial, sans-serif;
color: aliceblue;
}
.registro_cont{
background-color: black;
font-size: 20px;
text-align: center;
width: 90%;
font-family: 'Trebuchet MS', 'Lucida Sans Unicode', 'Lucida Grande', 'Lucida Sans', Arial, sans-serif;
color: aliceblue;
}
.inicio_sesion_boton{
background-image: url('https://static.vecteezy.com/system/resources/thumbnails/000/549/015/small/vector-apr-2018-19.jpg');
      background-size: cover;
      border: none;
      padding: 10px 20px;
      cursor: pointer;
      border-radius: 20px;
      text-align: center;
      font-size: 90%;
      margin-top: 50px;
      width: 70%;
      position: relative;
      font-family:'Times New Roman', Times, serif;
}
.inicio_sesion_letra{
font-size: 70%;
}

.frminputimg{
height: 50px;
width: 150px;
margin-left: 28%;
}
@media (max-width: 320px) {
/* Estilos para pantallas con un ancho máximo de 320px */
.inicio_sesion_contenedor{
font-size: 25px;
text-align: center;
font-family:'Lucida Sans', 'Lucida Sans Regular', 'Lucida Grande', 'Lucida Sans Unicode', Geneva, Verdana, sans-serif;
position: relative;
left: -10%;
margin-top: 67%;

}
.inicio_sesion_boton{
background-image: url('https://static.vecteezy.com/system/resources/thumbnails/000/549/015/small/vector-apr-2018-19.jpg');
      background-size: cover;
      border: none;
      padding: 10px 20px;
      cursor: pointer;
      border-radius: 20px;
      text-align: center;
      font-size: 90%;
      margin-top: 30px;
      width: 100%;
      position: relative;
      font-family:'Times New Roman', Times, serif;
}
.registro_contenedor{
position: absolute;
background-color: rgb(0, 0, 0);
width: 35%;
top: -5%;
left:16%;
box-shadow: 0 0 6px rgb(255, 255, 255);
border: solid;
border: 50px;
border-color: antiquewhite;

}
.registro_form{
background-color: rgb(0, 0, 0);
border: 5px solid rgb(255, 255, 255);
padding: 15px;
border-radius: 10px;
box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.5);
display: flex;
flex-direction: column;
gap: 5px; 
width: 100%; 
max-width: 400px; 
font-size: 50%;
margin-left: 5%;
margin-top: -5%;
}
}


@media (max-width: 480px) {
/* Estilos para pantallas con un ancho máximo de 480px */
.inicio_sesion_contenedor{
font-size: 25px;
text-align: center;
font-family:'Lucida Sans', 'Lucida Sans Regular', 'Lucida Grande', 'Lucida Sans Unicode', Geneva, Verdana, sans-serif;
position: relative;
left: -8%;
margin-top: 40%;

}
.inicio_sesion_boton{
background-image: url('https://static.vecteezy.com/system/resources/thumbnails/000/549/015/small/vector-apr-2018-19.jpg');
      background-size: cover;
      border: none;
      padding: 10px 20px;
      cursor: pointer;
      border-radius: 20px;
      text-align: center;
      font-size: 90%;
      margin-top: 30px;
      width: 100%;
      position: relative;
      font-family:'Times New Roman', Times, serif;
}
.registro_contenedor{
position: absolute;
background-color: rgb(0, 0, 0);
width: 80%;
top: -5%;
left:16%;
box-shadow: 0 0 6px rgb(255, 255, 255);
border: solid;
border: 50px;
border-color: antiquewhite;

}
.registro_form{
background-color: rgb(0, 0, 0);
border: 5px solid rgb(255, 255, 255);
padding: 15px;
border-radius: 10px;
box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.5);
display: flex;
flex-direction: column;
gap: 5px; 
width: 100%; 
max-width: 400px; 
font-size: 50%;
margin-left: 5%;
margin-top: -5%;
}
}
@media (min-width: 481px) and (max-width: 600px) {
/* Estilos para pantallas entre 481px y 600px */
.inicio_sesion_contenedor{
font-size: 35px;
text-align: center;
font-family:'Lucida Sans', 'Lucida Sans Regular', 'Lucida Grande', 'Lucida Sans Unicode', Geneva, Verdana, sans-serif;
position: relative;
left: 7%;
margin-top: 20%;

}
.inicio_sesion_boton{
background-image: url('https://static.vecteezy.com/system/resources/thumbnails/000/549/015/small/vector-apr-2018-19.jpg');
      background-size: cover;
      border: none;
      padding: 10px 20px;
      cursor: pointer;
      border-radius: 20px;
      text-align: center;
      font-size: 90%;
      margin-top: 30px;
      width: 100%;
      position: relative;
      font-family:'Times New Roman', Times, serif;
}
.registro_contenedor{
position: absolute;
background-color: rgb(0, 0, 0);
width: 80%;
top: -5%;
left:16%;
box-shadow: 0 0 6px rgb(255, 255, 255);
border: solid;
border: 50px;
border-color: antiquewhite;

}
.registro_form{
background-color: rgb(0, 0, 0);
border: 5px solid rgb(255, 255, 255);
padding: 15px;
border-radius: 10px;
box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.5);
display: flex;
flex-direction: column;
gap: 5px; 
width: 100%; 
max-width: 400px; 
font-size: 50%;
margin-left: 5%;
margin-top: -5%;
}

}

@media (min-width: 601px) and (max-width: 768px) {
/* Estilos para pantallas entre 601px y 768px */
.inicio_sesion_contenedor{
font-size: 30px;
text-align: center;
font-family:'Lucida Sans', 'Lucida Sans Regular', 'Lucida Grande', 'Lucida Sans Unicode', Geneva, Verdana, sans-serif;
position: relative;
left: 0%;
margin-top: 20%;

}
.inicio_sesion_boton{
background-image: url('https://static.vecteezy.com/system/resources/thumbnails/000/549/015/small/vector-apr-2018-19.jpg');
      background-size: cover;
      border: none;
      padding: 10px 20px;
      cursor: pointer;
      border-radius: 20px;
      text-align: center;
      font-size: 90%;
      margin-top: 30px;
      width: 100%;
      position: relative;
      font-family:'Times New Roman', Times, serif;
}
.registro_contenedor{
position: absolute;
background-color: rgb(0, 0, 0);
width: 80%;
top: -5%;
left:16%;
box-shadow: 0 0 6px rgb(255, 255, 255);
border: solid;
border: 50px;
border-color: antiquewhite;

}
.registro_form{
background-color: rgb(0, 0, 0);
border: 5px solid rgb(255, 255, 255);
padding: 15px;
border-radius: 10px;
box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.5);
display: flex;
flex-direction: column;
gap: 5px; 
width: 100%; 
max-width: 400px; 
font-size: 50%;
margin-left: 5%;
margin-top: -5%;
}
}


@media (min-width: 769px) and (max-width: 1024px) {
/* Estilos para pantallas entre 769px y 1024px */

.inicio_sesion_contenedor{
font-size: 30px;
text-align: center;
font-family:'Lucida Sans', 'Lucida Sans Regular', 'Lucida Grande', 'Lucida Sans Unicode', Geneva, Verdana, sans-serif;
position: relative;
left: 10%;
margin-top: 20%;

}
.inicio_sesion_container_titulo{
position: absolute;
background-color: rgb(0, 0, 0);
width: 30%;
top: -7%;
left:24%;
box-shadow: 0 0 6px rgb(255, 255, 255);
border: solid;
border: 50px;
border-color: antiquewhite;
}
.inicio_sesion_boton{
background-image: url('https://static.vecteezy.com/system/resources/thumbnails/000/549/015/small/vector-apr-2018-19.jpg');
      background-size: cover;
      border: none;
      padding: 10px 20px;
      cursor: pointer;
      border-radius: 20px;
      text-align: center;
      font-size: 90%;
      margin-top: 30px;
      width: 100%;
      position: relative;
      font-family:'Times New Roman', Times, serif;
}
.registro_contenedor{
position: absolute;
background-color: rgb(0, 0, 0);
width: 35%;
top: -5%;
left:16%;
box-shadow: 0 0 6px rgb(255, 255, 255);
border: solid;
border: 50px;
border-color: antiquewhite;

}
.registro_form{
background-color: rgb(0, 0, 0);
border: 5px solid rgb(255, 255, 255);
padding: 15px;
border-radius: 10px;
box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.5);
display: flex;
flex-direction: column;
gap: 5px; 
width: 100%; 
max-width: 400px; 
font-size: 50%;
margin-left: 5%;
margin-top: -5%;
}
}


@media (min-width: 1025px) and (max-width: 1280px) {
/* Estilos para pantallas entre 1025px y 1280px */

.inicio_sesion_contenedor{
font-size: 30px;
text-align: center;
font-family:'Lucida Sans', 'Lucida Sans Regular', 'Lucida Grande', 'Lucida Sans Unicode', Geneva, Verdana, sans-serif;
position: relative;
left: 15%;
margin-top: 15%;

}
.inicio_sesion_container_titulo{
position: absolute;
background-color: rgb(0, 0, 0);
width: 30%;
top: -7%;
left:23%;
box-shadow: 0 0 6px rgb(255, 255, 255);
border: solid;
border: 50px;
border-color: antiquewhite;
}
.inicio_sesion_boton{
background-image: url('https://static.vecteezy.com/system/resources/thumbnails/000/549/015/small/vector-apr-2018-19.jpg');
      background-size: cover;
      border: none;
      padding: 10px 20px;
      cursor: pointer;
      border-radius: 20px;
      text-align: center;
      font-size: 90%;
      margin-top: 30px;
      width: 100%;
      position: relative;
      font-family:'Times New Roman', Times, serif;
}
.registro_contenedor{
position: absolute;
background-color: rgb(0, 0, 0);
width: 35%;
top: -5%;
left:16%;
box-shadow: 0 0 6px rgb(255, 255, 255);
border: solid;
border: 50px;
border-color: antiquewhite;

}
.registro_form{
background-color: rgb(0, 0, 0);
border: 5px solid rgb(255, 255, 255);
padding: 15px;
border-radius: 10px;
box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.5);
display: flex;
flex-direction: column;
gap: 5px; 
width: 100%; 
max-width: 400px; 
font-size: 50%;
margin-left: 5%;
margin-top: -5%;
}


}



@media (min-width: 1281px) and (max-width: 2000px) {
/* Estilos para pantallas entre 1281px y 1440px */
.inicio_sesion_contenedor{
font-size: 30px;
text-align: center;
font-family:'Lucida Sans', 'Lucida Sans Regular', 'Lucida Grande', 'Lucida Sans Unicode', Geneva, Verdana, sans-serif;
position: relative;
left: 15%;
margin-top: 15%;
width: 100%;
height: 100%;

}
.inicio_sesion_container_titulo{
position: absolute;
background-color: rgb(0, 0, 0);
width: 30%;
top: -7%;
left:23%;
box-shadow: 0 0 6px rgb(255, 255, 255);
border: solid;
border: 50px;
border-color: antiquewhite;
}
.inicio_sesion_boton {
  background-image: url('https://static.vecteezy.com/system/resources/thumbnails/000/549/015/small/vector-apr-2018-19.jpg');
  background-size: cover;
  border: none;
  padding: 10px 20px;
  cursor: pointer;
  border-radius: 20px;
  text-align: center;
  font-size: 90%;
  margin-top: 30px;
  width: 100%;
  position: relative;
  font-family: 'Times New Roman', Times, serif;
  color: white;
  transition: transform 0.3s ease, box-shadow 0.3s ease, opacity 0.3s ease;
}

.inicio_sesion_boton:hover {
  transform: scale(1.05);
  box-shadow: 0 0 15px rgba(255, 255, 255, 0.5);
  opacity: 0.9;
}

.registro_contenedor{
position: absolute;
background-color: rgb(0, 0, 0);
width: 35%;
top: -5%;
left:16%;
box-shadow: 0 0 6px rgb(255, 255, 255);
border: solid;
border: 50px;
border-color: antiquewhite;

}
.registro_form{
background-color: rgb(0, 0, 0);
border: 5px solid rgb(255, 255, 255);
padding: 15px;
border-radius: 10px;
box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.5);
display: flex;
flex-direction: column;
gap: 5px; 
width: 100%; 
max-width: 400px; 
font-size: 50%;
margin-left: 5%;
margin-top: -5%;
}


}
@keyframes fadeInScale {
  from {
    opacity: 0;
    transform: scale(0.8);
  }
  to {
    opacity: 1;
    transform: scale(1);
  }
}

.logo-preview {
  text-align: center;
  margin-top: 15px;
}

.logo-preview img {
  max-width: 120px;
  max-height: 120px;
  border-radius: 10px;
  border: 2px solid #d4af37;
  box-shadow: 0 0 15px rgba(218, 165, 32, 0.8);
  animation: fadeInScale 0.5s ease-out;
}

.inicio_sesion_letra {
  font-size: 16px;
  color: #ffffff;
  text-align: center;
  margin-top: 20px;
}

.registro-link {
  color: #fbff00;
  text-decoration: none;
  font-weight: bold;
  margin-left: 5px;
  cursor: pointer;
  transition: color 0.3s ease;
}

.registro-link:hover {
    color: #fff205;
    text-shadow: 0 0 4px white;
    text-decoration: underline;
    transform: scale(5.1);
  }

  .inicia-sesion-link {
  color: #ffff00;
  text-decoration: none;
  font-weight: bold;
  margin-left: 5px;
  cursor: pointer;
  transition: color 0.3s ease, transform 0.2s ease;
}

.inicia-sesion-link:hover {

  text-shadow: 0 0 4px #ffffff;
  text-decoration: underline;
  transform: scale(1.3);
}
.input-fecha {
  padding: 10px 12px;
  font-size: 16px;
  border: 2px solid #aaa;
  border-radius: 8px;
  background-color: #000000;
  color: #ffffff;
  outline: none;
  transition: border-color 0.3s ease, box-shadow 0.3s ease;
}

.input-fecha:hover {
  border-color: #e2b307;
  color: #d4af37;

  box-shadow: 0 0 6px rgba(255, 247, 2, 0.5);

}
.select-posicion {
  width: 100%;
  padding: 10px 12px;
  font-size: 16px;
  color: #ffffff;
  background-color: #000000;
  border: 2px solid #aaa;
  border-radius: 8px;
  appearance: none; /* Oculta flechita por defecto */
  background-image: url("data:image/svg+xml;charset=US-ASCII,%3Csvg xmlns='http://www.w3.org/2000/svg' width='12' height='12' viewBox='0 0 24 24'%3E%3Cpath fill='%23333' d='M7 10l5 5 5-5z'/%3E%3C/svg%3E");
  background-repeat: no-repeat;
  background-position: right 10px center;
  background-size: 16px 16px;
  transition: border-color 0.3s ease, box-shadow 0.3s ease;
}

.select-posicion:focus {
  border-color: #fbff16;
  box-shadow: 0 0 6px rgba(208, 212, 0, 0.5);
  outline: none;
}
.form-imagen {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.form-imagen label {
  font-weight: bold;
  color: #444;
}
label{
  font-family: Georgia, 'Times New Roman', Times, serif;
  font-size: 15px;
}

.input-imagen {
  padding: 10px;
  background-color: #000000;
  border: 2px solid #aaa;
  border-radius: 8px;
  font-size: 14px;
  cursor: pointer;
  transition: border-color 0.3s ease, box-shadow 0.3s ease;
}

.input-imagen:hover {
  border-color: #d4b100;
  box-shadow: 0 0 6px rgba(212, 184, 0, 0.4);
}

.logo-preview img {
  width: 150px;
  height: 150;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.2);
}
.pa{
  font-size: 20px;
}
</style>