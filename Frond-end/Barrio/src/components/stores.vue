
<template>
   <button @click="$router.go(-1)" class="boton-volver">Volver</button>  
  <div class="container">
    <div class="partidos-section">
      <h2 class="title">Partidos en Espera</h2>
      <div v-for="partido in partidosEnEspera" :key="partido.id" class="card">
        <img :src="partido.logo" alt="logo" class="logo" />
        <div class="info">
          <h3 class="tit">{{ partido.nombre }}</h3>
          <p>{{ partido.fecha }} - {{ partido.hora }}</p>
          <p>Apuesta: {{ partido.apuesta }}</p>
        </div>
        <div class="acciones">
          <button @click="verDetalle(partido)" class="btn-detalle">Ver Contenido</button>
          <button  class="btn-detalle2">Ingresar</button>
        </div>
      </div>
    </div>

    <div class="partidos-section">
      <h2 class="title">Partidos Finalizados</h2>
      <div v-for="partido in partidosFinalizados" :key="partido.id" class="card">
        <img :src="partido.logo" alt="logo" class="logo" />
        <div class="info">
          <h3>{{ partido.nombre }}</h3>
          <p>{{ partido.fecha }} - {{ partido.hora }}</p>
          <p>Apuesta: {{ partido.apuesta }}</p>
        </div>
        <div class="acciones">
          <button @click="verDetalle(partido)" class="btn-detalle">Ver Contenido</button>
          <button  class="btn-detalle2">Ver Resultado</button>
        </div>
      </div>
    </div>

    <div v-if="modalActivo" class="modal-overlay" @click.self="modalActivo = false">
      <div class="modal">
        <button class="cerrar" @click="modalActivo = false">X</button>
        <h2>{{ partidoSeleccionado.nombre }}</h2>
        <p><strong>Fecha y Hora:</strong> {{ partidoSeleccionado.fecha }} - {{ partidoSeleccionado.hora }}</p>
        <p><strong>Apuesta:</strong> {{ partidoSeleccionado.apuesta }}</p>
        <p><strong>Modalidad:</strong> {{ partidoSeleccionado.modalidad || 'Fútbol 11' }}</p>
        <p><strong>Reglas:</strong> {{ partidoSeleccionado.reglas || 'Reglas estándar del torneo' }}</p>
        <p><strong>Cómo llegar:</strong> {{ partidoSeleccionado.comoLlegar || 'Disponible en Google Maps' }}</p>
        <img
  v-if="partidoSeleccionado.imagenCancha"
  :src="partidoSeleccionado.imagenCancha"
  alt="Cancha"
  class="imagen-cancha"
  @click="imagenAmpliada = true"
/>
<div v-if="imagenAmpliada" class="modal-img" @click="imagenAmpliada = false">
  <img :src="partidoSeleccionado.imagenCancha" alt="Cancha grande" />
</div>

        <p><strong>Ubicación:</strong> {{ partidoSeleccionado.ubicacion || 'Dirección no especificada' }}</p>
        <a
  class="btn-detalle2"
  :href="`https://www.google.com/maps/search/?api=1&query=${encodeURIComponent(partidoSeleccionado.ubicacion)}`"
  target="_blank"
  v-if="partidoSeleccionado.ubicacion"
>Ir a ubicación
</a>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      modalActivo: false,
      partidoSeleccionado: null,
      imagenAmpliada: false, // 
      partidosEnEspera: [
        {
          id: 1,
          nombre: "Partido 1",
          fecha: "2025-04-10",
          hora: "16:00",
          apuesta: "$50.000",
          logo: "logo1.png",
          modalidad: "Fútbol 11",
          reglas: "No se permite contacto físico brusco",
          comoLlegar: "Tomar bus hasta la cancha central",
          imagenCancha: "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD/2wCEAAkGBxMTEhUSExMWFRUXFRkYGBcVFxgaFxgdFhgYGBcYGBodHSggGholGxgYITEhJSkrLy4uFx8zODMtNygtLisBCgoKDg0OFxAQGi0fHx0tLS0tLSstLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tK//AABEIALUBFgMBIgACEQEDEQH/xAAbAAACAwEBAQAAAAAAAAAAAAADBAIFBgABB//EAD8QAAEDAgQDBgMDCwQDAQAAAAECAxEAIQQSMUEFIlEGEzJhcYFCkaEUI7EzUmJygqLB0eHw8QcVQ5IkNLIW/8QAGQEAAwEBAQAAAAAAAAAAAAAAAAECAwQF/8QAKBEAAgIBBAIBBAIDAAAAAAAAAAECESEDEjFBBFETBSIyYUKRFHGB/9oADAMBAAIRAxEAPwDSlaidalk6mlu/6V3f1ujlDOudKSdcNTW7SrgJpiAuO0FTtTcRQSKRdAXkk0ksEVYLNKvJpABS5UVroa6hmoKBumllLplYoC2qAAqeNBW4etGUzUCzQAspZ61yVHrTP2Y1NOFNMAKJoyEmmGsGaYThI1oAVSk1MJq0wvDlK2gVznDTMC5pCtCCaKAfOtDw7s4uRyZiauMR2PdyzAAFyKdMj5EY7DslRirJPDFDrWs4HgGCpKVAfwrZOcLaCSMoAik2kCc5cHzrhfZhayLitIvsx3aSqxgaUPBPLw7hJjLP0qwx/aMRGXX5022nghJSTbbGeApZKLBIO80t2hQLFtQBGtZt7iN+URSrjpUZJo7sKW2qLtnj60DLOm9I4vi617/Oq9Q60M0maR/Y0Hz1oncKUJApVs1f8Lx6EIOYAyLVlI7INUUiiRrUmHr17jXQtUjSk3nIpIci8ZxnnXVRs4iK6qoixJLqlGjoMa0QMhAvSwBWbada1RzZ7Gw5QlrplDKUC5pfJmNtOtMkXWqlnDVuttCU7UgGs5tpSHYlNRUKuEsISI3pZODUtXhIHmKGgUkVK2p0oCmCNq2OD4XsEKJ9K8xXZ9yZUnKmgSmjJM4VSjYUVzh5GtbfhvZ9wmEhMdabxvZcoGdRkDptQ0G8wmF4Kpe0Civ8ECfWt/wXgSHOYLOXoKa4nwRDSe8Cc0ajejF0G6VXRgMDwJJuoj0ojnBQTlSPevovAcOytOYIAPQi9C7SYEZR3cJVRauhfdt3GU4X2ZWqQEiOtFx3ZjuoWuIq94RxXuRldvO9G4lxZt1OXKcvU0m88CS+27Eez/CMO4Z1jarXi3BWg2SlIChp51lF8S7pX3VvOiu8dcIlSz6f0od2CSrjI1wfHKaWC4LdK0b3HWSmxmR0r5tiuILWq9hUkYkxGgNDVlRtKi5xLraFZm9Zrx/jSymMxn5VWNGucTUt5yOMaWAn2xSvEqa8Dk6mghE36UJK4poGh4JrwiDUGn4GlGYaccPKhSvQGnYtrIxNCJirB3gj4SpRSEwCYKhmIFzAFVGepsqqDJE1Bb21DLv+ajcwN6mjRSJqfoCsVUMYhSTBqGHZJlQEhNzRQPVo9OJArqrsbiJWSBA8q6nQbz6vwrs6ypOZQCj50p2i4G2nKUAJnUVxxboJDZgdaE8tZutU+tNSdhLSVUWWB7LM5AVDMSN6oeO8OSy5AEpI+VNscZeSMqNOpqDz6lSXCCetUpezN6fos+C9n2FNhZAUT1qu7T8ODRSWkg9RSTPEXUnK2rKKP3izdayr1oUskygqpcll2WwrSwVKSM/Qj8Kf7QYJPd8kBe1ZU4g5oQopHXem21xcqJPrSbzY1BVVFtwDFZJDsA9RTnFsS04goCgSelZZx0qN9KIXoEAXpN5stQ+2h3heL+zEgkqSetz7VYYvjYWkpyGDrWZKzMmg4rFmIFqSdux7KVFnhuK90qGt9RtTGL42sjnIjpWUaWRpRFkq1NWTVYLAcVUVWOUeW9ev8TOxJPraqyKJk3oEkTL5NyZr1WIURG1RQ3XjesGlYUBcoFWuH4c4sGG1noYt8zamGey76tcqPUyfkKdoEmUjLSVHnJAGwF6Egj61rW+zLabuPH2yp/GT9KI1hcE3OVGcjUwVfjA+lLcilB3ZlmASYSCT5XP0q0Y4TiFf8ZA6qhP41dHjiEhIbQkZtBPQxogVBzirhzwIiw0TebaSrrttUtlKKQmz2Yc1W4lI/RBP4wKZb7PYdN1qUr1VA+n8TU2m3FwSoyBKgBc7gSqT5aCvDw8C7qkpm6io3gXi5MDe0aUrKpDbCWEgd2hPUEAH3zc1eqxijoAOk/jcxHTrSKOItCMgKyqbxywmd4gaRc0DD4rvVXiCEmB4E5pTzK0WQoCAKRSRd8Pf7wKCvKJ1KVCCSPhvIisDim8qlJOqVFPyMV9DbQhJEKkuJPqT4x6Cx+dYztLhSMSuPiSHPmL/AFBoRMkVaBRnGYggzafSoYcSa0GE4WFNlRUARtTbozozGJCjc3pVYUElQ0mD7+VaR7h5IMCqrF4YtqBKdLwdxTshozThM3rynOLPd44VFOW2grqZR9KLgFDUgqqMyaaZrO6OpgEtZaUxEnWr7FpRlGU33qmxAFCIZWm1eFROpqTgoSztWhizgacZ0pUCmQq1JjQyyibVYtcNtNJYR0TFarBr5PD87fjWTNUZPGYWKqnhWwxuAK/iA+Z/CkDwRkeNwnyBA/maqLBmSTpRGmVK8KSr9UE/hWtDOGb0aBIvKhOnmqouceATyBMTECT6WQIq9xDiUbHAn1fBl/XIH01q0Z7NEDncA/VH8TFTXxJwqA5glQF+VAuPO5vQG3ypJuCoETGZZ6HyobYkkWDXC8Om3jPmf4CKmcS01dDQERchKdfM3+teYbEJCBM5jGpA0MeEVWutDnED5SbK/TP8Kkobe44olATHNHhBWbmNdPekMbxFwhckpgDxrCR4o0HMKKMMopQbkTpJ2VPhGUfSg9yEhUqCMx0Gus6IGY1SoltgEtEhslUHoEiTzHRTl9KgMMVZyQVZjAzFS981gYGw0Boz+OabzEDmQAOchI1I0TKzc7ga0L/cVkhKZShSJEANpkpPxK5zzCmCLROHCAhKiluBAk5cx8kiJuem1DD7aESlBUM2q4bQTGtxcegqowCivuykyoLIPdJKjsq61361pMBwsELECc25zqtPtvUNl0VmM4g6e9CSQBH5MZB4hq4b6GqlxwFfiTmLPwgurPJ+cZB0q+43hAnPmjwauG1sp8I9KzziySiM5SWlC0NN+FY1PpSTGQz3azA+BX5Zcbr/AOMXo/DeIBAQ4bpDKiCoZGxkWpXKjUmBVThXRmYCcgMrENpLqtT8RsNdqk0+mGQRlcIdTmWe8eMgwAkcqTJ30tVMaNOOIkOpVzAZ0mNVrAXlJPRGVaT7V529TkDaoBkqbJi4g5kwfdVUTa8wCSFSsCUTLis7ZH3h+AZ2xWl4+0cTgApIleVtwBJzXHKsA76q+VIlmQwj160nD1zWP4c6lLgDkhIMKG46+9aLCY5AWcnhm06x50SM0a3DYVRQoCI3mszj15FhR5o2N/arjE8dSUiLGIPSspxbG5zA1PSoQ5UUnG8UHHSsJCZ2GldVfxEKQuFCDXVoSfRkuxR28TFVJerw4i9KjWTLpWJmlMQ/SYf6Vo+ApQpoLyIzAKkkSeU+c7UUH6KJtpazyoUr0BNNN8EfVqkJ/WI/ASau/wDcFKHLGW0HUXveNLfjXmZxSZBv9D7i30p2xbRJjs6B43fZI/iT/Cm/sOHRcif1z/gV4MM4ZNz1BMfIpihqwIAhSkgbElMjr59N6B0Mox7aZShIkbJF7eg/jUVcSJEwfchPpuTSK3GROZ9OZH5sqIvFxfejNPNSMoWcwnlQQkz9KTQEnsQom5GUixhRid5MDWkMQlSgRKpFxBCZ6jkB9aslFsNlWU66KUkR50mnFZ1lCQiQmUklSjsRMAbedOgsUCJyrgEiAbSbW1UrceXWve6IJTJhQtcgdRYBPprXOY1aVJlNiYVDYAseqlGBBFJv4xzu1kqACFC5csLkEQ2kbxak0LA2MOcoMQUnoAYN9wd533pgN817hYtMnXyMjWqhOMK1jKVKC0TyNkiSn85ZPxDpXuI4opTbZUAnIqPvHI6KHKiPO3lQItVYlKU3UAArqBqJ09jtUHsaJWEpJ5ZmOU6HUwNKpy7d1CCdMwDTfQgjmO+VRoKnBnaUoAZk5SXnCTqUHlT5EfOgbTH3OLH7uVJCSYIBK/ig2TCdCNar1uqCFAhXIsH7wpaQZkHlFyJA33pV9a+5Md5Zf/EgNJggjxnaU0F91PeO/kgVN5viecPhXp4dAatGUuSzfSvOViwdbJHcN6nKFTnPmKSafAUwpWQHOU/eKLrllgxCbTzb6V4vFrV9nz5yiMv3qktI8Sk+AXNlDQ1WsPHueQklDlxh0ZQJTu4u8SnWgcWX+GxakIJ5hlcEFwhpOihZIuRatVgOMQVxfflEJvB8R9a+fqeSHHxyTmSqEy86ecDQ8osumcRilJUc8pzMSO/XeyQbNJv8NZtGyNRxXigUogG5aUYQM6vCd9BpWXViU52isIkoWkd6suL1XolNpvvQhiyruZKilTaxzEMtf8g8PiVSOAeJ+zlBJTmWD3CAhGo1cXzb+9CQDGGdVGHnPHeKHMUsI+D4NVC9TZxqnSwoaZygjDpyNxyDmcVc6+9VuAUJYju83fqFs2Ic/wCL4jyg1oH+HMIwjTrjoK0Oz98omCctsiIA00qgTFeEmUBKQDAVyNE5ZaWlwd46fIm2npW67ONk4dbMgFKnGxkBASFjMiOsTrWM4HiQhZzhRQl+JWEtNwvMiyfi29a2nCuModdIbBgtpVIEIBbUUkDqag0aPkhcUFkGSrMQesgwfrR2sflprtO79k4m6QgKAc7xIVoQ4Av+JFUHGOLd86pzKEybACAKo55ovkcSzEJzRJifWjcUxAwb6ZKXbAyDb0rJ43GNwju8wOXnzEeL9HyqudxJO9FEGt7W9qRiVpKEhICbwN66snhEoUCVOhBBACSCZBmTI6fxrqZVn0hWIrkvkzF6qBjSJjexomE4iUTG9CRbkuh9WIrXdhsVIWg7KB9ljKfwr5+04VrtqTWm7HlTeJLavjQoe6eYfgab4BF/kiZPOkkX5FmJTroZKE/Oip7w2lcSRPIYvKFT0gx7VLGJIfVAVCoXsocyQScuo5myP2qt8HgEKTMJuI0I00t6RWbZZmcU8oAKVsYUFuQDO5Snc3FKN4nL3jaFAwMw7trMY9TqSCD+zVvxZACoEc4jlbzHNsb+cfOs7iMQqErUHORWVQW4lsRtKfTMPaqTAb7xRUknvgFpgyUoAPhJPnICvegBzkBITmbVfO6VETpOU/nA1XLyALb+55TnTJcWYgSbfo5T7U5h3SpQKSYdTfu2LZupJ/TE361RJasKzqU2hSOYZk5WyfMXVbSRXjxcbUhRLtuVUZUJtaT+yR8qFgXXOQ/eylUHMtKLG4kfMVYcV4IrKvlQSecFZUrTUwPI1DkVtM5xAgJXn7vMhUy44pZvykwnzy141jVKVlQpRS6iYaZtmI1zG8501ziypSCCuHE5CWmQBJGQkqNxeDSmCAVk7/MAhyCXX0ggK5gSlJ6pNvOnF4JcaPHMSciFrBlCyPvngLWWJSL65reVMKWgKdbaUkgALT3bJUq0HVVvCqluJJZS682wpspKQ4nu2i4q3N8Vpyk71zLyszJX3uVSe7V3jiGhu2Tk9CDak2VBFqjDLWW1KSshSMp71zKNCjwD2qsC4bhJGZDmjLRURmH5yri6DetJwviIbwijkTAVEoSpcE9CdTIrNcXeK1PJUF5SnOO9dDabQvwjmiCaSyaNDHHOJ96FtLQhISjOC6u5gpWJQjmsCflQOFYdx1bIbzkKbKT3SA0i2ZHjInSLUngVhS2ckc6O7PcMlWmZv8ou4gZaf4UhR7sggOJcIBddK1DMAdEaHlNjV3RzuNla813aQCGwtt4ggJU+5cJO9gZSaHxRMDEBzQLCh9pc5QM5FmkXAhX4VecewK2+/QorPMlXiSyiJI8Q18X0qow+IyPKW2EKJYC4aaK5KUJVzOLtqk7007JqgRcUSsjOULw4MpCWGrJSq6zzHwmiJ4kt5xhWbMe4Uj7hGYiO8TBfV4RpSSnAp5lSsgWttxMKJfc/5BCUp5BqNfSgtvf+qXJH3ik/+QvJqUxlYb1PNYHSgpMsuA4cvO4YJy5gtYJviHfECZX4EnmvU+I8LVh1MB6CQ/AU+tS1XyRlbRYaaHSk+C8Ucw6WikkJGIy8wThmoIR4U3Usax1pjiXGXH1ByVwMSAS2AyjQTLjl1C21CFJ4ANKUEtZs4SMSRzlOHR/xxyC6hSqHj3Kw1MB82wzZHwnVxz01qDKxPIEkjGX7lCn17eJa+VJtcilOIuAtvBwps+P/AGHivXvBZtrT9U0MUGWmLxCQ5ibthVlgqUX3LOIPhHKPFV3wbHFGLaWoKjvVIzPKCAEvoCgEIm4mbVmw8ourCe9yrYn7ptLKPyIUPvFX1TS/2hKUhz7hCu6QuVKLy5w7hSdAUyEnXzqKN92DTf6z4bK9h3xo40UE+bZt+6r6V82U9X13/U5IxHCUYhN+6cbcmI5XBkUfISQa+MYZtbphtC3D0bSpZ/dBpmUgzrkbg22oCnask9m8T8aUMjq84hB/6yV/u0RPBGU/lMSVdQw2SP8As4U//JqJasFyyOCmSu9dV603hE2DC3PNbyh9GwkD615Wf+RALRoMpBE7wbHY01xRLQCe7mY5p60rheIAZAUphKidLmep3pztNjg4oOJa7pJTa1j6VvZVCOD4kWlSIqyY7SE4tlyYAcTPoTCvoTWY+0o58ySSRykGIPU9aUCzTLgj7p2lUEKac5NFouopUSghxIB00C9a8Z4qsDKkLJgxC0mch29UwahxB3vuHtP5gLMuklIUI8DgIO3MZNZHEY4MKkOM5m1AkhtwTlJZXGW1wlHzqGjVRtF5xbiBXmBm6e8TLyQJE5k2vbm/61UHENKNu6zPWlIW5ChrY28cGehpFDhuG+YtLC05MNmlCotKvVJ9zTbGBecDiEB4gAOolaGhB1TAE6H5opxQmqCYd1cNrh7lORQyoaBGxPlBI/Zp3HcNLScqlBRHOkrfJsYB0A/RNVzTaSsghoF5Nwe8cOcH/r4h+9Vvg21HIvmPwKyspFojU38J/dqmzOweGUO85O7+8TmGVK1HNrvbxBQ96sMbxB9GTN3ojlUAlCLazJJ+E/u0JbC0pglctqkZnUpsfIDSQP8AtSPEUpUpYV3ZzALTmLjhtfSY0Kh7VFl7it4kqELSvLLa5lx8qsTlJhFxfL86TDiVOLCCn71vOO6YK7+Ocy7apUPenlhRU2U54cSUEtsJTcDLmKlXHwq9qpMRiClCFrJlpyCHsSBY8wlKPMKEVUUTKQy7iSnuHFl3KJbV3jqGkwDqUDXlX+7SSXkpQ4hJaztO/wDG248sTyHxWnMlNAeaRD7Tfd8pDiQ1h1uqjSZcsSULTp0ozi1lcK72HmNHHm2U5wnTInmnvEfvUbRKRc4jiTpDjR7zu1t94AtTbKZhLkQJVsoVW4XEJK2FJLfMktnum1vKkEp8arDlUn61XYHEI/8AHWnuiQotK7ppx9UAzGddhyuG9SxKlpaWlZcHdPT9+8llNxl8Dd8soTbzootyLXBcRUyEOrTJad0xLoSLgGe7QDugwDVgcaSvEFuRCgsdy2G0gZo/KL1ssGYrPJUCrEBqIUEvD7OxJuUr/KuWnKs3qanwpxIWUlTuHIh51Tq5Sk6NN8vibFBlZc43GhbipKMy2J+J9yQkHTwaoNT4k5hy3hdQ4tJQoPrKU3CkR3aDJPNpVRh3lThsxWArM3BKMOk8x/4xzqssW8qBg0d2MOZDcPkcqQgmchjO9Lh0PhF6BcnmCdVkw6hmyB4pOUJwzUEoNyrnULnTWhYMZUJLYgJxNywmBonxPPX+HVNNYXhrix90w46pOJ1yKUrS57x+bcuqUjX3qwf7PP8AN3q2mfv86StYWsAZrjvJy6iyEUSmly6CimcbIStSQOXFTmSO9VoqZdeIQnT4dKhjFpzOiUqUnFA3K8S4J7zRIhCdParnGcLwkr711TuZ3PGVS48UAKdUlI8R0RFTdxjAnJhyqV5z3i1ZZExKGu7SQJNjPvXNLzNGPd/6JckUuOJlaVz/AO2Moecyj4vC01f2NHZ4RiVDEd006AXAQW2UMJMKXJDrpk6608njbqZ7vIyCST3LaESTqSUpzT6qqvxWIcXda1LPVRKvqqTXPL6iv4r+yfkQX/ZgHGnHnGBlQlKgt13EuWSUKADYCJg6k1FheHZSE53XMuayENYdELSElNgtcWnUGaUX5/0pJ251+QrJ+ZqS/QfIzQudsX+4+zoSgNZQk5wXVEC/MpwkE+1U2K4s8oQXFZfzUmE/9UwKWSkf5Nv4VBSouAAP78qhzlJ5ZLk2BUr1/vzoakk7fMzRHFzt/f1oKgbaX6a/WqSEeAwdfpXVLDqk9baAeetv7vXVYyyeMaT5/PahYziTi0pStRIQISDsKcx2HUZKUkgakCw9aoX116idmpIqMTBiYnaek1YMhj7OSVK7/MITHLl3v1oeM4Q63hkPlQLbirAHcWkjaq5lykzo0z7h2Cl/hXcmZHetWMGFDMiDt4vpWWIdIAP2gZgAfvE2LiMhv5ON/NVaH/SnjCFtOMCykw56gcp/h86p+IPtsP4lst4YkqcSnMXCRmAfbkCfiz6VJrw2gHB+0HcNy4kEH7pffYhKikdYF5ykj9micE40vDhaWsnIogpabcWSlZtdWtz+/VC24FLUG9HkBxPcYeYVdXiXG4Wn9qmUYqza3SrKQWnO9fAtFjkReSn/AOKtGMzQslfOkl3XvElSkNSDE2F9I/6mtJwZxIWVQg94mQCpSua8+VjIrN8IxzKGCjukqdaWBLba18pJ0K46ka7irfCYlSARKuQ5gSpCJSY2G2hqZGRf4vARCoHOIOVAPzn2PtWdxylJCVc/IqCCtDYgmb+Wo96fxXEEqBSSm6cyZWpWlz4R0zfKqfFOhRsJ71Pwsk8w0MqPUfWpKKZ/GBlayktFTSg4guLcdOUwCYSPzSk1WvqU444UpV9+33gLWFSkZhzeNe8pWL/nU29ilfdKJcAMtLlxlqxESQJM5VbfmUph+DvuZcrKVLZdPiL7pKTcwTlSTKT1HNWvAhF1+Syp1RyrSWV99igOqfA3qcqkG1JYUZW0KQhJUw9EM4ZbhEnNGd2I5kq5vOtOvsmtCXEKfaw6e8C0ZQ0hQFwRAC1zGW8fCKlieH4KXC484/3kFQSkqAIIMgumBedEb1jPyNOH5SRNpcmdxSSQ+yVKVlUlxKV4gJ5Zy2bZlQELTbyo6cMS4vKEpLzIWAhlKVFQAV4njmJzJV8O9X3+44dFm8MCcoTLy1KBAAEFCcqdulR/358DK2UtJ/NaQlsfQAxXLP6jpLi2S9WKF8P2cfc7txxteXuVNqU+pUAQpAJSsto0y6A0zheEttBrvMU2nuyeVmSCCZyw0Ep3OqiL71XYnFkmVrKldTJ+poOdM76axXNL6lN/jGiHq+i2YVgmQAhLrmVZWDmSykkxqG7qHKPEfWvG+MhFmMOy1cq5UBSpO8qmT5xVOvECwj+IoJxZ6wOpIvXPLydefZLnIuMVxZ9wc7qyOkwn5C30pCfOPf8AlFJodzGxn2J2nyqOUi6ikDYkwfS9YuDbyybGs6QLGfQGhOYhI0/v2oRSmx1HqDr6xOlTaw2aMqcx6C5taeUGBVKCAj9q6fgaAtazoCfY/wAavMN2exKxIaIndcJG1zv12OlHPZYIGbEYlpsfmiSf3in8DWsdJ+h0zLqSvp87H8PSolJSJnU739hNaZz/AGxnVTr6v0bD6ZfxNC//AFLSP/XwjaehUZV6xb/62rVQ9jKXC8MeXJbacVO6UmPnYAU+12WxJTKsjaeq1THykfWg47tTi3AYc7sfoAfQ3P12NUrji1863Vr81KKj8ptpWijHsMF+7wrBt/lsXmO6WhJttbNH0oC+K8Pbs3hVPHYuKlJ9lE/gKzucaBRE7AAfW9CUoddt7+341qkUaUdtnwYaaabAGgTPtsLeldWZaibxpuP5CuqqQzRN9oXGkutoIhwQqRNulIuYnC/Y1JKVfau9BSfhyRf/ABVE7iNaCXbXruqjag68SogJKjA0E2+VFwDedWXMlFiZWYHKJiepqvUqo56RcXRvv9J+J93xNkE2dSto/tpzD6pFart6otYwqClSppDgS2ylSiWVQrm1ugxXyns646MQy6yha1NuoX92lSoyqBMwLW/GvtX+o6GnVtEPoEKIUjvggZXEkKzASoxOgG1JtLkqUz57jsyEnNmlh0wcQ/lGVRlJyIvGZOn6VM4QgrWhqMrqQtHcMSAfEn7xf7af2qM3w7DoJKnkyppKVDDs51ZkhN+9eMap/NoocYGQBlbqm/CrEvLJ1n8mjKjXaDWEvL0o9mMtSITD4wHIVnxDunA4+VEGOU5GxrEH9k1fYHDOgJUWwnLLa/usoKbgQt5QkASJvtVG3xdxIytqQwCZIYQhv3JSAZvuaWefkytRUrWVKk+fU9a5p/UV/GJk9RGtOLbbgLxSZSTHdyvMDsUtpA/e3NJv8Vw2gbddhWZOYhMG3XOdhvtWcS+kdPQfL+/SjYYLc8NgTAJ3PQCJUR6etc78ryJuoKhfJJ8Fv/vixm7pllqTJIRJ9eaRPoKTxXFX3PG8sjoDb5C1aPgvYIvNJccfKc10hKRMbGSo2Oo9RUeNf6cvISVYdwPQLoWAlR/VMwT5Ej1ol43kyzJ2DhN8mSUpI8/U/wBaB9oA0gSfWhuNkKKVpWlW6VpUlY11SRpI10sTfWuSlQOn8vOK5Pip0zNquTjjY008tdZ/CoJfzQLiTv5R1/u1GYBUrKnmUBYJBJNo0A2q1wnZvErv3ak31UQI0vGp32rRQ9ICkU0rWR5wL+env9KiEa6/4Iveetac9lUo/LYhtsdARIvoJI9LChBHDGtS48RfUgH25QfrWi033gdPsoi1EHW3UQPSBf386Pg+EvrILbSiP1CB6ZiYjSrpntG0i2HwraDoCRfTeAD9aRxvajFknmi+iAEkjfXm/wA0KMfdhgbb7J4giXChtJ/OXNvYR13Gtep4bgmxDuLzHcM+wiBmjf51QrdW5JUcykx4yTqNs2gub38O9KLclInJJtfT36H0+VUtvoMejVHimARdvDlw3IU6YFvXN06ClcT23dulsNNp2CUlSvW/L7RttWcxDJlOWBzXi4ETa8wYGgjb2XWhcFWYAXBAP4bdKuL/AHQ7ZY4zj77mrzhB1CVZRewkJGl9KUS4k6ZZIFsuYmR1NyZpBLAF1EAfpBWhm5i2lSbRzZwIkEynMb9ZJnX3qpQXsVDbjibgnW+gtMfL+xSqnm5m5voon+EHrXjhVAMxa0iY0IJk75vO5vQAFGZUSCNst4AAFrG5+lEdOuxpEnEgmAmJgxt196AtcK8Mdbm5vvF655i0ZCZNpMGIGg/jvNDUhWYlVjJ9zt6itlFFUFidARaTG2/8aVkzACpOnodBRsygqc9wCRoYMG0+m/pSy0kDXy5QIPr/AH0q4oaGGnCLWtrInp/WuoLDBANwPU/08/xryhqI8HjPA8U5KksOZbnMtORMdcy4H1ozfAD/AMj7afJGZw/MAI/eq/4njRHdIWpaZlxxRUVOqHrcNjYT561Xpc9vr/WnLyZdIHqPoGzwrDJ17539ZSWx8k5j9afa7tPgYZRGhKM6v+zma9Klzz3teP5VFK80C2l5PTesZT1Jcshzk+y0fxylDKt0kbJKuX2GlKqCRoPaOvSgKWALGR5fyFEHW8WvGa+9p1sax2EhWcSR087CfPWiOYo6Rbznp8o0pdCptBBG2n0A/uL0ywnNACVLMwQlJP8AI7n5UnBXdAc08q0n5WHud6YLB+I9NxaYnTp/KnsNwDEKiGSB1XA89JJ+lWv/AOYyiX8Q23bQQo67SR12GtS4MdMpeHYHvlBCTFplSeXy+ZO3StH2T7JKnvsa5nXoGmyQ2hI0TIuesCBfeq9DzDCvu3VLSE5lLXbSSY5RYD1rT8C4ih1CVoUFJOhB/u9ej42moxv2b6caRpMfxNOFw63oJQ0gnInokWSmdOnSqDB9v3nboYQhP6SlKP0CYona1t13AvNsoK3FBMJBAJhxBVEmJyg23rBcJ4pkJacSULTYpWClQ9Qb11Gh9heYY4hhxnTrIsedtQ1AVqD+IivnXEXMJhXFt/ZFLcb1U5GU7ggkqsZnQa1sOwmGcShbpMIdKShBH5oIK/LMMo8wkHpWC7ZPF7iGJEFPdFCQDuO6SSQNwSfLX2rl8lVHcZ6ixYTE9r3UgJSlLI6ADoTvbQH4ZqvxfG3FiXHlhMXgr0taEjKP69IpJvDJiVLBsYGs+EGDPQqOmiaGtdoBA0B2teCTJ8xFee5N9mDbPcUyBESeoOtrQToTc/Kl3kLUQTl1g3tAMa/Pb0qagUmQpSgZ6FJAsLiJ2+nuJ1Z8JCJMAERGwmTveP8AMU4r/oEwQvc7pmbkg2kibcwiwFjppXret0qIBzeFRzC4JFxFusaa1429zSLWKlAQAQoEQAZHlJrr5yYsYTcj4VQDAiZjam0BFrcZYBvaJkAi4Pr6163zZssCAbgiRBOXMADck5RGtvbxAVmkJERdU20EaDoD7g+4WVHMoKRJt12B3NouDGuvWmo9joMEjwgESE+UZkiNRAmfLb1oBChOpAi2ZKfWCLRqPORUlN6kp2CgkAyLHLqbaJGvlpauRKdEhMi8mEgkgSBMwNrfzqq9BQujEA/HBndRAuIIEC/t18qC8g35gBAOpOnKT7fgNKacVoqQZttaQqyiNTJR63911K25Ra+UEixj+fyq0AsUqIMaa2ECQbRa0T9RXgSoEEE6EmbA/wB83nR3I3OmpAsSdpnyPyqK1ibn3EEG4+e4qk2OwLyieWVGDNiRc6nXXz/xQQ0BMk2HX+e1Od8IEQREQIBsTN4MXnaoO54Ucsga3TG+2swki3QeVUm+BiTht4SNBtH+P72rwqHX1/vfWm8v6MbXm5gW8PmD8qAHIgwLf3pVWBBtf93FeUdl2FEE28vL031r2i2AYev9+sRXifLfqfPaBWi//MpbH/kYplF9AZVHvB+hro4a2Ih18jXKMonofDNoteoJooO82Os7gRA2vvT2EwDrg+7ZWbSDBCdbmTAqxb7QIT+QwbaZMZiApR6zAHymlsX2lxK9Xii48ACB7kc0GNZpUgpDrXZF9SZdW02J1UTrbpI2Fiaab4Xg2p7zF59eVodNbpmss8VqVKlKUZglUqNzPxG+x2qaElSTMAxpte40Ntfr50mgNQviuBb/ACeGKzpmckk31glW0mYFRe7VvFI7sIbnRKE3ANr6iZnb8RWcgqMBVjeSTAnwkEeR+lcpQSpJCdAPFHzg7RN6VPhAWT/GHlnnfURcm5gTvAIHvS2FdEflFbyIGwtl9QKAVEqMkBMpPTa3l/CgqUoEBNyoiYtJAm/WxN/WlsvDFRDtK8oskJPTNBvlmfxI9hSPYPiTjWMZSlakoWsJWkHlUD1HXzo+IxRSnKRmFiQRBOaZt6Eig8KwbSXEuZl8qgoAECIMiZFdujiNM6IcUffMJiaYxWEYeyqdaQsoukqSCUkXsenlpWG4f2jQE5lKEAEk9ABJJGugOk6VQdof9UjGTBi+7qxb9hJ/FXy3rU0PuKcRXxftetJ4hiVBXiWgGFaBLSE3jzCqXw3+pmKcYVnQ2FzlSpOYZp1JTfy0NyfWqnDIWTnWQoySbnN4jmJIgmLmfTyrn12nHaZajxQ228ZKySRcD4ibTBiYIB+QOtc+VEchzCJMDrYCSNZKj7HrS+dSrqUCOg0iLAxEfMbe03HAAU63mUruNhExzECZ8/WuPbkwoYZxa0k6aIUJPSFZZ2GsaRaiB5K0nKU7pAJA6kHyAgGZ9Ii6mFxJERCQIMZp9pEdDN/xu2vDOTKoAEgxAEgAGTv8I3i+m8ySQCWJbUoWna+aRYgHMNhAJP08x4hLkKUkosTBkzlAEECYixUNxO+03GiJKiMwGYXFwQI2scwj/NSQpMFMnW8AmVGeW4kkyIHlvVp0M9SgCVgkgwYM5dpGw6Drc+lDcYAGY5t9CbTyi51MjQ+duk1LSEySQBYE+IaAE+UynyJteoYjDpygAqMTcpUZmJCoFoEfMUkAUslNwFSmIkK8UiQdrAkGdk9TQVBMaGc0A5RHMJ3Nj77V6pYUCCdUqtlgGd9NNTNxaiqEmUkwrMkAImJkkGfYX6k0cchQDEYY2KdCJgqAHqNJ0H9zUFCQZSreSCenTQXAt0nWpmBchSgZBJIGwA0G2ZR86Bnk2TYKMbDmJUQEDaTpteqQAnGZ2A0kgyQSLxcDz/jUEsX5b+t5HlU1nS0mBJjW9p61AqUZEGY3gQN5B9vlVpsZ79mgQCAdJO15MX1j+RoSm41M31Ogjb3Ij3ois4iUyDMQQTAm9pMWi42G0V68/KfCBJCrlVwRb1kR8hTyMGALTe8WER5X1sNutDBFrddTG9j/AE8q5T6pHKkegJ9uo/pUvtCswJIOllJB8wcptB6VVMKIoQJm34GuqTSSomEknXlB8q6iwJOKyiQBqff3969zkSQSIAtJ6TXV1IkklBC1Cba77+9HDEEiTqB9RcDa5mva6pmwZB2BNvMXPyPXX/NRbczEAAJuBpIvA0murqa4GuBtnD8uaTe8bCylHX9T60MpBJTe0iZM2uT0vXV1Z3kGEw6QZMCQAq999PTX50rxQ5RAtfLa0yTM9f611dVx/Ia6KfELJIk+XyqIBEQa8rq61wajLGKWJhX09BQWsCgGYm8fO/8ACurqTYWPsQE5oEgDa2pqaMUpShsU77mCmPSPKurqzik+TNjaXibSQnoD6ED0k0XCETBSDmECZtBIve4tp6V7XVjNEMZcwOUK5ieSSNiZEn1JJNRViimDfab35eWQdjBGnT5dXVms8g+R11sKIIKkzax8/Peb0stgDNNzZXqEKSnKfUmfavK6sk2lgGQGHShagJgoNjfQkV6nESEqCUjmiLkGIG56fhXV1aLNWD5BHEE2J6DpMzrG99aiJKrkHeSPNQ6+U+9e11OuRdhUsw4pBMm9wAPpfrQzgwLhShOtxOpsDFhbSvK6s3JoZ6+2QSConlOlpza9bX+lLP4LLCkqImdpNiRr6Curq005O0MYa4ekpCvbTzvN/X0pbE4RItqZuflcdP8APWurqdsGKEwdASkgXm8m1gdrfKvHmzOUK+I3j80W+h+ldXVshhGcGTl5yJSTppcDrXtdXUDR/9k=",
          ubicacion: "Barrio El Prado, Bogotá"
        },
        {
          id: 2,
          nombre: "Partido 2",
          fecha: "2025-04-12",
          hora: "18:00",
          apuesta: "$30.000",
          logo: "logo2.png"
        }
      ],
      partidosFinalizados: [
        {
          id: 3,
          nombre: "Partido 3",
          fecha: "2025-03-28",
          hora: "15:00",
          apuesta: "$40.000",
          logo: "logo3.png"
        }
      ]
    };
  },
  methods: {
    verDetalle(partido) {
      this.partidoSeleccionado = partido;
      this.modalActivo = true;
    }
  }
};
</script>

<style scoped>
.container {
  display: flex;
  flex-direction: column;
  gap: 20px;
  padding: 20px;
  background-color: #1c1c1c;
  color: #ffffff;
  font-family: 'Segoe UI', sans-serif;
  border: solid white 1px;
}

.partidos-section {
  background: #000000;
  padding: 20px;
  border-radius: 12px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.3);
  border-left: 6px solid gold;
  transition: transform 0.3s ease;
  border-bottom: 2px white solid;
  box-shadow: 0 0 10px;

}

.partidos-section:hover {
  transform: scale(1.01);
  box-shadow: 0 0 10px orange;
}

.card {
  display: flex;
  align-items: center;
  justify-content: space-between;
  background: #1a1a1a; /* Negro suave */
  color: #f5f5f5; /* Blanco grisáceo para texto */
  padding: 20px;
  margin: 20px 0;
  border-radius: 16px;
  border: 1px solid #333;
  box-shadow: 0 4px 12px rgba(255, 215, 0, 0.2);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  backdrop-filter: blur(3px);
  position: relative;
  overflow: hidden;
  font-family: Verdana, Geneva, Tahoma, sans-serif;
  border: 1px solid rgb(70, 70, 70);
}

.card::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(
    120deg,
    transparent,
    rgba(255, 215, 0, 0.1),
    transparent
  );
  transition: all 0.6s ease-in-out;
}

.card:hover::before {
  left: 100%;
}

.card:hover {
  transform: translateY(-6px);
  box-shadow: 0 8px 20px rgba(255, 215, 0, 0.3);
}


.logo {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  border: 2px solid gold;
  object-fit: cover;
  transition: transform 0.3s ease;
}

.logo:hover {
  transform: rotate(5deg) scale(1.1);
}

.info {
  flex-grow: 1;
  margin-left: 15px;
}

.btn-detalle {
  background: linear-gradient(135deg, #6d6d6d, #000000); /* Dorado degradado */
  color: #ffffff;
  padding: 5px 5px;
  border: 2px solid #ffcc00;
  border-radius: 10px;
  font-weight: 100px;
  letter-spacing: 1px;
  text-transform: uppercase;
  cursor: pointer;
  transition: all 0.3s ease;
  margin-right: 5px;
  box-shadow: 0 4px 10px rgba(255, 215, 0, 0.3);
}

.btn-detalle:hover {
  background: #525252;
  color: #ffcc00;
  transform: scale(1.08);
  box-shadow: 0 6px 18px rgba(255, 255, 255, 0.4);
}
.btn-detalle2 {
  background: linear-gradient(135deg, #ffcc00, #b8860b); /* Dorado degradado */
  color: #000;
  padding: 5px 5px;
  border: 2px solid #ffcc00;
  border-radius: 10px;
  font-weight: 100px;
  letter-spacing: 1px;
  text-transform: uppercase;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 4px 10px rgba(255, 215, 0, 0.3);
}

.btn-detalle2:hover {
  background: #5d5d5d;
  color: #ffcc00;
  transform: scale(1.08);
  box-shadow: 0 6px 18px rgba(255, 255, 255, 0.4);
}

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.7);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
  animation: fadeIn 0.3s ease;
}

.modal {
  background: #f0f0f0;
  color: #000;
  padding: 25px;
  border-radius: 12px;
  max-width: 550px;
  width: 95%;
  position: relative;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.4);
  animation: slideUp 0.4s ease;
}

.cerrar {
  position: absolute;
  top: 10px;
  right: 10px;
  border: none;
  background: crimson;
  color: white;
  border-radius: 50%;
  width: 30px;
  height: 30px;
  font-weight: bold;
  cursor: pointer;
  transition: transform 0.2s ease;
}

.cerrar:hover {
  transform: rotate(90deg);
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

@keyframes slideUp {
  from {
    transform: translateY(30px);
    opacity: 0;
  }
  to {
    transform: translateY(0);
    opacity: 1;
  }
}
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.85);
  backdrop-filter: blur(6px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 999;
  animation: overlayFade 0.4s ease-in-out;
}

.modal {
  background: linear-gradient(145deg, #1a1a1a, #2c2c2c);
  color: #f2f2f2;
  padding: 35px;
  border-radius: 20px;
  max-width: 600px;
  width: 92%;
  position: relative;
  box-shadow: 0 0 30px rgba(255, 215, 0, 0.2),
              0 0 8px rgba(255, 255, 255, 0.05);
  border: 1px solid #444;
  animation: modalPop 0.4s ease;
}
.modal h2 {
  font-size: 30px;
  color: #000000;
  margin-bottom: 20px;
  text-align: center;
  text-shadow: 1px 1px 3px #000;
  border-bottom: 2px solid #ffcc00;
  padding-bottom: 12px;
  letter-spacing: 1px;
  font-family: Georgia, 'Times New Roman', Times, serif;
  position: relative;

  /* Borde blanco fino */
  -webkit-text-stroke: 0.5px #ffffff;
}


.modal p {
  font-size: 17px;
  color: #d0d0d0;
  margin: 14px 0;
  line-height: 1.7;
  font-family: Cambria, Cochin, Georgia, Times, 'Times New Roman', serif;
}

.modal p strong {
  color: #ffd500;
  -webkit-text-stroke: 0.5px #ffffff;
  font-size: 20px;
}

.imagen-cancha {
  width: 20%;
  margin: 20px 0;
  border-radius: 12px;
  border: 3px solid #ffd700;
  box-shadow: 0 0 20px rgba(255, 215, 0, 0.3);
  cursor: pointer;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.imagen-cancha:hover {
  transform: scale(1.05);
  box-shadow: 0 0 30px rgba(255, 215, 0, 0.5);
}

.modal-img {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background: rgba(0, 0, 0, 0.85);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 9999;
}

.modal-img img {
  width: 600px;
  height: 500px;
  border: 5px solid #ffd700;
  border-radius: 16px;
  box-shadow: 0 0 50px rgba(255, 215, 0, 0.6);
  transition: transform 0.3s ease;
}


.imagen-cancha:hover {
  transform: scale(1.05);
  box-shadow: 0 0 30px rgba(255, 215, 0, 0.5);
}

.cerrar {
  position: absolute;
  top: 12px;
  right: 12px;
  background: #ff1a1a;
  color: white;
  border: none;
  border-radius: 50%;
  width: 34px;
  height: 34px;
  font-size: 18px;
  font-weight: bold;
  cursor: pointer;
  box-shadow: 0 0 8px rgba(255, 0, 0, 0.4);
  transition: background 0.3s ease, transform 0.3s ease;
}

.cerrar:hover {
  background: #cc0000;
  transform: scale(1.2) rotate(15deg);
}

@keyframes modalPop {
  from {
    opacity: 0;
    transform: scale(0.8) translateY(-20px);
  }
  to {
    opacity: 1;
    transform: scale(1) translateY(0);
  }
}

@keyframes overlayFade {
  from {
    background: rgba(0, 0, 0, 0);
  }
  to {
    background: rgba(0, 0, 0, 0.85);
  }
}

@keyframes fadeIn {
  from {
    transform: scale(0.8);
    opacity: 0;
  }
  to {
    transform: scale(1);
    opacity: 1;
  }
}
.title {
  font-size: 28px;
  font-weight: 900;
  color: #000000; /* Dorado elegante */
  text-align: center;
  text-transform: uppercase;
  letter-spacing: 2.5px;
  margin-bottom: 15px;
  position: relative;
  padding-bottom: 10px;

  /* Borde negro al texto */
  text-shadow: 
    -1px -1px 0 #ffffff,  
     1px -1px 0 #ffffff,
    -1px  1px 0 #ffffff,
     1px  1px 0 #ffffff;
}

.title::after {
  content: "";
  display: block;
  width: 60px;
  height: 3px;
  background: #ffbf00;
  margin: 5px auto 0;
  border-radius: 5px;
  transition: width 0.3s ease-in-out;
}

.title:hover::after {
  width: 100px;
}
.boton-volver {
  padding: 10px 25px;
  background-color: black;
  color: gold;
  border: 2px solid gold;
  font-size: 16px;
  font-weight: bold;
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 4px 10px rgba(255, 215, 0, 0.3);
}

.boton-volver:hover {
  background-color: gold;
  color: black;
  border: 2px solid white;
  box-shadow: 0 6px 15px rgba(255, 255, 255, 0.4);
}
.tit {
  font-size: 22px;
  font-weight: 700;
  color: #000000; /* Dorado intenso */
  margin: 0 0 10px 0;
  text-transform: uppercase;
  letter-spacing: 1.5px;
  text-shadow: 
    -1px -1px 0 #abaaaa, 
     1px -1px 0 #565656, 
    -1px  1px 0 #000, 
     1px  1px 0 #000; /* Contorno negro */
  transition: color 0.3s ease;
}

.tit:hover {
  color: #ffffff; /* Cambia a blanco al pasar el mouse */
}

</style>