document.addEventListener('DOMContentLoaded', function() {

    document.querySelector('#my-form').onsubmit = function() {
        const message = document.querySelector('#message-to-send').value;
        alert(`Hello ${message}!`);
    };
});
/*
document.addEventListener('DOMContentLoaded', () => {

    // Connect to websocket
    var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);

    // When connected, configure buttons
    socket.on('connect', () => {

        // Each button should emit a "submit vote" event
        document.querySelectorAll('button').forEach(button => {
            button.onclick = () => {
                const selection = button.dataset.vote;
                socket.emit('submit vote', {'selection': selection});
            };
        });
    });

    // When a new vote is announced, add to the unordered list
    socket.on('announce vote', data => {
        const p = document.createElement('p');
        const div = document.createElement('div');
        const span = document.createElement('span');
        const h5 = document.createElement('h5');     
        div.className = 'chat-container';
        span.className = 'time-right';
        h5.innerHTML = `Arsalan`;
        span.innerHTML = `11:01`;
        p.innerHTML = `Vote recorded: ${data.selection}`;
        div.appendChild(h5)
        div.appendChild(p)
        div.appendChild(span)
        document.querySelector('#votes').append(div);
    });
});

*/

