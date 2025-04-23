<template>
  <header>
    <Headerapp></Headerapp>

  </header>
    <div class="seller-container">
      <h1 class="title">BarrioShop 🏆</h1>
      <div class="tabs">
        <button @click="currentTab = 'ventas'" :class="{ active: currentTab === 'ventas' }">Ventas del mes</button>
        <button @click="currentTab = 'estadisticas'" :class="{ active: currentTab === 'estadisticas' }">Estadísticas</button>
        <button @click="currentTab = 'mensajes'" :class="{ active: currentTab === 'mensajes' }">Mensajes</button>
        <button @click="currentTab = 'configuracion'" :class="{ active: currentTab === 'configuracion' }">Configuración</button>
      </div>
  
      <!-- Sección de publicaciones -->
      <div v-if="currentTab === 'ventas'" class="form-container">
        <h2>Publicar Artículo</h2>
        <form @submit.prevent="addItem">
          <input v-model="name" type="text" placeholder="Nombre del artículo" class="input" />
          <select v-model="category" class="input">
            <option disabled value="">Selecciona categoría</option>
            <option value="fútbol">Fútbol</option>
            <option value="baloncesto">Baloncesto</option>
            <option value="ciclismo">Ciclismo</option>
            <option value="tenis">Tenis</option>
          </select>
          <input v-model="priceCOP" type="number" placeholder="Precio en COP" class="input" />
          <select v-model="condition" class="input">
            <option value="">Selecciona condición</option>
            <option value="nuevo">Nuevo</option>
            <option value="usado">Usado</option>
          </select>
          <input type="file" @change="previewImage" class="input" />
          <div v-if="imagePreview" class="image-preview">
            <img :src="imagePreview" alt="Vista previa" class="small-thumbnail" />
          </div>
          <textarea v-model="description" placeholder="Descripción adicional" class="input"></textarea>
          <button type="submit" class="btn">Publicar</button>
        </form>
  
        <div class="items-container" v-if="filteredItems.length">
          <h2 class="subtitle">Artículos Disponibles</h2>
          <div class="items-grid">
            <div v-for="(item, index) in filteredItems" :key="index" class="item-card">
              <div class="item-image" :style="{ backgroundImage: 'url(' + item.image + ')' }"></div>
              <div class="item-details">
                <h3>{{ item.name }}</h3>
                <p class="category">{{ item.category }}</p>
                <p class="condition">{{ item.condition }}</p>
                <p class="price">Precio: ${{ item.priceCOP }} COP ({{ convertToUSD(item.priceCOP) }} USD)</p>
                <p class="description">{{ item.description }}</p>
              </div>
              <button @click="removeItem(index)" class="btn-delete">Eliminar</button>
              <button @click="editItem(index)" class="btn-edit">Editar</button>
              <!-- Botón para marcar el artículo como vendido -->
              <button v-if="!item.sold" @click="markAsSold(index)" class="btn-sold">Marcar como Vendido</button>
            </div>
          </div>
        </div>
        <p v-else class="empty">No has publicado ningún artículo aún.</p>
      </div>
  
      <!-- Sección de estadísticas -->
      <div v-if="currentTab === 'estadisticas'" class="statistics-container">
        <h2>Estadísticas</h2>
        <p>Aquí puedes ver las estadísticas de tus ventas, como las ganancias mensuales, el número de artículos vendidos, etc.</p>
  
        <!-- Indicador de dinero -->
        <div class="money-ball">
          <span class="money-text">Dinero ganado: ${{ totalMoney }} COP</span>
        </div>
        
        <!-- Artículos vendidos -->
        <div v-if="soldItems.length">
          <h3>Artículos Vendidos</h3>
          <div class="items-grid">
            <div v-for="(item, index) in soldItems" :key="index" class="item-card">
              <div class="item-image" :style="{ backgroundImage: 'url(' + item.image + ')' }"></div>
              <div class="item-details">
                <h3>{{ item.name }}</h3>
                <p class="category">{{ item.category }}</p>
                <p class="condition">{{ item.condition }}</p>
                <p class="price">Precio: ${{ item.priceCOP }} COP ({{ convertToUSD(item.priceCOP) }} USD)</p>
                <p class="description">{{ item.description }}</p>
              </div>
            </div>
          </div>
        </div>
        <p v-else>No has vendido ningún artículo aún.</p>
      </div>
  
      <!-- Sección de mensajes -->
      <div v-if="currentTab === 'mensajes'" class="messages-container">
        <h2>Mensajes de Clientes</h2>
        <p>Aquí puedes ver los mensajes de los clientes interesados en tus artículos.</p>
      </div>
  
      <!-- Sección de configuración -->
      <div v-if="currentTab === 'configuracion'" class="config-container">
        <h2>Configuración de la Cuenta</h2>
        <form @submit.prevent="updateProfile">
          <input v-model="sellerName" type="text" placeholder="Nombre de vendedor" class="input" />
          <input v-model="email" type="email" placeholder="Correo electrónico" class="input" />
          <input v-model="phone" type="text" placeholder="Número de teléfono" class="input" />
          <textarea v-model="sellerDescription" placeholder="Descripción del vendedor" class="input"></textarea>
          <button type="submit" class="btn">Actualizar Datos</button>
        </form>
      </div>
    </div>
  </template>
  
  <script>
  import { ref, computed } from 'vue';
import Headerapp from './Headerapp.vue';
  
  export default {
  components:{
    Headerapp

  },
    setup() {
      const currentTab = ref('ventas');
      const name = ref('');
      const category = ref('');
      const priceCOP = ref('');
      const condition = ref('');
      const image = ref(null);
      const description = ref('');
      const items = ref([]);
      const soldItems = ref([]);
      const imagePreview = ref(null);
      const searchQuery = ref('');
      const sellerName = ref('');
      const email = ref('');
      const phone = ref('');
      const sellerDescription = ref('');
      const totalMoney = ref(0);  // Total de dinero ganado
  
      const conversionRate = 5000;
  
      const convertToUSD = (copPrice) => {
        return (copPrice / conversionRate).toFixed(2);
      };
  
      const previewImage = (event) => {
        const file = event.target.files[0];
        if (file) {
          const reader = new FileReader();
          reader.onload = (e) => {
            imagePreview.value = e.target.result;
          };
          reader.readAsDataURL(file);
          image.value = file;
        }
      };
  
      const addItem = () => {
        if (name.value && category.value && priceCOP.value && condition.value && image.value && description.value) {
          const newItem = {
            name: name.value,
            category: category.value,
            priceCOP: priceCOP.value,
            condition: condition.value,
            image: URL.createObjectURL(image.value),
            description: description.value,
            sold: false,  // Nuevo campo para marcar si el artículo está vendido
          };
          items.value.push(newItem);
          name.value = category.value = priceCOP.value = condition.value = image.value = description.value = '';
          imagePreview.value = null;
        }
      };
  
      const removeItem = (index) => {
        items.value.splice(index, 1);
      };
  
      const editItem = (index) => {
        const item = items.value[index];
        name.value = item.name;
        category.value = item.category;
        priceCOP.value = item.priceCOP;
        description.value = item.description;
        condition.value = item.condition;
        items.value.splice(index, 1); 
      };
  
      const updateProfile = () => {
        alert('Datos del vendedor actualizados');
      };
  
      const markAsSold = (index) => {
        const soldItem = items.value[index];
        soldItem.sold = true; // Marcar el artículo como vendido
        soldItems.value.push(soldItem); // Añadirlo a la lista de artículos vendidos
        totalMoney.value += soldItem.priceCOP;  // Aumentar el dinero ganado
        items.value.splice(index, 1); // Eliminarlo de la lista de artículos disponibles
      };
  
      const filteredItems = computed(() => {
        return items.value.filter(item => 
          item.name.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
          item.category.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
          item.description.toLowerCase().includes(searchQuery.value.toLowerCase())
        );
      });
  
      return {
        currentTab,
        name,
        category,
        priceCOP,
        condition,
        image,
        description,
        items,
        soldItems,
        imagePreview,
        searchQuery,
        sellerName,
        email,
        phone,
        sellerDescription,
        totalMoney,
        convertToUSD,
        previewImage,
        addItem,
        removeItem,
        editItem,
        updateProfile,
        markAsSold,
        filteredItems,
      };
    },
  };
  </script>
<style scoped>
/* Estilos para mejorar la interfaz */
.seller-container {
  max-width: 850px;
  margin: auto;
  padding: 40px;
  background-color: #2f2f2f;
  border-radius: 12px;
  box-shadow: 0 8px 15px rgba(0, 0, 0, 0.1);
  font-family: 'Arial', sans-serif;
  color: #fff;
  margin-top: 20%;
}

.title {
  text-align: center;
  font-size: 2.5rem;
  color: #fff;
  margin-bottom: 20px;
}

/* Estilo para las pestañas */
.tabs {
  display: flex;
  justify-content: space-around;
  margin-bottom: 20px;
}

.tabs button {
  padding: 12px;
  background-color: #444;
  border: none;
  color: #fff;
  font-size: 1rem;
  border-radius: 6px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.tabs button:hover {
  background-color: #007bff;
}

.tabs .active {
  background-color: #007bff;
}

/* Estilo para las secciones */
.form-container, .statistics-container, .messages-container, .config-container {
  margin-top: 20px;
}

/* Estilo de los campos de entrada */
.input {
  width: 100%;
  padding: 12px;
  margin: 12px 0;
  border: 1px solid #ddd;
  border-radius: 6px;
  font-size: 1rem;
  background-color: #444;
  color: #fff;
}

.input:focus {
  outline: none;
  border-color: #007bff;
}

/* Estilo del botón */
.btn {
  width: 100%;
  padding: 15px;
  background-color: #007bff;
  color: white;
  font-size: 1.1rem;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.btn:hover {
  background-color: #0056b3;
}

.items-container {
  margin-top: 40px;
}

/* Ajustes de la rejilla para hacerla responsive */
.items-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
}

.item-card {
  background-color: #333;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
}

/* Ajuste de las imágenes dentro de las tarjetas */
.item-image {
  height: 200px;
  background-size: cover;
  background-position: center;
  margin-bottom: 10px;
  border-radius: 6px;
}

.item-details {
  margin-bottom: 10px;
}

.btn-delete, .btn-edit {
  background-color: #e60000;
  color: #fff;
  padding: 8px 16px;
  margin: 5px;
  border: none;
  border-radius: 6px;
  cursor: pointer;
}

.btn-delete:hover, .btn-edit:hover {
  background-color: #d50000;
}

.empty {
  text-align: center;
  color: #aaa;
}

/* Vista previa de la imagen */
.image-preview {
  margin-top: 10px;
  max-height: 200px;
  overflow: hidden;
}

.image-preview img {
  width: 20%;
  height: auto;
  border-radius: 6px;
}

.subtitle {
  font-size: 1.5rem;
  color: #fff;
}

.category, .condition, .price {
  font-size: 1rem;
  margin: 10px 0;
}

.category {
  font-weight: bold;
}

.condition {
  color: #ff6b00;
}

.price {
  font-size: 1.2rem;
  font-weight: bold;
}

/* Media Queries para Responsividad */
@media (max-width: 768px) {
  .title {
    font-size: 2rem;
  }
  .seller-container {
  margin-top: 40%;
}


  .tabs button {
    font-size: 0.9rem;
    padding: 10px;
  }

  .input, .btn {
    font-size: 0.9rem;
    padding: 10px;
  }

  .items-grid {
    grid-template-columns: 1fr 1fr;
  }

  .item-card {
    padding: 15px;
  }

  .item-image {
    height: 180px;
  }
}

@media (max-width: 480px) {
  .title {
    font-size: 1.7rem;
  }

  .tabs {
    flex-direction: column;
    align-items: center;
  }

  .tabs button {
    width: 100%;
    margin-bottom: 10px;
  }

  .items-grid {
    grid-template-columns: 1fr;
  }

  .input, .btn {
    font-size: 0.9rem;
    padding: 10px;
  }

  .item-image {
    height: 150px;
  }
  .seller-container {
  margin-top: 55%;
}
}

</style>
