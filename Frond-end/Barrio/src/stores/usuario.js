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
      equipo_tiene: "",
      esLider: false, // Nuevo campo
    }
  }),
  actions: {
    async setUsuario(userData) {
      this.usuario = { ...userData };

      try {
        const response = await axios.get(`http://127.0.0.1:8000/equipos/es_capitan/${userData.documento}`);
        this.usuario.esLider = response.data; // Devuelve true o false
      } catch (error) {
        console.error("Error al verificar si el usuario es líder:", error);
      }
    },
    limpiarUsuario() {
      this.usuario = {
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
        equipo_tiene: "",
        esLider: false,
      };
    }
  },
  actualizarEquipo(equipoId) {
    this.usuario.equipo_tiene = equipoId;
  },  
  persist: true, // Asegura la persistencia en localStorage
});
