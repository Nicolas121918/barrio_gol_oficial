<template>
  <section class="sobre-nosotros">
    <div class="overlay"></div>

    <div class="contenido">
      <h1 class="titulo">Sobre Nosotros</h1>
      <p class="frase">"¡Esfuerzo, trabajo y Barrio Gol! Juntos hacemos realidad lo que soñaste."</p>

      <div class="secciones">
        <div class="bloque" v-for="(seccion, i) in secciones" :key="i">
          <h2 class="subtitulo">{{ seccion.titulo }}</h2>
          <p class="texto">{{ seccion.texto }}</p>
        </div>
      </div>
      <p class="frase2">"El esfuerzo tiene recompensa, y tu momento es ahora. ¡Hazlo junto al barrio!"</p>
      
    </div>
  </section>
</template>

<script>
export default {
  data() {
    return {
      secciones: [
        {
          titulo: 'Misión',
          texto: 'Nuestra misión es que ningún sueño del barrio se quede sin cancha. Sabemos que cada jugador lleva un sueño en el corazón, y estamos aquí para hacerlo posible. Creamos un espacio donde el fútbol no solo une, sino que da vida a los sueños, donde los equipos nacen con pasión y donde, paso a paso, juntos vamos convirtiendo esos sueños en realidad.'
        },
        {
          titulo: 'Visión',
          texto: 'Nuestra visión es ser el lugar donde tu sueño nunca se detenga. Queremos que cada persona, sin importar de dónde venga, encuentre aquí un espacio para crecer, competir y avanzar hacia lo que siempre ha deseado. Si crecemos juntos, te ayudamos a acercarte más a lo que siempre has soñado.'
        },
        {
          titulo: 'Qué Hacemos',
          texto: 'Nuestra visión es ser el lugar donde tu sueño nunca se detenga. Queremos que cada persona, sin importar de dónde venga, encuentre aquí un espacio para crecer, competir y avanzar hacia lo que siempre ha deseado. Si crecemos juntos, te ayudamos a acercarte más a lo que siempre has soñado.'
        },
        {
          titulo: '¿Por qué elegirnos?',
          texto: 'Porque en Barrio Gol, entendemos que cada sueño es único. Sabemos que muchas plataformas solo se enfocan en el rendimiento y en las estadísticas, dejando atrás lo más importante: la conexión real con tu comunidad. Aquí, en cambio, creemos que el verdadero éxito está en el esfuerzo compartido y el crecimiento conjunto. No buscamos solo usuarios, buscamos soñadores que, como nosotros, crean que con trabajo y apoyo mutuo, todo es posible. Elige Barrio Gol, elige un lugar donde tu esfuerzo no se mide solo en victorias, sino en progreso constante.'
        }
      ]
    }
  }
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600&family=Poppins:wght@300;400;600&display=swap');

.sobre-nosotros {
  border: solid white;
  position: relative;
  background-image: url('https://www.elagora.net/wp-content/uploads/2021/04/Crack-del-barrio.jpg');
  background-size: cover;
  background-position: center;
  min-height: 100vh;
  color: #fff;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 60px 20px;
  font-family: 'Poppins', sans-serif;
  text-align: center;
}

.overlay {
  position: absolute;
  inset: 0;
  background: rgba(0, 0, 0, 0.7);
  z-index: 1;
}

.contenido {
  position: relative;
  z-index: 2;
  max-width: 1200px;
  width: 100%;
}

.titulo {
  font-size: 3.5rem;
  font-family: 'Playfair Display', serif;
  color: #FFD700;
  margin-bottom: 10px;
}
.frase2{
  font-size: 1.5rem;
  font-family: 'Playfair Display', serif;
  color: #FFD700;
  margin-bottom: 10px;
  margin-top: 20px;
}
.frase {
  font-size: 1.2rem;
  font-style: italic;
  color: #ccc;
  margin-bottom: 40px;
}

.secciones {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 30px;
}

.bloque {
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 20px;
  padding: 30px;
  width: 270px;
  backdrop-filter: blur(10px);
  transition: all 0.3s ease;
}

.bloque:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 20px rgba(255, 215, 0, 0.3);
  border-color: #FFD700;
}

.subtitulo {
  font-size: 1.5rem;
  font-weight: 600;
  color: #FFD700;
  margin-bottom: 15px;
  font-family: 'Playfair Display', serif;
}

.texto {
  font-size: 1rem;
  color: #ddd;
  line-height: 1.5;
}

/* Responsive */
@media (max-width: 768px) {
  .secciones {
    flex-direction: column;
    align-items: center;
  }
}
</style>