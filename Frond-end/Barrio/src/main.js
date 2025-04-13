import 'leaflet/dist/leaflet.css'; // ✅ Esto es lo que hace falta para que se vea el mapa
import { createApp } from 'vue';
import App from './App.vue';
import router from '../src/rutas/rutas';
import { createPinia } from 'pinia';
import piniaPersistedState from 'pinia-plugin-persistedstate';

const pinia = createPinia();
pinia.use(piniaPersistedState);

createApp(App)
  .use(router)
  .use(pinia)
  .mount('#root');
