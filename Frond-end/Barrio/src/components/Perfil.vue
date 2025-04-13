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
<article>
  <div class="caja_perfil">
    <div class="videooo" data-text="PERFIL JUGADOR"> PERFIL JUGADOR</div> 
     
    <section class="fondo" v-if="isUserLoaded">
      <router-link class="actualizar_perfil" to="/actualizar_perfil">Actualizar Datos</router-link>
      <router-link class="link equipo" to="/equipos">
        <img class="clan" src="../assets/iconos header/clan.png" alt="" />
      </router-link>
    
      <div class="container_profile">
        <div class="card_profile">
          <div class="front">
            <div class="card-top">
              <p class="card-top-para">Barrio Gol</p>
            </div>
            <div class="circle-container">
              <img :src="url" alt="Foto de perfil" v-if="url !== 'Sin Foto de perfil'" />
            </div>
            <p class="heading">
              Nombre: {{ nombre?.split(' ')[0] }} {{ nombre?.split(' ')[2] }}
            </p>
            <p class="follow">Ciudad: {{ ciudad }}</p>
            <p class="follow">Edad: {{ edad }}</p>
            <p class="follow">Posición: {{ posicion }}</p>
            <p class="follow">
              Email: {{ correo.slice(0, 5) + '******' + correo.slice(correo.indexOf('@')) }}
            </p>
          </div>

          <div class="back">
            <p class="heading_2">Descripción: {{ descripcion }}</p>
          </div>
        </div>
      </div>
    </section>
  </div>
  <br>
  <br>
  <div>
      </div>
      <h1 class="subidoss">Mis videos</h1>
    </article>
    <article>
      <div>
        <videos_de_usuario></videos_de_usuario>
      </div>
    </article>
</template>

<script setup>
import headerapp from './headerapp.vue';
import headermobile from './headermobile.vue';
import { ref, onMounted, onUnmounted, computed, watch } from 'vue';
import videos_de_usuario from './videos_de_usuario.vue';
  import { useUsuarios } from '@/stores/usuario';

  const usuariosStore = useUsuarios();
// Usamos computed para obtener los valores directamente del store
const nombre = computed(() => usuariosStore.usuario?.nombreUsuario || 'Sin nombre');
const correo = computed(() => usuariosStore.usuario?.correo || 'Sin correo');
const ciudad = computed(() => usuariosStore.usuario?.ciudad || 'Sin ciudad');
const descripcion = computed(() => usuariosStore.usuario?.descripcion || 'Sin descripción');
const edad = computed(() => usuariosStore.usuario?.Edad || 'Sin edad');
const posicion = computed(() => usuariosStore.usuario?.posicion || 'Sin posición');

// Computed para obtener la URL de la imagen
const url = computed(() => {
  return usuariosStore.usuario?.fileInput
    ? `http://127.0.0.1:8000/${usuariosStore.usuario.fileInput}`
    : 'Sin Foto de perfil';
});


// Estado para verificar si el usuario está cargado
const isUserLoaded = ref(false);
const fecha = ref('');
let interval = null;

// Depuración: Verificar la URL de la imagen en consola
watch(url, (newValue) => {
  console.log('URL de imagen:', newValue);
});

// Cargar el perfil cuando el componente se monta
onMounted(() => {
  isUserLoaded.value = true;

  // Actualizar la fecha cada segundo
  interval = setInterval(() => {
    fecha.value = new Date().toLocaleString();
  }, 1000);
});

// Limpiar el intervalo cuando el componente se desmonte
onUnmounted(() => {
  clearInterval(interval);
});
</script>




<style scoped>

/* Quita Los estilos Predefinidos de las rutas color verde*/
a.router-link-active, a.router-link-exact-active {
    color: inherit;
    text-decoration: none;
    background-color: none;
  }
.subidoss {
    width: 90%;
    margin-top: 2%;
    padding: 20px;
    display: flex;
    flex-direction: column;
    align-items: center;  
    font-weight: bold;
    font-family: Cambria, Cochin, Georgia, Times, 'Times New Roman', serif;
    color: #ffd700; 
    text-shadow: 0 0 10px rgba(255, 215, 0, 0.8);
    border: 2px solid #7e7e7e; 
    padding: 10px 15px;
    border-radius: 8px;
    margin-bottom: 20px;
    background: linear-gradient(90deg, rgba(212, 212, 212, 0.2), rgba(255, 215, 0, 0));
  }


  .link {
    display: inline-block;
    margin: 0;
    padding: 0;
  }
  .link:hover {
  background: none;
}




.caja_perfil{
  all: unset;
  display: flex;
  flex-direction: column;
  justify-content:center;
  width: 100%;
  text-align: center;
  margin-top: 40%;
}



.circle-container {
width: 150px; 
height: 100px;
border-radius: 50%; 
overflow: hidden; 
display: flex;
justify-content: center; 
align-items: center; 
background-color: rgb(255, 251, 251);
}


.circle-container img {
width: 100%; 
height: 100%; 
object-fit: cover; 
}



.videooo {
  width: 110%;
  text-align: center;
  font-family: 'Courier New', Courier, monospace;
  font-size: 3rem;
  font-weight: bold;
  position: relative;
  color: #fff;
  overflow: hidden;
  text-shadow: 2px 2px 4px #000000, -2px -2px 4px #000000, 2px -2px 4px #000000, -2px 2px 4px #000000; /* Borde negro */
}

.videooo:before,
.videooo:after {
  content: attr(data-text);
  position: absolute;
  top: 0;
  left: 0;
  color: #ffdd00; /* Color dorado */
  z-index: -1;
  animation: glitch 1s infinite;
  clip-path: inset(0 0 0 0);
}

.videooo:before {
  left: 2px;
  text-shadow: 2px 0px #ffd700, -2px 0px #000000; /* Dorado y negro */
}

.videooo:after {
  left: -2px;
  text-shadow: -2px 0px #ffcc00, 2px 0px #000000; /* Dorado más claro y negro */
  animation-delay: 0.3s;
}

@keyframes glitch {
  0% {
    clip-path: inset(0 0 0 0);
    transform: skew(0.1deg);
  }
  20% {
    clip-path: inset(10% 0 80% 0);
    transform: skew(0.2deg);
  }
  40% {
    clip-path: inset(60% 0 40% 0);
    transform: skew(0.1deg);
  }
  60% {
    clip-path: inset(10% 0 80% 0);
    transform: skew(0.3deg);
  }
  80% {
    clip-path: inset(50% 0 50% 0);
    transform: skew(0.2deg);
  }
  100% {
    clip-path: inset(0 0 0 0);
    transform: skew(0.1deg);
  }
}

.card_profile {
margin-left: 0;
border-radius: 2rem;
transition: transform 1500ms;
transform-style: preserve-3d;

}


.card-top-para {
font-size: 20px;
font-weight: bold;
}

.container_profile:hover > .card_profile {
cursor: pointer;
transform: rotateX(180deg) rotateZ(-180deg);
}
.container_profile{
  display: flex;
  flex-direction:column;

}

.front,
.back {
height: 200%;
width: 200%;
border-radius: 2rem;
box-shadow: 0px 0px 10px 5px rgba(255, 255, 0, 0.7);
backface-visibility: hidden;
display: flex;
flex-direction: column;
align-items: center;
justify-content: center;
gap:5px;
background-color: black;
color: white;
margin-left: -50%;
}

.back {
transform: rotateX(180deg) rotateZ(-180deg);
position: absolute;
top: 0%; 
height: 100%;
}

.heading {
font-size: 15px;
font-weight: bold;
}
.heading_2 {
font-size: 20px;
font-weight: bold;
text-align: center;
width: auto;
}

.follow {
font-size: 15px;
font-weight: 500;
}

.icons {
display: flex;
flex-direction: row;
gap: 20px;
margin-top: 20px;

}


.texto-2 {
  margin: 10px 0; 
  color: white;
  text-shadow: 0 0 4px rgb(0, 0, 0);
  font-family: monospace;
  font-size: 20px;
}

.clan {
  height: 70px;
  width: 70px; /* Asegurar que sea un círculo */
  margin-top: 50%;
  background-color: rgb(255, 255, 255);
  border-radius: 50%;
  border: 4px solid rgba(255, 255, 255, 0.986);
  transition: all 0.3s ease-in-out;
  box-shadow: 0px 5px 15px rgba(0, 0, 0, 0.1);
  display: flex;
  align-items: center;
  justify-content: center;
  margin-left: 600%;
}

.clan:hover {
  transform: scale(1.2);
  border-color: #ffcc00;
  box-shadow: 0px 0px 50px rgba(255, 204, 0, 0.8), 0px 0px 40px rgba(255, 136, 0, 0.6);
}


.link  {
margin-left: 80%;
color: rgb(0, 0, 0);
font-family: monospace;
}
.link:hover {
box-shadow: 0 0 100% rgb(255, 2, 2);
transform: scale(1.05);
}



.actualizar_perfil {
  all: unset;
  position: absolute;
  left: 5%;
  width: 100px;
  height: 10px;
  background: linear-gradient(45deg, #3a3a3a, #6e6e6e);
  border: none;
  border-radius: 10px;
  font-family: 'Arial', sans-serif;
  font-size: 14px;
  font-weight: bold;
  cursor: pointer;
  transition: all 0.3s ease;
  text-transform: uppercase;
  letter-spacing: 2px;
  box-shadow: 0px 5px 15px rgba(0, 0, 0, 0.2);
  display: flex;
  align-items: center;
  justify-content: center;
  text-align: center;
}

.actualizar_perfil:hover {
  background: linear-gradient(45deg, #575757, #bdbebe);
  transform: scale(1.1);
  box-shadow: 0px 5px 25px rgba(255, 255, 255, 0.3);
}

.actualizar_perfil:active {
  transform: scale(0.95);
}


@keyframes pulseGlow {
  0% { text-shadow: 4px 4px 10px #0077ff, 8px 8px 20px #00ffea; }
  100% { text-shadow: 6px 6px 15px #00ffea, 12px 12px 30px #00ffff; }
}

@keyframes shake {
  0% { transform: translateX(0px) rotate(-0deg); }
  100% { transform: translateX(-1px) rotate(1deg); }
}
.texto-2:hover {
color: rgb(255, 251, 0);
text-shadow: 0 0 4px rgb(0, 0, 0);

}

.linea {
position: absolute;
background-color: rgb(255, 255, 255);
width: 1535px;
height: 5px;
right: 0;
top: 550px;
}

.videos {
width: 100%;
height: 100%; 
display: flex;
justify-content: center;
align-items: center;
top: 600px;
right: 5px;
}

video {
width: 500px;
height: 800px;
}


@media (min-width: 320px ) and (max-width: 480px) {
  /* Estilos para pantallas muy pequeñas */
.card_profile {
width: 50%;
height: auto;
border-radius: 2rem;
transition: transform 1500ms;
transform-style: preserve-3d;
margin-left: 26%;
}
  .caja_perfil{
  display: flex;
  flex-direction: column;
  justify-content:center;
  text-align: center;
  margin-top: 0%;
}

.front,
.back {

border-radius: 2rem;
backface-visibility: hidden;
display: flex;
flex-direction: column;
align-items: center;
justify-content: center;

}
@keyframes pulseGlow {
  0% { text-shadow: 4px 4px 10px #0077ff, 8px 8px 20px #00ffea; }
  100% { text-shadow: 6px 6px 15px #00ffea, 12px 12px 30px #00ffff; }
}

@keyframes shake {
  0% { transform: translateX(0px) rotate(-0deg); }
  100% { transform: translateX(-1px) rotate(1deg); }
}
.actualizar_perfil {
  margin-top: -30%;
position: absolute;
left: 5%;
width: 45%;
background: linear-gradient(45deg, #bdbebe, #575757); 
color: rgb(255, 255, 255);
border: none;
padding: 5% 1%;
border-radius: 100px;
font-family: 'Arial', sans-serif;
font-size:10px;
font-weight: bold;
cursor: pointer;
transition: all 0.5s ease; 
}

.videooo {
  margin-top: 50%;
  width: 100%;
  text-align: center;
  font-family: 'Courier New', Courier, monospace;
  font-size: 2rem;
  font-weight: bold;
  position: relative;
  color: #fff;
  overflow: hidden;
  text-shadow: 2px 2px 4px #000000, -2px -2px 4px #000000, 2px -2px 4px #000000, -2px 2px 4px #000000; /* Borde negro */
}
.videooo:before,
.videooo:after {
  content: attr(data-text);
  position: absolute;
  top: 0;
  left: 0;
  color: #ffdd00; /* Color dorado */
  z-index: -1;
  animation: glitch 1s infinite;
  clip-path: inset(0 0 0 0);
}

.videooo:before {
  left: 2px;
  text-shadow: 2px 0px #ffd700, -2px 0px #000000; /* Dorado y negro */
}

.videooo:after {
  left: -1px;
  text-shadow: -1px 0px #ffcc00, 2px 0px #000000; /* Dorado más claro y negro */
  animation-delay: 0.3s;
}

.link{
  display: none;
}
}


@media (min-width: 481px) and (max-width: 600px) {
  /* Estilos para pantallas entre 481px y 600px */
.card_profile {
width: 50%;
height: auto;
border-radius: 2rem;
transition: transform 1500ms;
transform-style: preserve-3d;
margin-left: 25%;
}
  .caja_perfil{
  display: flex;
  flex-direction: column;
  justify-content:center;
  text-align: center;
  margin-top: 0%;
}
.front,
.back {

border-radius: 2rem;
backface-visibility: hidden;
display: flex;
flex-direction: column;
align-items: center;
justify-content: center;

}
#datos {
color: rgb(255, 255, 255);
font-size: 160%;
margin-top:35%;
margin-left: 20%;
font-family: Arial, Helvetica, sans-serif;
text-align: center;
}
.actualizar_perfil {
  margin-top: 2%;
position: absolute;
left: 5%;
width: 25%;
background: linear-gradient(45deg, #bdbebe, #575757); 
color: rgb(255, 255, 255);
border: none;
padding: 2% 2%;
border-radius: 5%;
font-family: 'Arial', sans-serif;
font-size:10px;
font-weight: bold;
cursor: pointer;
transition: all 0.5s ease; 
}

.videooo {
  margin-top: 50%;
  width: 100%;
  text-align: center;
  font-family: 'Courier New', Courier, monospace;
  font-size: 3rem;
  font-weight: bold;
  position: relative;
  color: #fff;
  overflow: hidden;
  text-shadow: 2px 2px 4px #000000, -2px -2px 4px #000000, 2px -2px 4px #000000, -2px 2px 4px #000000; /* Borde negro */
}
}

@media (min-width: 601px) and (max-width: 768px) {
   /* Estilos para pantallas muy pequeñas */
.card_profile {
width: 40%;
height: auto;
border-radius: 2rem;
transition: transform 1500ms;
transform-style: preserve-3d;
margin-left: 35%;
}
  .caja_perfil{
  display: flex;
  flex-direction: column;
  justify-content:center;
  text-align: center;
}
.front,
.back {

border-radius: 2rem;
backface-visibility: hidden;
display: flex;
flex-direction: column;
align-items: center;
justify-content: center;


}
#datos {
color: rgb(255, 255, 255);
font-size: 160%;
margin-top:6%;
margin-left: 10%;
font-family: Arial, Helvetica, sans-serif;
text-align: center;
}
.actualizar_perfil {
  margin-top: 0%;
position: absolute;
left: 5%;
width: 20%;
background: linear-gradient(45deg, #bdbebe, #575757); 
color: rgb(255, 255, 255);
border: none;
padding: 2% 2%;
border-radius: 5%;
font-family: 'Arial', sans-serif;
font-size:10px;
font-weight: bold;
cursor: pointer;
transition: all 0.5s ease; 
}
}

@media (min-width: 769px) and (max-width: 1024px) {
     /* Estilos para pantallas muy pequeñas */
.card_profile {
width: 40%;
height: auto;
border-radius: 2rem;
transition: transform 1500ms;
transform-style: preserve-3d;
margin-left: 35%;
}
  .caja_perfil{
  display: flex;
  flex-direction: column;
  justify-content:center;
  text-align: center;
}
.front,
.back {

border-radius: 2rem;
backface-visibility: hidden;
display: flex;
flex-direction: column;
align-items: center;
justify-content: center;

}
#datos {
color: rgb(255, 255, 255);
font-size: 160%;
margin-top:6%;
margin-left: 10%;
font-family: Arial, Helvetica, sans-serif;
text-align: center;
}
.actualizar_perfil {
  margin-top: 0%;
position: absolute;
left: 5%;
width: 20%;
background: linear-gradient(45deg, #bdbebe, #575757); 
color: rgb(255, 255, 255);
border: none;
padding: 1%;
border-radius: 5%;
font-family: 'Arial', sans-serif;
font-size:10px;
font-weight: bold;
cursor: pointer;
transition: all 0.5s ease; 
}
  
}
  


@media (min-width: 1025px) and (max-width: 1280px) {
  /* Estilos para pantallas entre 1025px y 1280px */
.card_profile {
width: 50%;
height: auto;
border-radius: 2rem;
transition: transform 1500ms;
transform-style: preserve-3d;
margin-left: 40%;
}
  .caja_perfil{
  display: flex;
  flex-direction: column;
  justify-content:center;
  text-align: center;
}
.front,
.back {

border-radius: 2rem;
backface-visibility: hidden;
display: flex;
flex-direction: column;
align-items: center;
justify-content: center;


}
#datos {
color: rgb(255, 255, 255);
font-size: 160%;
margin-top:6%;
margin-left: 30%;
font-family: Arial, Helvetica, sans-serif;
text-align: center;
}
.actualizar_perfil {
  margin-top: 0%;
position: absolute;
left: 5%;
width: 30%;
background: linear-gradient(45deg, #bdbebe, #575757); 
color: rgb(255, 255, 255);
border: none;
padding: 2% 2%;
border-radius: 5%;
font-family: 'Arial', sans-serif;
font-size:100%;
font-weight: bold;
cursor: pointer;
transition: all 0.5s ease; 
}
  
  
}

@media (min-width: 1281px) and (max-width: 1440px) {
  /* Estilos para pantallas entre 1281px y 1440px */
   /* Estilos para pantallas muy pequeñas */
.card_profile {
width: 60%;
height: auto;
border-radius: 2rem;
transition: transform 1500ms;
transform-style: preserve-3d;
margin-left: 20%;
}
  .caja_perfil{
  display: flex;
  flex-direction: column;
  justify-content:center;
  text-align: center;
}
.front,
.back {

border-radius: 2rem;
backface-visibility: hidden;
display: flex;
flex-direction: column;
align-items: center;
justify-content: center;

}
#datos {
color: rgb(255, 255, 255);
font-size: 160%;
margin-top:6%;
margin-left: 0%;
font-family: Arial, Helvetica, sans-serif;
text-align: center;
}

}

@media (min-width: 1025px) and (max-width: 2000px) {
  .actualizar_perfil {
  margin-top: 0%;
position: absolute;
left: 5%;
width: 12%;
background: linear-gradient(45deg, #bdbebe, #575757); 
color: rgb(255, 255, 255);
border: none;
padding: 1%;
border-radius: 5%;
font-family: 'Arial', sans-serif;
font-size:13px;
font-weight: bold;
cursor: pointer;
transition: all 0.5s ease; 
}
.card_profile {
width: 60%;
height: auto;
border-radius: 2rem;
transition: transform 1500ms;
transform-style: preserve-3d;
margin-left: 22%;
}
#datos {
color: rgb(255, 255, 255);
font-size: 160%;
margin-top:6%;
margin-left: 5%;
font-family: Arial, Helvetica, sans-serif;
text-align: center;
}

}
@media (min-width: 1441px) and (max-width: 2000px) {
  /* Estilos para pantallas entre 1441px y 1920px */
  .card_profile {
width: 60%;
height: auto;
border-radius: 2rem;
transition: transform 1500ms;
transform-style: preserve-3d;
margin-left: 20%;
}
  .caja_perfil{
  display: flex;
  flex-direction: column;
  justify-content:center;
  text-align: center;
}
.front,
.back {
border-radius: 2rem;
backface-visibility: hidden;
display: flex;
flex-direction: column;
align-items: center;
justify-content: center;
}

.actualizar_perfil {
margin-top: 0%;
position: absolute;
left: 5%;
width: 12%;
background: linear-gradient(45deg, #bdbebe, #575757); 
color: rgb(255, 255, 255);
border: none;
padding: 1%;
border-radius: 5%;
font-family: 'Arial', sans-serif;
font-size:10px;
font-weight: bold;
cursor: pointer;
transition: all 0.5s ease; 
}
  
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
