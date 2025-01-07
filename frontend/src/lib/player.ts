export interface PlayerData {
    username: string | null;
    currentQuestion: number;
    score: number;
    correct: number;
}

export async function updatePlayerData(gameId: string, playerData: PlayerData): Promise<boolean> {
    const res = await fetch(`${import.meta.env.VITE_BACKEND_URL}/player/${gameId}/${playerData.username}`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({
            "current_question": playerData.currentQuestion,
            "score": playerData.score,
            "correct": playerData.correct,
        }),
    })
    if (res.ok) {
        const data = await res.json();
        if (data.success) {
            return true;
        }
    }
    return false;
}

export async function getAllPlayersFromGame(gameId: string): Promise<PlayerData[] | null> {
    const res = await fetch(`${import.meta.env.VITE_BACKEND_URL}/players/${gameId}`, {
        method: "GET",
        headers: {
            "Content-Type": "application/json",
        }
    })
    if (res.ok) {
        const data = await res.json();
        if (data.success) {
            const players: PlayerData[] = data.players.map((player: any) => ({
                username: player.username,
                currentQuestion: player.current_question,
                score: player.score,
                correct: player.correct,
            }));
            return players
        }
    }
    return null
}

export async function getPlayerData(gameId: string, username: string): Promise<PlayerData | null> {
    const response = await fetch("http://localhost:5000/api/player", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ gameId: gameId, username: username }),
    });
    if (response.ok) {
        const data = await response.json();
        return data;
    }
    return null;
}

export function getUsername(gameId: string): string | null {
    return localStorage.getItem(`domain-player-${gameId}`);
}