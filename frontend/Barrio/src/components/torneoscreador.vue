<template>
    <div class="torneo-container">
      <!-- Sección visual de equipos disponibles -->
      <div class="equipos-listado-visual">
        <h2 class="titulo">Equipos en el Torneo</h2>
        <div class="equipos-lista">
          <div v-for="(equipo, index) in equipos" :key="index" class="equipo-listado">
            <img :src="equipo.logo" alt="logo" class="equipo-logo-listado" />
            <span class="equipo-nombre-listado">{{ equipo.nombre }}</span>
          </div>
        </div>
      </div>
  
      <!-- Sección VS -->
      <div class="vs-section">
        <div class="equipo-selector">
          <div class="equipo-container">
            <img :src="equipo1.logo || '/placeholder.png'" alt="Equipo 1" class="equipo-logo" />
            <select v-model="equipo1" class="equipo-select">
              <option v-for="(equipo, index) in equipos" :key="'e1-'+index" :value="equipo">
                {{ equipo.nombre }}
              </option>
            </select>
          </div>
          <div class="vs-text">VS</div>
          <div class="equipo-container">
            <img :src="equipo2.logo || '/placeholder.png'" alt="Equipo 2" class="equipo-logo" />
            <select v-model="equipo2" class="equipo-select">
              <option v-for="(equipo, index) in equipos" :key="'e2-'+index" :value="equipo">
                {{ equipo.nombre }}
              </option>
            </select>
          </div>
        </div>
        <button @click="agregarPartido" class="agregar-btn">Agregar Partido</button>
      </div>
  
      <!-- Lista de partidos -->
      <div class="partidos-lista">
        <h2 class="titulo">Partidos del Torneo</h2>
        <div v-for="(partido, index) in partidos" :key="index" class="partido-item">
          <div class="partido-equipos">
            <div class="partido-equipo">
              <img :src="partido.equipo1.logo" alt="logo" class="partido-logo" />
              <span class="partido-nombre">{{ partido.equipo1.nombre }}</span>
            </div>
            <div class="vs-small">VS</div>
            <div class="partido-equipo">
              <img :src="partido.equipo2.logo" alt="logo" class="partido-logo" />
              <span class="partido-nombre">{{ partido.equipo2.nombre }}</span>
            </div>
          </div>
          <button @click="eliminarPartido(index)" class="eliminar-btn">Eliminar</button>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        equipos: [
          { nombre: 'Equipo A', logo: '/logos/equipoA.png' },
          { nombre: 'Equipo B', logo: '/logos/equipoB.png' },
          { nombre: 'Equipo C', logo: '/logos/equipoC.png' },
          { nombre: 'Equipo D', logo: '/logos/equipoD.png' },
          { nombre: 'Equipo E', logo: '/logos/equipoE.png' },
          { nombre: 'Equipo F', logo: '/logos/equipoF.png' }
        ],
        equipo1: { nombre: '', logo: '' },
        equipo2: { nombre: '', logo: '' },
        partidos: []
      };
    },
    created() {
      if (this.equipos.length > 0) {
        this.equipo1 = this.equipos[0];
        this.equipo2 = this.equipos[1] || this.equipos[0];
      }
    },
    methods: {
      agregarPartido() {
        if (this.equipo1.nombre && this.equipo2.nombre) {
          this.partidos.push({
            equipo1: { ...this.equipo1 },
            equipo2: { ...this.equipo2 }
          });
        }
      },
      eliminarPartido(index) {
        this.partidos.splice(index, 1);
      }
    }
  };
  </script>
  
  <style scoped>
  .torneo-container {
    max-width: 800px;
    margin: 0 auto;
    padding: 20px;
    color: white;
  }
  
  .titulo {
    color: #fff;
    text-align: center;
    margin-bottom: 20px;
    font-size: 1.8em;
    text-transform: uppercase;
    letter-spacing: 2px;
  }
  
  /* Estilos para la sección de equipos disponibles */
  .equipos-listado-visual {
    margin-bottom: 30px;
    background: #181818;
    border-radius: 10px;
    padding: 20px;
    box-shadow: 0 0 8px #fff3;
  }
  
  .equipos-lista {
    display: flex;
    flex-wrap: wrap;
    gap: 20px;
    justify-content: flex-start;
  }
  
  .equipo-listado {
    display: flex;
    align-items: center;
    background: #222;
    border-radius: 8px;
    padding: 10px 18px;
    box-shadow: 0 0 4px #fff2;
  }
  
  .equipo-logo-listado {
    width: 36px;
    height: 36px;
    border-radius: 50%;
    margin-right: 12px;
    border: 1px solid #fff;
  }
  
  .equipo-nombre-listado {
    color: #fff;
    font-weight: bold;
    font-size: 1.1em;
    letter-spacing: 1px;
  }
  
  /* Estilos para la sección VS */
  .vs-section {
    background: #222;
    border-radius: 10px;
    padding: 20px;
    margin-bottom: 30px;
    box-shadow: 0 0 10px rgba(255, 255, 255, 0.1);
  }
  
  .equipo-selector {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 20px;
  }
  
  .equipo-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    width: 40%;
  }
  
  .equipo-logo {
    width: 80px;
    height: 80px;
    border-radius: 50%;
    margin-bottom: 10px;
    border: 2px solid #fff;
    background-color: #333;
  }
  
  .equipo-select {
    width: 100%;
    padding: 8px;
    background-color: #333;
    color: white;
    border: 1px solid #555;
    border-radius: 5px;
  }
  
  .vs-text {
    font-size: 2em;
    font-weight: bold;
    color: #ff5722;
  }
  
  .agregar-btn {
    width: 100%;
    padding: 12px;
    background-color: #4CAF50;
    color: white;
    border: none;
    border-radius: 5px;
    cursor: pointer;
    font-size: 1em;
    font-weight: bold;
    transition: background-color 0.3s;
  }
  
  .agregar-btn:hover {
    background-color: #45a049;
  }
  
  /* Estilos para la lista de partidos */
  .partidos-lista {
    background: #222;
    border-radius: 10px;
    padding: 20px;
    box-shadow: 0 0 10px rgba(255, 255, 255, 0.1);
  }
  
  .partido-item {
    display: flex;
    justify-content: space-between;
    align-items: center;
    background-color: #333;
    padding: 15px;
    margin-bottom: 10px;
    border-radius: 5px;
  }
  
  .partido-equipos {
    display: flex;
    align-items: center;
    width: 80%;
  }
  
  .partido-equipo {
    display: flex;
    align-items: center;
    width: 45%;
  }
  
  .partido-logo {
    width: 40px;
    height: 40px;
    border-radius: 50%;
    margin-right: 10px;
    border: 1px solid #fff;
  }
  
  .partido-nombre {
    font-weight: bold;
  }
  
  .vs-small {
    margin: 0 10px;
    color: #ff5722;
    font-weight: bold;
  }
  
  .eliminar-btn {
    background-color: #f44336;
    color: white;
    border: none;
    border-radius: 5px;
    padding: 8px 12px;
    cursor: pointer;
    transition: background-color 0.3s;
  }
  
  .eliminar-btn:hover {
    background-color: #d32f2f;
  }
  </style>
  