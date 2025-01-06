export interface PlayerData {
    username: string | null;
    currentQuestion: number;
    score: number;
    correct: number;
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