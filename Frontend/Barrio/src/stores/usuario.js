
import { defineStore } from "pinia";
import axios from "axios";

export const useUsuarios = defineStore("usuario", {
  state: () => ({
    usuario: {
      id: "",
      documento: "",
      nombreUsuario: "",
      correo: "",
      ciudad: "",
      descripcion: "",
      fechaNacimiento: "",
      celular: "",
      Edad: "",
      posicion: "",
      fileInput: "",
      equipo_tiene: 0,
      esLider: false,
    },
  }),
  actions: {
    async setUsuario(userData) {
      // Actualiza las propiedades del usuario de forma reactiva
      Object.assign(this.usuario, userData);

      // Verifica si el usuario es líder solo si tiene un equipo
      if (this.usuario.equipo_tiene !== 0) {
        try {
          const response = await axios.get(
            `http://127.0.0.1:8000/es_lider/${this.usuario.documento}`
          );
          this.usuario.esLider = response.data.esLider;
        } catch (error) {
          console.error("Error al verificar si el usuario es líder:", error);
          this.usuario.esLider = false;
        }
      } else {
        this.usuario.esLider = false;
      }
    },

    actualizarEquipo(equipo_tiene) {
      // Actualiza solo la propiedad equipo_tiene y esLider de forma reactiva
      this.usuario.equipo_tiene = equipo_tiene;
      this.usuario.esLider = false;
    },
  },
  persist: true,
});
