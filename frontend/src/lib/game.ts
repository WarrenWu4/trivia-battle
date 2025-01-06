export interface CreateGameForm {
    gameId: string;
    username: string;
    gameMode: "FFA" | "Team";
    playerNum: number;
    questionNum: number;
    questionTimer: number;
    category: number;
    difficulty: "Easy" | "Medium" | "Hard";
}

export interface GameConfig {
    gameMode: "FFA" | "Team";
    playerNum: number;
    questionNum: number;
    questionTimer: number;
    category: number;
    difficulty: "Easy" | "Medium" | "Hard";
}

export interface GameData {
    questions: string[];
    answers: string[];
}

export async function getGameConfig(gameId: string): Promise<GameConfig | null> {
    const response = await fetch(`http://localhost:5000/api/game/${gameId}/config`, {
        method: "GET",
        headers: {
            "Content-Type": "application/json",
        },
    });
    if (response.ok) {
        const data = await response.json();
        return data;
    }
    return null;
}

export async function getGameData(gameId: string): Promise<GameData | null> {
    const response = await fetch(`http://localhost:5000/api/game/${gameId}/data`, {
        method: "GET",
        headers: {
            "Content-Type": "application/json",
        },
    });
    if (response.ok) {
        const data = await response.json();
        return data;
    }
    return null;
}