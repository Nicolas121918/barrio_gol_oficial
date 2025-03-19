<template>

  <header>
    <headerapp></headerapp>
  </header>
      
      <table id="update">
        <thead>
            <tr>
              <th>Tus Pqrs <br>Hoy ⬇</th>
              <th>Fecha De Radicacion</th>
              <th>Nombre</th>
              <th>Tipo</th>
              <th>Email</th>
                <th>Comentario</th>
                <th>Eliminar</th>
            </tr>
        </thead>
        <tbody>
            <tr>
              <td>({{ fecha }})</td>
                <td>{{ fechaHoraGuardado }}</td>
                <td>{{ nombre }}</td>
                <td>{{ queja_reclamo_quest }}</td>
                <td>{{ email }}</td>
                <td>{{ comentario }}</td>
                <td><button id="delete" @click="eliminarpqr"><img id="logo_delete" src="../assets/imagenes/borrar.png" alt=""></button></td>
            </tr>
            



        </tbody>
    </table>

</template>


<script setup> 
import { onMounted, ref, onBeforeUnmount } from 'vue';
import Headerapp from './Headerapp.vue';
const verificar = ref(false);
const nombre = ref('');
const queja_reclamo_quest = ref('');
const email = ref('');
const celular = ref('');
const comentario = ref('');
const fecha = ref('');
const fechaHoraGuardado = ref('');

onMounted(() => {
  loadProfileFromStorage();
  
  // Actualiza la fecha cada segundo
  const interval = setInterval(() => {
    fecha.value = new Date().toLocaleString();
  }, 1000);

  onBeforeUnmount(() => {
    clearInterval(interval);
  });
});
import Swal from 'sweetalert2';

const eliminarpqr = () => {
  const usuarioId = JSON.parse(localStorage.getItem('usuario'))?.id; // Obtiene el id del usuario actual
  const pqrsUsuario = JSON.parse(localStorage.getItem('pqrs')) || {}; // Obtener los datos almacenados en pqrs


  if (usuarioId && pqrsUsuario[usuarioId]) {
    const pqr = pqrsUsuario[usuarioId][0];

    if (pqr) {
      delete pqrsUsuario[usuarioId];
      localStorage.setItem('pqrs', JSON.stringify(pqrsUsuario))
      

      Swal.fire({
        title: 'Éxito',
        text: 'Los datos han sido eliminados correctamente.',
        icon: 'success',
        confirmButtonText: 'Aceptar'
      });
      verificar.value=false;
      document.getElementById('update').innerHTML='Eliminado Correctamente';
      


      console.log('Datos eliminados');
    }
  } else {
    Swal.fire({
      title: 'Error',
      text: 'No se encontraron Pqrs para este usuario.',
      icon: 'error',
      confirmButtonText: 'Aceptar'
    });
  }
};


const loadProfileFromStorage = () => {
  const usuarioId = JSON.parse(localStorage.getItem('usuario'))?.id; // Obtiene el id del usuario actual para mostrar el localStorage
  const pqrsUsuario = JSON.parse(localStorage.getItem('pqrs')) || {}; // Obtener los datos almacenados en pqrs
  verificar.value=true;

  if (usuarioId && pqrsUsuario[usuarioId]) {
    // Obtener las PQRs del usuario específico
    const pqr = pqrsUsuario[usuarioId][0];

    if (pqr) {
      const tiempoGuardado = new Date(pqr.fechaHoraGuardado).getTime();
      const tiempoActual = Date.now(); 
      const tiempoLimite = 15 * 24 * 60 * 60 * 1000; //tiempo restante 15 dias


      // Verificacion para saber  si ha pasado el tiempo límite
      if (tiempoActual - tiempoGuardado > tiempoLimite) {
        // Limpiar los datos si el tiempo ha expirado
        delete pqrsUsuario[usuarioId];
        localStorage.setItem('pqrs', JSON.stringify(pqrsUsuario));
        console.log('Datos eliminados después de 1 minuto');
      } else {
        nombre.value = pqr.nombre || 'Haz Tu primera PQR';
        queja_reclamo_quest.value = pqr.queja_reclamo_quest || 'Haz Tu primera PQR';
        email.value = pqr.email || 'Haz Tu primera PQR';
        celular.value = pqr.celular || 'Haz Tu primera PQR';
        comentario.value = pqr.comentario || 'Haz Tu primera PQR';
        fechaHoraGuardado.value = pqr.fechaHoraGuardado || '';
      }
    }
  }
};
onMounted(loadProfileFromStorage)
</script>




<style scoped>
#logo_delete{
  width: 25px;
  height: auto;
}


#delete{
  border-radius: 5%;
  transition: transform 0.8s;
  background-color: white;
}
#delete:hover{
  background-color: rgb(255, 255, 255);
  transform: scale(1.2);
  color: white;
}

/* Contenedor de la tabla */
#update {
  margin: 0 auto; /* Centra la tabla horizontalmente */
  width: 80%; /* Ajusta el tamaño de la tabla, puedes modificar el porcentaje según lo necesites */
  max-width: 100%; /* Asegura que la tabla no se extienda más allá del 100% de su contenedor */
  border-collapse: collapse;
  background-color: rgba(28, 28, 28, 0.538);
  color: white;
  overflow: hidden;
  margin-top: 100px; /* Espaciado superior, puedes ajustarlo */
}

table {
  width: 100%;
  border-collapse: collapse;
  background-color: rgba(28, 28, 28, 0.538);
  color: white;
  overflow: hidden;
}

th, td {
    border: 1px solid #000000; 
    padding: 20px; 
    text-align: center;
}

th {
    background-color: #000000;
    color: rgb(255, 255, 255);
    font-weight: bold; 
}

tr:nth-child(even) {
    background-color: #ffd900a4;
}


/* Estilo de la tabla */
#update {
  margin: 20% auto;
  width: 100%;
  border-collapse: collapse;
  background-color: rgba(28, 28, 28, 0.538);
  color: white;
  overflow-x: auto; /* Habilita el desplazamiento horizontal */
  display: block; /* Hace que la tabla sea un bloque para que el scroll funcione */
}

table {
  width: 100%;
  border-collapse: collapse;
  background-color: rgba(28, 28, 28, 0.538);
  color: white;
}

th, td {
  border: 1px solid #000000; 
  padding: 15px; 
  text-align: center;
}

th {
  background-color: #000000;
  color: rgb(255, 255, 255);
  font-weight: bold; 
}

tr:nth-child(even) {
  background-color: #ffd900a4;
}

/* Para pantallas pequeñas */
@media (max-width: 768px) {
  #update {
    font-size: 12px; /* Reduce el tamaño del texto */
  }

  th, td {
    padding: 10px; /* Reduce el espacio interno */
  }

  #update table {
    display: block; /* Activa el scroll horizontal */
    overflow-x: auto; /* Permite desplazamiento */
    white-space: nowrap; /* Evita que el texto se ajuste a una nueva línea */
  }
}

/* Para pantallas extra pequeñas */
@media (max-width: 480px) {
  #update {
    font-size: 10px; /* Reduce aún más el tamaño del texto */
  }

  th, td {
    padding: 8px; /* Ajusta el espacio interno */
  }

  #delete img {
    width: 20px; /* Ajusta el tamaño del ícono de eliminar */
  }
}

</style>



