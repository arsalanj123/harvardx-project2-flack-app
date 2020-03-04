
document.addEventListener("DOMContentLoaded", () => {
  // Connect to websocket
  var socket = io.connect(
    location.protocol + "//" + document.domain + ":" + location.port
  );

  // When connected, configure buttons
  socket.on("connect", () => {

    document.querySelector("#btnSubmit").addEventListener("click", function() {
      const txtMessage = document.querySelector("#message-to-send");
      socket.emit("submit vote", { selection: txtMessage.value });
    });
  });

  // When a new vote is announced, add to the unordered list
  socket.on("announce vote", data => {
    const p = document.createElement("p");
    const div = document.createElement("div");
    const span = document.createElement("span");
    const h5 = document.createElement("h5");
    div.className = "chat-container";
    span.className = "time-right";
    h5.innerHTML = `Arsalan`;
    span.innerHTML = `11:01`;
    p.innerHTML = `${data.selection}`;
    div.appendChild(h5);
    div.appendChild(p);
    div.appendChild(span);
    document.querySelector("#votes").append(div);
  });
});

