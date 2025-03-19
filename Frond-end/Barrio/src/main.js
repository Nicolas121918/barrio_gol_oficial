import './assets/main.css'
import { createApp } from 'vue'
import App from './App.vue'
import router from '../src/rutas/rutas'
import { createPinia } from 'pinia'
import piniaPersistedState from 'pinia-plugin-persistedstate' // Importa el plugin

const pinia = createPinia();
pinia.use(piniaPersistedState); // Activa la persistencia en Pinia

createApp(App)
  .use(router)
  .use(pinia)
  .mount('#root')
  
