<template>
    <div v-if="estado === 'en espera'">
      <torneo_sala_espera />
    </div>
  
    <div v-else-if="estado === 'en sorteo'">
      
      <torneoensorteo />
    </div>
  
    <div v-else-if="estado === 'finalizado'">
      <ganadortorneo/>
    </div>
  </template>
  
  <script setup>
  import { ref, onMounted } from 'vue'
  import { useRoute } from 'vue-router'
  import axios from 'axios'
  import torneoensorteo from './torneoensorteo.vue'
  import torneo_sala_espera from './torneo_sala_espera.vue'
  import ganadortorneo from './ganadortorneo.vue'
  
  const estado = ref(null)
  const route = useRoute()
    const idTorneo = route.params.id_torneo

  const obtenerEstadoTorneo = async () => {
    try {
      const res = await axios.get(`http://localhost:8000/estado_torneo/${idTorneo}`)
      console.log(idTorneo)
      estado.value = res.data.estado
    } catch (error) {
      console.error("Error al obtener el estado del torneo", error)
      estado.value = 'error'
    }
  }
  
  onMounted(() => {
    obtenerEstadoTorneo()
  })
  </script>
  
  <style scoped>
  h2 {
    color: #333;
  }
  p {
    font-size: 16px;
  }
  </style>
  