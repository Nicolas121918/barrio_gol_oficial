<template>
  <header>
    <Headerapp />
  </header>
  <div>
    <div class="padre">
      <button class="botones_" @click="$router.go(-1)">Volver</button>
      <h1>GALERÍA DE EQUIPO</h1>

      <!-- Barra de búsqueda -->
      <div class="caja">
        <div v-if="!isUploading">
          <input
            class="buscador"
            type="text"
            v-model="searchQuery"
            placeholder="Buscar por descripción o usuario"
            @input="applyFilters"
          />
        </div>
      </div>

      <!-- Botón para subir publicación -->
      <button class="botones_2" v-if="!isUploading" @click="startUpload">
        Subir Publicación
      </button>

      <!-- Formulario para subir archivo -->
      <div v-if="isUploading">
        <div class="children">
          <label>
            <input type="radio" value="video" v-model="selectedMediaType" />
            Subir Video
          </label>
          <label>
            <input type="radio" value="image" v-model="selectedMediaType" />
            Subir Imagen
          </label>
          <button class="botones_2" @click="cancelUpload">Volver</button>
        </div>

        <div class="caja_video" v-if="selectedMediaType">
          <h3>
            Seleccionaste:
            {{ selectedMediaType === "video" ? "Video" : "Imagen" }}
          </h3>
          <br />
          <input
            type="file"
            :accept="selectedMediaType === 'video' ? 'video/*' : 'image/*'"
            @change="handleFileUpload"
          />
          <br />
          <textarea
            v-model="description"
            placeholder="Descripción de la publicación"
          ></textarea>
          <button class="botones_" @click="uploadPost">Subir</button>
        </div>
      </div>

      <!-- Tarjetas de publicaciones -->
      <div v-if="!isUploading && filteredPosts.length" class="card-container">
        <div v-for="(post, index) in filteredPosts" :key="index" class="card">
          <div class="card-header">
            <button @click="openModal(index)">&#x22EE;</button>
          </div>

          <div class="card-body">
            <div v-if="post.mediaType === 'video'">
              <video
                :src="post.media"
                controls
                class="media"
                @click="enlargeMedia(post)"
              ></video>
            </div>
            <div v-else-if="post.mediaType === 'image'">
              <img
                :src="post.media"
                alt="imagen"
                class="media"
                @click="enlargeMedia(post)"
              />
            </div>
          </div>
          <div class="card-footer">
            <p>{{ post.description }}</p>
          </div>
        </div>
      </div>

      <!-- Modal para confirmación de eliminación -->
      <div v-if="showModal" class="modal">
        <div class="modal-content">
          <p class="letra">
            ¿Estás seguro de que deseas eliminar esta publicación?
          </p>
          <button class="eliminar" @click="deletePost(modalIndex)">
            Eliminar
          </button>
          <button @click="closeModal">Cancelar</button>
        </div>
      </div>

      <!-- Modal para ampliar imagen o video -->
      <div v-if="showMediaModal" class="modal">
        <div class="modal-content">
          <div v-if="currentMedia.mediaType === 'video'">
            <video
              :src="currentMedia.media"
              controls
              autoplay
              class="enlarged-media"
            ></video>
          </div>
          <div v-else-if="currentMedia.mediaType === 'image'">
            <img
              :src="currentMedia.media"
              alt="imagen ampliada"
              class="enlarged-media"
            />
          </div>
          <button class="botones_2" @click="closeMediaModal">Cerrar</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import Headerapp from "./Headerapp.vue";
import axios from "axios";
import { useUsuarios } from "@/stores/usuario";


export default {
  components: {
    Headerapp,
  },
  data() {
    
    return {
  Galeria : [],
      isUploading: false,
      selectedMediaType: null,
      description: "",
      mediaFile: null,
      posts: [],
      searchQuery: "",
      filteredPosts: [],
      showModal: false,
      modalIndex: null,
      showMediaModal: false,
      currentMedia: {},
    };
  },
  mounted() {
    this.getGaleria();
    
  },
  methods: {
    
    getGaleria() {
  const usuariosStore = useUsuarios();
  const idTeam = usuariosStore.usuario.equipo_tiene;


  if (!idTeam) {
    console.error("No se encontró un equipo asignado.");
    return;
  }

  axios
    .get(`http://localhost:8000/galeria/${idTeam}`)
    .then((response) => {

      // Mapea los datos del backend al formato esperado por el frontend
      this.posts = response.data.map((post) => {
  const mediaUrl = `http://localhost:8000${post.archivo_url}`;
  console.log("URL generada para media:", mediaUrl);
  return {
    mediaType: post.tipo_media === "imagen" ? "image" : post.tipo_media, // Ajusta "imagen" a "image"
    media: mediaUrl,
    description: post.descripcion,
    id: post.id,
    idTeam: post.id_team,
  };
});

      console.log("Posts después de mapear:", this.posts); // Verifica los datos mapeados
      this.applyFilters(); // Aplica los filtros iniciales
    })
    .catch((err) => {
      console.error("Error al obtener las publicaciones:", err);
      alert("Error al cargar las publicaciones");
    });
},
    
    startUpload() {
      this.isUploading = true;
    },
    cancelUpload() {
      this.resetUpload();
    },
    resetUpload() {
      this.isUploading = false;
      this.selectedMediaType = null;
      this.description = "";
      this.mediaFile = null;
    },
    handleFileUpload(event) {
      this.mediaFile = event.target.files[0];
    },
    uploadPost() {
      const usuariosStore = useUsuarios();
      const idTeam = usuariosStore.usuario.equipo_tiene;

      if (!this.mediaFile || !this.description || !this.selectedMediaType || !idTeam) {
        alert("Completa todos los campos y asegúrate de tener equipo asignado");
        return;
      }

      const formData = new FormData();
      formData.append("id_team", idTeam);
      formData.append("descripcion", this.description);
      formData.append("tipo_media", this.selectedMediaType === "video" ? "video" : "imagen");
      formData.append("archivo", this.mediaFile);

      axios
        .post("http://localhost:8000/galeria/subir", formData)
        .then(() => {
          alert("Publicación subida exitosamente");
          this.getGaleria();
          this.resetUpload();
        })
        .catch((err) => {
          console.error(err);
          alert("Error al subir publicación");
        });
    },
    applyFilters() {
      this.filteredPosts = this.posts.filter(
        (post) =>
          (!this.filterType || post.mediaType === this.filterType) &&
          (post.description.toLowerCase().includes(this.searchQuery.toLowerCase()) ||
            post.userName.toLowerCase().includes(this.searchQuery.toLowerCase()))
      );
    },
    openModal(index) {
      this.modalIndex = index;
      this.showModal = true;
    },
    closeModal() {
      this.showModal = false;
      this.modalIndex = null;
    },
    deletePost(index) {
      const post = this.filteredPosts[index];

      axios
        .delete(`http://localhost:8000/galeria/${post.id}`)
        .then(() => {
          alert("Publicación eliminada");
          this.getGaleria();
          this.closeModal();
        })
        .catch((err) => {
          console.error(err);
          alert("Error al eliminar");
        });
    },
    enlargeMedia(post) {
      this.currentMedia = post;
      this.showMediaModal = true;
    },
    closeMediaModal() {
      this.showMediaModal = false;
      this.currentMedia = {};
    },
  },
};
</script>

  
  <style scoped>
  .padre{
    background-color: black;
    border: solid white;
    box-shadow: white 0 0 30px;
    margin-top: 15%;
    min-width: 1000px;
  }
  .card-container {
    display: flex;
    flex-wrap: wrap;
    gap: 20px;
    justify-content: center;
  }
  .card {
    color: black;
    font-family:Cambria, Cochin, Georgia, Times, 'Times New Roman', serif;
    border: 1px solid #ddd;
    font-size: 120%;
    margin: 10px;
    padding: 10px;
    width: 300px;
    box-sizing: border-box;
    background-image: url("https://st4.depositphotos.com/9899294/37915/i/450/depositphotos_379158544-stock-photo-gold-golden-beautiful-metallic-polished.jpg")
  }
  .card-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    color: white;
    text-shadow: 0 0 10px black;
    font-size: 130%;
  }
  .children{
    display: flex;
    flex-direction: column;
    align-items: center;
    font-size: 140%;
  }
  .user-logo {
    width: 40px;
    height: 40px;
    border-radius: 50%;
  }
  .card-body {
    margin-top: 10px;
  }
  .card-footer {
    margin-top: 10px;
    font-size: 14px;
  }
  .caja_video{
    padding: 10%;
    display: flex;
    flex-direction: column;
    align-items: center;
    font-size: 150%;
    gap: 20%;
    color: white;
  }
  .eliminar{
    background-color: red;
    color: white;
    margin-right: 20%;
    width: 20%;
    height: 30%;
  }
  .media {
    width: 100%;
    height: 200px;
    object-fit: cover;
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
    padding: 20px;
    border-radius: 5px;
    text-align: center;
    color: rgb(255, 255, 255);
    background-color: white;
  
  }
  .enlarged-media {
    max-width: 100%;
    max-height: 100%;
    object-fit: contain;
  }
  .caja{
    display: flex;
    flex-direction:row;
    gap: 50%;
    padding: 1%;
    justify-content: center;
  }
  .letra{
    font-family: 400%;
    color: rgb(0, 0, 0);
  }
  h1 {
    text-align: center;
    font-family: 'Georgia', serif; /* Fuente más formal */
    font-size: 3rem; /* Tamaño grande */
    font-weight: bold; /* Negrita */
    color: #fdfeff; /* Color claro para el texto */
    text-shadow: 2px 2px 5px rgba(0, 0, 0, 0.2); /* Sombra sutil */
    padding: 20px; /* Espaciado interno */
    letter-spacing: 2px; /* Espaciado entre letras */
    position: relative; /* Posicionamiento relativo para usar con el borde / / Borde negro alrededor del texto */
    -webkit-background-clip: text; /* Permite ver el fondo a través del borde del texto */
    background-clip: text; /* Soporte cruzado para todos los navegadores */
    text-decoration: underline;
  }
  .botones_ {
    background-image: url("https://static.vecteezy.com/system/resources/thumbnails/000/549/015/small/vector-apr-2018-19.jpg"); /* Fondo morado */
    color: white; /* Color del texto blanco */
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; /* Fuente más moderna y elegante */
    font-size: 1.1rem; /* Tamaño de fuente ligeramente mayor */
    font-weight: 600; /* Peso de fuente intermedio para un toque sofisticado */
    padding: 14px 28px; /* Más espaciado interno para un botón más grande */
    border: 2px solid transparent; /* Borde inicial transparente */
    border-radius: 50px; /* Bordes redondeados extremos para un efecto de píldora */
    text-transform: uppercase; /* Convierte el texto a mayúsculas */
    letter-spacing: 1px; /* Espaciado entre las letras para un toque elegante */
    cursor: pointer; /* Cambio de cursor a mano */
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2); /* Sombra sutil para profundidad */
    transition: all 0.3s ease; /* Transición suave para todos los cambios */
  }
  
  .botones_:hover {
    background-color: #9b59b6; /* Fondo morado más claro al pasar el ratón */
    border-color: #fff; /* Borde blanco al pasar el ratón */
    transform: translateY(-4px); /* Eleva el botón ligeramente al pasar el ratón */
  }
  
  .botones_:active {
    background-color: #8e44ad; /* Fondo original morado oscuro al hacer clic */
    transform: translateY(2px); /* Desplazamiento hacia abajo al hacer clic */
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2); /* Sombra más pequeña al hacer clic */
  }
  .buscador {
    width: 140%; /* El input ocupará todo el ancho disponible */
    max-width: 400px; /* Límite de ancho máximo para que no se haga demasiado grande */
    padding: 12px 20px; /* Espaciado interno para que el texto no toque los bordes */
    border: 2px solid #8e44ad; /* Borde morado para que destaque */
    border-radius: 30px; /* Bordes redondeados para un estilo suave */
    font-size: 1rem; /* Tamaño de texto cómodo */
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; /* Fuente moderna y clara */
    color: #555; /* Color de texto gris oscuro */
    background-color: #f9f9f9; /* Fondo gris claro */
    outline: none; /* Elimina el contorno de selección predeterminado */
    transition: all 0.3s ease; /* Transición suave para interacciones */
  }
  
  .buscador:focus {
    border-color: #3498db; /* Cambia el borde a azul cuando se hace focus */
    background-color: #fff; /* Cambia el fondo a blanco cuando se hace focus */
    box-shadow: 0 0 5px rgba(52, 152, 219, 0.6); /* Añade una sombra suave de enfoque */
  }
  
  .buscador::placeholder {
    color: #aaa; /* Color gris claro para el texto de placeholder */
    font-style: italic; /* Estilo itálico para el texto de placeholder */
  }
  
  .botones_2 {
    background-color: #0ce1fd; /* Fondo morado */
    color: rgb(0, 0, 0); /* Color del texto blanco */
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; /* Fuente más moderna y elegante */
    font-size: 120%; /* Tamaño de fuente ligeramente mayor */
    font-weight: 600; /* Peso de fuente intermedio para un toque sofisticado */
    padding: 10px; /* Más espaciado interno para un botón más grande */
    border: 2px solid transparent; /* Borde inicial transparente */
    text-transform: uppercase; /* Convierte el texto a mayúsculas */
    letter-spacing: 1px; /* Espaciado entre las letras para un toque elegante */
    cursor: pointer; /* Cambio de cursor a mano */
    box-shadow: 0 0px 30px rgba(255, 255, 255, 0.486); /* Sombra sutil para profundidad */
    transition: all 0.3s ease; /* Transición suave para todos los cambios */
    margin: 1%;
    border-radius: 40px;
    width: 20%;
  }
  
  .botones_2:hover {
    background-color: #0b41b6; /* Fondo morado más claro al pasar el ratón */
    border-color: #fff; /* Borde blanco al pasar el ratón */
    transform: translateY(-4px); /* Eleva el botón ligeramente al pasar el ratón */
    color: white;
  }
  
  .botones_2:active {
    background-color: #fcfcfc; /* Fondo original morado oscuro al hacer clic */
    transform: translateY(2px); /* Desplazamiento hacia abajo al hacer clic */
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2); /* Sombra más pequeña al hacer clic */
  }
  p{
    text-align: center;
    font-size: 120%;
  }
  p.letra{
    color: rgb(0, 0, 0);
    font-family: Georgia, 'Times New Roman', Times, serif;
    font-size: 150%;
  }
  </style>