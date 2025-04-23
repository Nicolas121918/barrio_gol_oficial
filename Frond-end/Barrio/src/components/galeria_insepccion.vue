
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
        <div>
          <input
            class="buscador"
            type="text"
            v-model="searchQuery"
            placeholder="Buscar por descripción"
            @input="applyFilters"
          />
        </div>
      </div>

      <!-- Tarjetas de publicaciones -->
      <div v-if="filteredPosts.length" class="card-container">
        <div v-for="(post, index) in filteredPosts" :key="index" class="card">
          <div class="card-header">
            <!-- Sin botón de opciones -->
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
      Galeria: [],
      posts: [],
      searchQuery: "",
      filteredPosts: [],
      showMediaModal: false,
      currentMedia: {},
    };
  },
  mounted() {
    this.getGaleria();
  },
  methods: {
    getGaleria() {
      // Aquí deberías recibir el idTeam como prop o parámetro, ya que no hay usuario logueado con equipo
      // Por ejemplo, podrías recibirlo como prop: this.$props.idTeam
      // Aquí lo dejo como ejemplo:
      const idTeam = this.$route.params.id; // O como lo manejes en tu router

      if (!idTeam) {
        console.error("No se encontró un equipo para inspeccionar.");
        return;
      }

      axios
        .get(`http://localhost:8000/galeria/${idTeam}`)
        .then((response) => {
          this.posts = response.data.map((post) => {
            const mediaUrl = `http://localhost:8000${post.archivo_url}`;
            return {
              mediaType: post.tipo_media === "imagen" ? "image" : post.tipo_media,
              media: mediaUrl,
              description: post.descripcion,
              id: post.id,
              idTeam: post.id_team,
            };
          });
          this.applyFilters();
        })
        .catch((err) => {
          console.error("Error al obtener las publicaciones:", err);
          alert("Error al cargar las publicaciones");
        });
    },
    applyFilters() {
      this.filteredPosts = this.posts.filter(
        (post) =>
          post.description.toLowerCase().includes(this.searchQuery.toLowerCase())
      );
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
      width: 40%;
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