<template >
    <header class="header" v-if="showHeader">
    <!-- Botón de hamburguesa -->
    <div class="boton-hamburguesa" @click="toggleMenu">
      <div></div>
      <div></div>   
      <div></div>
    </div>
    <nav>
      <section class="botones-prin">
        <router-link id="boton" to="/videohome">Home</router-link>
        <router-link id="boton"  to="/contactanos">Sobre Nosotros</router-link>
        <router-link id="boton"  to="/inicioSesion">Iniciar Sesión</router-link>
      </section>
    </nav>
    
  <!-- Menú desplegable -->
  <div class="menu-desplegable" id="menu">
    <router-link id="boton" to="/videohome">Home</router-link>
    <router-link id="boton" class="sobreNosotros" to="/contactanos">Sobre Nosotros</router-link>
    <router-link id="boton" class="consultar" to="/inicioSesion">Iniciar Sesión</router-link>
  </div>
  
</header>


</template>


<style>
/* Estilo para los botones */
#boton {
  padding: 10px 20px;
  font-weight: bold;
  border-radius: 8px;
  transition: background-color 0.3s ease;
  border: 2px solid black;
  color: white;
  text-align: center;
  text-decoration: none;
  cursor: pointer;
  background-image: linear-gradient(
    rgba(0, 0, 0, 0.2),
    rgba(0, 0, 0, 0.3)
  ),
  url(https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQRliDRc-R2CvZHWA7uopNByFtaWoUIhmqk3Q&s);
  background-size: cover;
  background-position: center;
}

#boton:hover {
  background-image: linear-gradient(
    rgba(0, 0, 0, 0.7),
    rgba(0, 0, 0, 0.7)
  ),
  url(https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQRliDRc-R2CvZHWA7uopNByFtaWoUIhmqk3Q&s);
}

#boton:active {
  background-color: #FFD700;
}

/* Estilo para los botones específicos */
.sobreNosotros, .Contacto, .consultar {
  background-color: #444;
}

/* Estilos para el botón de hamburguesa */
.boton-hamburguesa {
  display: none;
  flex-direction: column;
  justify-content: space-between;
  width: 30px;
  height: 25px;
  cursor: pointer;
}
/* Barra navegacion*/
.botones-prin{
display: flex;
width: auto;
justify-content: space-around;
align-items: flex-start;
flex-wrap: wrap;
margin: 0; 
align-self: flex-start;

gap: 150px;
}


.boton-hamburguesa div {
  background-color: rgba(255, 255, 255, 0.959); /* Color de las barras */
  height: 20%;
  width: 100%;
  border-radius: 5px;
  transition: all 0.3s ease-in-out;
}

/* Menú desplegable */
.menu-desplegable {
  display: none;
  position: absolute;
  top: 60px; /* Ajustar según necesidad */
  right: 10px;
  background-color: rgb(0, 0, 0);
  border: 1px solid #ccc;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  padding: 10px;
  z-index: 1000;
  flex-direction: column;
}

.menu-desplegable.activo {
  display: flex;
}

/* Estilo para los enlaces dentro del menú desplegable */
.menu-desplegable a {
  text-decoration: none;
  color: black;
  padding: 8px 12px;
  border-radius: 4px;
  background-color: #000000;
  transition: background-color 0.3s ease;
}

.menu-desplegable a:hover {
  background-color: #000000;
}

.header {
  display: flex;
  justify-content: flex-end; 
  align-items: flex-start;  
  padding: 10px;
}


  /* Contenedor principal contenedor del header */
  .caja_principal5 {
    display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: flex-start;
      height: auto;
      width: auto;
      padding-top: 0; 
       
  }
  @media (max-width: 320px) {
  /* Estilos para pantallas muy pequeñas */
  .boton-hamburguesa {
    display: flex; /* Asegura que el botón hamburguesa sea visible */
    position: absolute;
    width: 30px;
    height: 25px;
    top: 10px;
    left: 10px;
    cursor: pointer;
    background-color: rgb(0, 119, 255);
  }
.botones-prin{
    display: none;
    gap: 5%;
}
.menu-desplegable{
  margin-right: -20%;
}
/* Estilo para los botones */
#boton {
  padding: 1px 10px;
  font-weight: bold;
  border-radius: 8px;
  transition: background-color 0.3s ease;
  border: 2px solid black;
  color: rgb(255, 255, 255);
  text-align: center;
  text-decoration: none;
  cursor: pointer;
  background-size: cover;
  background-position: center;
  margin-bottom: 2px;
}

}

@media (max-width: 480px) {
/* Estilos para pantallas muy pequeñas */
  .boton-hamburguesa {
    display: flex; /* Asegura que el botón hamburguesa sea visible */
    position: absolute;
    width: 30px;
    height: 25px;
    top: 10px;
    left: 10px;
    cursor: pointer;
    background-color: rgb(0, 119, 255);
  }
.botones-prin{
    display: none;
}
 
 .menu-desplegable {
   top: 5%;
   right: 60%;
   background-color: transparent;
   border: 1px solid #ccc;
   padding: 10px;
   z-index: 1000;
   flex-direction: column;
 }
 /* Estilo para los botones */
#boton {
  padding: 1px 10px;
  font-weight: bold;
  border-radius: 8px;
  transition: background-color 0.3s ease;
  border: 2px solid black;
  color: white;
  text-align: center;
  text-decoration: none;
  cursor: pointer;
  background-image: linear-gradient(
    rgba(0, 0, 0, 0.2),
    rgba(0, 0, 0, 0.3)
  ),
  url(https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQRliDRc-R2CvZHWA7uopNByFtaWoUIhmqk3Q&s);
  background-size: cover;
  background-position: center;
  margin-bottom: 2px;
}

}


@media (min-width: 481px) and (max-width: 600px) {
  /* Estilos para pantallas entre 481px y 600px */
  .header{
    width: auto;
    
  }

  /* Barra navegacion*/
.botones-prin{
width: 150%;
display: flex;
justify-content: space-around;
flex-wrap: wrap;
margin: 0; 
align-self: flex-start;
gap: 10%;
}
}

@media (min-width: 601px) and (max-width: 768px) {
  /* Estilos para pantallas entre 601px y 768px */
  .header{
    width: auto;
    
  }

  /* Barra navegacion*/
.botones-prin{
width: 150%;
display: flex;
justify-content: space-around;
flex-wrap: wrap;
margin: 0; 
align-self: flex-start;
gap: 10%;
}
}
  


@media (min-width: 1025px) and (max-width: 1280px) {
  /* Estilos para pantallas entre 1025px y 1280px */
  
}

@media (min-width: 1281px) and (max-width: 1440px) {
  /* Estilos para pantallas entre 1281px y 1440px */
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

<script setup>
import { computed } from 'vue';
import { useRoute } from 'vue-router';
const route = useRoute();
const showHeader = computed(() =>
  route.path !== '/Perfil' &&
  route.path !== '/contacto' &&
  route.path !== '/torneos' &&
  route.path !== '/equipos' &&
  route.path !=='/creartorneo' && 
  route.path !=='/diego' &&
  route.path !=='/diegos' && 
  route.path !=='/pay' &&
  route.path !=='/perfiles' &&
  route.path !=='/torneoscreador' &&
  route.path !=='/targetas' && 
  route.path !=='/galeria' &&
  route.path !=='/torneo_creados' &&
  route.path !=='/gana'&& 
  route.path !== '/store' && 
  route.path !== '/vendedor' && 
  route.path !=='/crearpartido' && 
  route.path !=='/subirvideo'

);
function toggleMenu() {
  const menu = document.getElementById('menu');
  menu.classList.toggle('activo'); // Alterna la visibilidad del menú
}

</script>
