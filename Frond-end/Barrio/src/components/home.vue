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
<div class="caja_salir">


<div id="input">
  <button class="value" style="position: relative; width: 70%;" >
    <svg viewBox="0 0 16 16" xmlns="http://www.w3.org/2000/svg" data-name="Layer 2"><path fill="#7D8590" d="m1.5 13v1a.5.5 0 0 0 .3379.4731 18.9718 18.9718 0 0 0 6.1621 1.0269 18.9629 18.9629 0 0 0 6.1621-1.0269.5.5 0 0 0 .3379-.4731v-1a6.5083 6.5083 0 0 0 -4.461-6.1676 3.5 3.5 0 1 0 -4.078 0 6.5083 6.5083 0 0 0 -4.461 6.1676zm4-9a2.5 2.5 0 1 1 2.5 2.5 2.5026 2.5026 0 0 1 -2.5-2.5zm2.5 3.5a5.5066 5.5066 0 0 1 5.5 5.5v.6392a18.08 18.08 0 0 1 -11 0v-.6392a5.5066 5.5066 0 0 1 5.5-5.5z"></path></svg>
    <router-link id="mi_perfil_link"  to="/Perfil">
      Mi Perfil
    </router-link>
  </button>
  <button class="value" style="position: relative; width:60%;">
    <svg id="Line" viewBox="0 0 32 32" xmlns="http://www.w3.org/2000/svg"><path fill="#7D8590" id="XMLID_1646_" d="m17.074 30h-2.148c-1.038 0-1.914-.811-1.994-1.846l-.125-1.635c-.687-.208-1.351-.484-1.985-.824l-1.246 1.067c-.788.677-1.98.631-2.715-.104l-1.52-1.52c-.734-.734-.78-1.927-.104-2.715l1.067-1.246c-.34-.635-.616-1.299-.824-1.985l-1.634-.125c-1.035-.079-1.846-.955-1.846-1.993v-2.148c0-1.038.811-1.914 1.846-1.994l1.635-.125c.208-.687.484-1.351.824-1.985l-1.068-1.247c-.676-.788-.631-1.98.104-2.715l1.52-1.52c.734-.734 1.927-.779 2.715-.104l1.246 1.067c.635-.34 1.299-.616 1.985-.824l.125-1.634c.08-1.034.956-1.845 1.994-1.845h2.148c1.038 0 1.914.811 1.994 1.846l.125 1.635c.687.208 1.351.484 1.985.824l1.246-1.067c.787-.676 1.98-.631 2.715.104l1.52 1.52c.734.734.78 1.927.104 2.715l-1.067 1.246c.34.635.616 1.299.824 1.985l1.634.125c1.035.079 1.846.955 1.846 1.993v2.148c0 1.038-.811 1.914-1.846 1.994l-1.635.125c-.208.687-.484 1.351-.824 1.985l1.067 1.246c.677.788.631 1.98-.104 2.715l-1.52 1.52c-.734.734-1.928.78-2.715.104l-1.246-1.067c-.635.34-1.299.616-1.985.824l-.125 1.634c-.079 1.035-.955 1.846-1.993 1.846zm-5.835-6.373c.848.53 1.768.912 2.734 1.135.426.099.739.462.772.898l.18 2.341 2.149-.001.18-2.34c.033-.437.347-.8.772-.898.967-.223 1.887-.604 2.734-1.135.371-.232.849-.197 1.181.089l1.784 1.529 1.52-1.52-1.529-1.784c-.285-.332-.321-.811-.089-1.181.53-.848.912-1.768 1.135-2.734.099-.426.462-.739.898-.772l2.341-.18h-.001v-2.148l-2.34-.18c-.437-.033-.8-.347-.898-.772-.223-.967-.604-1.887-1.135-2.734-.232-.37-.196-.849.089-1.181l1.529-1.784-1.52-1.52-1.784 1.529c-.332.286-.81.321-1.181.089-.848-.53-1.768-.912-2.734-1.135-.426-.099-.739-.462-.772-.898l-.18-2.341-2.148.001-.18 2.34c-.033.437-.347.8-.772.898-.967.223-1.887.604-2.734 1.135-.37.232-.849.197-1.181-.089l-1.785-1.529-1.52 1.52 1.529 1.784c.285.332.321.811.089 1.181-.53.848-.912 1.768-1.135 2.734-.099.426-.462.739-.898.772l-2.341.18.002 2.148 2.34.18c.437.033.8.347.898.772.223.967.604 1.887 1.135 2.734.232.37.196.849-.089 1.181l-1.529 1.784 1.52 1.52 1.784-1.529c.332-.287.813-.32 1.18-.089z"></path><path id="XMLID_1645_" fill="#7D8590" d="m16 23c-3.859 0-7-3.141-7-7s3.141-7 7-7 7 3.141 7 7-3.141 7-7 7zm0-12c-2.757 0-5 2.243-5 5s2.243 5 5 5 5-2.243 5-5-2.243-5-5-5z"></path></svg>
    
    <router-link id="ayuda_link"  to="/contacto">
      Ayuda
    </router-link>
   
  </button>
  <button class="value">
    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#7D8590" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="feather feather-clock">
        <circle cx="12" cy="12" r="10"></circle>
        <line x1="12" y1="12" x2="12" y2="7"></line>
        <line x1="12" y1="12" x2="15" y2="12"></line>
    </svg>
    {{ fecha+('/')}}
    {{ fecha2+('/') }}
    {{ fecha3}}
</button>



  <button class="value" style="position: relative; width: 80%;" >
    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="#7D8590"  stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="feather feather-log-out"><path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"></path><polyline points="16 17 21 12 16 7"></polyline><line x1="21" y1="12" x2="9" y2="12"></line></svg>
  <router-link id="cerrar_sesion_link" to="/inicioSesion">Cerrar Sesión</router-link>
</button>
</div>



</div>


</template>


<script setup>
import { ref } from 'vue';
import headerapp from './headerapp.vue'
import headermobile from './headermobile.vue' 
const fecha = ref(new Date().getUTCDate());
const fecha2 = ref (new Date().getMonth() + 1)

const fecha3 = ref(new Date().getUTCFullYear());



</script>

<style scoped>
.caja_salir{
  margin-top: 30%;
  text-align: center;
  display: flex;
  flex-direction: column;
  align-items: center ;
}
#input {
  all: unset;
  width: 100%;
  height: 115%;
  border-radius: 5px;
  background-color: #0D1117;
  display: flex;

  justify-content: center;
}
#input:hover{
  box-shadow: 0 0 5px 5px #7d6c1833
}

#ayuda_link {
  all: unset;
  top: 35%;
  left: 0;
  width: 100%;
  height:100%;
  z-index: 1;
  background: transparent; 
  border: none; 
}

#mi_perfil_link{
  all: unset;

  top: 35%;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: 1;
  background: transparent; 
  border: none; 

}

#cerrar_sesion_link{
  all: unset;
  top: 40%;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: 1;
  background: transparent; 
  border: none; 
  color: red;
  
}

.value {
  background-color: transparent;
  border: none;
  padding: 35px;
  color: #e5c210;
  display: flex;
  position: relative;
  gap: 20px;
  cursor: pointer;
 
}

.value:not(:active):hover,
.value:focus {
  background-color: #21262C;
}

.value:focus,
.value:active {
  background-color: #1A1F24;
  outline: none;
}

.value::before {
  content: "";
  position: absolute;
  top: 5px;
  left: -10px;
  width: 5px;
  height: 80%;
  background-color: #2F81F7;
  border-radius: 5px;
  opacity: 0;
}

.value:focus::before,
.value:active::before {
  opacity: 1;
}

.value svg {
  width: 15px
}

#input:hover > :not(.value:hover) {
  transition: 300ms;
  filter: blur(1px);
  transform: scale(0.95,0.95);
}



</style>