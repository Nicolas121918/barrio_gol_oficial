<template>
    <h1 class="titulo-principal">Torneos Creados</h1>

  
    <router-link to="/inicio" class="btn-volver">
      ← Volver
    </router-link>
  
    <input
      type="text"
      v-model="busqueda"
      placeholder="Buscar torneo por nombre..."
      class="buscador"
    />
  
    <div class="contenedor-torneos">
      <div class="secciones-torneos">
  
        <!-- Sección: En juego -->
        <section class="torneo-columna">
          <h2 class="titulo-principal2">Torneos en juego</h2>
  
          <div v-if="torneosFiltradosEnJuego.length" class="lista-torneos">
            <div
              v-for="torneo in torneosFiltradosEnJuego"
              :key="torneo.id"
              class="card"
            >
              <div class="card-header">
                <img :src="torneo.logo" alt="Logo torneo" class="logo-torneo" />
                <h3 class="nombre-torneo">{{ torneo.nombre }}</h3>
              </div>
              <p>Lugar: {{ torneo.lugar }}</p>
              <p>Fecha: {{ torneo.fecha }}</p>
  
              <div class="botones">
                <button @click="abrirModal(torneo)">Información</button>
                <button @click="ingresarTorneo(torneo.id)">Ingresar</button>
              </div>
            </div>
          </div>
          <p v-else class="mensaje-vacio">Aún no tienes torneos en juego que coincidan.</p>
        </section>
  
        <div class="separador"></div>
  
        <!-- Sección: Terminados -->
        <section class="torneo-columna">
          <h2 class="titulo-principal2">Torneos terminados</h2>
  
          <div v-if="torneosFiltradosTerminados.length" class="lista-torneos">
            <div
              v-for="torneo in torneosFiltradosTerminados"
              :key="torneo.id"
              class="card"
            >
              <div class="card-header">
                <img :src="torneo.logo" alt="Logo torneo" class="logo-torneo" />
                <h3 class="nombre-torneo">{{ torneo.nombre }}</h3>
              </div>
              <p>Lugar: {{ torneo.lugar }}</p>
              <p>Fecha: {{ torneo.fecha }}</p>
  
              <div class="botones">
                <button @click="abrirModal(torneo)">Información</button>
                <button @click="ingresarTorneo(torneo.id)">ver resultado</button>
              </div>
            </div>
          </div>
          <p v-else class="mensaje-vacio">Aún no tienes torneos terminados que coincidan.</p>
        </section>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        busqueda: '',
        torneos: [], // Aquí deberías tener tu lista de torneos original
      };
    },
    computed: {
      torneosEnJuego() {
        return this.torneos.filter(t => t.estado === 'en_juego');
      },
      torneosTerminados() {
        return this.torneos.filter(t => t.estado === 'terminado');
      },
      torneosFiltradosEnJuego() {
        return this.torneosEnJuego.filter(t =>
          t.nombre.toLowerCase().includes(this.busqueda.toLowerCase())
        );
      },
      torneosFiltradosTerminados() {
        return this.torneosTerminados.filter(t =>
          t.nombre.toLowerCase().includes(this.busqueda.toLowerCase())
        );
      }
    },
    methods: {
      abrirModal(torneo) {
        // lógica para abrir modal
        console.log('Mostrar info de', torneo);
      },
      ingresarTorneo(id) {
        // lógica para ingresar al torneo
        console.log('Ingresar a torneo', id);
      }
    },
    mounted() {
      // Puedes cargar los torneos aquí si vienen de una API o backend
      this.torneos = [
        {
          id: 1,
          nombre: 'Torneo Apertura',
          lugar: 'Bogotá',
          fecha: '2025-03-15',
          logo: 'https://via.placeholder.com/100',
          estado: 'en_juego'
        },
        {
          id: 2,
          nombre: 'Cierre 2024',
          lugar: 'Medellín',
          fecha: '2024-12-10',
          logo: 'https://via.placeholder.com/100',
          estado: 'terminado'
        },
        // Agrega más si necesitas
      ];
    }
  };
  </script>
  
<style scoped>
.contenedor-torneos {
  background-color: #0a0a0a;
  padding: 2rem;
  min-height: 100vh;
  color: #e0e0e0;
  font-family: 'Segoe UI', sans-serif;
  font-family:Impact, Haettenschweiler, 'Arial Narrow Bold', sans-serif;
  min-width: 1200px;
  max-width: 1200px;
}

.seccion-titulo {
  font-size: 2rem;
  color: #d4af37; /* dorado suave */
  border-left: 5px solid #d4af37;
  padding-left: 1rem;
  margin-bottom: 1.5rem;
  text-shadow: 1px 1px 3px rgba(255, 255, 255, 0.1);
}

.lista-torneos {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 2rem;
  margin-bottom: 3rem;
}

.card {
  background: linear-gradient(145deg, #1a1a1a, #0d0d0d);
  border: 1px solid #2c2c2c;
  border-radius: 16px;
  padding: 1.5rem;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.5);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  position: relative;
  overflow: hidden;
}

.card:hover {
  transform: translateY(-6px);
  box-shadow: 0 8px 24px rgba(212, 175, 55, 0.3);
  border-color: #d4af37;
}

.card-header {
  display: flex;
  align-items: center;
  margin-bottom: 1rem;
}

.logo-torneo {
  width: 55px;
  height: 55px;
  object-fit: cover;
  border: 2px solid #d4af37;
  border-radius: 50%;
  margin-right: 1rem;
}

.nombre-torneo {
  font-size: 1.2rem;
  font-weight: bold;
  color: #f0d98c;
  text-shadow: 1px 1px 2px #000;
  border: 1px solid #000;
  padding: 4px 10px;
  border-radius: 6px;
  background-color: #1c1c1c;
}

.botones {
  display: flex;
  justify-content: space-between;
  margin-top: 1rem;
  gap: 1rem;
}

.botones button {
  flex: 1;
  padding: 10px 12px;
  font-size: 0.95rem;
  font-weight: 600;
  background-color: transparent;
  color: #d4af37;
  border: 2px solid #d4af37;
  border-radius: 8px;
  transition: all 0.3s ease;
  cursor: pointer;
  position: relative;
  z-index: 1;
  overflow: hidden;
}

.botones button::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background-color: #d4af37;
  z-index: -1;
  transition: all 0.3s ease;
}
.titulo-principal2 {
  font-size: 2rem;
  color: #989898; /* Dorado */
  text-align: center;
  margin-bottom: 2rem;
  padding: 1rem;
  background: linear-gradient(to right, #111, #1a1a1a);
  border-bottom: 3px solid #222;
  border-top: 3px solid #222;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.6);
  text-shadow:
    0 0 5px rgb(46, 46, 46),
    1px 1px 2px rgb(78, 78, 78),
    2px 2px 4px #ffffff;

  font-family: Arial, Helvetica, sans-serif;
  letter-spacing: 1px;
  border-left: solid rgb(255, 208, 0) 5px;
  border-radius: 10px;
}

.botones button:hover {
  color: #0a0a0a;
  font-weight: bold;
}

.botones button:hover::before {
  left: 0;
}

.mensaje-vacio {
  font-style: italic;
  color: #aaa;
  margin-bottom: 3rem;
  text-align: center;
  font-size: 1.1rem;
}

.modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(10, 10, 10, 0.9);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 999;
}

.modal-content {
  background-color: #1b1b1b;
  padding: 2rem;
  border-radius: 12px;
  width: 90%;
  max-width: 500px;
  border: 1px solid #d4af37;
  color: #f5f5f5;
  box-shadow: 0 0 25px rgba(212, 175, 55, 0.2);
}

.secciones-torneos {
  display: flex;
  flex-wrap: wrap;
  gap: 2rem;
  justify-content: space-between;
}

.torneo-columna {
  flex: 1;
  min-width: 300px;
}

@media (max-width: 768px) {
  .secciones-torneos {
    flex-direction: column;
  }
}
.contenedor-torneos {
  padding: 2rem;
  background: #111;
  color: #fff;
  font-family: 'Segoe UI', sans-serif;
}

.titulo-principal {
  font-size: 2rem;
  color: #FFD700; /* Dorado */
  text-align: center;
  margin-bottom: 2rem;
  padding: 1rem;
  background: linear-gradient(to right, #111, #1a1a1a);
  border-bottom: 3px solid #222;
  border-top: 3px solid #222;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.6);

  text-shadow:
    0 0 5px white,
    1px 1px 2px black,
    2px 2px 4px #000;

  font-family: Arial, Helvetica, sans-serif;
  letter-spacing: 1px;

  border-radius: 10px;
}


.secciones-torneos {
  display: flex;
  gap: 2rem;
  justify-content: space-between;
  flex-wrap: wrap;
}

.torneo-columna {
  flex: 1;
  min-width: 300px;
}

.separador {    
  width: 2px;
  background-color: #333;
  margin: 0 1rem;
}
.btn-volver {
  display: inline-block;
  margin-bottom: 1rem;
  padding: 0.6rem 1.2rem;
  background-color: gold;
  color: #000;
  font-weight: bold;
  border: 2px solid #000;
  border-radius: 10px;
  text-decoration: none;
  transition: all 0.3s ease;
  box-shadow: 2px 2px 5px #000;
}

.btn-volver:hover {
  background-color: #222;
  color: gold;
  border-color: gold;
  transform: scale(1.05);
}

/* Modal */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.7); /* fondo oscuro translúcido */
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 999;
}

.modal-contenido {
  background-color: #1e1e1e; /* gris oscuro / casi negro */
  border: 2px solid #d4af37; /* borde dorado */
  border-radius: 15px;
  padding: 25px;
  width: 90%;
  max-width: 500px;
  color: #fff; /* texto blanco */
  box-shadow: 0 0 20px rgba(212, 175, 55, 0.5); /* sombra dorada */
  position: relative;
  animation: fadeIn 0.3s ease;
}

.modal-cerrar {
  position: absolute;
  top: 10px;
  right: 15px;
  background: none;
  border: none;
  font-size: 22px;
  color: #d4af37;
  cursor: pointer;
  transition: transform 0.2s;
}
.modal-cerrar:hover {
  transform: scale(1.2);
}

.modal-titulo {
  font-size: 24px;
  margin-bottom: 15px;
  color: #d4af37;
  border-bottom: 1px solid #444;
  padding-bottom: 10px;
}

.modal-logo {
  max-width: 100px;
  margin: 10px auto 20px;
  display: block;
  border-radius: 8px;
  border: 1px solid #ccc;
}

.modal-contenido p {
  margin: 10px 0;
  font-size: 16px;
  color: #ccc;
}

.modal-contenido strong {
  color: #fff;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(-20px); }
  to { opacity: 1; transform: translateY(0); }
}

.buscador {
  width: 100%;
  max-width: 400px;
  padding: 10px 15px;
  margin: 20px auto;
  display: block;
  font-size: 16px;
  border: 2px solid #d4af37;
  border-radius: 8px;
  background-color: #1e1e1e;
  color: white;
  outline: none;
}
.buscador::placeholder {
  color: #ccc;
}

</style>