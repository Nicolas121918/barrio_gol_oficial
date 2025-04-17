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

  <!-- WRAPPER para centrar -->
  <div class="navbar-wrapper">
    <nav class="navbar navbar-expand-lg bg-body-tertiary">
      <div class="container-fluid">
        <a class="navbar-brand" >BarrioGol</a>
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNavDropdown"
          aria-controls="navbarNavDropdown" aria-expanded="false" aria-label="Toggle navigation">
          <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarNavDropdown">
          <ul class="navbar-nav mx-auto">


            <li class="nav-item">
              <a class="nav-link active" aria-current="page"> <router-link id="mi_perfil_link"  to="/Perfil">
      Mi Perfil
    </router-link> 
</a>
            </li>
            <li class="nav-item">
              <a class="nav-link">
 <router-link id="ayuda_link"  to="/contacto">
      Ayuda
    </router-link></a>
            </li>
            <li class="nav-item">
              <a class="nav-link"> <router-link id="cerrar_sesion_link" to="/inicioSesion">Cerrar Sesión</router-link></a>
            </li>
          </ul>
        </div>
      </div>
    </nav>
  </div>
</template>



<script setup>
import { ref } from 'vue';
import headerapp from './headerapp.vue'
import headermobile from './headermobile.vue' 
import "bootstrap/dist/css/bootstrap.css";
import "bootstrap/dist/js/bootstrap.js";
const fecha = ref(new Date().getUTCDate());
const fecha2 = ref (new Date().getMonth() + 1)

const fecha3 = ref(new Date().getUTCFullYear());



</script>

<style scoped>


.navbar-wrapper {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
}

.navbar {
  border-radius: 12px;
  padding: 1rem 2rem;
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.1);
}

.navbar-brand {
  font-weight: bold;
  font-size: 1.5rem;
  color: #343a40;
  letter-spacing: 1px;
  text-transform: uppercase;
}

.navbar-nav .nav-link {
  color: #495057;
  font-weight: 500;
  padding: 0.5rem 1rem;
  border-radius: 8px;
  transition: all 0.3s ease;
  text-decoration: none;
}

.navbar-nav .nav-link:hover {
  background-color: #f1f3f5;
  color: #0d6efd;
  text-decoration: none;
}

.router-link-active {
  color: #0d6efd !important;
  font-weight: bold;
}

#mi_perfil_link, #cerrar_sesion_link, #ayuda_link {
  text-decoration: none;
  color: inherit;
}

.navbar-toggler {
  border: none;
}





</style>