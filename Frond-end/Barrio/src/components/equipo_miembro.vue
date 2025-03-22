<template>
  <div class="padre">
    <div v-if="mostrarImagen" class="modal-overlay" @click.self="mostrarImagen = false">
    <img :src="team.logo" alt="Logo ampliado" class="logo-modal" />
  </div>
    <div class="team-leader">
      <!-- Encabezado: Logo y nombre del equipo -->
      <header class="header">
        <div class="logo-container" @click="mostrarImagen = true">
    <img :src="team.logo" alt="Logo del equipo" class="logo" v-if="team.logo" />
  </div>
        <router-link class="linktorneos" to="/galeria">
          <img class="api5" src="../assets/imagenes/galeria.png" alt="galeria">
        </router-link>
  
          <div class="epic-banner">
    <h1 class="epic-name">{{ team.name }}</h1>
            <p class="description">{{ team.description }}</p>
        </div> <!-- Descripción debajo del nombre -->
  
        <router-link class="linktorneos" to="/calendario">
          <img class="api5" src="../assets/imagenes/calendario.png" alt="calendario">
        </router-link>
  
        <div class="caja_hijo">
        
        <p class="miembros_style">
    Miembros: <br class="numeros">
    <span class="contador_style">{{ team.integrantes_actuales }}/{{ team.numero_integrantes }}</span>
  </p>
  
    </div>
      </header>
  
      <!-- Lista de integrantes -->
      <section class="members-section">
    <h2 class="name2">Integrantes:</h2>
  
    <!-- Mostrar el líder del equipo -->
    <div class="leader-section">
      <h3 class="name">Líder:</h3>
      <ul class="members-list2">
        <li
  class="member-item2 leader"
  v-if="team.leader && team.leader.name"
  @click="openMemberMenu(team.leader)"
>
  <div class="member-info">
    <img :src="team.leader.profilePicture" alt="Foto de perfil" class="profile-picture" />
    <span class="nombre2">{{ team.leader.name }}</span>
    <span class="role">(Líder)</span>
    <p class="details">
      Fecha de Nacimiento: {{ team.leader.birthDate || "No disponible" }}
    </p>
  </div>
</li>

      </ul>
    </div>
  
    <!-- Mostrar los miembros del equipo -->
    <div class="members-list-section">
      <h3 class="name">Miembros de "{{ team.name }}"</h3>
      <ul class="members-list">
        <li
          v-for="(member, index) in team.members"
          :key="index"
          class="member-item"
          @click="openMemberMenu(member)"
        >
          <div class="member-info">
            <img :src="member.profilePicture" alt="Foto de perfil" class="profile-picture" />
            <span class="nombre2">{{ member.name }}</span>
            <span class="role">({{ member.role }})</span>
            <p class="details">
              Fecha de Nacimiento: {{ member.birthDate || "No disponible" }}
            </p>
          </div>
        </li>
      </ul>
    </div>
  </section>
  
  
      <!-- Modal para editar integrante -->
      <div v-if="showMemberMenu" class="modal">
        <div class="modal-content">
          <h3 class="edit">Opciones para {{ selectedMember.name }}</h3>
          <button
  id="espacio"
  class="button_danger2"
  @click="verPerfil(selectedMember.documento !== undefined ? selectedMember.documento : team.leader.document)"
>
  ver perfil
</button>
  
          <button id="espacio"  class="button_close" @click="closeMemberMenu">Cerrar</button>
        </div>
      </div>
  
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
          numero_integrantes: 0,
          integrantes_actuales: 0,
          members: [],
          leader: {}, 
          requests: [],
          tournaments: ["Torneo A", "Torneo B"],
          chat: [
          ],
        },
        selectedMember: null,
        showMemberMenu: false,
        showConfig: false,
        newMessage: "",
        newDescription: "",
        mostrarImagen: false,
  
      };
    },
    async mounted() {
      await this.obtenerDatosEquipo(); // Llamar al cargar el componente
      await this.obtenerLiderEquipo();
      await this.obtenerCantidadIntegrantes();
    },
    methods: {
      async obtenerLiderEquipo() {
        try {
          const movistore = useUsuarios();
          if (!movistore.usuario.equipo_tiene) return;
  
          const response = await axios.get(`http://127.0.0.1:8000/equipos/${movistore.usuario.equipo_tiene}/lider`);
          
          this.team.leader = {
            name: response.data.lider.nombre,
            document: response.data.lider.documento,
            email: response.data.lider.correo,
            phone: response.data.lider.telefono,
            profilePicture: response.data.lider.imagen, // Se puede cambiar si el backend envía foto
            role: "Líder",
          };
  
        } catch (error) {
          console.error("Error al obtener datos del líder del equipo:", error);
        }
      },
      async obtenerDatosEquipo() {
        try {
          
          const movistore = useUsuarios();
          const response = await axios.get(`http://127.0.0.1:8000/equipos/${movistore.usuario.equipo_tiene}/detalle/`);
          console.log("logo: ",response.data.equipo.logo)
          this.team = {
            logo: `http://127.0.0.1:8000/${response.data.equipo.logo}`,
            name: response.data.equipo.nombre,
            description: response.data.equipo.descripcion,
            numero_integrantes: response.data.equipo.numero_integrantes,
            integrantes_actuales: 0,
            members: response.data.miembros.map(m => ({
              documento:m.documento,
              name: m.nombre,
              role: "Miembro", 
              profilePicture: "https://via.placeholder.com/50",
            })),
            tournaments: ["Torneo A", "Torneo B"],
            chat: [],
          };
  
          console.log("Datos del equipo:", this.team);
        } catch (error) {
          console.error("Error al obtener datos:", error);
        }
      },  
      
      openMemberMenu(member) {
        this.selectedMember = member;
        this.showMemberMenu = true;
      },
      closeMemberMenu() {
        this.showMemberMenu = false;
        this.selectedMember = null;
      },
  verPerfil(documento) {
    this.$router.push(`/perfiles/${documento}`); // Redirige usando el documento
  },
  
      sendMessage() {
        if (this.newMessage.trim() !== "") {
          this.team.chat.push({ sender: "Tú", content: this.newMessage });
          this.newMessage = "";
        }
      },
      
      openConfig() {
        this.showConfig = true;
        this.showBuzon = false; // Cerrar buzón si está abierto
      },
      updateLogo(event) {
    const file = event.target.files[0];
    if (file) {
      this.team.logo = URL.createObjectURL(file); // Previsualiza
    }
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
  
  async obtenerCantidadIntegrantes() {
    try {
      const movistore = useUsuarios();
      const response = await axios.get(`http://127.0.0.1:8000/equipos/${movistore.usuario.equipo_tiene}/integrantes`);
      
      this.team.integrantes_actuales = response.data; // Aquí guardamos la cantidad actual
    } catch (error) {
      console.error("Error al obtener cantidad de integrantes:", error);
      this.team.integrantes_actuales = 0;
    }
  },
  salir_equipo() {
  const movistore = useUsuarios();

  if (!movistore.usuario.documento) {
    Swal.fire("Error", "No se encontró el usuario. Inicia sesión.", "error");
    return;
  }

  const formData = new FormData();
  formData.append("documento_user", movistore.usuario.documento);

  axios
    .post("http://localhost:8000/equipos/salir", formData, {
      headers: {
        "Content-Type": "multipart/form-data",
      },
    })
    .then(async (response) => {
      if (response.status === 200) {
        Swal.fire("¡Éxito!", response.data.mensaje, "success");

        movistore.setUsuario({
          ...movistore.usuario,
          equipo_tiene: 0,
        });

        // ⚡ Limpia los datos del equipo localmente
        this.team = {
          logo: "",
          name: "",
          description: "",
          numero_integrantes: 0,
          integrantes_actuales: 0,
          members: [],
          leader: {},
          requests: [],
          tournaments: [],
          chat: [],
        };
      }
    })
    .catch((error) => {
      console.error("Error completo:", error);
      Swal.fire("Error", "Ocurrió un error al salir del equipo", "error");
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
  max-width: 850px;
  min-width: 800px;
  font-family: 'Arial', sans-serif;
  padding: 20px;
  background-image: url("../assets/imagenes/miembro_imagen.jpg"); 
  background-repeat: no-repeat;
  background-size: cover; /* Esto asegura que la imagen cubra todo el contenedor */
  color: #fff;
  border-radius: 10px;
  color: black;
  z-index:-6; /* Desenfoque de la imagen */
  border: solid white;
  }
  .api5 {
    height: 35px;
    width: 35px; /* Fijamos el ancho para que sea cuadrado */
    object-fit: cover; /* Rellena el contenedor sin deformarse */ /* Hace que sea circular */
    filter: drop-shadow(0 0 1px rgb(0, 0, 0));
    transition: transform 0.5s;
    margin: 0 5px;
  }
  /* Efecto al pasar el mouse */
  .api5:hover {
    transform: scale(1.15);
    box-shadow: 0 0 8px rgba(0, 150, 255, 0.6);
    background-color: #fff;
  }
  .linktorneos {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    padding: 6px;
    background-color: transparent;
    transition: background-color 0.3s, transform 0.3s;
    border-radius: 50%;
    width: 60px;
    background-color: rgb(255, 255, 255);
  }
  
  .linktorneos:hover {
    background-color: rgba(0, 0, 0, 0.05); /* efecto suave al pasar el mouse */
    transform: scale(1.1); /* efecto de agrandado */
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
  .name2{
    color: rgb(254, 212, 0);
    font-size: 220%;
    font-family :initial;
    text-align: center;
    text-shadow: 0 0 5px rgb(0, 0, 0);
    border: solid rgb(255, 255, 255);
    background-color: #ffffff30;
    margin-bottom: 5%;
  
  }
  
  
  
  
  .logo-container {
    display: flex;
    justify-content: center;
    align-items: center;
    padding: 10px;
  }
  
  .logo {
    width: 100px;
    height: 100px;
    object-fit: cover; /* rellena el espacio sin deformarse */
    border-radius: 50%; /* círculo perfecto */
    border: 3px solid #ffe100; /* color verde estilo pro, puedes cambiarlo */
    background-color: #fff;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
    box-shadow: 0 0 12px #ffe100;
  }
  
  
  .description {
    font-size: 1rem;
    color: #bcbcbc; /* más notorio que #ccc pero aún sutil */
    font-style: italic;
    margin-top: 10px;
    padding-left: 10px;/* línea suave a la izquierda */
    border: solid rgb(102, 102, 102);
    padding: 8px 12px;
    max-width: 500px;
    
    font-family: Cambria, Cochin, Georgia, Times, 'Times New Roman', serif;
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
  .member-item2 {
    display: flex;
    align-items: center;
    padding: 10px;
    background-color: rgba(0, 0, 0, 0.1);
    border-radius: 8px;
    margin-bottom: 10px;
    cursor: pointer;
    transition: background-color 0.3s;
  }
  .member-item2{
    background-color: rgba(0, 0, 0, 0.644);
    border: solid rgb(255, 210, 10)
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
  .button_danger2{
    background-color: #005bb5;
    padding: 2%;
    color: white;
    border-radius: 5px;
    font-family: Cambria, Cochin, Georgia, Times, 'Times New Roman', serif;
  }
  .button_danger2:hover{
    background-color: rgb(3, 17, 73);
    color: #aaa;
  
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
    margin-top: 1-0%;
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
  .modal-overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0, 0, 0, 0.7);
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 9999;
    cursor: pointer;
  }
  
  .logo-modal {
    width: 350px;   /* Puedes ajustar el tamaño predeterminado aquí */
    height: 350px;
    object-fit: cover;
    background-color: white;
    box-shadow: 0 0 15px rgba(255, 255, 255, 0.4);
    transition: transform 0.3s ease;
  }
  
  .logo-modal:hover {
    transform: scale(1.05);
  }
  
  @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@900&display=swap');
  
  .epic-banner {
    text-align: center;
    padding: 40px 20px;
    background-color: transparent;
    max-width: 90%;
    min-width: 40%;
  }
  
  .epic-name {
    font-family:initial;
    color: #ffffff; /* Dorado */
    text-shadow:
      1px 1px 0 #000000,
      2px 2px 0 #ffcc00,
      3px 3px 4px #000;
    letter-spacing: 4px;
    text-transform: uppercase;
    padding-left: 10%;
    padding-right: 10%;
  }
  .miembros_style {
    font-weight: bold;
    font-size: 18px;
    color: #fff7f7;
    border-top: solid white;
    border-bottom: solid white;
    
    padding: 10%;
    margin-top: 10px;
  }
  
  .contador_style {
    font-size: 24px;
    font-weight: 900;
    color: #ff9500; /* azul vibrante */
    display: inline-block;
    margin-top: 5px;
    background-color: #fffcea;
    padding: 4px 10px;
    border-radius: 8px;
    box-shadow: 1px 1px 4px rgba(0, 0, 0, 0.1);
  }
  
  .descripcion_actualizar{
    border: solid rgb(134, 134, 134);
    padding: 3%;
    margin-top: 7%;
    margin-bottom: 3%;
  }
  .logo-preview {
    width: 100px;
    height: 100px;
    object-fit: cover;
    margin-top: 10px;
    border-radius: 10px;
    border: 2px solid #ccc;
  }
  
  </style>