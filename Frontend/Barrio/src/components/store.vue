<template>
    <header>
      <Headerapp></Headerapp>
    </header>
    <div class="store-container">
      <!-- Header -->
      <header class="store-header">
        <div class="logo">
          <h1>⚽ BarrioStore</h1>
        </div>
        <div class="search-bar">
          <input v-model="searchQuery" type="text" placeholder="Buscar productos..." />
          <button @click="searchProducts" class="search-btn">🔍</button>
        </div>
        <div class="icons">
          <span class="cart-icon" @click="toggleCart">🛒<span class="cart-count">{{ cart.length }}</span></span>
          <span class="favorites-icon" @click="toggleFavorites">❤️</span>
          <span class="settings-icon" @click="toggleSettings">⚙️</span>
        </div>
      </header>
  
      <!-- Configuración -->
      <div v-if="settingsVisible" class="overlay" @click="toggleSettings">
        <div class="settings-panel" @click.stop>
          <h2>Opciones de Cuenta</h2>
          <router-Link to="pay"><button class="btn">💰 Recargar Cuenta</button></router-Link>
          <router-Link to="pay"><button class="btn">📊 Ver Saldo</button></router-Link>
          <router-Link to="vendedor"><button class="btn">💸 Vender</button></router-Link>
          <button @click="toggleSettings" class="btn close-settings-btn">Cerrar</button>
        </div>
      </div>
  
      <!-- Carrito de Compras -->
      <div v-if="cartVisible" class="overlay" @click="toggleCart">
        <div class="cart-panel" @click.stop>
          <h2>Carrito de Compras</h2>
          <div v-if="cart.length > 0">
            <div v-for="(product, index) in cart" :key="product.id" class="cart-item">
              <img :src="product.image" :alt="product.name" />
              <div>{{ product.name }} - ${{ product.price }}</div>
              <button @click="removeFromCart(index)" class="btn remove-btn">Eliminar</button>
            </div>
          </div>
          <div v-else>
            <p>Tu carrito está vacío.</p>
          </div>
          <button @click="toggleCart" class="btn close-btn">Cerrar</button>
        </div>
      </div>
  
      <!-- Favoritos -->
      <div v-if="favoritesVisible" class="overlay" @click="toggleFavorites">
        <div class="favorites-panel" @click.stop>
          <h2>Favoritos</h2>
          <div v-if="favorites.length > 0">
            <div v-for="(product, index) in favorites" :key="product.id" class="favorite-item">
              <img :src="product.image" :alt="product.name" />
              <div>{{ product.name }} - ${{ product.price }}</div>
              <button @click="removeFromFavorites(index)" class="btn remove-btn">Eliminar</button>
            </div>
          </div>
          <div v-else>
            <p>No tienes favoritos.</p>
          </div>
          <button @click="toggleFavorites" class="btn close-btn">Cerrar</button>
        </div>
      </div>
  
      <!-- Overlay para mostrar más información sobre el producto -->
      <div v-if="selectedProduct" class="overlay" @click="selectedProduct = null">
        <div class="product-detail-panel" @click.stop>
          <img :src="selectedProduct.image" :alt="selectedProduct.name" class="product-detail-image" />
          <h2>{{ selectedProduct.name }}</h2>
          <p>{{ selectedProduct.description }}</p>
          <p class="price">${{ selectedProduct.price }}</p>
          <button @click="addToCart(selectedProduct)" class="btn action-btn">🛒 Comprar</button>
          <button @click="addToFavorites(selectedProduct)" class="btn action-btn">🖇️ Compartir Producto </button>
          <button @click="selectedProduct = null" class="btn close-btn">✘ Cerrar</button>
        </div>
      </div>
  
      <!-- Lista de Productos -->
      <div class="product-list">
        <div class="product-card" v-for="product in filteredProducts" :key="product.id">
          <div class="product-image">
            <img :src="product.image" :alt="product.name" @click="showProductDetail(product)" />
          </div>
          <div class="product-info">
            <h3>{{ product.name }}</h3>
            <p>{{ product.description }}</p>
            <p class="price">${{ product.price }}</p>
            <div class="actions">
              <button @click="addToCart(product)" class="btn action-btn">🛍️ Agregar al Carrito</button>
              <button @click="addToFavorites(product)" class="btn action-btn">❤️ Favorito</button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import Headerapp from './Headerapp.vue';
  import guayoimagen from '@/assets/imagenes/guayo.png'
  
  export default {
    components: {
      Headerapp
    },
    data() {
      return {
        searchQuery: '',
        cart: [],
        favorites: [],
        settingsVisible: false,
        cartVisible: false,
        favoritesVisible: false,
        selectedProduct: null,  // Nuevo estado para el producto seleccionado
        products: [
          { id: 1, name: 'Canilleras Nike', description: 'Protección máxima', price: 25, image: guayoimagen },
          { id: 2, name: 'Balón Adidas', description: 'Balón de alta calidad', price: 30, image: guayoimagen },
          { id: 3, name: 'Botines Puma', description: 'Máximo agarre y comodidad', price: 45, image: guayoimagen },
          { id: 4, name: 'Guantes de arquero Reusch', description: 'Protección para tus manos', price: 40, image: guayoimagen },
          { id: 5, name: 'Espinilleras Adidas', description: 'Protección ligera y duradera', price: 20, image: guayoimagen },
          { id: 6, name: 'Camiseta Nike', description: 'Transpirable y cómoda', price: 35, image: guayoimagen },
          { id: 7, name: 'Pantalones Nike', description: 'Comodidad para tus entrenamientos', price: 30, image: guayoimagen },
          { id: 8, name: 'Chaqueta Puma', description: 'Resistente al viento', price: 50, image: guayoimagen },
          { id: 9, name: 'Calcetines Nike', description: 'Comodidad y soporte', price: 15, image: guayoimagen },
          { id: 10, name: 'Mallas Under Armour', description: 'Comodidad y rendimiento', price: 28, image: guayoimagen },
          // ... otros productos
        ],
        filteredProducts: []
      };
    },
    methods: {
      addToCart(product) {
        this.cart.push(product);
      },
      removeFromCart(index) {
        this.cart.splice(index, 1);
      },
      addToFavorites(product) {
        if (!this.favorites.includes(product)) {
          this.favorites.push(product);
        }
      },
      removeFromFavorites(index) {
        this.favorites.splice(index, 1);
      },
      searchProducts() {
        this.filteredProducts = this.products.filter(p => p.name.toLowerCase().includes(this.searchQuery.toLowerCase()));
      },
      toggleSettings() {
        this.settingsVisible = !this.settingsVisible;
      },
      toggleCart() {
        this.cartVisible = !this.cartVisible;
      },
      toggleFavorites() {
        this.favoritesVisible = !this.favoritesVisible;
      },
      showProductDetail(product) {
        this.selectedProduct = product;
      },
    },
    watch: {
      searchQuery() {
        this.searchProducts();
      }
    },
    mounted() {
      this.filteredProducts = this.products;
    }
  };
  </script>
  
  <style scoped>
  
  /* Estilos para el overlay de producto */
  .overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 50%;
    height: 50%;
    background: rgba(0, 0, 0, 0.5);
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 999;
    margin-top: 5%;
  }
  
  .product-detail-panel {
    background: rgb(0, 0, 0);
    padding: 20px;
    border-radius: 8px;
    text-align: center;
    max-width: 500px;
    width: 100%;
  }
  
  .product-detail-image {
    width: 100%;
    max-width: 300px;
    margin-bottom: 20px;
    border-radius: 5%;
  }
  
  .close-btn {
    background-color: red;
    color: white;
    padding: 10px;
    border: none;
    border-radius: 5px;
    cursor: pointer;
  }
  
  .close-btn:hover {
    background-color: darkred;
  }
  /* Contenedor principal */
  .store-container {
    font-family: 'Inter', sans-serif;
    background-color: #121212;
    padding: 30px;
    color: #f5f5f5;
    margin-top: 18%;
  }
  
  /* Encabezado */
  .store-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    background: #1e1e1e;
    padding: 20px;
    border-radius: 15px;
    box-shadow: 0 4px 10px rgba(255, 255, 255, 0.1);
  }
  
  /* Barra de búsqueda */
  .search-bar {
    display: flex;
    align-items: center;
    gap: 12px;
  }
  
  .search-bar input {
    padding: 12px;
    border: none;
    border-radius: 8px;
    width: 280px;
    font-size: 14px;
    background: #333;
    color: white;
    outline: none;
  }
  
  .search-btn {
    background: #ffcc00;
    color: #1e1e1e;
    padding: 12px 15px;
    border: none;
    cursor: pointer;
    border-radius: 8px;
    font-size: 14px;
    transition: background 0.3s, transform 0.2s;
  }
  
  .search-btn:hover {
    background: #ffaa00;
    transform: scale(1.1);
  }
  
  /* Íconos */
  .icons {
    display: flex;
    gap: 20px;
  }
  
  .icons span {
    font-size: 1.8rem;
    cursor: pointer;
    transition: transform 0.2s;
  }
  
  .icons span:hover {
    transform: scale(1.15);
    color: #ffcc00;
  }
  
  /* Lista de productos */
  .product-list {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 30px;
    margin-top: 30px;
  }
  
  /* Tarjeta de producto */
  .product-card {
    background: #1e1e1e;
    padding: 20px;
    border-radius: 20px;
    box-shadow: 0 6px 15px rgba(255, 255, 255, 0.05);
    text-align: center;
    transition: transform 0.3s, box-shadow 0.3s;
  }
  
  .product-card:hover {
    transform: translateY(-8px);
    box-shadow: 0 10px 20px rgba(255, 255, 255, 0.08);
  }
  
  .product-card img {
    max-width: 100%;
    border-radius: 15px;
  }
  
  /* Botones de acción */
  .actions {
    display: flex;
    justify-content: center;
    gap: 12px;
    margin-top: 15px;
  }
  
  .actions button {
    padding: 14px 18px;
    background: #ffcc00;
    color: #1e1e1e;
    border: none;
    cursor: pointer;
    border-radius: 10px;
    font-weight: bold;
    transition: background 0.3s, transform 0.2s;
  }
  
  .actions button:hover {
    background: #ffaa00;
    transform: scale(1.08);
  }
  
  /* Panel de configuraciones */
  .settings-panel {
    position: fixed;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    background: #1e1e1e;
    padding: 25px;
    border-radius: 12px;
    box-shadow: 0 6px 15px rgba(255, 255, 255, 0.08);
    width: 280px;
    z-index: 1000;
  }
  
  .btn {
    background: #ffcc00;
    color: #1e1e1e;
    padding: 12px 15px;
    border: none;
    width: 100%;
    margin-bottom: 10px;
    cursor: pointer;
    border-radius: 8px;
    font-size: 14px;
    transition: background 0.3s;
  }
  
  .btn:hover {
    background: #ffaa00;
  }
  
  .close-settings-btn {
    background: #e74c3c;
  }
  
  .close-settings-btn:hover {
    background: #c0392b;
  }
  
  /* Panel de carrito */
  .cart-panel, .favorites-panel {
    position: fixed;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    background: #1e1e1e;
    padding: 25px;
    border-radius: 12px;
    box-shadow: 0 6px 15px rgba(255, 255, 255, 0.08);
    width: 300px;
    max-height: 80%;
    overflow-y: auto;
    z-index: 1000;
  }
  
  /* Overlay */
  .overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0, 0, 0, 0.7);
    z-index: 999;
  }
  
  /* Botón de cerrar */
  .close-btn {
    background: #e74c3c;
  }
  
  .close-btn:hover {
    background: #c0392b;
  }
  
  /* Productos en carrito */
  .cart-item, .favorite-item {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 10px 0;
  }
  
  .cart-item img, .favorite-item img {
    width: 50px;
    height: 50px;
    margin-right: 15px;
  }
  
  /* Botón eliminar */
  .remove-btn {
    background: #ff4d4d;
    color: white;
    padding: 8px 12px;
    border-radius: 6px;
    cursor: pointer;
    transition: background 0.3s;
  }
  
  .remove-btn:hover {
    background: #e74c3c;
  }
  
  
  /* Responsive*/
  
  /* Panel responsivo */
  @media (max-width: 768px) {
    .store-container {
      padding: 15px;
      margin-top: 10%;
    }
  
    .store-header {
      flex-direction: column;
      align-items: center;
      text-align: center;
      gap: 15px;
    }
  
    .search-bar {
      width: 100%;
      justify-content: center;
    }
  
    .search-bar input {
      width: 100%;
    }
  
    .product-list {
      grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    }
  
    .actions {
      flex-direction: column;
      align-items: center;
    }
  
    .actions button {
      width: 100%;
    }
  
    .icons {
      justify-content: center;
    }
  }
  
  @media (max-width: 480px) {
    .store-container {
      margin-top: 72%;
      padding: 10px;
    }
  
    .product-list {
      grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
    }
  
    .product-card {
      padding: 15px;
    }
  
    .search-bar {
      flex-direction: column;
      gap: 8px;
    }
  
    .search-btn {
      width: 100%;
    }
  }
  </style>