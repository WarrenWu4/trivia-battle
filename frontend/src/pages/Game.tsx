import { redirect, useParams } from "react-router-dom";
import { useContext, useEffect, useState } from "react";
import { base64Decoder, base64Encoder } from "../lib/base64Functions";
import { UserContext } from "../layouts/AuthLayout";

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

    const [playerData, setPlayerData] = useState<PlayerData | null>(null)
    const user = useContext(UserContext);

    async function getQuestion(questionNumber: number) {
        const response = await fetch(`http://localhost:5000/game/${gameId}/question/${questionNumber}`, {
            method: "GET",
            headers: {
                "Content-Type": "application/json",
            }
        })
        const data = await response.json();
        if (!data.success) {
            redirect(`/error`);
            return
        }
        setQuestion(base64Decoder(data.trivia.question));
        setAnswers(data.trivia.answers.map((answers: string) => base64Decoder(answers)));
    }
    
    async function checkAnswer(e: React.MouseEvent<HTMLButtonElement>, currentQuestion: number, answer: string) {
        e.preventDefault();
        const response = await fetch(`http://localhost:5000/game/${gameId}/question/${currentQuestion}/check`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({answer: base64Encoder(answer)})
        })
        const data = await response.json();
        if (!data.success) {
            redirect(`/error`);
            return
        }
        if (data.correct) {
            console.log("correct answer");
        } else {
            console.log("incorrect answer");
        }
    } 

    useEffect(() => {
        if (user !== null) {
            setPlayerData(user);
            getQuestion(user.currentQuestion);
        } else {
            redirect(`/join/${gameId}`);
        }
    }, [])

    return (
        <>
            
            {playerData === null ?
            <></>
            :      
            <TriviaDisplay
                question={question}
                answers={answers}
                currentQuestion={playerData.currentQuestion}
                score={playerData.score}
                timer={timer}
                handleAnswerCheck={checkAnswer}
            />
            }

        </>
    )
}

interface TriviaDisplayProps {
    question: string;
    answers: string[];
    currentQuestion: number;
    score: number;
    timer: number;
    handleAnswerCheck: (e: React.MouseEvent<HTMLButtonElement>, currentQuestion: number, answer: string) => void;
}

function TriviaDisplay({ question, answers, currentQuestion, score, timer, handleAnswerCheck }: TriviaDisplayProps) {
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
            <p className="w-full text-center break-words">
                {question}
            </p>
            <div className="w-full grid grid-cols-2 gap-4">
                {answers.map((answer: string, index: number) => (
                    <button
                        key={index}
                        onClick={(e) => handleAnswerCheck(e, currentQuestion, answer)}
                        className="text-left w-full"
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
