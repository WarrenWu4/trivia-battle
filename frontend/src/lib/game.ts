import { base64Decoder, base64Encoder } from "./base64Functions";

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
    answers: string[][];
}

export async function getGameConfig(gameId: string): Promise<GameConfig | null> {
    const response = await fetch(`${import.meta.env.VITE_BACKEND_URL}/game/${gameId}/config`, {
        method: "GET",
        headers: {
            "Content-Type": "application/json",
        },
    });
    if (response.ok) {
        const data = await response.json();
        if (data.success) {
            const gameConfig:GameConfig = {
                gameMode: data.config.gamemode,
                playerNum: data.config.player_num,
                questionNum: data.config.question_num,
                questionTimer: data.config.question_timer,
                category: data.config.category,
                difficulty: data.config.difficulty,
            };
            return gameConfig;
        }
    }
    return null;
}

export async function getGameData(gameId: string): Promise<GameData | null> {
    const response = await fetch(`${import.meta.env.VITE_BACKEND_URL}/game/${gameId}/questions`, {
        method: "GET",
        headers: {
            "Content-Type": "application/json",
        },
    });
    if (response.ok) {
        const data = await response.json();
        if (data.success) {
            const triviaData: GameData = {
                questions: data.questions.map((question: string) => base64Decoder(question)),
                answers: data.answers.map((choices: string[]) => choices.map((choice: string) => base64Decoder(choice))),
            };
            return triviaData;
        }
    }
    return null;
}

export async function checkAnswer(gameId: string, currentQuestion: number, answer: string): Promise<boolean | null> {
    const response = await fetch(`http://localhost:5000/game/${gameId}/question/${currentQuestion}/check`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({answer: base64Encoder(answer)})
    })
    if (response.ok) {
        const data = await response.json();
        if (data.success) {
            return data.correct;
        }
    }
    return null
}
