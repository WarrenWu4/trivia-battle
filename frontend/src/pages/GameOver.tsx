import { redirect, useParams } from "react-router-dom";
import MainLayout from "../layouts/MainLayout";
import { useContext, useEffect, useState } from "react";
import { getAllPlayersFromGame, PlayerData } from "../lib/player";
import { GameConfig, getGameConfig } from "../lib/game";
import { UserContext } from "../layouts/AuthLayout";
import Navbar from "../components/Navbar";

export default function GameOver() {
    const { gameId } = useParams<{ gameId: string }>();
    const [leaderboard, setLeaderboard] = useState<PlayerData[]>([]);
    const [playerData, setPlayerData] = useState<PlayerData | null>(null);
    const [gameConfig, setGameConfig] = useState<GameConfig | null>(null);
    const user = useContext(UserContext);

    useEffect(() => {
        async function fetchData() {
            if (!gameId || !user) {
                redirect("/error"); return;
            }
            const gameConfig = await getGameConfig(gameId);
            const leaderboardData = await getAllPlayersFromGame(gameId);
            if (!gameConfig || !leaderboardData) {
                redirect("/error"); return;
            }
            setGameConfig(gameConfig);
            setPlayerData(user);
            setLeaderboard(leaderboardData);
        }
        fetchData();
    }, [])

    return (
        <MainLayout>

            <Navbar title="RESULTS"/>

            <div className="w-full flex flex-col gap-y-8">
                <div className="retro p-4 flex flex-col gap-y-4">
                    <p className="font-bold text-center">
                        {playerData ? playerData.correct : "??"}/{gameConfig ? gameConfig.questionNum : "??"} 
                    </p>
                    <a className="px-4 py-2 bg-black text-white text-center dark:bg-white dark:text-black" href="/">
                        CREATE NEW GAME
                    </a>
                </div>
                <div className="retro p-4 flex flex-col gap-y-4">
                    <p className="font-bold text-center">LEADERBOARD</p>
                    <div className="w-full flex font-bold justify-between items-center gap-x-4">
                        <p>Name</p>
                        <p>Score</p>
                    </div>
                    {leaderboard.map((player: any, index: number) => (
                        <div key={index} className="w-full flex justify-between items-center gap-x-4">
                            <p>{player.username}</p>
                            <p>{player.score}</p>
                        </div>
                    ))}
                </div>
            </div>
        
        </MainLayout>
    )
}