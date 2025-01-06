import { redirect, useParams } from "react-router-dom";
import MainLayout from "../layouts/MainLayout";
import { useEffect, useState } from "react";
import { getPlayerData, getUsername, PlayerData } from "../lib/player";

export default function GameOver() {

    const { gameId } = useParams<{ gameId: string }>();
    const [leaderboard, setLeaderboard] = useState([
        {
            name: "Player 1",
            score: 10
        },
        {
            name: "Player 2",
            score: 9
        },
        {
            name: "Player 3",
            score: 8
        }
    ]);
    const [playerData, setPlayerData] = useState<PlayerData | null>(null);
    const [gameConfig, setGameConfig] = useState({});

    useEffect(() => {

        if (!gameId) {
            redirect("/error");
            return
        }

        const username = getUsername(gameId)
        if (!username) {
            redirect("/error");
            return
        }

        async function fetchData(gameId: string, username: string) {
            const data = await getPlayerData(gameId, username)
            if (!data) {
                redirect("/error");
                return
            }
            setPlayerData(data)
        }

        fetchData(gameId, username)

    }, [])

    return (
        <MainLayout>

            <div className="w-full flex flex-col gap-y-8">
                <div className="retro p-4 flex flex-col gap-y-4">
                    <p className="font-bold text-center">
                        {playerData ? playerData.correct : "??"}/{"??"}
                    </p>
                    <a className="px-4 py-2 bg-black text-white text-center" href="/">
                        PLAY AGAIN
                    </a>
                </div>
                <div className="retro p-4 flex flex-col gap-y-4">
                    <p className="font-bold text-center">LEADERBOARD</p>
                    {leaderboard.map((player: any, index: number) => (
                        <div key={index} className="w-full justify-between items-center gap-x-4">
                            <p>{player.name}</p>
                            <p>{player.score}</p>
                        </div>
                    ))}
                </div>
            </div>
        
        </MainLayout>
    )
}