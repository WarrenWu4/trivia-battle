const username = localStorage.getItem('domain_username') || '';
checkPlayerExists(username);

function promptUsername() {
    document.getElementById('content').style.display = 'none';
    document.getElementById('modal').style.display = 'flex';
}

async function addPlayer() {
    const usernameForm = document.getElementById('username-form');
    usernameForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const username = document.getElementById('username').value;
        const response = await fetch(`/game/${game_id}/add-player`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ username })
        });
        if (response.ok) {
            localStorage.setItem('domain_username', username);
            document.getElementById('content').style.display = 'flex';
            document.getElementById('modal').style.display = 'none';
        }
    });
}

async function checkPlayerExists(username) {
    const response = await fetch(`/game/${game_id}/check-player`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ username })
    });
    const data = await response.json();
    if (data.ok && !data.exists) {
        promptUsername();
        addPlayer();
    }
}

const startBtn = document.getElementById('startBtn');
startBtn.addEventListener('click', async () => {
    const response = await fetch(`/game/${game_id}/start`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({})
    });
    if (response.ok) {
        window.location.href = `/game/${game_id}`;
    }
});