import { useParams } from "react-router-dom";
import MainLayout from "../layouts/MainLayout";
import { useEffect, useState } from "react";
import names from "../assets/data/names.json";

interface PlayerData {
    username: string | null;
    currentQuestion: number;
    score: number;
    correct: number;
}

export default function Game() {

    const { gameId } = useParams<{ gameId: string }>();
    const [question, setQuestion] = useState<string>("");
    const [answers, setAnswers] = useState<string[]>([]);
    const [timer, setTimer] = useState<number>(60);
    const [playerData, setPlayerData] = useState<PlayerData>({
        username: null,
        currentQuestion: 0,
        score: 0,
        correct: 0,
    })

    async function validatePlayer() {
        const player = localStorage.getItem(`domain-player-${gameId}`);
        if (!player) {
            setPlayerData((prev) => ({
                ...prev,
                username: "",
            }));
            return false;
        }
        // check that player is in game database
        const response = await fetch("http://localhost:5000/api/player", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ gameId: gameId, username: player }),
        });
        const data = await response.json();
        console.log(data);
        if (data.success) {
            setPlayerData((prev) => ({
                ...prev,
                username: player,
            }));
            return true;
        } else {
            // if not reset username and prompt username
            setPlayerData((prev) => ({
                ...prev,
                username: "",
            }));
            return false;
        }
    }

    async function getQuestion() {
        const response = await fetch("http://localhost:5000/api/game", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ gameId }),
        })
        const data = await response.json();
        if (data.success) {
        }
        setQuestion((_) => "test");
        setAnswers((_) => ["test1", "test2", "test3", "test4"]);
    }

    useEffect(() => {
        validatePlayer();
        getQuestion();
    }, [])

    return (
        <MainLayout>
            
            {playerData.username === null ?
            <></>
            : playerData.username === "" ?
            <UsernameForm />
            :      
            <TriviaDisplay
                question={question}
                answers={answers}
                currentQuestion={playerData.currentQuestion}
                score={playerData.score}
                timer={timer}
            />
            }

        </MainLayout>
    )
}

interface TriviaDisplayProps {
    question: string;
    answers: string[];
    currentQuestion: number;
    score: number;
    timer: number;
}

function TriviaDisplay({ question, answers, currentQuestion, score, timer }: TriviaDisplayProps) {
    return (
    <div className="w-full flex flex-col gap-y-8">
        <div className="retro px-4 py-2 flex justify-between items-center">
            <p>
                Q{currentQuestion + 1}
            </p>
            <p>
                {timer} sec
            </p>
        </div>
        <div className="retro p-4 flex flex-col items-center gap-y-4">
            <p className="text-center">
                {question}
            </p>
            <div className="w-full grid grid-cols-2 gap-4">
                {answers.map((answer: string, index: number) => (
                    <button
                        key={index}
                        className="text-left w-full px-4 py-2"
                    >
                        {answer}
                    </button>
                ))}
            </div>
        </div>
        <div className="retro px-4 py-2">
            <p>
                {score} pts
            </p>
        </div>
    </div>
    )
}

function UsernameForm() {

    const [formData, setFormData] = useState({
        username: names[Math.floor(Math.random() * names.length)],
    });

    function handleChange(e: React.ChangeEvent<HTMLInputElement>) {
        const { name, value } = e.target;
        setFormData((prev) => ({
            ...prev,
            [name]: value,
        }));
    }

    function handleSubmit(e: React.FormEvent<HTMLFormElement>) {
        e.preventDefault();
    }

    return (
        <form
            className="w-full flex flex-col gap-y-8"
            onSubmit={handleSubmit}
        >
            <div className="w-full flex flex-col gap-y-2">
                <label>Username</label>
                <input
                    name="username"
                    className="retro px-4 py-2 outline-none"
                    type="text"
                    value={formData.username}
                    onChange={handleChange}
                    required
                />
            </div>
            <button className="px-4 py-2 bg-black text-white" type="submit">
                ENTER GAME
            </button>
        </form>
    )
}