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
        <!-- Botones para abrir el submenú -->
        <section class="submenu-section">
          <button class="button" @click="openConfig">Configuración</button>
          <router-link class="padre" to="torneo_guardado">
            <button class="button2" @click="">incritos</button>
          </router-link>   
        </section>
        <!-- Modal de Configuración -->
        <div v-if="showConfig" class="modal config-modal">
          <div class="modal-content config-content">
            <h3 class="confi">Configuración</h3>
            <button id="espacio"class="button_danger" @click="salir_equipo">salir de equipo</button>
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
    import Swal from "sweetalert2";

    export default {
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
          showConfig: false,
          newMessage: "",
          newDescription: "",
        };
      },
      methods: {
        sendMessage() {
          if (this.newMessage.trim() !== "") {
            this.team.chat.push({ sender: "Tú", content: this.newMessage });
            this.newMessage = "";
          }
        },
        openConfig() {
          this.showConfig = true;
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
        salir_equipo() {
  const movistore = useUsuarios();

  if (!movistore.usuario.documento) {
    Swal.fire("Error", "No se encontró el usuario. Inicia sesión.", "error");
    return;
  }

  // ✅ Crear `FormData` para enviar como formulario
  const formData = new FormData();
  formData.append("documento_user", movistore.usuario.documento);

  axios
    .post("http://localhost:8000/equipos/salir", formData, {
      headers: {
        "Content-Type": "multipart/form-data", // ✅ Importante para `FormData`
      },
    })
    .then((response) => {
      if (response.status === 200) { // ✅ Asegurar que la respuesta es exitosa
        Swal.fire("¡Éxito!", response.data.mensaje, "success");

        // 🔄 **Actualizar la información del usuario en el store**
        movistore.setUsuario({
          ...movistore.usuario,
          equipo_tiene: 0, // El usuario ya no pertenece a ningún equipo
        });

        // 🚀 **Actualizar la lista de equipos sin recargar la página**
        fetchTeams();
      } else {
        console.warn("Respuesta inesperada del servidor:", response);
      }
    })
    .catch((error) => {
      console.error("Error completo:", error);
      console.error("Error en la solicitud:", error.response ? error.response.data : "Sin respuesta del servidor");

      // Solo mostrar el error si realmente ocurrió
      if (error.response?.data?.detail) {
        Swal.fire("Error", JSON.stringify(error.response.data.detail), "error");
      }
    });
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