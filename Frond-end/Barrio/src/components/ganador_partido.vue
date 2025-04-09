<template>
    <div v-if="showResults" class="modal">
      <div class="modal-content">
        <h2 class="result_fin">Resultados Finales "{{ nombrepartido }}"</h2>
        <div class="result-container">
          <div v-if="isMatchTied" class="tie-result">
            <p class="tie-message">¡Es un empate!</p>
            <div class="resul empate-logos">
  <div class="equipo2">
    <img :src="teamAWinnerLogo" alt="Logo equipo A" class="team-logo-modal4" />
    <p>{{ teamA.name }} - {{ teamA.score }} goles</p>
  </div>
  <div class="equipo">
    <img :src="teamBWinnerLogo" alt="Logo equipo B" class="team-logo-modal4" />
    <p>{{ teamB.name }} - {{ teamB.score }} goles</p>
  </div>
</div>
          </div>
  
          <div class="contiene3" v-else>
            <!-- Ganador -->
            <div class="team-result" :class="{ winner: isTeamAWinner }">
              <div class="team-logo-container">
                <p class="ganr2">Ganador</p>
                <img
  :src="isTeamAWinner ? teamAWinnerLogo : teamBWinnerLogo"
  alt="Logo Equipo Ganador"
  class="team-logo-modal1"
/>
              </div>
              <p class="ganr">
                {{ isTeamAWinner ? teamA.name : teamB.name }} -
                {{ isTeamAWinner ? teamA.score : teamB.score }} goles
              </p>
              <img src="../assets/imagenes/balondeoro.png" alt="Ganador" class="gif" />
            </div>
  
            <!-- Perdedor -->
            <div class="team-result" :class="{ winner: !isTeamAWinner }">
              <div class="team-logo-container">
                <p class="ganr3">Perdedor</p><img
  :src="!isTeamAWinner ? teamAWinnerLogo : teamBWinnerLogo"
  alt="Logo Equipo Perdedor"
  class="team-logo-modal5"
/>
              </div>
              <p class="ganr">
                {{ !isTeamAWinner ? teamA.name : teamB.name }} -
                {{ !isTeamAWinner ? teamA.score : teamB.score }} goles
              </p>
              <img src="https://i.pinimg.com/originals/a4/38/4c/a4384c5d86fa696a392ab216bc09a3d3.gif" alt="Perdedor" class="gif2" />
            </div>
          </div>
        </div>
        <button class="close-button" @click="goToComponent">Cerrar</button>
      </div>
    </div>
  </template>
 <script>
 import axios from 'axios';
 
 export default {
   data() {
     return {
       teamA: {
         name: "",
         logo: "",
         score: 0,
       },
       teamB: {
         name: "",
         logo: "",
         score: 0,
       },
       nombrepartido: "",
     };
   },
   computed: {
     showResults() {
       return this.teamA.score >= 0 && this.teamB.score >= 0;
     },
     isTeamAWinner() {
       return this.teamA.score > this.teamB.score;
     },
     isMatchTied() {
       return this.teamA.score === this.teamB.score;
     },
     teamAWinnerLogo() {
       return this.teamA.logo ? `http://127.0.0.1:8000/${this.teamA.logo}` : '';
     },
     teamBWinnerLogo() {
       return this.teamB.logo ? `http://127.0.0.1:8000/${this.teamB.logo}` : '';
     }
   },
   methods: {
     async fetchResultados() {
       try {
         const id = this.$route.params.id;
         const response = await axios.get(`http://localhost:8000/resultado_detallado/${id}`);
         const data = response.data;
 
         this.nombrepartido = data.nombre_partido;
 
         if (data.resultado === "Empate") {
           this.teamA = {
            
             name: data.equipos[0].nombre,
             logo: data.equipos[0].logo,
             score: data.equipos[0].goles,
           };
           this.teamB = {
             name: data.equipos[1].nombre,
             logo: data.equipos[1].logo,
             score: data.equipos[1].goles,
           };
         } else {
           this.teamA = {
             name: data.ganador.nombre,
             logo: data.ganador.logo,
             score: data.ganador.goles,
           };
           this.teamB = {
             name: data.perdedor.nombre,
             logo: data.perdedor.logo,
             score: data.perdedor.goles,
           };
         }
 
       } catch (error) {
         console.error("Error al obtener resultados:", error);
       }
     },
     goToComponent() {
       this.$router.push({ name: 'partidos_creados' });
     },
   },
   mounted() {
     this.fetchResultados();
   },
 };
 </script>
 
 
    
     <style scoped>
   .result_fin{
     color: rgb(255, 255, 255);
     font-size: 220%;
     font-family:Impact, Haettenschweiler, 'Arial Narrow Bold', sans-serif;
     text-shadow: 
       1px 1px 0 black,   /* Sombra a la derecha y abajo */
       -1px -1px 0 rgb(255, 213, 0), /* Sombra a la izquierda y arriba */
       4px -1px 0 rgb(255, 187, 0),  /* Sombra a la derecha y arriba */
       -1px 1px 0 rgb(0, 0, 0);  /*
   }
   /* General Styles */
   }
   .match-container {
     display: flex;
     flex-direction: column;
     align-items: center;
     gap: 20px;
     text-align: center;
     padding: 10px;
     font-family: "Poppins", sans-serif;
     position: relative; /* Necesario para la colocación del pseudo-elemento */
     border-radius: 20px;
     box-shadow: 0 8px 20px rgba(0, 0, 0, 0.1);
     max-width: 750px;
     margin: 30px auto;
     border: 5px solid #ffffff; /* Dorado */
     overflow: hidden; 
     z-index: 1;
     box-shadow: rgb(255, 255, 255) 0 0 40px;
     margin-top: 50%;
     /* Asegura que no haya desbordamiento del contenido */
 }
 
 .match-container::before {
     content: '';
     position: absolute;
     top: 0;
     left: 0;
     width: 100%;
     height: 100%;
     background-image: url("https://st5.depositphotos.com/11450098/66357/i/450/depositphotos_663570442-stock-photo-black-white-classic-photo-football.jpg");
     background-repeat: no-repeat;
     background-size: cover;
     filter: blur(2px); /* Aplica desenfoque solo a la imagen de fondo */
     z-index: -1; /* Coloca la imagen detrás del contenido */
 }
 .resul {
    color: rgb(255, 255, 255);
    text-shadow: 
       1px 1px 0 black,   /* Sombra a la derecha y abajo */
       -1px -1px 0 black, /* Sombra a la izquierda y arriba */
       1px -1px 0 black,  /* Sombra a la derecha y arriba */
       -1px 1px 0 black;  /* Sombra a la izquierda y abajo */
    font-family: Georgia, 'Times New Roman', Times, serif;
 }
 
 
   
   .match-title {
     font-size: 250%;
     color: #ffffff;
     font-weight: 700;
     font-family:Cambria, Cochin, Georgia, Times, 'Times New Roman', serif;
     text-shadow: rgb(0, 0, 0) 0 0 5px;
     text-decoration:underline;
   }
   
   .match-subtitle {
     font-size: 20px;
     color: #ffffff;
     margin-bottom: 15px;
     text-shadow: black 0 0 5px;
   }
   
   .match-subtitle span {
     font-weight: 700;
     color: #ffd000; /* Dorado */
   }
   
   .match-info {
     background-color: #f1f1f1;
     padding: 10px 20px;
     border-radius: 10px;
     font-size: 18px;
     color: #333333;
   }
   
   .match-info span {
     color: #d4af37;
     font-weight: bold;
   }
   
   .match-content {
     display: flex;
     justify-content: center;
     align-items: center;
     gap: 60px;
   }
   
   .team {
     text-align: center;
   }
   
   .team-logo {
     width: 130px;
     height: 130px;
     object-fit: cover;
     border-radius: 50%;
     border: solid rgb(0, 0, 0);
     box-shadow: 0 0 40px rgb(255, 238, 0);
     margin-bottom: 10px;
   }
   
   .team-name {
     font-size: 180%;
     font-weight: 600;
     color: #ffffff;
     text-shadow: 0 0 2px rgb(255, 208, 0);
     box-shadow: 0 0 10px white;
     border: solid rgb(252, 252, 252);
     background-color: black;
   }
    
   .scoreboard {
     display: flex;
     justify-content: center;
     gap: 40px;
   }
   .contiene3{
     display: flex;
   }
   
   .team-score {
     text-align: center;
   }
   .team-logo-modal1 {
    margin-top: 5vh;
    margin-right: 10px;
    width: 150px;
    height: 150px;
    max-width: 200px;
    height: auto;
    border: 5px solid rgb(251, 255, 0);
    border-radius: 50%;
    padding: 8px;
    background: radial-gradient(circle, rgba(255, 255, 255, 0.5) 20%, rgba(0, 0, 0, 0) 80%);
    box-shadow: 0 0 80px rgba(255, 255, 0, 1),
                0 0 120px rgb(109, 109, 109),
                0 0 150px rgb(255, 255, 255);
    animation: glow 7s infinite alternate ease-in-out;
    transition: transform 0.3s ease, box-shadow 0.3s ease, filter 0.3s ease;
}

/* Efecto de resplandor PERMANENTE */
@keyframes glow {
    0% { box-shadow: 0 0 80px rgba(255, 255, 0, 1), 0 0 120px rgba(255, 215, 0, 1); }
    100% { box-shadow: 0 0 100px rgba(255, 255, 0, 1), 0 0 150px rgba(255, 215, 0, 1); }
}

/* Hover con destello repentino + vibración ligera */
.team-logo-modal1:hover {
    transform: scale(1.1);
    animation: shine 0.3s forwards, vibrate 0.2s ease-in-out 2;
    filter: brightness(10);

}

/* Destello dorado intenso al hacer hover */
@keyframes shine {
    0% { filter: brightness(1); }
    100% { filter: brightness(2); }
}

/* Efecto de vibración leve en hover */
@keyframes vibrate {
    0% { transform: scale(1.1) translateX(0); }
    25% { transform: scale(1.1) translateX(-2px); }
    50% { transform: scale(1.1) translateX(2px); }
    75% { transform: scale(1.1) translateX(-2px); }
    100% { transform: scale(1.1) translateX(0); }
}
.team-logo-modal3 {
    margin-top: 5vh;
    width: 100px;
    height: 100px;
    max-width: 200px;
    height: auto;
    border: 2px solid rgb(255, 255, 246);
    border-radius: 50%;
    padding: 8px;
    background: radial-gradient(circle, rgba(255, 255, 255, 0.5) 20%, rgba(0, 0, 0, 0) 80%);
    box-shadow: 0 0 80px rgba(255, 255, 0, 1),
                0 0 120px rgb(109, 109, 109),
                0 0 150px rgb(255, 255, 255);

    transition: transform 0.3s ease, box-shadow 0.3s ease, filter 0.3s ease;
}

/* Efecto de resplandor PERMANENTE */

/* Hover con destello repentino + vibración ligera */
.team-logo-modal3:hover {
    transform: scale(1.1);
    filter: brightness(10);

}
.team-logo-modal4 {
  margin-top: 60px;
  height: 160px;
  width: 160px;
  border-radius: 50%;
  border: 2px solid rgb(255, 255, 255);
  box-shadow: 0 0 10px rgb(121, 121, 121);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  object-fit: cover;
}

.team-logo-modal4:hover {
  transform: scale(1.05);
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.4);
  cursor: pointer;
}

.team-logo-modal5 {
  margin-top: 60px;
  height: 130px;
  width: 130px;
  border-radius: 50%;
  border: 2px solid rgb(255, 255, 255);
  box-shadow: 0 0 10px rgb(121, 121, 121);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  object-fit: cover;
}

.team-logo-modal5:hover {
  transform: scale(1.05);
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.4);
  cursor: pointer;
}


   .ganr {
     color: beige;
     font-size: 30px; /* Ajusta el tamaño de la fuente según lo necesites */
     text-shadow: 
       1px 1px 0 black,   /* Sombra a la derecha y abajo */
       -1px -1px 0 black, /* Sombra a la izquierda y arriba */
       1px -1px 0 black,  /* Sombra a la derecha y arriba */
       -1px 1px 0 black;
      font-family:Impact, Haettenschweiler, 'Arial Narrow Bold', sans-serif;
      z-index: 10;
 }
 .ganr3 {
    color: rgb(68, 68, 68); /* Un gris más apagado */
    font-family: 'Press Start 2P', cursive;
    font-size: 30px; /* Un poco más pequeño, como si se "achicara" */
    text-shadow: 
        1px 1px 0 rgb(226, 226, 226),  
        -1px -1px 0 black,  
        1px -1px 0 black,  
        -1px 1px 0 black;
    margin-top: 20%;
    
    opacity: 0.7; /* Lo hace ver más "débil" */
    filter: blur(0.5px); /* Leve desenfoque para que parezca "borroso" */
    
    animation: loserShake 2s infinite alternate ease-in-out, 
               fadeOut 5s infinite alternate ease-in-out;
}

/* Temblor leve para que parezca derrotado */
@keyframes loserShake {
    0% { transform: translateX(0); }
    25% { transform: translateX(-2px); }
    50% { transform: translateX(2px); }
    75% { transform: translateX(-1px); }
    100% { transform: translateX(0); }
}

/* Efecto de desvanecimiento, como si el texto "perdiera fuerza" */
@keyframes fadeOut {
    0% { opacity: 0.7; }
    100% { opacity: 0.4; }
}

.ganr2 {
    z-index: 10;
    margin-top: 10%;
    font-family: Impact, Haettenschweiler, 'Arial Narrow Bold', sans-serif;
    font-size: 250%; 
    background: url('https://i.pinimg.com/736x/82/77/8d/82778d6d72c05cf2808e3bd2bcaeb823.jpg') no-repeat center center;
    background-size: cover;
    background-clip: text;
    -webkit-background-clip: text; /* Compatibilidad con Webkit */
    color: transparent;

    /* Animación de brillo y escala */
    animation: ganadorBrillo 3s infinite alternate ease-in-out;
}

/* Animación de brillo épico */
@keyframes ganadorBrillo {
    0% {
        filter: brightness(1) saturate(1);
        transform: scale(1);
    }
    50% {
        filter: brightness(1.8) saturate(1.5); /* Más brillo y color más intenso */
        transform: scale(1.05); /* Un leve aumento para dar efecto dinámico */
    }
    100% {
        filter: brightness(1) saturate(1);
        transform: scale(1);
    }
}

 
   /* Modal de Resultados */
   .modal {
     position: fixed;
     top: 0;
     left: 0;
     right: 0;
     bottom: 0;
     background-color: rgba(0, 0, 0, 0.7);
     display: flex;
     justify-content: center;
     align-items: center;
     z-index: 1000;
   }
   
   .modal-content {
     background-image: url("https://img.freepik.com/foto-gratis/cesped-verde-iluminacion-cinematografica-estadio-futbol_1409-7657.jpg");
     background-size: cover;
     background-position: center;
     background-color: rgba(0, 0, 0, 0.7); /* Aumento la oscuridad */
     padding: 40px;
     text-align: center;
     display: flex;
     flex-direction: column;
     align-items: center;
     border-radius: 15px;
     width: 80%;
     max-width: 700px;
     border: solid black;
     box-shadow: white 0 0 20px;
     margin-top: 5%;
 }
 
 
   
   .result-container {
     display: flex;
     justify-content: space-between;
     align-items: center;
     gap: 50px;
   }
   
   .team-result {
     text-align: center;
     flex: 1;
   }
   
   .winner {
     color: #4caf50;
     font-weight: bold;
   }
   
   .tie-result {
     font-size: 30px;
    font-family: Georgia, 'Times New Roman', Times, serif;
     font-weight: 700;
     color: #08b1ff;
     margin-left: 10%;
   }
   
   .tie-message {
     font-size: 40px;
     text-align: center;
     font-weight: 700;
     background-image: url("https://i.pinimg.com/736x/82/77/8d/82778d6d72c05cf2808e3bd2bcaeb823.jpg");
     background-clip: text; /* Aplica la imagen solo al texto */
     -webkit-background-clip: text; /* Requerido para algunos navegadores */
     color: transparent; /* Hace el color del texto transparente para que se vea la imagen de fondo */
     text-align:left;
     width: 120%;
 }
 .gif2 {
     width: 100px;
     height: 100px;
     margin-top: 10px;
 
 }
 
 .gif {
     width: 150px;
     height: 150px;
     margin-top: 10px;
     animation: glow 2.5s ease-in-out infinite;
     filter: brightness(10);
 }
 
 @keyframes glow {
     10% {
         transform: scale(1); /* Imagen en su tamaño original */
         filter: brightness(1); /* Brillo normal al inicio */
     }
     50% {
         transform: scale(1.2); /* Aumenta un poco el tamaño */
         filter: brightness(2); /* Aumenta significativamente el brillo */
     }
     100% {
         transform: scale(1); /* Vuelve a su tamaño original */
         filter: brightness(1); /* Vuelve al brillo normal */
     }
 }
 
 
   
 .close-button {
    background-color: #2c2c2c; /* Un gris oscuro más elegante */
    color: white;
    padding: 12px 30px;
    font-size: 18px;
    font-weight: bold;
    border: none;
    border-radius: 10px;
    cursor: pointer;
    margin-top: 20px;
    transition: all 0.3s ease-in-out;
    box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.2); /* Sombra ligera para elevar el botón */
}

/* Efecto al pasar el mouse */
.close-button:hover {
    background-color: #000000;
    color: #bbbbbb;
    transform: scale(1.05); /* Pequeño agrandamiento */
}

/* Efecto al hacer clic */
.close-button:active {
    transform: scale(0.95); /* Simula que se hunde al presionar */
    background-color: #1a1a1a;
}

.empate-logos {
  display: flex;
  justify-content: space-around;
  align-items: center;
  gap: 2rem;
 
}
.equipo2 {
  display: flex;
  flex-direction: column;
  align-items: center;
}


   </style>