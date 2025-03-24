const { Server } = require("socket.io");
const http = require("http");
const express = require("express");
const cors = require("cors");

const app = express();
app.use(cors());
app.use(express.json());

// Crear servidor HTTP para Socket.IO
const server = http.createServer(app);
const io = new Server(server, {
  cors: { origin: "*" }
});

// Eventos de WebSocket
io.on("connection", (socket) => {
  console.log("🟢 Usuario conectado:", socket.id);

  socket.on("joinRoom", (team_Id) => {
    socket.join(team_Id);
    console.log(`✅ Usuario ${socket.id} se unió a la sala ${team_Id}`);
  });

  socket.on("sendMessage", (message) => {
    console.log("📩 Mensaje recibido:", message);
    io.to(message.team_id).emit("nuevoMensaje", message);
  });

  socket.on("disconnect", () => {
    console.log("🔴 Usuario desconectado:", socket.id);
  });
});

// Iniciar servidor Socket.IO en el puerto 9000
server.listen(9000, () => {
  console.log("🚀 Servidor de WebSockets corriendo en http://localhost:9000");
});
