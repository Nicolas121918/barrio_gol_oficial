<template>
  <div id="root">
  <div class="caja_principal5">
    <header>
<Principal></Principal>
    </header>
  </div>
</div>
<routerView></routerView>
</template>
<script setup>

import Principal from './components/Principal.vue';
import 'leaflet/dist/leaflet.css';
import { useUsuarios } from './stores/usuario';
const movieStore=useUsuarios();

</script>

<style>
/* Estilo para el body */
body {
  
background: 
  linear-gradient(rgba(0, 0, 0, 0.3), rgba(0, 0, 0, 0.3)), 
  url('../src/assets/imagenes/fondo.jpeg');
background-size: cover;
background-attachment: fixed;
background-position: center;
display: flex;
justify-content: center; /* Centrado horizontal */
align-items: flex-start; /* Centrado vertical */
width: auto;
height: auto;
padding: 0;
margin: 0;

}

@media (max-width: 320px) {
  /* Estilos para pantallas muy pequeñas */

  /* Estilo para el body */

  body{

    width: 100%;
    height: 100%;

  }

}



</style>

