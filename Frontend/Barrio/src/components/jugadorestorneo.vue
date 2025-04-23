<template>
    <header>
      <Headerapp></Headerapp>
  
    </header>
      <link href="https://fonts.googleapis.com/css2?family=Press+Start+2P&display=swap" rel="stylesheet">
      <link href="https://fonts.googleapis.com/css2?family=Orbitron&display=swap" rel="stylesheet">
    <div class="negro">
      <div class="match-container">
        <h1 class="match-title">{{ nombre }}</h1>
        <p class="match-subtitle">Eres el encargado, Matías: <span>¡Estamos bajo tus manos!</span></p>
        <div v-if="!isMatchStarted" class="match-info">
          <p>⏰ El partido se juega hoy a las <span>{{ matchTime }}</span></p>
        </div>
        <div v-else class="match-content">
          <div class="team">
            <img :src="teamA.logo" alt="Logo Equipo A" class="team-logo" />
            <p class="team-name">{{ teamA.name }}</p>
            <router-Link to="targetas"><button>Targetas</button></router-Link>
            
          </div>
          <div class="vs">VS</div>
          <div class="team">
            <img :src="teamB.logo" alt="Logo Equipo B" class="team-logo" />
            <p class="team-name">{{ teamB.name }}</p>
            <router-Link to="targetas"><button>Targetas</button></router-Link>
          </div>
        </div>
        <div class="scoreboard" v-if="isMatchStarted && !isMatchEnded">
          <div class="team-score">
            <p class="score-team-name">{{ teamA.name }}</p>
            <div class="score-buttons">
              <button class="score-btn" @click="adjustScore('A', 1)">+</button>
              <p class="score">{{ teamA.score }}</p>
              <button class="score-btn" @click="adjustScore('A', -1)">-</button>
            </div>
          </div>
          <div class="team-score">
            <p class="score-team-name">{{ teamB.name }}</p>
            <div class="score-buttons">
              <button class="score-btn" @click="adjustScore('B', 1)">+</button>
              <p class="score">{{ teamB.score }}</p>
              <button class="score-btn" @click="adjustScore('B', -1)">-</button>
            </div>
          </div>
        </div>
        <button  class="finish-button" @click="showEndConfirmation">
          VOLVER
        </button>
        <button v-if="isMatchStarted && !isMatchEnded" class="finish-button" @click="showEndConfirmation">
          Finalizar
        </button>
  
        <!-- Modal de Confirmación -->
        <div v-if="showConfirmation" class="confirmation-modal">
          <div class="confirmation-content">
            <h2 class="advertencia">⚠ ¡Advertencia! ⚠</h2>
            <p>¿Estás seguro de terminar el partido? No hay vuelta atrás.</p>
            <div class="confirmation-buttons">
              <button class="confirm-btn" @click="finalizeMatch">Aceptar</button>
              <button class="cancel-btn" @click="cancelMatch">Cancelar</button>
            </div>
          </div>
        </div>
  
        <!-- Modal de Resultados Finales -->
        <div v-if="isMatchEnded" class="modal">
          <div class="modal-content">
            <h2 class="result_fin">Resultados Finales</h2>
            <div class="result-container">
              <div v-if="isMatchTied" class="tie-result">
                <p class="tie-message">¡Es un empate!</p>
                <div class="resul">
                  <p>{{ teamA.name }} - {{ teamA.score }} goles</p>
                  <p>{{ teamB.name }} - {{ teamB.score }} goles</p>
                </div>
              </div>
  
              <div class="contiene3" v-else>
                <!-- Equipo Ganador -->
                <div class="team-result" :class="{ winner: isTeamAWinner }">
                  <div class="team-logo-container">
                    <p class="ganr2">Ganador</p>
                    <img :src="isTeamAWinner ? teamA.logo : teamB.logo" alt="Logo Equipo Ganador" class="team-logo-modal1" />
                  </div>
                  <p class="ganr">{{ isTeamAWinner ? teamA.name : teamB.name }} - {{ isTeamAWinner ? teamA.score : teamB.score }} goles</p>
                  <img src="../assets/imagenes/balondeoro.png" alt="Ganador" class="gif" />
                </div>
  
                <!-- Equipo Perdedor -->
                <div class="team-result" :class="{ winner: !isTeamAWinner }">
                  <div class="team-logo-container">
                    <p class="ganr3">Perdedor</p>
                    <img :src="!isTeamAWinner ? teamA.logo : teamB.logo" alt="Logo Equipo Perdedor" class="team-logo-modal" />
                  </div>
                  <p class="ganr">{{ !isTeamAWinner ? teamA.name : teamB.name }} - {{ !isTeamAWinner ? teamA.score : teamB.score }} goles</p>
                  <img src="https://i.pinimg.com/originals/a4/38/4c/a4384c5d86fa696a392ab216bc09a3d3.gif" alt="Perdedor" class="gif2" />
                </div>
              </div>
            </div>
            <button class="close-button" @click="resetMatch">Cerrar</button>
          </div>
        </div>
      </div>
    </div>
  </template>
  
    <script>
  import Headerapp from './Headerapp.vue';
  
    export default {
      components : {
        Headerapp
  
      },
    data() {
      return {
        nombre: "partido de muerte",
        matchTime: "5:00 AM",
        teamA: {
          name: "Diego",
          logo: "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQgcadZp6orYwW2SrUcyJhyTRredhg_sf_vzQ&s",
          score: 0,
        },
        teamB: {
          name: "Santi",
          logo: "https://marketplace.canva.com/EAFtzm5feNI/1/0/1600w/canva-logo-circular-escudo-club-de-f%C3%BAtbol-ilustrativo-negro-MwzhJEsdrNM.jpg",
          score: 0,
        },
        isMatchStarted: false,
        isMatchEnded: false,
        showConfirmation: false,
      };
    },
    computed: {
      isTeamAWinner() {
        return this.teamA.score > this.teamB.score;
      },
      isMatchTied() {
        return this.teamA.score === this.teamB.score;
      },
    },
    mounted() {
    const now = new Date();
    const matchDateTime = new Date(now.getFullYear(), now.getMonth(), now.getDate(), 12, 30, 0); // Fecha de hoy a las 8:30 PM
  
    console.log("Fecha y hora actual:", now.toLocaleString());
    console.log("Hora del partido:", matchDateTime.toLocaleString());
  
    if (now <= matchDateTime) {
      this.isMatchStarted = true;
    }
  },
  
    methods: {
      adjustScore(team, increment) {
        if (team === "A") {
          this.teamA.score = Math.max(0, this.teamA.score + increment);
        } else if (team === "B") {
          this.teamB.score = Math.max(0, this.teamB.score + increment);
        }
      },
      showEndConfirmation() {
        this.showConfirmation = true;
      },
      finalizeMatch() {
        this.isMatchEnded = true;
        this.showConfirmation = false;
      },
      cancelMatch() {
        this.showConfirmation = false;
      },
      resetMatch() {
        this.teamA.score = 0;
        this.teamB.score = 0;
        this.isMatchEnded = false;
        this.isMatchStarted = false;
      },
    },
  };
  
    </script>
    
    <style scoped>
    .result_fin{
      color: rgb(255, 255, 255);
      text-decoration:underline;
      font-size: 180%;
      text-shadow: 
        1px 1px 0 black,   /* Sombra a la derecha y abajo */
        -1px -1px 0 black, /* Sombra a la izquierda y arriba */
        1px -1px 0 black,  /* Sombra a la derecha y arriba */
        -1px 1px 0 black;  /*
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
    
    .vs {
    font-family: 'Orbitron', sans-serif; /* Fuente futurista */
    font-size: 50px;
    font-weight: 700;
    color: #d4af37; /* Color dorado */
    text-shadow: 
      2px 2px 0px rgba(255, 255, 255, 0.7),   /* Sombra blanca para resaltar */
      -2px -2px 5px rgba(0, 0, 0, 0.7),       /* Sombra negra para el borde */
      2px 2px 3px rgba(0, 0, 0, 0.5),          /* Sombra negra adicional */
      0px 0px 10px rgba(255, 215, 0, 0.8);     /* Resplandor dorado */
    padding: 10px 20px;
    border-radius: 15px;
    text-align: center;
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
    .team-logo-modal1{
      margin-top: 10%;
      width: 50%;
      box-shadow: 0 0 20px rgb(255, 230, 0);
      border: solid rgb(251, 255, 0);
    }
    .team-logo-modal{
      width: 30%;
      margin-top: 10%;
      box-shadow: 0 0 20px rgb(0, 0, 0);
      border: solid rgba(172, 171, 171, 0.363);
    }
    .score-team-name {
      font-size: 24px;
      font-weight: bold;
      color: #ffffff;
      margin-bottom: 10px;
      text-shadow: 0 0 10px black;
    }
    
    .score-buttons {
      display: flex;
      align-items: center;
      gap: 15px;
  
    }
    .ganr {
      color: beige;
      font-family: 'Press Start 2P', cursive; /* Fuente tipo videojuego */
      font-size: 100%; /* Ajusta el tamaño de la fuente según lo necesites */
      text-shadow: 
        1px 1px 0 black,   /* Sombra a la derecha y abajo */
        -1px -1px 0 black, /* Sombra a la izquierda y arriba */
        1px -1px 0 black,  /* Sombra a la derecha y arriba */
        -1px 1px 0 black;
  }
  .ganr3{
      color: rgb(145, 144, 144);
      font-family: 'Press Start 2P', cursive; /* Fuente tipo videojuego */
      font-size: 100%; /* Ajusta el tamaño de la fuente según lo necesites */
      text-shadow: 
        1px 1px 0 black,   /* Sombra a la derecha y abajo */
        -1px -1px 0 black, /* Sombra a la izquierda y arriba */
        1px -1px 0 black,  /* Sombra a la derecha y arriba */
        -1px 1px 0 black;
        margin-top: 20%
  }
  .ganr2 {
      margin-top: 10%;
      font-family: 'Press Start 2P', cursive; /* Fuente tipo videojuego */
      font-size: 140%; 
      background: url('https://i.pinimg.com/736x/82/77/8d/82778d6d72c05cf2808e3bd2bcaeb823.jpg') no-repeat center center; /* Imagen de fondo */
      background-size: cover; /* Asegura que la imagen cubra todo el texto */
      background-clip: text; /* Funciona solo en navegadores que soportan Webkit */
      color: transparent; /* Hace que el color del texto sea transparente para mostrar solo la imagen */
  }
  
  
  
    .advertencia{
      color: red;
      font-family:Impact, Haettenschweiler, 'Arial Narrow Bold', sans-serif;
    }
    .score-btn {
      background-image: url("https://img.lovepik.com/background/20211022/large/lovepik-golden-background-image_401782626.jpg");
      color: white;
      padding: 5px 15px;
      font-size: 20px;
      border: none;
      border-radius: 8px;
      cursor: pointer;
      color: black;
      text-shadow: white 0 0 5px;
      box-shadow: #ffffff 0 0 10px;
      border: 3px solid black;
    }
    
    .score-btn:hover {
      background-color: #c79c2f;
    }
    
    .score {
      font-size: 30px;
      font-weight: 600;
      color: #333333;
      text-shadow: 0 0 5px rgb(255, 255, 255);
      
    }
    
    .finish-button {
      background-color: rgb(7, 186, 231);
      color: white;
      padding: 10px 25px;
      font-size: 22px;
      border: none;
      border-radius: 10px;
      cursor: pointer;
      margin-top: 30px;
      color: black;
      text-shadow: white 0 0 5px;
      box-shadow: #ffffff 0 0 10px;
      border: 3px solid black;
    }
    
    .finish-button:hover {
      background-color: #360dee;
      font-family: Arial, Helvetica, sans-serif;
    }
    
    /* Modal de Confirmación */
    .confirmation-modal {
      position: fixed;
      top: 0;
      left: 0;
      right: 0;
      bottom: 0;
      background-color: rgba(0, 0, 0, 0.5);
      display: flex;
      justify-content: center;
      align-items: center;
      
    }
    
    .confirmation-content {
      color: black;
      background-color: #ffffff;
      padding: 40px;
      text-align: center;
      border-radius: 15px;
      width: 80%;
      max-width: 500px;
      box-shadow: 0 0 40px rgb(255, 255, 255);
      border: 1px solid black;
    }
    
    .confirmation-buttons {
      display: flex;
      justify-content: space-around;
      margin-top: 20px;
    }
    
    .confirm-btn, .cancel-btn {
      background-color: #5fc72f;  
      color: white;
      padding: 12px 25px;
      font-size: 18px;
      border: none;
      border-radius: 8px;
      border: 2px solid black;
      cursor: pointer;
    }
    
    .cancel-btn {
      background-color: #424242;
      border: 2px solid black
    }
    
    .confirm-btn:hover {
      background-color: #287007;  
      color: white;
      
    }
    
    .cancel-btn:hover {
      background-color: #a8a8a8;
      color: black;
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
      margin-top: 10%;
  }
  
  
    
    .result-container {
      display: flex;
      justify-content: space-between;
      align-items: center;
      gap: 20px;
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
      font-weight: 700;
      background-image: url("https://i.pinimg.com/736x/82/77/8d/82778d6d72c05cf2808e3bd2bcaeb823.jpg");
      background-clip: text; /* Aplica la imagen solo al texto */
      -webkit-background-clip: text; /* Requerido para algunos navegadores */
      color: transparent; /* Hace el color del texto transparente para que se vea la imagen de fondo */
      text-align: center;
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
      animation: glow 1.5s ease-in-out infinite;
      filter: brightness(10);
  }
  
  @keyframes glow {
      0% {
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
      background-color: #4b4a4a;
      color: white;
      padding: 12px 25px;
      font-size: 18px;
      border: none;
      border-radius: 8px;
      cursor: pointer;
      margin-top: 20px;
    }
    
    .close-button:hover {
      background-color: #000000;
      color: gray;
    }
    </style>