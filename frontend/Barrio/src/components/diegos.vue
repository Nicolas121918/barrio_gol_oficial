<template>
    <div>
        <Headerapp></Headerapp>
    </div>
    <link href="https://fonts.googleapis.com/css2?family=Press+Start+2P&display=swap" rel="stylesheet">
    <div class="tournament">
      <h1 class="letra">Torneo de Fútbol</h1>
  
      <!-- Mostrar Equipos Inscritos -->
      <div class="teams">
        <h2>Equipos Inscritos</h2>
        <div class="team-list">
          <div v-for="team in teams" :key="team.id" class="team">
            <div class="team-info">
              <img :src="team.logo" alt="logo" class="team-logo" />
              <p><strong>{{ team.name }}</strong></p>
              <p><em>Inscrito por: {{ team.player }}</em></p>
            </div>
          </div>
        </div>
      </div>
  
      <!-- Mostrar Partidos -->
      <div class="matches">
        <h2>Primera Ronda</h2>
        <div v-for="(match, index) in firstRoundMatches" :key="match.id" class="match">
          <div class="match-info">
            <div class="team-score">
              <img :src="getTeamLogo(match.team1)" alt="logo" class="team-logo" />
              <p><strong class="letra3">{{ match.team1 }}</strong></p>
              <input v-model.number="match.score1" type="number" min="0" placeholder="Goles equipo 1" :disabled="match.finished" />
            </div>
            <span class="vs"> vs </span>
            <div class="team-score">
              <img :src="getTeamLogo(match.team2)" alt="logo" class="team-logo" />
              <p><strong class="letra2">{{ match.team2 }}</strong></p>
              <input v-model.number="match.score2" type="number" min="0" placeholder="Goles equipo 2" :disabled="match.finished" />
            </div>
            <!-- Fecha del Partido -->
            <p @click="editDate(match)"><em>✏ Fecha: {{ match.date }}</em></p>
          </div>
          <button @click="finishMatch(match)" :disabled="match.finished || match.score1 === null || match.score2 === null">Finalizar Partido</button>
        </div>
  
        <!-- Botón para pasar a la siguiente ronda -->
        <div v-if="firstRoundMatches.every(match => match.finished)" class="next-round">
          <button @click="startNextRound">Siguiente Ronda</button>
        </div>
  
        <!-- Mostrar Partidos de la Segunda Ronda -->
        <h2 v-if="secondRoundMatches.length > 0">Segunda Ronda</h2>
        <div v-for="(match, index) in secondRoundMatches" :key="match.id" class="match" v-if="secondRoundMatches.length > 0">
          <div class="match-info">
            <div class="team-score">
              <img :src="getTeamLogo(match.team1)" alt="logo" class="team-logo" />
              <p><strong>{{ match.team1 }}</strong></p>
              <input v-model.number="match.score1" type="number" min="0" placeholder="Goles equipo 1" :disabled="match.finished" />
            </div>
            <span> vs </span>
            <div class="team-score">
              <img :src="getTeamLogo(match.team2)" alt="logo" class="team-logo" />
              <p><strong>{{ match.team2 }}</strong></p>
              <input v-model.number="match.score2" type="number" min="0" placeholder="Goles equipo 2" :disabled="match.finished" />
            </div>
            <p @click="editDate(match)"><em>Fecha: {{ match.date }}</em></p>
          </div>
          <button @click="finishMatch(match)" :disabled="match.finished || match.score1 === null || match.score2 === null">Finalizar Partido</button>
        </div>
  
        <!-- Botón Finalizar Torneo --> 
        <div v-if="secondRoundMatches.every(match => match.finished)" class="finalize-tournament">
          <button @click="finalizeTournament">Finalizar Torneo</button>
        </div>
  
        <!-- Mostrar Ganador del Torneo -->
        <div class="results" v-if="tournamentFinished">
          <h2>Resultado Final del Torneo</h2>
          <img :src="getTeamLogo(tournamentWinner)" alt="Logo del ganador" />
          <p><strong>¡El ganador es {{ tournamentWinner }}!</strong></p>
        </div>
      </div>
  
      <div class="winner-info" v-if="tournamentFinished">
        <p>{{ tournamentWinner }}</p>
      </div>
  
      <!-- Modal para Editar Fecha -->
      <div v-if="isDateModalVisible" class="modal">
        <div class="modal-content">
          <h3>Actualizar Fecha del Partido</h3>
          <input v-model="newDate" type="date" />
          <button @click="updateDate">Actualizar</button>
          <button class="cance" @click="closeModal">Cancelar</button>
        </div>
      </div>
  
      <!-- Modal de Confirmación para Finalizar Partido -->
      <div v-if="isConfirmModalVisible" class="modal">
        <div class="modal-content">
          <h3>¿Estás seguro de que quieres finalizar el partido?</h3>
          <button @click="confirmFinishMatch">Sí, finalizar</button>
          <button class="cance" @click="cancelFinishMatch">Cancelar</button>
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
        teams: [
          { id: 1, name: 'Equipo A', logo: 'https://marketplace.canva.com/EAFzhZVxJKY/1/0/800w/canva-logo-simple-deportivo-de-futbol-minimalista-violeta-rosa-8DgSzaEcFjo.jpg', player: 'diego' },
          { id: 2, name: 'Equipo B', logo: 'https://marketplace.canva.com/EAFtzm5feNI/1/0/1600w/canva-logo-circular-escudo-club-de-f%C3%BAtbol-ilustrativo-negro-MwzhJEsdrNM.jpg', player: 'sebas' },
          { id: 3, name: 'Equipo C', logo: 'https://w7.pngwing.com/pngs/109/983/png-transparent-soccer-logo-football-icon-team-logo-thumbnail.png', player: 'Luis' },
          { id: 4, name: 'Equipo D', logo: 'https://www.zarla.com/images/zarla-ocho-players-1x1-2400x2400-20220325-p787f3q8rmcj8tbjpw8c.png?crop=1:1,smart&width=250&dpr=2', player: 'Pedro' },
          { id: 5, name: 'Equipo E', logo: 'https://d1csarkz8obe9u.cloudfront.net/posterpreviews/futsal-logo-design-template-7eaf9400ccb100711fa1fd340ca0e285_screen.jpg?ts=1671285271', player: 'Jorge' },
          { id: 6, name: 'Equipo F', logo: 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTn021Gu2-ecJrMM5frmTr_ZuWQ4mDCxVopEA&s', player: 'María' },
          { id: 7, name: 'Equipo G', logo: 'https://www.zarla.com/images/zarla-ocho-players-1x1-2400x2400-20220325-rkm6mfhpfc64y8bw4vdr.png?crop=1:1,smart&width=250&dpr=2', player: 'Julia' },
          { id: 8, name: 'Equipo H', logo: 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQ6RYikt3FZ0LHiuItNyY3Hk9VK6BuuwPm0fA&s', player: 'Carlos' },
        ],
        firstRoundMatches: [],
        secondRoundMatches: [],
        tournamentFinished: false,
        tournamentWinner: '',
        isDateModalVisible: false,
        isConfirmModalVisible: false,
        newDate: '',
        matchToUpdate: null
      };
    },
    methods: {
      initializeMatches() {
        const totalTeams = this.teams.length;
        const matchups = [];
  
        for (let i = 0; i < totalTeams / 2; i++) {
          matchups.push({
            id: `match-${i}`,
            team1: this.teams[i].name,
            team2: this.teams[totalTeams - i - 1].name,
            score1: null,
            score2: null,
            finished: false,
            date: '2024-12-10'
          });
        }
        this.firstRoundMatches = matchups;
      },
      getTeamLogo(teamName) {
        const team = this.teams.find(team => team.name === teamName);
        return team ? team.logo : '';
      },
      startNextRound() {
        const winners = this.firstRoundMatches
          .filter(match => match.score1 > match.score2)
          .map(match => match.team1);
        if (winners.length < 4) {
          winners.push(...this.firstRoundMatches.filter(match => match.score2 > match.score1).map(match => match.team2));
        }
        const matchups = [];
  
        for (let i = 0; i < winners.length / 2; i++) {
          matchups.push({
            id: `match-${i + 5}`,
            team1: winners[i],
            team2: winners[winners.length - i - 1],
            score1: null,
            score2: null,
            finished: false,
            date: '2024-12-12'
          });
        }
        this.secondRoundMatches = matchups;
      },
      finishMatch(match) {
        this.isConfirmModalVisible = true;
        this.matchToUpdate = match;
      },
      confirmFinishMatch() {
        if (this.matchToUpdate.score1 > this.matchToUpdate.score2) {
          this.tournamentWinner = this.matchToUpdate.team1;
        } else if (this.matchToUpdate.score2 > this.matchToUpdate.score1) {
          this.tournamentWinner = this.matchToUpdate.team2;
        }
        this.matchToUpdate.finished = true;
        this.isConfirmModalVisible = false;
        if (this.secondRoundMatches.every(match => match.finished)) {
          this.tournamentFinished = true;
        }
      },
      cancelFinishMatch() {
        this.isConfirmModalVisible = false;
      },
      editDate(match) {
        this.isDateModalVisible = true;
        this.matchToUpdate = match;
        this.newDate = match.date;
      },
      updateDate() {
        this.matchToUpdate.date = this.newDate;
        this.isDateModalVisible = false;
      },
      closeModal() {
        this.isDateModalVisible = false;
      },
      finalizeTournament() {
        alert(`Torneo Finalizado. El Ganador es: ${this.tournamentWinner}`);
      }
    },
    created() {
      this.initializeMatches();
    }
  };
  </script>
  
  <style scoped>
  /* CSS style for responsive design */
  .tournament {
    font-family: 'Press Start 2P', sans-serif;
    display: inline-block;
  transform: translate(0%, 10%); /* Mueve verticalmente */
  }
  
  .team-list {
    display: flex;
    flex-wrap: wrap;
    gap: 20px;
  }
  
  .team {
    background: #ececec;
    padding: 20px;
    border-radius: 10px;
    width: calc(33.33% - 20px);
    text-align: center;
    box-sizing: border-box;
  }
  
  .team-logo {
    width: 50px;
    height: 50px;
  }
  
  .matches {
    margin-top: 30px;
  }
  
  .match {
    background: #f4f4f4;
    margin-bottom: 20px;
    padding: 20px;
    border-radius: 10px;
  }
  
  .team-score {
    display: flex;
    align-items: center;
  }
  
  .team-logo {
    width: 40px;
    height: 40px;
  }
  
  .vs {
    font-size: 20px;
    margin: 0 15px;
  }
  
  input {
    width: 50px;
    padding: 5px;
    font-size: 14px;
  }
  
  button {
    background-color: #38A1DB;
    color: white;
    padding: 10px;
    border: none;
    border-radius: 5px;
    cursor: pointer;
    font-size: 14px;
  }
  
  button:disabled {
    background-color: #ccc;
    cursor: not-allowed;
  }
  
  .next-round,
  .finalize-tournament {
    text-align: center;
  }
  
  .finalize-tournament button {
    background-color: #FF4081;
    font-weight: bold;
  }
  
  .results {
    text-align: center;
  }
  
  .modal {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(0, 0, 0, 0.5);
    display: flex;
    justify-content: center;
    align-items: center;
  }
  
  .modal-content {
    background: white;
    padding: 20px;
    border-radius: 5px;
  }
  
  button.cance {
    background-color: #FF0000;
  }
  
  input[type="date"] {
    width: 200px;
  }
  </style>
  
  
  <style scoped>
  /* Estilos adicionales para los nuevos botones y modales */
  .finalize-tournament {
    margin-top: 20px;
  }
  
  .finalize-tournament button {
    background-color: #28a745;
    color: white;
    border: none;
    padding: 10px 20px;
    cursor: pointer;
    font-size: 16px;
  }
  
  .modal {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0, 0, 0, 0.5);
    display: flex;
    justify-content: center;
    align-items: center;
  }
  
  .modal-content {
    background: white;
    padding: 20px;
    border-radius: 8px;
    text-align: center;
  }
  h2{
    text-align: center;
    color: white;
    font-family: Cambria, Cochin, Georgia, Times, 'Times New Roman', serif;
    font-size: 200%;
  }
  .letra {
    font-size: 40px; /* Puedes ajustar el tamaño de la fuente según lo desees */
    background-image: url("https://i.pinimg.com/736x/82/77/8d/82778d6d72c05cf2808e3bd2bcaeb823.jpg");
    background-size: cover;
    color: transparent; /* Hacemos el color del texto transparente para ver la imagen a través */
    -webkit-background-clip: text; /* Para que la imagen se aplique solo al texto */
    background-clip: text; /* Para que la imagen se aplique solo al texto */
    font-family: Cambria, Cochin, Georgia, Times, 'Times New Roman', serif;
    text-align: center;
  }
  .letra3 {
    color: rgb(255, 255, 255); /* Color blanco para el texto */
    font-family: 'Press Start 2P', cursive; /* Fuente de estilo pixelado (retro de videojuegos) */
    font-size: 120%; /* Tamaño de fuente ajustado */
    text-transform: uppercase; /* Todo en mayúsculas */
    letter-spacing: 2px; /* Espaciado entre las letras */
    text-shadow: 
      2px 2px 4px rgb(0, 0, 0), /* Sombra oscura a la derecha y abajo */
      -2px -2px 4px rgb(0, 0, 0), /* Sombra oscura a la izquierda y arriba */
      2px -2px 4px rgb(0, 0, 0), /* Sombra oscura a la derecha y arriba */
      -2px 2px 4px rgb(0, 0, 0), /* Sombra oscura a la izquierda y abajo */
      0 0 10px rgb(17, 245, 245); /* Resplandor suave azul */
    padding: 10px 20px; /* Espacio dentro del texto */
    border-radius: 15px; /* Bordes redondeados */
    
  }
  .cance{
    background-color: blue;
    margin-left: 20%;
  }
  
  
  .letra2 {
    text-align: center;
    color: rgb(255, 255, 255); /* Color blanco para el texto */
    font-family: 'Press Start 2P', cursive; /* Fuente de estilo pixelado (retro de videojuegos) */
    font-size: 100%; /* Tamaño de fuente ajustado */
    text-shadow: 
      2px 2px 4px rgb(0, 0, 0), /* Sombra oscura a la derecha y abajo */
      -2px -2px 4px rgb(0, 0, 0), /* Sombra oscura a la izquierda y arriba */
      2px -2px 4px rgb(0, 0, 0), /* Sombra oscura a la derecha y arriba */
      -2px 2px 4px rgb(0, 0, 0), /* Sombra oscura a la izquierda y abajo */
      0 0 10px rgb(248, 0, 54); /* Resplandor suave azul // Espacio dentro del texto */
    border-radius: 15px; /* Bordes redondeados */
  }
  button {
    cursor: pointer;
  }
  
  button:disabled {
    cursor: not-allowed;
    background-color: #ccc;
  }
  .results {
    text-align: center;
    margin-top: 30px;
  }
  
  .results h2 {
    font-size: 2em;
    color: #FF6347; /* Un color llamativo para el encabezado */
  }
  
  .results p {
    font-size: 1.5em;
    font-weight: bold;
    color: #333;
  }
  
  .results .winner-info {
    display: flex;
    justify-content: center;
    align-items: center;
    margin-top: 20px;
  }
  
  .results .winner-info img {
    width: 50px; /* Tamaño del logo */
    height: 50px;
    margin-right: 15px; /* Espacio entre el logo y el texto */
  }
  
  .results .winner-info p {
    font-size: 1.2em;
    font-weight: bold;
    color: #00FF00; /* Color verde para destacar el ganador */
  }
  
  /* Estilos Generales */
  .tournament {
    font-family: 'Arial', sans-serif;
    background: linear-gradient(to bottom, #313131, #4e4e4e,#8d8d8d); /* Degradado de gris a blanco */
    padding: 20px;
    border-radius: 10px;
    max-width: 900px;
    margin: 0 auto;
    color: black; 
    border: solid white;
    box-shadow: 0 0 40px white;
  }
  
  
  /* Equipos Inscritos */
  .teams {
    margin-bottom: 20px;
    border: solid black;
    padding:20px;
    text-align: center;
    background-color: grey;
    border: 5 solid black;
  }
  
  .team-list {
    display: flex;
    flex-wrap: wrap;
    gap: 20px;
    border: 5 solid black;
  
  }
  
  .team {
    background-color: #fff;
    padding: 10px;
    border-radius: 8px;
    width: calc(33.333% - 20px);
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    border: 5 solid black;
  }
  
  .team-logo {
    width: 60px;
    height: 60px;
    border-radius: 50%;
    margin-right: 10px;
     border: 2px solid rgb(0, 0, 0);
     box-shadow: 0 0 20px rgb(0, 0, 0);
  
  }
  
  .team-info {
    display: flex;
    align-items: center;
    background-image: url("https://static5.depositphotos.com/1003494/456/i/450/depositphotos_4564054-stock-photo-golden-artistic-fabric-background.jpg")
  }
  
  /* Partidos */
  .match {
    background-color: #d3d3d37e;
    padding: 15px;
    margin-bottom: 15px;
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    border: solid black;
  }
  
  .match-info { 
    display: flex;
    justify-content: space-between;
    align-items: center;
  }
  
  .team-score {
    display: flex;
    align-items: center;
  }
  
  .team-score input {
    width: 50px;
    text-align: center;
    margin-left: 10px;
  }
  
  button {
    background-color: #4CAF50;
    color: white;
    padding: 10px 20px;
    border: none;
    border-radius: 5px;
    cursor: pointer;
    margin-top: 10px;
  }
  
  button:disabled {
    background-color: #ccc;
    cursor: not-allowed;
  }
  .vs {
    margin: 6px;
    font-family: 'Press Start 2P', cursive; /* Estilo de fuente pixelada */
    font-size: 200%; /* Puedes ajustar el tamaño de la fuente */
    color: #acaaaa; /* Un color verde típico de videojuegos retro */
    text-transform: uppercase; /* Opcional: para que el texto esté en mayúsculas */
    letter-spacing: 4px; /* Opcional: para darle un poco de espacio entre las letras */
    text-shadow: 
      2px 2px 0px rgb(0, 0, 0), /* Borde rojo a la derecha y abajo */
      -2px -2px 0px rgb(0, 0, 0), /* Borde rojo a la izquierda y arriba */
      2px -2px 0px rgb(73, 73, 73), /* Borde rojo a la derecha y arriba */
      -2px 2px 0px rgb(82, 82, 82); /* Borde rojo a la izquierda y abajo */
  }
  
  .modal {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0, 0, 0, 0.5);
    display: flex;
    justify-content: center;
    align-items: center;
  }
  
  .modal-content {
    background-color: #fff;
    padding: 20px;
    border-radius: 10px;
    max-width: 400px;
    width: 100%;
  }
  
  input[type="date"] {
    width: 100%;
    padding: 10px;
    margin-top: 10px;
    border: 1px solid #ddd;
    border-radius: 5px;
  }
  </style>