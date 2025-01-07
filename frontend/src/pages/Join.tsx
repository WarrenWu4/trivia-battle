import { useState } from "react";
import names from "../assets/data/names.json";
import MainLayout from "../layouts/MainLayout";
import Navbar from "../components/Navbar";
import { useNavigate, useParams } from "react-router-dom";

export default function Join() {
    const navigate = useNavigate();
    const { gameId } = useParams<{ gameId: string}>();
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

    async function handleSubmit(e: React.FormEvent<HTMLFormElement>) {
        e.preventDefault();
        const res = await fetch(`${import.meta.env.VITE_BACKEND_URL}/player/create`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                game_id: gameId,
                username: formData.username,
            }),
        });
        const data = await res.json();
        if (data.success) {
            localStorage.setItem(`domain-player-${gameId}`, formData.username);
            navigate(`/game/${gameId}`); return;
        }
        navigate("/error"); return;
    }

    return (
        <MainLayout>
            <Navbar title="JOIN GAME"/>
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
        </MainLayout>
    )
}