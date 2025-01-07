import { useNavigate, useParams } from "react-router-dom";
import { useContext, useEffect, useState } from "react";
import { UserContext } from "../layouts/AuthLayout";
import Navbar from "../components/Navbar";
import { checkAnswer, GameConfig, GameData, getGameConfig, getGameData } from "../lib/game";
import { PlayerData, updatePlayerData } from "../lib/player";

export default function Game() {
    const navigate = useNavigate();
    const { gameId } = useParams<{ gameId: string }>();
    const [gameConfig, setGameConfig] = useState<GameConfig | null>(null);
    const [gameData, setGameData] = useState<GameData | null>(null);
    const [qTime, setQTime] = useState<number | null>(null);

    const user = useContext(UserContext);
    const [playerData, setPlayerData] = useState<PlayerData | null>(null)
    const [correct, setCorrect] = useState<boolean | null>(null);
    const [answerState, setAnswerState] = useState<boolean>(false);

    async function checkAns(e: React.MouseEvent<HTMLButtonElement>, currentQuestion: number, answer: string) {
        e.preventDefault();
        if (gameId === undefined) {
            navigate("/error"); return;
        }
        const correct: boolean | null = await checkAnswer(gameId, currentQuestion, answer);
        if (correct !== null) {
            if (correct) {
                setPlayerData((prev) => ({
                    ...prev!,
                    score: prev!.score + 1,
                    correct: prev!.correct + 1,
                }))
            } else {
                setPlayerData((prev) => ({
                    ...prev!,
                    score: prev!.score - 1,
                }))
            }
            setCorrect(correct);
            setAnswerState(true);
            setQTime(5);
        } else {
            navigate('/error'); return;
        }
    }

    async function nextQ() {
        const res = await updatePlayerData(gameId!, {
            ...playerData!,
            currentQuestion: playerData!.currentQuestion + 1,
        });
        if (!res) {
            navigate('/error'); return 0;
        }
        if (playerData!.currentQuestion + 1 === gameConfig!.questionNum) {
            navigate(`/game/${gameId}/over`); return 0;
        }
        setPlayerData((prev) => ({
            ...prev!,
            currentQuestion: prev!.currentQuestion + 1,
        }))
    }

    useEffect(() => {
        let timerId: any;
        if (qTime && qTime > 0) {
            timerId = setInterval(() => {
                setQTime((prev) => {
                    if (prev && prev - 1 == 0) {
                        clearInterval(timerId);
                        if (answerState) {
                            nextQ();
                            setCorrect(null);
                            setAnswerState(false);
                            setQTime(gameConfig!.questionTimer);
                        } else {
                            setCorrect(false);
                            setAnswerState(true);
                            setQTime(5);
                        }
                    }
                    return prev ? prev - 1 : 0;
                });
            }, 1000)
        }
        return () => {
            if (timerId) {
                clearInterval(timerId);
            }
        }
    }, [qTime])

    useEffect(() => {
        async function fetchData() {
            if (gameId === undefined) {
                navigate("/error"); return;
            }
            if (user === null) {
                navigate(`/join/${gameId}`); return;
            }
            const gameConfig = await getGameConfig(gameId);
            const gameData = await getGameData(gameId);
            if (gameConfig === null || gameData === null) {
                navigate("/error"); return;
            }
            if (user.currentQuestion >= gameConfig.questionNum) {
                navigate(`/game/${gameId}/over`); return;
            }
            setGameConfig(gameConfig);
            setGameData(gameData);
            setPlayerData(user);
            setQTime(gameConfig.questionTimer);
        }
        fetchData();
    }, [])

    return (
        <>
            <Navbar title="TRIVIA BATTLE"/>
            {playerData === null || gameData === null || gameConfig === null || qTime === null ?
            <></>
            :      
            <TriviaDisplay
                question={gameData.questions[playerData.currentQuestion]}
                answers={gameData.answers[playerData.currentQuestion]}
                currentQuestion={playerData.currentQuestion}
                score={playerData.score}
                timer={qTime}
                handleAnswerCheck={checkAns}
                correct={correct}
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
    correct: boolean | null;
}

function TriviaDisplay({ question, answers, currentQuestion, score, timer, handleAnswerCheck, correct }: TriviaDisplayProps) {

    return (
    <div className="w-full flex flex-col gap-y-8">
        <div className="retro px-4 py-2 flex justify-between items-center">
            <p>
                Q{currentQuestion + 1}
            </p>
            <p>
                {score} pts 
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
            <p>
                {correct !== null ? correct ? "Correct" : "Incorrect" : ""}
            </p>
        </div>
        <div className="retro px-4 py-2 flex items-center justify-center">
            <p>
                {correct === null ?
                `${timer} sec remaining`
                :
                `${timer} sec until next question`
                }
            </p>
        </div>
    </div>
    )
}
