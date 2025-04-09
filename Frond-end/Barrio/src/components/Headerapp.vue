<template>

<header class="header1">
  <!-- perfil del usuario -->
      <router-link class="link perfil" to="/Perfil">
        <img class="api1" src="../assets/iconos header/perfil-del-usuario.png" alt="Perfil">
      </router-link>
        <!-- casa-->
      <router-link class="link home" to="/home">
        <img class="api2" src="../assets/iconos header/hogar.png" alt="Home">
      </router-link>
        <!-- Encabezado principal con enlaces a distintas rutas -->
      <router-link class="link torneos" to="/torneos">
        <img class="api3" src="../assets/iconos header/torneo.png" alt="Torneo">
      </router-link>
      <router-link class="link equipo" to="/equipos">
        <img class="api5" src="../assets/iconos header/clan.png" alt="Equipo">
      </router-link>
      <router-link class="link video" to="/jugadores">
        <img class="api4" src="../assets/imagenes/personas.png" alt="Video">
      </router-link>

      <router-link to="/videos" class=" link">
        <img class="api4" src="../assets/imagenes/video.png" alt="">
      </router-link>
    <router-link to="/notificaciones" class="link bell">
      <div class="loader">
    <svg
      viewBox="0 0 24 24"
      fill="none"
      height="24"
      width="24"
      xmlns="http://www.w3.org/2000/svg"
      aria-hidden="true"
      class="w-6 h-6 text-gray-800 dark:text-white">
      <path
        d="M12 5.365V3m0 2.365a5.338 5.338 0 0 1 5.133 5.368v1.8c0 2.386 1.867 2.982 1.867 4.175 0 .593 0 1.292-.538 1.292H5.538C5 18 5 17.301 5 16.708c0-1.193 1.867-1.789 1.867-4.175v-1.8A5.338 5.338 0 0 1 12 5.365ZM8.733 18c.094.852.306 1.54.944 2.112a3.48 3.48 0 0 0 4.646 0c.638-.572 1.236-1.26 1.33-2.112h-6.92Z"
        stroke-width="2"
        stroke-linejoin="round"
        stroke-linecap="round"
        stroke="currentColor"></path>
    </svg>
    <div class="point"></div>
    <div class="notification">  No tienes Notificaciones Hoy: {{fecha }}</div>
  </div>
  </router-link>
      <router-link class="link torneos" to="/stores">
        <img class="api4" src="../assets/imagenes/futbol.png" alt="Tienda">
      </router-link>
      <router-link class="link api8" to="/home">
        <img class="api8" src="../assets/imagenes/logo.png" alt="Logo">
      </router-link>
    </header>
</template>

<script setup>


</script>

<style scoped>
.loader {
width: fit-content;
height: fit-content;
background-color: rgb(58, 58, 58);
border-radius: 7px;
padding: 10px;
display: flex;
align-items: center;
justify-content: center;
position: relative;
cursor: pointer;
transition: 0.2s;
}

.loader:hover {
background-color: rgb(26, 26, 26);
}

.loader:hover svg {
color: white;
}

.loader svg {
color: rgba(255, 255, 255, 0.651);
transform: scale(1.2);
transition: 0.2s;
}

.point {
position: absolute;
bottom: 5px;
left: 5px;
width: 6px;
height: 6px;
background-color: rgb(0, 255, 0);
border-radius: 25px;
display: flex;
align-items: center;
justify-content: center;
}

.point::before {
content: "";
position: absolute;
width: 1px;
height: 1px;
background-color: rgb(0, 255, 0);
border-radius: 25px;
animation: loop 1s 0s infinite;
}

.notification {
position: absolute;
left: 50%;
transform: translateX(-50%);
background-color: #333;
color: white;
padding: 8px;
border-radius: 5px;
white-space: nowrap;
display: none;
font-size: 12px;
z-index: 10;
top: 45px;
}

.loader:hover .notification {
display: block;
}

@keyframes loop {
0% {
  background-color: rgb(0, 255, 0);
  width: 1px;
  height: 1px;
}
100% {
  background-color: rgba(0, 255, 0, 0);
  width: 30px;
  height: 30px;
}
}

.header1 {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    padding: 10px;
    z-index: 1000;
    background: linear-gradient(rgb(129, 126, 126), rgb(255, 255, 255));
    display: flex;
    align-items: center;
    justify-content: space-around;
    flex-wrap: wrap;
    height: auto;
    overflow: hidden;

  }

  

  .api1, .api2, .api3, .api4, .api5, .api6 {
    filter: drop-shadow(0 0 1px rgb(0, 0, 0));
    transition: transform 0.5s;
    height: 55px;
    width: auto;
    margin: 0 5px;
  }
  

  .api8 {
    position: relative;
    height: 110px;
    width: auto;
    border-right: black;
    border-right-style: solid;
    border-right-width: 1px;
  }
  .api11 {
    position: relative;
    height: 110px;
    width: auto;

  }

  .api8:hover {
  animation: bounce 0.6s ease-in-out;
}

@keyframes bounce {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-10px); } 
}


  .api1:hover, .api2:hover, .api3:hover, .api4:hover, .api5:hover, .api6:hover {
    transform: scale(1.2);

  }


  a.router-link-active, a.router-link-exact-active {
    color: inherit;
    text-decoration: none;
    background-color: none;
  }
  

  .link {
    display: inline-block;
    margin: 0;
    padding: 0;
  }
  .link:hover {
  background: none;
}



@media (max-width: 480px) {
  /* Estilos para pantallas con un ancho máximo de 480px */
  .header1 {
    background: linear-gradient(rgb(56, 118, 103), rgb(255, 255, 255));
 
  }
  .api1, .api2, .api3, .api4, .api5, .api6 {
    filter: drop-shadow(0 0 1px rgb(0, 0, 0));
    transition: transform 0.5s;
    height:20px;
    width: auto;
  }

  .api8 {
    position: relative;
    height: 36px;
    width: auto;
    border-right: black;
    border-right-style: solid;
    border-right-width: 1px;
  }
}


@media (min-width: 481px) and (max-width: 600px) {
  /* Estilos para pantallas entre 481px y 600px */
  .header1 {
    background: linear-gradient(rgb(56, 118, 103), rgb(255, 255, 255));
 
  }
  .api1, .api2, .api3, .api4, .api5, .api6 {
    filter: drop-shadow(0 0 1px rgb(0, 0, 0));
    transition: transform 0.5s;
    height:38px;
    width: auto;
  }

  .api8 {
    position: relative;
    height: 70px;
    width: auto;
    border-right: black;
    border-right-style: solid;
    border-right-width: 1px;
  }
}


@media (min-width: 601px) and (max-width: 768px) {
  /* Estilos para pantallas entre 601px y 768px */
  .header1 {
    background: linear-gradient(rgb(56, 118, 103), rgb(255, 255, 255));
 
  }
  .api1, .api2, .api3, .api4, .api5, .api6 {
    filter: drop-shadow(0 0 1px rgb(0, 0, 0));
    transition: transform 0.5s;
    height:38px;
    width: auto;
  }

  .api8 {
    position: relative;
    height: 70px;
    width: auto;
    border-right: black;
    border-right-style: solid;
    border-right-width: 1px;
  }
}


@media (min-width: 769px) and (max-width: 1024px) {
  /* Estilos para pantallas entre 769px y 1024px */
  .header1 {
    background: linear-gradient(rgb(56, 118, 103), rgb(255, 255, 255));
 
  }
  .api1, .api2, .api3, .api4, .api5, .api6 {
    filter: drop-shadow(0 0 1px rgb(0, 0, 0));
    transition: transform 0.5s;
    height:38px;
    width: auto;
  }

  .api8 {
    position: relative;
    height: 70px;
    width: auto;
    border-right: black;
    border-right-style: solid;
    border-right-width: 1px;
  }
}


@media (min-width: 1025px) and (max-width: 1280px) {
  /* Estilos para pantallas entre 1025px y 1280px */
  .header1 {
    background: linear-gradient(rgb(56, 118, 103), rgb(255, 255, 255));
 
  }
  .api1, .api2, .api3, .api4, .api5, .api6 {
    filter: drop-shadow(0 0 1px rgb(0, 0, 0));
    transition: transform 0.5s;
    height:38px;
    width: auto;
  }

  .api8 {
    position: relative;
    height: 70px;
    width: auto;
    border-right: black;
    border-right-style: solid;
    border-right-width: 1px;
  }
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

