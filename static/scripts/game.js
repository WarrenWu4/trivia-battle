document.addEventListener("DOMContentLoaded", () => {
    console.log(`ROOM: ${room_id}`);
    const socket = io();

    socket.on('connect', function() {
        // on socket connection fetch username from url query and check that it exists
        console.log('connected to server');
        socket.emit('join', {room_id: room_id})
    });

    socket.on('disconnect', function() {
        console.log('disconnected from server');
    });

    socket.on('client_start_game', function() {
        // reload the client with the updated game state
        window.location.reload();
    });

    if (game_state === 'waiting') {
        // check local storage for if there's a username associated with the game room
        const username = localStorage.getItem(room_id+'_username');
        console.log(connections);
        // if not prompt for a username
        if (!username && connections > 0){
            localStorage.setItem(room_id+'_username', username);
            document.getElementById('popup').style.display = 'grid';
        }
        
        socket.on('update_connections', function(data) {
            document.getElementById('num_players').innerText = data.connections
        })

        socket.on('update_players', function(data) {
            document.getElementById('players').innerHTML = data.players.map(player => `<p class='player'>${player}</p>`);
            document.getElementById('popup').style.display = 'none';
        })
    
        document.getElementById('start-game').addEventListener('click', () => {
            socket.emit('start_game', {room_id: room_id});
        })
        document.getElementById('popup-btn').addEventListener('click', () => {
            const username = document.getElementById('username').value;
            socket.emit('add_player', {room_id: room_id, username: username})
        })
    } else {
        const answerIds = ['answer1', 'answer2', 'answer3', 'answer4']
        answerIds.map((id, idx) => {
            document.getElementById(id).addEventListener('click', () => {         
                socket.emit('answer', {room_id: room_id, username:'', answer: idx+1});
            })
        });
    }
});