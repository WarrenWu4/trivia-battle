const answers = ['answer1', 'answer2', 'answer3', 'answer4'];
answers.map(answer => {
    const answerChoice = document.getElementById(answer);
    answerChoice.addEventListener('click', async() => {
        const response = await fetch('/check_answer', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({answer: answer})
        })

    })
})

// document.addEventListener("DOMContentLoaded", () => {
//     console.log(`ROOM: ${game_data.room_id}`);
//     const socket = io();

//     socket.on('connect', function() {
//         // on socket connection fetch username from url query and check that it exists
//         console.log('connected to server');
//         console.log(game_data)
//         socket.emit('join', {room_id: room_id})
//     });

//     socket.on('disconnect', function() {
//         console.log('disconnected from server');
//     });

//     socket.on('client_start_game', function() {
//         // reload the client with the updated game state
//         window.location.reload();
//     });

//     if (game_data.state === 'waiting') {
//         // check local storage for if there's a username associated with the game room
//         const username = localStorage.getItem(room_id+'_username');
//         console.log(connections);
//         // if not prompt for a username
//         if (!username && connections > 0){
//             localStorage.setItem(room_id+'_username', username);
//             document.getElementById('popup').style.display = 'grid';
//         }
        
//         socket.on('update_connections', function(data) {
//             document.getElementById('num_players').innerText = data.connections
//         })

//         socket.on('update_players', function(data) {
//             document.getElementById('players').innerHTML = data.players.map(player => `<p class='player'>${player}</p>`);
//             document.getElementById('popup').style.display = 'none';
//         })
    
//         document.getElementById('start-game').addEventListener('click', () => {
//             socket.emit('start_game', {room_id: room_id});
//         })
//         document.getElementById('popup-btn').addEventListener('click', () => {
//             const username = document.getElementById('username').value;
//             socket.emit('add_player', {room_id: room_id, username: username})
//         })
//     } else {
//     }
// });