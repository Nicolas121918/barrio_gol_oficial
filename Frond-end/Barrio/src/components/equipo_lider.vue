<template>
<div class="padre">
  
  <div class="team-leader">
    <!-- Encabezado: Logo y nombre del equipo -->
    <header class="header">
      <img :src="team.logo" alt="Logo del equipo" class="logo" />
      <router-link class="link torneos" to="/galeria">
        <img class="api5" src="../assets/imagenes/galeria.png" alt="galeria">
      </router-link>
      <div>
          <h1>{{ team.name }}</h1>
          <p class="description">{{ team.description }}</p>
      </div> <!-- Descripción debajo del nombre -->

      <router-link class="link torneos" to="/calendario">
        <img class="api5" src="../assets/imagenes/calendario.png" alt="calendario">
      </router-link>

      <div class="caja_hijo">
      <p>Torneos Ganados: {{ team.tournaments.length }}</p>
      <p>Miembros: {{ team.members.length }}</p>
  </div>
    </header>

    <!-- Lista de integrantes -->
    <section class="members-section">
      <h2 class="name">Integrantes</h2>
      <ul class="members-list">
        <li
          v-for="(member, index) in team.members"
          :key="index"
          :class="{ leader: member.isLeader }"
          @click="!member.isLeader && openMemberMenu(member)"
          class="member-item"
        >
          <div class="member-info">
            <img :src="member.profilePicture" alt="Foto de perfil" class="profile-picture" />
            <span class="nombre2">{{ member.name }}</span>
            <span class="role">({{ member.role }})</span>
            <p class="details">
              Fecha de Nacimiento: {{ member.birthDate }}
            </p>
          </div>
        </li>
      </ul>
    </section>

    <!-- Modal para editar integrante -->
    <div v-if="showMemberMenu" class="modal">
      <div class="modal-content">
        <h3 class="edit">Opciones para {{ selectedMember.name }}</h3>
        <button id="espacio" class="button2" @click="editRole(selectedMember)" v-if="!selectedMember.isLeader">
          Actualizar Posición
        </button>
        <button id="espacio"  class="button_danger" @click="confirmExpel(selectedMember)" v-if="!selectedMember.isLeader">
          Expulsar
        </button>
        <button id="espacio"  class="button" @click="editRole(selectedMember)" v-if="selectedMember.isLeader">
          Actualizar Posición
        </button>
        <button id="espacio"  class="button_close" @click="closeMemberMenu">Cerrar</button>
      </div>
    </div>

    <!-- Botones para abrir el submenú -->
    <section class="submenu-section">
      <button class="button" @click="openBuzon">Buzón</button>
      <button class="button" @click="openConfig">Configuración</button>
      <router-link class="padre" to="torneo_guardado">
        <button class="button2" @click="">incritos</button>
      </router-link>
      
    </section>
    

    <!-- Modal de Buzón -->
    <div v-if="showBuzon" class="modal buzón-modal">
      <div id="caja" class="modal-content buzón-content">
        <h3>Buzón de Solicitudes</h3>
        <ul class="request-list">
          <li v-for="(solicitud, index) in team.requests" :key="index" class="request-item">
            <span>{{ solicitud.name }} solicita unirse al equipo</span>
            <div class="request-actions">
              <button  @click="acceptRequest(solicitud)" class="button_accept-btn">Aceptar</button>
              <button @click="rejectRequest(solicitud)" class="button_reject-btn">Rechazar</button>
            </div>
          </li>
        </ul>
        <button class="button_close" @click="closeBuzon">Cerrar</button>
        <router-link class="link home" to="/invitar">
          <button class="button_accept-btn" @click="closeBuzon">invitar</button>
      </router-link>
        
      </div>
    </div>

    <!-- Modal de Configuración -->
    <div v-if="showConfig" class="modal config-modal">
      <div class="modal-content config-content">
        <h3 class="confi">Configuración</h3>
        <label class="confi2" for="newLogo">Actualizar Foto de Perfil</label>
        <input type="file" id="newLogo" @change="updateLogo" class="file-input"/>
        
        <label class="confi2" for="newDescription">Actualizar Descripción</label>
        <textarea id="newDescription" v-model="newDescription" rows="4" class="textarea"></textarea>

        <button id="espacio" @click="updateTeam" class="button2">Guardar Cambios</button>
        <button id="espacio"class="button_danger" @click="deleteTeam">Eliminar Equipo</button>
        <button id="espacio" class="button_close" @click="closeConfig">Cerrar</button>
      </div>
    </div>

    <!-- Sección de chat -->
    <section class="chat-section">
      <h2 class="vamoss2">Chat del Equipo</h2>
      <div class="chat-box">
        <div v-for="(message, index) in team.chat" :key="index" class="chat-message">
          <strong class="vamoss1">{{ message.sender }}:</strong> <span>{{ message.content }}</span>
        </div>
      </div>
      <input
        v-model="newMessage"
        type="text"
        placeholder="Escribe un mensaje..."
        class="chat-input"
      />
      <button @click="sendMessage" class="button">Enviar</button>
    </section>
  </div>
</div>
</template>

<script>
import { useUsuarios } from '@/stores/usuario';
import axios from 'axios';
export default {
  components: {
    useUsuarios,
  },
  data() {
    return {
      team: {
        logo: "https://via.placeholder.com/100",
        name: "Equipo Campeón",
        description: "Descripción pequeña del equipo",
        members: [
          { 
            name: "Diego", 
            role: "Portero", 
            birthDate: "1995-08-12", 
            isLeader: true,
            profilePicture: "https://via.placeholder.com/50"
          },
          { 
            name: "Carlos", 
            role: "Defensa", 
            birthDate: "1998-05-23", 
            isLeader: false,
            profilePicture: "https://via.placeholder.com/50"
          },
          { 
            name: "Ana", 
            role: "Delantera", 
            birthDate: "2000-09-17", 
            isLeader: false,
            profilePicture: "https://via.placeholder.com/50"
          },
        ],
        requests: [
          { name: "Juan", role: "Delantero", birthDate: "1997-03-15" },
          { name: "santiago", role: "Delantero", birthDate: "1997-03-15" },
        ],
        tournaments: ["Torneo A", "Torneo B"],
        chat: [
          { sender: "Diego", content: "¡Vamos equipo!" },
          { sender: "Ana", content: "¡A ganar el próximo partido!" },
        ],
      },
      selectedMember: null,
      showMemberMenu: false,
      showBuzon: false,
      showConfig: false,
      newMessage: "",
      newDescription: "",

    };
  },
  methods: {
    openMemberMenu(member) {
      this.selectedMember = member;
      this.showMemberMenu = true;
    },
    closeMemberMenu() {
      this.showMemberMenu = false;
      this.selectedMember = null;
    },
    editRole(member) {
      if (member.isLeader) {
        const newRole = prompt("Ingresa la nueva posición para el líder (" + member.name + ")");
        if (newRole) {
          member.role = newRole;
          this.closeMemberMenu();
        }
      } else {
        const newRole = prompt("Ingrese la nueva posición para " + member.name);
        if (newRole) {
          member.role = newRole;
          this.closeMemberMenu();
        }
      }
    },
    confirmExpel(member) {
      if (confirm(`¿Estás seguro de expulsar a ${member.name}?`)) {
        this.team.members = this.team.members.filter((m) => m !== member);
        this.closeMemberMenu();
      }
    },
    sendMessage() {
      if (this.newMessage.trim() !== "") {
        this.team.chat.push({ sender: "Tú", content: this.newMessage });
        this.newMessage = "";
      }
    },
    openBuzon() {
      this.showBuzon = true;
      this.showConfig = false; // Cerrar configuración si está abierta
    },
    openConfig() {
      this.showConfig = true;
      this.showBuzon = false; // Cerrar buzón si está abierto
    },
    closeBuzon() {
      this.showBuzon = false;
    },
    closeConfig() {
      this.showConfig = false;
    },
    acceptRequest(solicitud) {
      this.team.members.push({
        name: solicitud.name,
        role: "Nuevo Miembro",
        birthDate: solicitud.birthDate,
        isLeader: false,
        profilePicture: "https://via.placeholder.com/50",
      });
      this.team.requests = this.team.requests.filter((req) => req !== solicitud);
    },
    rejectRequest(solicitud) {
      this.team.requests = this.team.requests.filter((req) => req !== solicitud);
    },
    updateTeam() {
      if (this.newDescription) {
        this.team.description = this.newDescription;
      }
      alert("Cambios guardados.");
      this.closeConfig();
    },
    async deleteTeam() {
  try {
    const movistore = useUsuarios();
    
    // Obtener el ID del equipo a eliminar
    const response = await axios.get(`http://127.0.0.1:8000/id_equipo/${movistore.usuario.documento}`);
    const id_delete = response.data.Id_team;
    console.log("Id del equipo a eliminar: ", id_delete);
    
    if (!id_delete) {
      alert("No hay un equipo asociado para eliminar.");
      return;
    }

    // Hacer la petición DELETE
    const deleteResponse = await axios.delete(`http://127.0.0.1:8000/equipos/eliminar/${id_delete}`);
    
    console.log("Respuesta del servidor:", deleteResponse.data);
    alert(deleteResponse.data.mensaje);

    // **Actualizar el estado en Pinia**
    movistore.usuario.equipo_tiene = 0; // Indicar que no tiene equipo
    movistore.usuario.esLider = false; // Indicar que ya no es líder

    this.$router.push('/equipos');
  } catch (error) {
    console.error("Error al eliminar el equipo:", error);
    alert("Hubo un error al eliminar el equipo. Por favor, inténtalo de nuevo.");
  }
},



    updateLogo(event) {
      const file = event.target.files[0];
      if (file) {
        this.team.logo = URL.createObjectURL(file);
      }
    },
  },
};
</script>

<style scoped>
/* Estilos generales */
.caja_hijo{
  margin-left: 10%;
}
.team-leader {
font-family: 'Arial', sans-serif;
padding: 20px;
background-image: url("../assets/imagenes/cancha.jpg"); 
background-repeat: no-repeat;
background-size: cover; /* Esto asegura que la imagen cubra todo el contenedor */
color: #fff;
border-radius: 10px;
color: black;
z-index:-6; /* Desenfoque de la imagen */
border: solid white;
}
.api5{
    filter: drop-shadow(0 0 1px rgb(0, 0, 0));
    transition: transform 0.5s;
    height: 55px;
    width: auto;
    margin: 0 5px;
  }

.padre{
  margin-top: 25%
}
.header {
  text-align: center;
  background-color: rgba(3, 0, 0, 0.822);
  padding: 20px;
  border-radius: 10px;
  color: white;
}
.nombre2{
  color: rgb(255, 255, 255);
  font-size: 120%;
}
.name{
  color: white;
  font-size: 180%;
  font-family: Impact, Haettenschweiler, 'Arial Narrow Bold', sans-serif;
  text-align: center;
  text-shadow: 0 0 3px rgb(151, 153, 4);
}

.header h1 {
  font-size: 2rem;
  font-weight: bold;
}

.logo {
  width: 100px;
  height: 100px;
  border-radius: 50%;
  object-fit: cover;
  margin-bottom: 10px;
  margin-right: 2%;
}

.description {
  font-size: 1rem;
  color: #ccc;
}

.members-section {
  margin-top: 20px;
}

.members-list {
  list-style: none;
  padding: 0;
  margin-top: 10px;
}

.member-item {
  display: flex;
  align-items: center;
  padding: 10px;
  background-color: rgba(0, 0, 0, 0.1);
  border-radius: 8px;
  margin-bottom: 10px;
  cursor: pointer;
  transition: background-color 0.3s;
}
.member-item{
  background-color: rgba(0, 0, 0, 0.644);
  border: solid white
}


.member-item:hover {
  background-color: rgba(122, 122, 122, 0.3);
  color: black;
}

.profile-picture {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  margin-right: 10px;
}

.role {
  font-size: 0.9rem;
  color: #aaa;
}

.details {
  font-size: 0.8rem;
  color: #bbb;
}

.modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.7);
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 20px;
}

.modal-content {
  background-color: rgb(255, 254, 254);
  padding: 20px;
  border-radius: 10px;
  max-width: 400px;
  width: 100%;
  box-shadow: 0 0 10px white;
  text-align: center;
  
}



.button_accept-btn {
  background-color: green;
  padding: 2%;
  color: white;
  border-radius: 5px;
  font-family: Cambria, Cochin, Georgia, Times, 'Times New Roman', serif;
}
.button2{
  background-color: #005bb5;
  padding: 2%;
  color: white;
  border-radius: 5px;
  font-family: Cambria, Cochin, Georgia, Times, 'Times New Roman', serif;
}
.button2:hover{
  background-color: #003061;
  color: grey;
}

.button_accept-btn:hover{
  color: rgb(89, 90, 89);
  background: rgb(1, 63, 1);
}
.button_reject-btn:hover,.button_danger:hover{
  color: rgb(89, 90, 89);
  background: rgb(112, 1, 1);
}
.button_reject-btn {
  background-color: red;
  padding: 2%;
  color: white;
  border-radius: 5px;
  font-family: Cambria, Cochin, Georgia, Times, 'Times New Roman', serif;
}

.button_danger{
  background-color: red;
  padding: 2%;
  color: white;
  border-radius: 5px;
  font-family: Cambria, Cochin, Georgia, Times, 'Times New Roman', serif;

}

.button_close {
  background-color: gray;
  padding: 2%;
  color: white;
  border-radius: 5px;
  font-family: Cambria, Cochin, Georgia, Times, 'Times New Roman', serif;
  margin-right: 10%;
}
.button_close:hover{
  background-color: rgb(75, 75, 75);
  color: black;

}

.button:hover {
  background-color: #005bb5;
}

.chat-section {
  margin-top: 20px;
  padding: 20px;
  background-color: #000000;
  border-radius: 10px;
}

.chat-box {
  max-height: 200px;
  overflow-y: auto;
  margin-bottom: 10px;
  
}
.edit{
  font-family: Georgia, 'Times New Roman', Times, serif;
  margin-bottom: 5%;
}

.chat-message {
  padding: 5px;
  background-color: #8a888886;
  border-radius: 5px;
  margin-bottom: 5px;
  color: white;
}

.chat-input {
  width: 100%;
  padding: 10px;
  border-radius: 5px;
  margin-top: 10px;
  border: 1px solid #ccc;
  background-color: rgba(255, 255, 255, 0.74)
}

textarea {
  width: 100%;
  padding: 10px;
  margin-top: 10px;
  border-radius: 5px;
  resize: none;
}

.file-input {
  margin-top: 10px;
}

.request-list {
  list-style: none;
  margin-top: 5%;
  
}

.request-item {
  background-color: rgb(204, 202, 202);
  border: solid black;
  box-shadow: 0 0 10px white;
  padding: 5px;
  text-align: center;
  margin-bottom: 10px;
}

.request-actions {
  display: flex;
  justify-content: space-between;
}
.button {
  padding: 10px 20px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  background-image: url("https://static.vecteezy.com/system/resources/thumbnails/000/549/015/small/vector-apr-2018-19.jpg");
  color: white;
  transition: background-color 0.3s;
  margin-left: 10%;
  margin-bottom: 5%;
}
.button2 {
  padding: 10px 20px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  background-image: url("https://static.vecteezy.com/system/resources/thumbnails/000/549/015/small/vector-apr-2018-19.jpg");
  color: white;
  transition: background-color 0.3s;
  margin-left: 10%;
  margin-bottom: 5%;
}

.vamoss1{
  color: #ffffff;
  font-weight: bold;
  font-family: 'Times New Roman', Times, serif;
  font-size: 130%;
}
.aceptar2_0{
  background-color: RED;
}
.vamoss2{
  color: #ffffff;
  font-weight: bold;
  font-family: 'Times New Roman', Times, serif;
  font-size: 150%;
  text-align: center
}
#caja{
  background-color: rgb(255, 255, 255);
  text-align: center;
  font-family:'Trebuchet MS', 'Lucida Sans Unicode', 'Lucida Grande', 'Lucida Sans', Arial, sans-serif;
  border: solid black;
  box-shadow: white 0 0 10px ;
}
#espacio{
  margin-right: 10%;
  top: 5%;
}
#espacio2{
  margin-right: 10%;
  margin-top: 10%;
}
.confi{
  box-shadow: 0 0 5px black;
  background-color: gray;
  margin-bottom: 5%;
  font-family: 'Times New Roman', Times, serif;
  text-shadow: 0 0 5px white;
  font-size: 150%;
}
.confi2{
  
  margin-bottom: 5%;
  font-family: 'Times New Roman', Times, serif;
  text-shadow: 0 0 2px rgb(112, 112, 112);
  font-size: 140%;
}
</style>