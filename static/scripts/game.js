document.addEventListener("DOMContentLoaded", () => {
    const socket = io();

    socket.on('connect', function() {
        // on socket connection fetch username from url query and check that it exists
        const urlParams = new URLSearchParams(window.location.search);
        const username = urlParams.get('username');
        if (!username) {
            const popup = document.getElementById('popup');
            popup.style.display = 'grid';
        }
        console.log('connected to server');
    });

    socket.on('disconnect', function() {
        console.log('disconnected from server');
    });

    socket.on('update_connections', function(data) {
        console.log("emitted")
        const message = document.getElementById('message');
        message.innerHTML = `waiting for players (${data.connections}/2)`;
    })

    document.getElementById("add-user").addEventListener("click", function() {
        const username = document.getElementById("username").value;
        window.history.pushState({join: true}, "", `${window.location.href}?username=${username}`)
        document.getElementById('popup').style.display = 'none';
        socket.emit("join", {room_id: room_id, username: username})
    });
});
