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
import crearequipo from "@/components/crearequipo_form.vue";
import Diego from "@/components/resultados_partidos.vue";
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
import Store from "@/components/ReportarUsuario.vue";
import Stores from "@/components/stores.vue";
import Partidos_creado from "@/components/partidos_creado.vue";
import Sala_espera_partidos from "@/components/sala_espera_partidos.vue";
import Ganador_partido from "@/components/ganador_partido.vue";
import Resultados_partidos from "@/components/resultados_partidos.vue";
import Partidos_finalizados from "@/components/partidos_finalizados.vue";
import Inpeccion_equipo from "@/components/inpeccion_equipo.vue";
import Torneos_finalizados from "@/components/torneos_finalizados.vue";
import Torneo_sala_espera from "@/components/torneo_sala_espera.vue";





const routes=[
    {
        path: '/contactanos',//sobre nosotros
        name: 'contactanos',
        component: AboutUs,
        
      },
      {
        path: '/videohome',//video de inicio
        name: 'videohome',
        component: Videohome,
        
      },
      {
        path: '/partidos_creados',//partidos ver los creados
        name: 'partidos_creados',
        component: Partidos_creado,
        
      },
        {
          path: '/sala_partidos/:id', // ← aquí está la diferencia
          name: 'sala_partidos',
          component: Sala_espera_partidos,
          props: true // opcional: pasa el id como prop
        },      
      {
        path: '/iniciosesion',//form inicio de sesion
        name: 'iniciosesion',
        component: iniciosesion,
        
      },
      {
        path: '/Perfil',//perfil del usuario
        name: 'Perfil',
        component: Perfil,
        
      },
      {
        path: '/actualizar_perfil',//donde se actualiza
        name: 'actualizar_perfil',
        component: actualizar_perfil,
        
      },
      {
        path: '/home',//donde se ve la hora , ayuda, cerrar sesion y mas
        name: 'home',
        component: home,
        
      },
      {
        path: '/contacto',//para enviar pqrs
        name: 'contacto',
        component: Contacto,
        
      },
      {
        path: '/torneos',// interfaz base de partidos torneos
        name: 'torneos',
        component: Eventos,
        
      },
      {
        path: '/equipos',//interfaz lider equipo
        name: 'equipos',
        component: equipo,
        
      },
      {
      path: "/one_video/:id",//para ver un video en especifico
      name: "One_Video",
      component: One_video
    },
      {
        path: '/videos',//tik tok barrio gol
        name: 'videos',
        component: Videos,
        
      },
      {
        path: '/subirvideo',//fomr de subir los videos
        name: 'subirvideo',
        component: subir_video,
        
      },
      {
        path: '/notificaciones',//notificaciones de pqrs
        name: 'notificaciones',
        component: Notificaciones,
        
      },
      {
        path: '/creartorneo',//formulario para crear torneo
        name: 'creartorneo',
        component: Creartorneo,
        
      },
      {
        path: '/creacionequipo',//formulario para crear equipo
        name: 'creacionequipo',
        component: crearequipo,
        
      },
      {
        path: '/resultados_partidos/:id', // ← Agregamos ":id" para recibir el ID del partido
        name: 'resultados_partidos',
        component: Resultados_partidos,
        props: true // Opcional: Pasa el id como una prop
      },      
      {
        path: '/crearpartido',//formulario para crear partido
        name: 'crearpartido',
        component: crearpartido,
        
      },
      {
        path: '/partido_finalizados',//formulario para crear partido
        name: 'partidos_finalizados',
        component: Partidos_finalizados,
        
      },
      {
        path: '/ganador_partido/:id',//ganador de partido
        name: 'ganador_partido',
        component: Ganador_partido,
        props: true
      },
      {
        path: '/diegos',//torneos anterior creador
        name: 'diegos',
        component: diegos,
        
      },

      {
        path: '/torneo_guardado',//torneos de equipo
        name: 'torneo_guardado',
        component: Torneos_guardado,
      },
      {
        path: '/torneo_sala_espera/:id_torneo', // Ruta dinámica con el id_torneo
        name: 'torneo_sala_espera',
        component: Torneo_sala_espera,
        props: true, // Esto pasa el parámetro id_torneo como prop al componente
      },      
      {
        path: '/torneo_creados',//torneos y partidos creados
        name: 'torneo_creados',
        component: Torneos_creados,
      },
      {
        path: '/torneos_finalizados',//torneos y partidos creados
        name: 'torneos_finalizados',
        component: Torneos_finalizados,
      },
      { path: '/perfiles/:documento',//perfil de usuarios inspeccionados
        name: 'perfiles',
        component: Perfiles,
      },
      { path: '/inspeccion_equipo/:id',//inspeccionar equipo
        name: 'inspeccion_equipo',
        component: Inpeccion_equipo,
      },
      {
        path: '/jugadores',//todos los jugadores
        name: 'jugadores',
        component: Jugadores,
      },
      {
        path: '/invitar',//inivtar a equipo
        name: 'invitar',
        component: Invitar,
      },
      {
        path: '/pay',//billetera
        name: 'pay',
        component: Pagos,
      },
      {
        path: '/torneoscreador',//interfaz creadr torneo
        name: 'torneoscreador',
        component: Torneoscreador,
      },
      {
        path: '/gana',//escoger ganador torneo
        name: 'ganadortorneo', 
        component: ganadortorneo,
      },
      {
        path: '/jugadorestorneo',//interfaz de torneo(goles)
        name: 'jugadorestorneo',
        component: jugadorestorneo,
      },
      {
        path: '/targetas',//donde se sacan tarjetas rojas azules,amarilas
        name: 'targetas',
        component: targetas,
      },
      {
        path: '/galeria',//galeria de equipo
        name: 'galeria',
        component: Galeria
      },
      {
        path: '/stores',
        name: 'stores',
        component: Stores
      },
      {
        path: '/calendario',//calendario de equipo
        name: 'calendario',
        component: Calendario
      },
      {
        path: '/vendedor',//interfaz de vendedor
        name: 'vendedor',
        component: Vender
      }
];
const router=createRouter({
    history:createWebHistory(),
    routes
})
export default router


