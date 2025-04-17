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



  
          <div class="epic-banner">
    <h1 class="epic-name">{{ team.name }}</h1>
            <p class="description">{{ team.description }}</p>
        </div> <!-- Descripción debajo del nombre -->

  
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
    <img :src="getImagenUrl(team.leader.profilePicture)" alt="Foto de perfil" class="profile-picture" />
    <span class="nombre2">{{ team.leader.name }}</span>
    <span class="role">(Líder)</span>
    <p class="details">
      Fecha de Nacimiento: {{ team.leader.fecha_nacimiento || "Sin Fecha De Nacimiento" }}
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
            <img :src="getImagenUrl(member.profilePicture)" alt="Foto de perfil" class="profile-picture" />
            <span class="nombre2">{{ member.name }}</span>
            <span class="role">({{ member.role }})</span>
            <p class="details">
              Fecha de Nacimiento: {{ member.fecha_nacimiento || "No disponible" }}
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
          <button class="button2" @click="">Inscritos</button>
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
        <div v-for="(message, index) in chats" :key="index" class="chat-message">
          <div class="message-header">
            <img :src="message.sender.profilePicture" alt="Foto de perfil" class="profile-pic" />
            <strong class="sender-name">{{ message.sender.nombre }}</strong>
            <span class="timestamp">{{ message.timestamp }}</span>
          </div>
          <p class="message-content">{{ message.content }}</p>
         <!-- Botón pequeño con ícono de reportar -->
         <button class="report-icon-button" @click="abrirModalReporte(message)">
  &#9888; <!-- Carácter Unicode para una bandera -->
</button>
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
  <div v-if="mostrarModalReporte" class="modal-overlay">
  <div class="modal-content">
    <h3 class="modal-title">Reportar Mensaje</h3>
    
    <p class="modal-text">
      <strong>Mensaje:</strong> {{ mensajeSeleccionado.content }}
    </p>

    <label for="motivo" class="modal-label">Motivo:</label>
    <select v-model="motivoReporte" id="motivo" class="modal-select">
      <option disabled value="">Selecciona un motivo</option>
      <option>Contenido ofensivo</option>
      <option>Spam</option>
      <option>Comportamiento inapropiado</option>
      <option>Otro</option>
    </select>

    <label for="comentario" class="modal-label">Comentario:</label>
    <textarea v-model="comentarioReporte" id="comentario" rows="4" class="modal-textarea" placeholder="Escribe un comentario..."></textarea>

    <div class="modal-buttons">
      <button @click="enviarReporte" class="modal-button modal-button-send">Enviar Reporte</button>
      <button @click="cerrarModalReporte" class="modal-button modal-button-cancel">Cancelar</button>
    </div>
  </div>
</div>
  </template>
  
  <script>
import { useUsuarios } from '@/stores/usuario';
import axios from 'axios';
import { io } from "socket.io-client";


export default {
  components: {
    useUsuarios,
  },
  data() {
    return {
      chats : [],
      nuevoMensaje: "",
      team: {
        logo: "",
        name: "",
        description: "",
        numero_integrantes: 0,
        integrantes_actuales: 0,
        members: [],
        leader: {}, 
        requests: [
        ],
        tournaments: [],
        puntos: 0, // Puntos del equipo
      nivel: 1,  // Nivel del equipo
      },
      mostrarModalReporte: false,
      mensajeSeleccionado: null,
      motivoReporte: "",
      comentarioReporte: "",
      selectedMember: null,
      showMemberMenu: false,
      showBuzon: false,
      showConfig: false,
      newMessage: "",
      newDescription: "",
      mostrarImagen: false,

    };
  },
  computed: {
  nivel() {
    if (!this.team.puntos || this.team.puntos < 500) return 1; // Si no tiene puntos o tiene menos de 500, está en nivel 1
    if (this.team.puntos < 2000) return 2; // Entre 500 y 1999, nivel 2
    if (this.team.puntos < 5000) return 3; // Entre 2000 y 4999, nivel 3
    return 4; // 5000 o más, nivel 4
  },
  siguienteNivel() {
    if (this.nivel === 1) return 500; // Próximo nivel para nivel 1
    if (this.nivel === 2) return 2000; // Próximo nivel para nivel 2
    if (this.nivel === 3) return 5000; // Próximo nivel para nivel 3
    return null; // Nivel máximo alcanzado
  },
  progreso() {
    if (!this.siguienteNivel) return 100; // Si no hay siguiente nivel, progreso completo

    const niveles = [0, 500, 2000, 5000];
    const inicio = niveles[this.nivel - 1];
    const fin = this.siguienteNivel;
    const porcentaje = ((this.team.puntos - inicio) / (fin - inicio)) * 100;

    return Math.min(100, Math.max(0, porcentaje.toFixed(2)));
  },
},

  async mounted() {
  await this.obtenerDatosEquipo();
  await this.obtenerLiderEquipo();
  await this.obtenerCantidadIntegrantes();
  await this.viewMessages();
  await this.requests();
  this.conectarSocket(); // Llamar a la conexión WebSocket

  const movistore = useUsuarios();
  const team_Id = movistore.usuario.equipo_tiene;
  
  
  this.socket = io("http://localhost:8000");
  
  // Unirse a la sala del equipo
  this.socket.emit("joinRoom", team_Id);
  
  // Escuchar nuevos mensajes y agregarlos en tiempo real
  this.socket.on("nuevoMensaje", (message) => {
  console.log("📩 Nuevo mensaje recibido:", message);
  this.chats.push({
    sender: {
      nombre: message.sender.nombre,
      profilePicture: this.getImagenUrl(message.sender.imagen),
    },
    content: message.content,
    timestamp: message.timestamp,
  });
});

},

methods: {
  
  async sendMessage() {
    const movistore = useUsuarios();
    const team_Id = movistore.usuario.equipo_tiene;
    

    if (this.newMessage.trim() !== "") {
      const messageData = {
        team_id: team_Id,
        sender: movistore.usuario.documento,
        content: this.newMessage,
      };

      try {
        // Enviar el mensaje a la base de datos
        await axios.post("http://localhost:8000/chat/send", messageData);

        // Emitir el mensaje por WebSocket
        this.socket.emit("sendMessage", messageData);

        this.newMessage = "";
      } catch (error) {
        console.error("❌ Error al enviar el mensaje:", error);
      }
    }
  },

  async viewMessages() {
    const movistore = useUsuarios();
    const team_Id = movistore.usuario.equipo_tiene;


    try {
      // Obtener mensajes desde la base de datos
      const response = await axios.get(`http://localhost:8000/chat/${team_Id}`);
      this.chats = response.data.messages.map((message) => ({
        sender: {
          nombre: message.sender.nombre,
          profilePicture: this.getImagenUrl(message.sender.imagen),
          documento: message.sender.documento,
        },
        content: message.content,
        timestamp: message.timestamp,
      }));
    } catch (error) {
      console.error("❌ Error al obtener los mensajes:", error);
    }
  },

  conectarSocket() {
    this.socket = io("http://localhost:8000", {
      path: "/socket.io/",
      transports: ["websocket", "polling"],
    });

    this.socket.on("connect", () => {
      console.log("🔗 Conectado al WebSocket con ID:", this.socket.id);
    });

    this.socket.on("nuevoMensaje", (message) => {
      console.log("📩 Nuevo mensaje recibido:", message);

      // Verificar si el mensaje ya existe para evitar duplicados
      const exists = this.chats.some(
        (chat) => chat.timestamp === message.timestamp && chat.content === message.content
      );

      if (!exists) {
        this.chats.push({
          sender: {
            nombre: message.sender.nombre,
            profilePicture: this.getImagenUrl(message.sender.imagen),
          },
          content: message.content,
          timestamp: message.timestamp,
        });
      }
    });

    this.socket.on("connect_error", (err) => {
      console.error("❌ Error de conexión:", err.message);
    });
  },
    getImagenUrl(path) {
    return path ? `http://127.0.0.1:8000/${path}` : '';
  },
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
          profilePicture: response.data.lider.imagen,
          fecha_nacimiento : response.data.lider.fecha_nacimiento,
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
    this.team = {
      logo: `http://127.0.0.1:8000/${response.data.equipo.logo}`,
      name: response.data.equipo.nombre,
      description: response.data.equipo.descripcion,
      numero_integrantes: response.data.equipo.numero_integrantes,
      integrantes_actuales: 0,
      puntos: response.data.equipo.puntos, // Asegúrate de que el backend envíe los puntos
      nivel: response.data.equipo.nivel,  // Asegúrate de que el backend envíe el nivel
      members: response.data.miembros.map(m => ({
        documento: m.documento,
        name: m.nombre,
        role: "Miembro",
        profilePicture: m.imagen,
        fecha_nacimiento: m.fecha_nacimiento,
      })),
      tournaments: ["Torneo A", "Torneo B"],
      chat: [],
    };
  } catch (error) {
    console.error("Error al obtener datos del equipo:", error);
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

    async confirmExpel(documento, nombre) {
  const movistore = useUsuarios();
     // **Actualizar el estado en Pinia**
   

  if (!movistore.usuario.equipo_tiene) {
    console.error("Error: No hay equipo seleccionado.");
    alert("No tienes un equipo asignado.");
    return;
  }

  if (!documento) {
    console.error("Error: El documento del miembro es inválido.", documento);
    alert("Error al expulsar: el documento es inválido.");
    return;
  }

  if (confirm(`¿Estás seguro de expulsar a ${nombre}?`)) {
    try {
      const formData = new FormData();
      formData.append("id_team", movistore.usuario.equipo_tiene);
      formData.append("documento_miembro", documento);

      console.log("Enviando FormData:", Object.fromEntries(formData));

      const response = await axios.post("http://127.0.0.1:8000/equipos/expulsar", formData, {
        headers: { "Content-Type": "multipart/form-data" }
      });

      console.log("Respuesta del servidor:", response.data);

      // ✅ Actualizar la lista de miembros
      this.team.members = this.team.members.filter(m => m.documento !== documento);
      
      this.closeMemberMenu();
      alert(`${nombre} ha sido expulsado del equipo.`);

    } catch (error) {
      console.error("Error al expulsar:", error.response ? error.response.data : error);
      alert(error.response?.data?.detail || "Hubo un error al expulsar al miembro.");
    }
  }
},

// Modal reporte
abrirModalReporte(mensaje) {
  console.log("Mensaje seleccionado:", mensaje); // Verifica el contenido del mensaje
  this.mensajeSeleccionado = mensaje;
  this.mostrarModalReporte = true;
},
    cerrarModalReporte() {
      this.mostrarModalReporte = false;
      this.mensajeSeleccionado = null;
      this.motivoReporte = "";
      this.comentarioReporte = "";
    },
    async enviarReporte() {
  if (!this.motivoReporte || !this.comentarioReporte) {
    alert("Por favor completa todos los campos.");
    return;
  }

  const movistore = useUsuarios(); // Obtén el estado del usuario actual
 

  const reporte = {
    documento_reportante: movistore.usuario.documento, // Documento del usuario actual
    documento_reportado: this.mensajeSeleccionado.sender.documento, // Documento del remitente del mensaje
    motivo: this.motivoReporte, // Motivo seleccionado
    comentario: this.comentarioReporte, // Comentario adicional
  };

  console.log("Datos enviados al backend:", reporte); // Inspecciona los datos enviados

  try {
    const response = await axios.post("http://127.0.0.1:8000/reportar_usuario/", reporte, {
      headers: {
        "Content-Type": "application/x-www-form-urlencoded", // Asegúrate de que el backend reciba datos en formato Form-Encoded
      },
    });
    alert(response.data.mensaje);
    this.cerrarModalReporte();
  } catch (error) {
    console.error("Error al enviar el reporte:", error.response?.data || error.message);
    alert("Hubo un error al enviar el reporte.");
  }
},




verPerfil(documento) {
  this.$router.push(`/perfiles/${documento}`); // Redirige usando el documento
},

    openBuzon() {
      this.showBuzon = true;
      this.showConfig = false; // Cerrar configuración si está abierta
    },
    openConfig() {
      this.showConfig = true;
      this.showBuzon = false; // Cerrar buzón si está abierto
    },
    verUsuario(documento) {
  this.$router.push({ name: 'perfiles', params: { documento } });
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


    salir_equipo() {
  const movistore = useUsuarios();
  const formData = new FormData();
  formData.append('documento_user', movistore.usuario.documento); // Usa el documento del usuario logueado

  axios.post('http://localhost:8000/equipos/salir', formData)
    .then(response => {
      console.log(response.data.mensaje);
      // ✅ Actualizar estado local
      movistore.usuario.equipo_tiene = 0;
      // ✅ Mostrar notificación si quieres
      alert('Has salido del equipo exitosamente.');
    })
    .catch(error => {
      console.error('Error al salir del equipo:', error);
      alert(error.response?.data?.detail || 'No se pudo salir del equipo.');
    });
},






  
      rejectRequest(solicitud) {
        this.team.requests = this.team.requests.filter((req) => req !== solicitud);
      },
    async updateTeam() {
  try {
    const movistore = useUsuarios();
    const formData = new FormData();

    // Agregar la nueva descripción si hay
    if (this.newDescription) {
      formData.append("nueva_descripcion", this.newDescription);
    }

    // Buscar el archivo de logo (input file)
    const inputFile = document.getElementById("newLogo");
    if (inputFile && inputFile.files.length > 0) {
      formData.append("nuevo_logo", inputFile.files[0]);
    }

    const id_equipo = movistore.usuario.equipo_tiene;

    const response = await axios.put(
      `http://127.0.0.1:8000/equipos/actualizar/${id_equipo}`,
      formData,
      {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      }
    );

    console.log("Respuesta al actualizar equipo:", response.data);
    alert("Equipo actualizado correctamente");

    // Actualizar descripción en el frontend
    this.team.description = this.newDescription;

    // Cerrar la ventana de configuración
    this.closeConfig();

    // Refrescar los datos del equipo (opcional)
    await this.obtenerDatosEquipo();
    await this.obtenerLiderEquipo();
    await this.obtenerCantidadIntegrantes();
  } catch (error) {
    console.error("Error al actualizar el equipo:", error.response || error);
    alert("Hubo un error al actualizar el equipo.");
  }
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
async requests() {
  const usuarioStore = useUsuarios(); // Usamos el store de usuario
  try {
    const idEquipo = usuarioStore.usuario.equipo_tiene;
    console.log("ID del equipo:", idEquipo);

    const res = await axios.get(
      `http://127.0.0.1:8000/solicitudes_pendientes/${idEquipo}`,
      {
        headers: {
          Accept: 'application/json',
        },
      }
    );

    console.log("Respuesta del backend:", res.data);

    this.team.requests = res.data.map(solicitud => ({
      id_solicitud: solicitud.id_solicitud,
      documento: solicitud.documento_usuario,
      name: solicitud.nombre_usuario,
      picture: solicitud.logo_usuario || 'default.png',
      fecha: solicitud.fecha_solicitud,
    }));

    console.log("Solicitudes procesadas:", this.team.requests);
  } catch (error) {
    console.error("Error al obtener solicitudes-------------------:", error);
  }
},


async acceptRequest(solicitud) {
    try {
      const response = await fetch(`http://localhost:8000/solicitudes_ingreso/${solicitud.id_solicitud}/aceptar`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({})
      });

      if (!response.ok) {
        const errorData = await response.json();
        console.error("Error en la solicitud:", errorData.detail);
        alert(`Error: ${errorData.detail}`);
        return;
      }

      const data = await response.json();
      console.log("Respuesta del servidor:", data);
      alert("Solicitud aceptada con éxito");
    } catch (error) {
      console.error("Error en fetch:", error);
      alert("Ocurrió un error al aceptar la solicitud");
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
max-width: 850px;
min-width: 800px;
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
  padding-top: 50px;
  padding-right: 50px;
  
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
  margin-top: 6%;
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




.button_info-btn {
  background-color: #6a6a6a;
  color: #ffffff;
  padding: 5px;
  border: none;

  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  font-size: 10px;
  font-weight: bold;
  cursor: pointer;
  transition: all 0.2s ease-in-out;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
}

.button_info-btn:hover {
  background-color: #a3a3a3;
  color: white;
  transform: scale(1.05);
  box-shadow: 0 0 10px white;
}
.button_info-btn2 {
  background-color: #6a6a6a;
  color: #ffffff;
  padding: 5px;
  border: none;
  font-family:Arial, Helvetica, sans-serif;
  font-size: 15px;
  font-weight: bold;
  margin-right: 15px;
  cursor: pointer;
  transition: all 0.2s ease-in-out;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
}

.button_info-btn2:hover {
  background-color: #a3a3a3;
  color: white;
  transform: scale(1.05);
  box-shadow: 0 0 10px white;
}
.button_accept-btn {
  background-color: #ffd814; /* verde más moderno */
  font-family: Georgia, 'Times New Roman', Times, serif;
  padding: 5px;
  color: #000000;
  border: none;
  
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  font-size: 13px;
  cursor: pointer;
  box-shadow: 0 4px 8px rgba(0, 128, 0, 0.2);
  transition: background-color 0.3s ease, transform 0.2s ease, box-shadow 0.3s ease;
  border-radius: 8px;
}

.button_accept-btn:hover {
  background-color: #d0ae29;
  color: #e5ffe5;
  transform: scale(1.05);
  box-shadow: 0 6px 12px rgba(0, 128, 0, 0.4);
  box-shadow: 0 0 10px white;
}

.vertical{
  display: flex;
  align-items: center;
  margin-bottom: 10px;
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
  padding: 5px;
  background-color: #fb0820; /* rojo más moderno */
  color: white;
  border: none;
  border-radius: 8px;
  font-family: Cambria, Cochin, Georgia, Times, 'Times New Roman', serif;
  font-size: 15px;
  cursor: pointer;
  box-shadow: 0 4px 8px rgba(220, 53, 69, 0.2);
  transition: background-color 0.3s ease, transform 0.2s ease, box-shadow 0.3s ease;
}

.button_reject-btn:hover {
  background-color: #a71d2a; /* rojo más oscuro para el hover */
  color: #ffeaea;
  transform: scale(1.05);
  box-shadow: 0 6px 12px rgba(220, 53, 69, 0.4);
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
  padding: 20px;
  
}
.edit{
  font-family: Georgia, 'Times New Roman', Times, serif;
  margin-bottom: 5%;
}

.chat-message {
background-color: #1a1a1a;
border: 1px solid #333;
border-left: 4px solid transparent;
border-radius: 12px;
padding: 14px;
margin-bottom: 18px;
color: #fff;
position: relative;
box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
transition: all 0.3s ease;
cursor: pointer;
width: 100%;
/* 🛠 Estas líneas son clave para textos largos */
word-wrap: break-word;
white-space: pre-wrap;
overflow-wrap: break-word;
}
.chat-message:hover {
  border-color: #d4af37; /* dorado */
  border-left: 4px solid #d4af37;
  background-color: #222;
  transform: scale(1.015);
}

.message-header {
  display: flex;
  align-items: center;
  margin-bottom: 5px;
}
.profile-pic {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  object-fit: cover;
  margin-right: 12px;
  border: 2px solid #d4af37;
  transition: transform 0.3s ease;
}
.chat-message:hover .profile-pic {
  transform: rotate(5deg);
}


.chat-input {
  width: 100%;
  padding: 10px;
  border-radius: 5px;
  margin-top: 10px;
  border: 1px solid #ccc;
  background-color: rgba(255, 255, 255, 0.74)
}

.sender-name {
  color: #d4af37; /* dorado */
  font-weight: bold;
  margin-right: auto;
}

.timestamp {
  font-size: 0.75rem;
  color: #ccc; /* gris claro */
}
.message-content {
  font-size: 1rem;
  color: #eee;
  padding-left: 52px;
  position: relative;
  margin-left: 20px;
}
.report-icon-button {
  position: absolute;
  top: 8px;
  right: 8px;
  background: transparent;
  border: none;
  color: #d4af37; /* dorado */
  font-size: 1.2rem;
  cursor: pointer;
  transition: transform 0.2s ease, color 0.2s ease;
}
.report-icon-button:hover {
  color: #fff;
  transform: scale(1.2);
}

.report-icon-button i {
  font-size: 1.2rem; /* Tamaño del ícono */
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
}

.modal-content {
  background-color: white;
  padding: 20px;
  border-radius: 10px;
  width: 90%;
  max-width: 400px;
  text-align: center;
}

.button-close {
  background-color: gray;
  color: white;
  margin-top: 10px;
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
  max-height: 300px; /* Altura máxima visible */
  overflow-y: auto;  /* Agrega scroll vertical solo si es necesario */
  padding-right: 10px; 
  
}
.request-list::-webkit-scrollbar {
  width: 8px;
}
.request-list::-webkit-scrollbar-thumb {
  background-color: #888;
  border-radius: 4px;
}
.request-list::-webkit-scrollbar-thumb:hover {
  background-color: #555;
}
.request-item {
  gap: 10px;
  background-color: #1e1e1e;
  border: 1px solid #444;
  border-radius: 12px;
  margin-top: 10px;
  box-shadow: 0 4px 10px rgba(255, 255, 255, 0.05);
  padding: 10px 15px;
  margin-bottom: 12px;
  color: white;
  transition: transform 0.2s ease, background-color 0.2s ease;
}

.request-item:hover {
  transform: scale(1.05);
  background-color: #fdd70074;
  box-shadow: 0 4px 15px rgba(255, 255, 255, 0.1);
  box-shadow: 0 0 10px orange;
  color: black;
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
.profile-pic{
  width: 60px;
  height: 60px;
  border-radius: 50px;
  border: solid rgb(0, 0, 0);
}
.letra2p{
  font-family: Cambria, Cochin, Georgia, Times, 'Times New Roman', serif;
  margin-left: 10px;
}

.nivel-container {
  max-width: 420px;
  margin: 1px auto;
  padding: 5px;
  border-radius: 20px;
  font-family: 'Rajdhani', sans-serif;
  color: #fff;
  text-align: center;
  position: relative;
  overflow: hidden;
}

.nivel-titulo {
  font-size: 30px;
  color: #ffd700;
  margin-bottom: 20px;
  position: relative;
  z-index: 1;
  text-shadow: 0 0 6px rgba(255, 215, 0, 0.6);
}

.barra-progreso {
  width: 100%;
  height: 26px;
  background-color: #444;
  border: 1px solid #888;
  border-radius: 30px;
  overflow: hidden;
  position: relative;
  z-index: 1;
}

.progreso {
  height: 100%;
  background: linear-gradient(
    90deg,
    #ffd700 0%,
    #fff3b0 50%,
    #ffd700 100%
  );
  background-size: 200% 100%;
  animation: shineProgress 2s linear infinite;
  border-radius: 30px 0 0 30px;
  transition: width 0.6s ease-in-out;
  box-shadow: 0 0 10px rgba(255, 215, 0, 0.6);
}

@keyframes shineProgress {
  0% {
    background-position: 200% 0;
  }
  100% {
    background-position: -200% 0;
  }
}

.nivel-detalle {
  font-size: 16px;
  color: #ccc;
  margin-top: 14px;
  position: relative;
  z-index: 1;
  letter-spacing: 1px;
}
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.75);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  backdrop-filter: blur(3px);
}

.modal-content {
  background-color: #1a1a1a;
  padding: 24px;
  border-radius: 16px;
  width: 90%;
  max-width: 400px;
  color: #fff;
  border: 2px solid #d4af37;
  box-shadow: 0 0 20px rgba(212, 175, 55, 0.4);
  animation: fadeInUp 0.4s ease;
}

.modal-title {
  color: #d4af37;
  font-size: 1.4rem;
  margin-bottom: 16px;
}

.modal-text {
  color: #eaeaea;
  margin-bottom: 12px;
  word-wrap: break-word;
white-space: pre-wrap;
overflow-wrap: break-word;
}

.modal-label {
  display: block;
  margin: 12px 0 4px;
  color: #ccc;
  font-weight: bold;
}

.modal-select,
.modal-textarea {
  width: 100%;
  padding: 10px;
  border-radius: 8px;
  border: 1px solid #555;
  background-color: #2a2a2a;
  color: #fff;
  font-size: 0.95rem;
  transition: border 0.3s;
}

.modal-select:focus,
.modal-textarea:focus {
  border: 1px solid #d4af37;
  outline: none;
}

.modal-buttons {
  display: flex;
  justify-content: space-between;
  margin-top: 20px;
}

.modal-button {
  padding: 10px 16px;
  border-radius: 8px;
  font-weight: bold;
  cursor: pointer;
  transition: all 0.3s;
  font-size: 0.95rem;
  border: none;
}

.modal-button-send {
  background-color: #d4af37;
  color: #1a1a1a;
}

.modal-button-send:hover {
  background-color: #f5d76e;
}

.modal-button-cancel {
  background-color: transparent;
  color: #ccc;
  border: 1px solid #555;
}

.modal-button-cancel:hover {
  background-color: #333;
  color: #fff;
  border-color: #777;
}

/* Animación al mostrar el modal */
@keyframes fadeInUp {
  0% {
    opacity: 0;
    transform: translateY(20px);
  }
  100% {
    opacity: 1;
    transform: translateY(0);
  }
}





@media (min-width: 320px) and (max-width: 480px) {

.team-leader {
max-width: 50vw;
min-width: 100vw;
font-family: 'Arial', sans-serif;
padding: 1rem;
background-image: url("../assets/imagenes/cancha.jpg"); 
background-repeat: no-repeat;
background-size: cover; /* Esto asegura que la imagen cubra todo el contenedor */
color: #fff;
border-radius: 10px;
color: black;
z-index:-6; /* Desenfoque de la imagen */
border: solid white;
}


.header {
text-align: center;
background-color: rgba(3, 0, 0, 0.822);
padding: 0rem;
border-radius: 10px;
color: white;
}



.logo-container {
display: flex;
justify-content: center;
align-items: center;
padding-top: 1rem;
padding-right: 0rem

}

.logo {
width: 40%;
height: 20%;
object-fit: cover; /* rellena el espacio sin deformarse */
border-radius: 50%; /* círculo perfecto */
border: 3px solid #ffe100; /* color verde estilo pro, puedes cambiarlo */
background-color: #fff;
box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
box-shadow: 0 0 12px #ffe100;

}

.epic-banner {
text-align: center;
padding: 1rem 2.1rem;
background-color: transparent;
max-width: 5%;
min-width: 10%;
}

.epic-name {
font-family:initial;
color: #ffffff; /* Dorado */
text-shadow:
  1px 1px 0 #000000,
  2px 2px 0 #ffcc00,
  3px 3px 4px #000;
letter-spacing: 0rem;
text-transform: uppercase;
padding-left: 1%;
padding-right: 10%;
font-size: 1.3rem;
}

.description {
font-size: 1rem;
color: #bcbcbc; /* más notorio que #ccc pero aún sutil */
font-style: italic;
margin-top: 0%;
border: solid transparent;
padding: 0rem 0rem;
font-family: Cambria, Cochin, Georgia, Times, 'Times New Roman', serif;
}


.miembros_style {
font-weight: bold;
font-size: 1rem;
color: #fff7f7;
border-top: solid white;
border-bottom: solid white;
padding: 0rem;
margin-top: 150%;
margin-right: 1rem;
}


.caja_hijo{
margin-left: 0rem; 
}


.chat-section {
margin-top: 0%;
padding: 2rem;
background-color: #000000;
border-radius: 10px;
}

.chat-box {
max-height: 80%;
max-width: 200%;
overflow-y: auto;
margin-bottom: 0%;
padding: 1rem;

}

.chat-message {
background-color: #1a1a1a;
border: 1px solid #333;
border-left: 4px solid transparent;
border-radius: 12px;
padding: 14px;
margin-bottom: 18px;
color: #fff;
position: relative;
box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
transition: all 0.3s ease;
cursor: pointer;
width: 100%;
/* 🛠 Estas líneas son clave para textos largos */
word-wrap: break-word;
white-space: pre-wrap;
overflow-wrap: break-word;
}

.chat-message:hover {
border-color: #d4af37; /* dorado */
border-left: 4px solid #d4af37;
background-color: #222;
transform: scale(1.015);
}

.message-header {
display: flex;
align-items: center;
margin-bottom: 5px;
}


.sender-name {
color: #ffffff; /* dorado */
font-weight: bold;
margin-right: 0%;
font-size: 15px;
}

.timestamp {
display: none;
}


.message-content {
font-size: 1rem;
color: #eee;
padding-left: 0%;
position: relative;
margin-left: 0%;
}


.members-section {
margin-top: 0%;
}




.logo-container {
display: flex;
justify-content: center;
align-items: center;
padding-top: 50px;

}

.logo {
width: 15vh;
height: 15vh;
object-fit: cover; /* rellena el espacio sin deformarse */
border-radius: 50%; /* círculo perfecto */
border: 3px solid #ffe100; /* color verde estilo pro, puedes cambiarlo */
background-color: #fff;
box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
box-shadow: 0 0 12px #ffe100;

}

}




@media (min-width: 481px) and (max-width: 600px) {

.team-leader {
max-width: 50vw;
min-width: 100vw;
font-family: 'Arial', sans-serif;
padding: 1rem;
background-image: url("../assets/imagenes/cancha.jpg"); 
background-repeat: no-repeat;
background-size: cover; /* Esto asegura que la imagen cubra todo el contenedor */
color: #fff;
border-radius: 10px;
color: black;
z-index:-6; /* Desenfoque de la imagen */
border: solid white;
}


.header {
text-align: center;
background-color: rgba(3, 0, 0, 0.822);
padding: 0rem;
border-radius: 10px;
color: white;
}



.logo-container {
display: flex;
justify-content: center;
align-items: center;
padding-top: 1rem;
padding-right: 0rem

}

.logo {
width: 40%;
height: 20%;
object-fit: cover; /* rellena el espacio sin deformarse */
border-radius: 50%; /* círculo perfecto */
border: 3px solid #ffe100; /* color verde estilo pro, puedes cambiarlo */
background-color: #fff;
box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
box-shadow: 0 0 12px #ffe100;

}

.epic-banner {
text-align: center;
padding: 1rem 7rem;
background-color: transparent;
max-width: 5%;
min-width: 10%;
}

.epic-name {
font-family:initial;
color: #ffffff; /* Dorado */
text-shadow:
  1px 1px 0 #000000,
  2px 2px 0 #ffcc00,
  3px 3px 4px #000;
letter-spacing: 0rem;
text-transform: uppercase;
padding-left: 1%;
padding-right: 10%;
font-size: 1.5rem;
}

.description {
font-size: 1.5rem;
color: #bcbcbc; /* más notorio que #ccc pero aún sutil */
font-style: italic;
margin-top: 0%;
border: solid transparent;
padding: 0rem 0rem;
font-family: Cambria, Cochin, Georgia, Times, 'Times New Roman', serif;
}


.miembros_style {
font-weight: bold;
font-size: 1rem;
color: #fff7f7;
border-top: solid white;
border-bottom: solid white;
padding: 0rem;
margin-top: 150%;
margin-right: 1rem;
}


.caja_hijo{
margin-left: 0rem; 
}


.chat-section {
margin-top: 0%;
padding: 2rem;
background-color: #000000;
border-radius: 10px;
}

.chat-box {
max-height: 80%;
max-width: 200%;
overflow-y: auto;
margin-bottom: 0%;
padding: 1rem;

}

.chat-message {
background-color: #1a1a1a;
border: 1px solid #333;
border-left: 4px solid transparent;
border-radius: 12px;
padding: 14px;
margin-bottom: 18px;
color: #fff;
position: relative;
box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
transition: all 0.3s ease;
cursor: pointer;
width: 100%;
/* 🛠 Estas líneas son clave para textos largos */
word-wrap: break-word;
white-space: pre-wrap;
overflow-wrap: break-word;
}

.chat-message:hover {
border-color: #d4af37; /* dorado */
border-left: 4px solid #d4af37;
background-color: #222;
transform: scale(1.015);
}

.message-header {
display: flex;
align-items: center;
margin-bottom: 5px;
}


.sender-name {
color: #ffffff; /* dorado */
font-weight: bold;
margin-right: 0%;
font-size: 15px;
}

.timestamp {
display: none;
}


.message-content {
font-size: 1rem;
color: #eee;
padding-left: 0%;
position: relative;
margin-left: 0%;
}


.members-section {
margin-top: 0%;
}




.logo-container {
display: flex;
justify-content: center;
align-items: center;
padding-top: 50px;

}

.logo {
width: 15vh;
height: 15vh;
object-fit: cover; /* rellena el espacio sin deformarse */
border-radius: 50%; /* círculo perfecto */
border: 3px solid #ffe100; /* color verde estilo pro, puedes cambiarlo */
background-color: #fff;
box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
box-shadow: 0 0 12px #ffe100;

}



}
@media (min-width: 601px) and (max-width: 768px) {

.team-leader {
max-width: 50vw;
min-width: 100vw;
font-family: 'Arial', sans-serif;
padding: 1rem;
background-image: url("../assets/imagenes/cancha.jpg"); 
background-repeat: no-repeat;
background-size: cover; /* Esto asegura que la imagen cubra todo el contenedor */
color: #fff;
border-radius: 10px;
color: black;
z-index:-6; /* Desenfoque de la imagen */
border: solid white;
}


.header {
text-align: center;
background-color: rgba(3, 0, 0, 0.822);
padding: 0rem;
border-radius: 10px;
color: white;
}



.logo-container {
display: flex;
justify-content: center;
align-items: center;
padding-top: 1rem;
padding-right: 0rem

}

.logo {
width: 40%;
height: 20%;
object-fit: cover; /* rellena el espacio sin deformarse */
border-radius: 50%; /* círculo perfecto */
border: 3px solid #ffe100; /* color verde estilo pro, puedes cambiarlo */
background-color: #fff;
box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
box-shadow: 0 0 12px #ffe100;

}

.epic-banner {
text-align: center;
padding: 1rem 5rem;
background-color: transparent;
max-width: 5%;
min-width: 10%;
}

.epic-name {
font-family:initial;
color: #ffffff; /* Dorado */
text-shadow:
  1px 1px 0 #000000,
  2px 2px 0 #ffcc00,
  3px 3px 4px #000;
letter-spacing: 0rem;
text-transform: uppercase;
padding-left: 1%;
padding-right: 10%;
font-size: 2rem;
}

.description {
font-size: 2rem;
color: #bcbcbc; /* más notorio que #ccc pero aún sutil */
font-style: italic;
margin-top: 0%;
border: solid transparent;
padding: 0rem 0rem;
font-family: Cambria, Cochin, Georgia, Times, 'Times New Roman', serif;
}


.miembros_style {
font-weight: bold;
font-size: 1rem;
color: #fff7f7;
border-top: solid white;
border-bottom: solid white;
padding: 0rem;
margin-top: 150%;
margin-right: 1rem;
}


.caja_hijo{
margin-left: 10rem; 
}


.chat-section {
margin-top: 0%;
padding: 2rem;
background-color: #000000;
border-radius: 10px;
}

.chat-box {
max-height: 80%;
max-width: 200%;
overflow-y: auto;
margin-bottom: 0%;
padding: 1rem;

}

.chat-message {
background-color: #1a1a1a;
border: 1px solid #333;
border-left: 4px solid transparent;
border-radius: 12px;
padding: 14px;
margin-bottom: 18px;
color: #fff;
position: relative;
box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
transition: all 0.3s ease;
cursor: pointer;
width: 100%;
/* 🛠 Estas líneas son clave para textos largos */
word-wrap: break-word;
white-space: pre-wrap;
overflow-wrap: break-word;
}

.chat-message:hover {
border-color: #d4af37; /* dorado */
border-left: 4px solid #d4af37;
background-color: #222;
transform: scale(1.015);
}

.message-header {
display: flex;
align-items: center;
margin-bottom: 5px;
}


.sender-name {
color: #ffffff; /* dorado */
font-weight: bold;
margin-right: 0%;
font-size: 15px;
}

.timestamp {
display: none;
}


.message-content {
font-size: 1rem;
color: #eee;
padding-left: 0%;
position: relative;
margin-left: 0%;
}


.members-section {
margin-top: 0%;
}




.logo-container {
display: flex;
justify-content: center;
align-items: center;
padding-top: 50px;

}

.logo {
width: 15vh;
height: 15vh;
object-fit: cover; /* rellena el espacio sin deformarse */
border-radius: 50%; /* círculo perfecto */
border: 3px solid #ffe100; /* color verde estilo pro, puedes cambiarlo */
background-color: #fff;
box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
box-shadow: 0 0 12px #ffe100;

}

}
@media (min-width: 769px) and (max-width: 900px) {
.team-leader {
max-width: 50vw;
min-width: 100vw;
font-family: 'Arial', sans-serif;
padding: 1rem;
background-image: url("../assets/imagenes/cancha.jpg"); 
background-repeat: no-repeat;
background-size: cover; /* Esto asegura que la imagen cubra todo el contenedor */
color: #fff;
border-radius: 10px;
color: black;
z-index:-6; /* Desenfoque de la imagen */
border: solid white;
}


.header {
text-align: center;
background-color: rgba(3, 0, 0, 0.822);
padding: 0rem;
border-radius: 10px;
color: white;
}



.logo-container {
display: flex;
justify-content: center;
align-items: center;
padding-top: 1rem;
padding-right: 0rem

}

.logo {
width: 50%;
height: 50%;
object-fit: cover; /* rellena el espacio sin deformarse */
border-radius: 50%; /* círculo perfecto */
border: 3px solid #ffe100; /* color verde estilo pro, puedes cambiarlo */
background-color: #fff;
box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
box-shadow: 0 0 12px #ffe100;

}

.epic-banner {
text-align: center;
padding: 1rem 5rem;
background-color: transparent;
max-width: 5%;
min-width: 10%;
}

.epic-name {
font-family:initial;
color: #ffffff; /* Dorado */
text-shadow:
  1px 1px 0 #000000,
  2px 2px 0 #ffcc00,
  3px 3px 4px #000;
letter-spacing: 0rem;
text-transform: uppercase;
padding-left: 1%;
padding-right: 10%;
font-size: 3rem;
}

.description {
font-size: 2.5rem;
color: #bcbcbc; /* más notorio que #ccc pero aún sutil */
font-style: italic;
margin-top: 0%;
border: solid transparent;
padding: 0rem 0rem;
font-family: Cambria, Cochin, Georgia, Times, 'Times New Roman', serif;
}


.miembros_style {
font-weight: bold;
font-size: 1rem;
color: #fff7f7;
border-top: solid white;
border-bottom: solid white;
padding: 0rem;
margin-top: 150%;
margin-right: 5rem;
}


.caja_hijo{
margin-left: 10rem; 
}


.chat-section {
margin-top: 0%;
padding: 2rem;
background-color: #000000;
border-radius: 10px;
}

.chat-box {
max-height: 80%;
max-width: 200%;
overflow-y: auto;
margin-bottom: 0%;
padding: 1rem;

}

.chat-message {
background-color: #1a1a1a;
border: 1px solid #333;
border-left: 4px solid transparent;
border-radius: 12px;
padding: 14px;
margin-bottom: 18px;
color: #fff;
position: relative;
box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
transition: all 0.3s ease;
cursor: pointer;
width: 100%;
/* 🛠 Estas líneas son clave para textos largos */
word-wrap: break-word;
white-space: pre-wrap;
overflow-wrap: break-word;
}

.chat-message:hover {
border-color: #d4af37; /* dorado */
border-left: 4px solid #d4af37;
background-color: #222;
transform: scale(1.015);
}

.message-header {
display: flex;
align-items: center;
margin-bottom: 5px;
}


.sender-name {
color: #ffffff; /* dorado */
font-weight: bold;
margin-right: 0%;
font-size: 15px;
}

.timestamp {
display: none;
}


.message-content {
font-size: 1rem;
color: #eee;
padding-left: 0%;
position: relative;
margin-left: 0%;
}


.members-section {
margin-top: 0%;
}




.logo-container {
display: flex;
justify-content: center;
align-items: center;
padding-top: 50px;

}

.logo {
width: 15vh;
height: 15vh;
object-fit: cover; /* rellena el espacio sin deformarse */
border-radius: 50%; /* círculo perfecto */
border: 3px solid #ffe100; /* color verde estilo pro, puedes cambiarlo */
background-color: #fff;
box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
box-shadow: 0 0 12px #ffe100;

}
}

@media (min-width: 1025px) and (max-width: 1440px) {

  




}
@media (min-width: 1441px) and (max-width: 1920px) {




}
@media (min-width: 1921px) and (max-width: 2560px) {




}
@media (min-width: 2561px) and (max-width: 3840px) {




}
@media (min-width: 3841px) and (max-width: 5120px) {




}


  
  </style>