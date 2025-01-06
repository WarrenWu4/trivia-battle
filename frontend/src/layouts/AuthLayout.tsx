import { redirect, useParams, Outlet } from "react-router-dom";
import MainLayout from "./MainLayout";
import { createContext, useEffect, useState } from "react";
import { PlayerData } from "../lib/player";

export const UserContext = createContext<PlayerData | null>(null);

export default function AuthLayout() {

    const { gameId } = useParams<{ gameId: string }>();
    const username = localStorage.getItem(`domain-player-${gameId}`);
    const [player, setPlayer] = useState<PlayerData | null>(null);

    async function checkPlayer(username: string, gameId: string) {
        const response = await fetch(`http://localhost:5000/player/${gameId}/${username}`, {
            method: "GET",
            headers: {
                "Content-Type": "application/json",
            },
        });
        const data = await response.json();
        if (!data.success) {
            redirect(`/join/${gameId}`);
            return
        }
        setPlayer({
            username: data.player.username,
            currentQuestion: data.player.current_question,
            score: data.player.score,
            correct: data.player.correct
        });
    }

    useEffect(() => {
        if (username !== null && gameId !== undefined) {
            checkPlayer(username, gameId);
        } else {
            redirect(`/join/${gameId}`);
        }
    }, []);

    return (
        <MainLayout>
            {player === null ? <></> : 
            <UserContext.Provider value={player}> 
                <Outlet />
            </UserContext.Provider>
            }
        </MainLayout>
    );
}
