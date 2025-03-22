import AboutUs from "@/components/AboutUs.vue";
import iniciosesion from "@/components/Iniciosesion.vue";
import Perfil from "@/components/Perfil.vue";
import Videohome from "@/components/videohome.vue";
import actualizar_perfil from "@/components/actualizar_perfil.vue";
import home from "@/components/home.vue";
import Contacto from "@/components/Contacto.vue";
import equipo from "@/components/equipo.vue";
import Eventos from "@/components/Eventos.vue";
import subir_video from "@/components/subir_video.vue";
import Notificaciones from "@/components/Notificaciones.vue";
import Formulario_join from "@/components/Formulario_join.vue";
import crearequipo from "@/components/crearequipo_form.vue";
import Diego from "@/components/diego.vue";
import crearpartido from "@/components/crearpartido.vue";
import diegos from "@/components/diegos.vue";
import { createRouter,createWebHistory } from "vue-router";
import Torneos_guardado from "@/components/torneos_guardado.vue";
import Torneos_creados from "@/components/torneos_creados.vue";
import Perfiles from "@/components/perfiles.vue";
import Jugadores from "@/components/jugadores.vue";
import Invitar from "@/components/invitar.vue";
import Videos from "@/components/videos.vue";
import Pagos from "@/components/pagos.vue";
import Torneoscreador from "@/components/torneoscreador.vue";
import ganadortorneo from "@/components/ganadortorneo.vue";
import jugadorestorneo from "@/components/jugadorestorneo.vue";
import targetas from "@/components/targetas.vue";
import Galeria from "@/components/galeria.vue";
import tienda from "@/components/test.vue";
import Calendario from "@/components/calendario.vue";
import Vender from "@/components/vender.vue";
import Creartorneo from "@/components/creartorneo.vue";
import One_video from "@/components/one_video.vue";
import Store from "@/components/store.vue";





const routes=[
    {
        path: '/contactanos',
        name: 'contactanos',
        component: AboutUs,
        
      },
      {
        path: '/videohome',
        name: 'videohome',
        component: Videohome,
        
      },
      {
        path: '/iniciosesion',
        name: 'iniciosesion',
        component: iniciosesion,
        
      },
      {
        path: '/Perfil',
        name: 'Perfil',
        component: Perfil,
        
      },
      {
        path: '/actualizar_perfil',
        name: 'actualizar_perfil',
        component: actualizar_perfil,
        
      },
      {
        path: '/home',
        name: 'home',
        component: home,
        
      },
      {
        path: '/contacto',
        name: 'contacto',
        component: Contacto,
        
      },
      {
        path: '/torneos',
        name: 'torneos',
        component: Eventos,
        
      },
      {
        path: '/equipos',
        name: 'equipos',
        component: equipo,
        
      },
      {
      path: "/one_video/:id",
      name: "One_Video",
      component: One_video
    },
      {
        path: '/videos',
        name: 'videos',
        component: Videos,
        
      },
      {
        path: '/subirvideo',
        name: 'subirvideo',
        component: subir_video,
        
      },
      {
        path: '/notificaciones',
        name: 'notificaciones',
        component: Notificaciones,
        
      },
      {
        path: '/creartorneo',
        name: 'creartorneo',
        component: Creartorneo,
        
      },
      {
        path: '/formulario',
        name: 'formulario',
        component: Formulario_join,
        
      },
      {
        path: '/creacionequipo',
        name: 'creacionequipo',
        component: crearequipo,
        
      },
      {
        path: '/diego',
        name: 'diego',
        component: Diego,
        
      },
      {
        path: '/crearpartido',
        name: 'crearpartido',
        component: crearpartido,
        
      },
      {
        path: '/diegos',
        name: 'diegos',
        component: diegos,
        
      },

      {
        path: '/torneo_guardado',
        name: 'torneo_guardado',
        component: Torneos_guardado,
        
      },
      {
        path: '/torneo_creados',
        name: 'torneo_creados',
        component: Torneos_creados,
        
      },
      { path: '/perfiles/:documento',
        name: 'perfiles',
        component: Perfiles,
      },
      {
        path: '/jugadores',
        name: 'jugadores',
        component: Jugadores,
      },
      {
        path: '/invitar',
        name: 'invitar',
        component: Invitar,
      },
      {
        path: '/pay',
        name: 'pay',
        component: Pagos,
      },
      {
        path: '/torneoscreador',
        name: 'torneoscreador',
        component: Torneoscreador,
      },
      {
        path: '/gana',
        name: 'ganadortorneo', 
        component: ganadortorneo,
      },
      {
        path: '/jugadorestorneo',
        name: 'jugadorestorneo',
        component: jugadorestorneo,
      },
      {
        path: '/targetas',
        name: 'targetas',
        component: targetas,
      },
      {
        path: '/galeria',
        name: 'galeria',
        component: Galeria
      },
      {
        path: '/store',
        name: 'store',
        component: Store
      },
      {
        path: '/calendario',
        name: 'calendario',
        component: Calendario
      },
      {
        path: '/vendedor',
        name: 'vendedor',
        component: Vender
      }
];
const router=createRouter({
    history:createWebHistory(),
    routes
})
export default router


