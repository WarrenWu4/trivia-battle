import React, { useState } from "react";
import MainLayout from "../layouts/MainLayout";
import { twMerge } from "tailwind-merge";
import categories from "../assets/data/categories.json";
import names from "../assets/data/names.json";

export default function Create() {
    const [formData, setFormData] = useState({
        gameId: crypto.randomUUID().toString(),
        username: names[Math.floor(Math.random() * names.length)],
        gameMode: "FFA",
        playerNum: 1,
        questionNum: 10,
        questionTimer: 60,
        category: "9",
        difficulty: "Easy"
    });
    const inputWrapperClass = "w-full flex flex-col gap-y-2";

    function handleChange(e: React.ChangeEvent<HTMLInputElement>) {
        const { name, value } = e.target;
        setFormData((prev) => ({
            ...prev,
            [name]: value,
        }));
    }

    function handleClick(e: React.MouseEvent<HTMLButtonElement>, name: string, value: string) {
        e.preventDefault();
        setFormData((prev) => ({
            ...prev,
            [name]: value,
        }));
    }

    async function handleSubmit(e: React.FormEvent<HTMLFormElement>) {
        e.preventDefault();
        /**
         * ! validate data
         * gameMode: "FFA" | "Team"
         * questionNum: number, 1-20
         * questionTimer: number, 1-600
         * category: number, 9-32
         * difficulty: "Easy" | "Medium" | "Hard"
         */
        if (!["FFA", "Team"].includes(formData.gameMode)) {
            alert("Invalid game mode");
            return;
        }
        if (formData.questionNum < 1 || formData.questionNum > 20) {
            alert("Invalid number of questions");
            return;
        }
        if (formData.questionTimer < 30 || formData.questionTimer > 600) {
            alert("Invalid question timer");
            return;
        }
        if (!categories.find((category) => category.id === formData.category)) {
            alert("Invalid category");
            return;
        }
        if (!["Easy", "Medium", "Hard"].includes(formData.difficulty)) {
            alert("Invalid difficulty");
            return;
        }
        /**
         * send data to backend
         * upon success:
         *  store username in local storage
         *  redirect to game page
         */
        const response = await fetch("http://localhost:5000/api/create", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(formData),
        });
        const data = await response.json();
        if (data.success) {
            localStorage.setItem(`domain-player-${formData.gameId}`, formData.username);
            window.location.href = `/game/${formData.gameId}`;
        } else {
            alert("Failed to create game");
        }
    }

    return (
        <MainLayout>

            <nav className="flex items-center justify-between pb-2 border-b-4 border-black mb-4">
                <a href="/" className="text-lg font-bold">
                    CREATE GAME
                </a>
            </nav>
            
            <form 
                className="w-full flex flex-col gap-y-8" 
                onSubmit={handleSubmit}
            >
                <div className={inputWrapperClass}>
                    <label>
                        Your Username
                    </label>
                    <input
                        name="username"
                        className="retro px-4 py-2 outline-none"
                        type="text"
                        value={formData.username}
                        onChange={handleChange}
                        required
                    />
                </div>
                <div className={inputWrapperClass}>
                    <label>Game Mode</label>
                    <div className="flex flex-wrap gap-2">
                        {["FFA", "Team"].map((mode) => (
                            <button 
                                key={mode}
                                type="button"
                                onClick={(e) => handleClick(e, "gameMode", mode)}
                                className={twMerge(
                                    "retro px-4 py-2",
                                    formData.gameMode === mode ? "bg-green-300" : ""
                                )}
                            >
                                {mode}
                            </button>
                        ))}
                    </div>
                    <input
                        className="hidden"
                        type="text"
                        defaultValue={formData.gameMode}
                        required
                    />
                </div>
                <div className={inputWrapperClass}>
                    <label>Number of Players</label>
                    <input
                        className="retro px-4 py-2 outline-none"
                        type="number"
                        name="playerNum"
                        value={formData.playerNum}
                        onChange={handleChange}
                        required
                    />
                </div>
                <div className={inputWrapperClass}>
                    <label>Number of Questions</label>
                    <input
                        className="retro px-4 py-2 outline-none"
                        type="number"
                        name="questionNum"
                        value={formData.questionNum}
                        onChange={handleChange}
                        required
                    />
                </div>
                <div className={inputWrapperClass}>
                    <label>Timer Per Question</label>
                    <input
                        className="retro px-4 py-2 outline-none"
                        type="number"
                        name="questionTimer"
                        value={formData.questionTimer}
                        onChange={handleChange}
                        required
                    />
                </div>
                <div className={inputWrapperClass}>
                    <label>Category</label>
                    <div className="flex flex-wrap gap-2">
                        {categories.map((category) => (
                            <button
                                key={category.id}
                                type="button"
                                onClick={(e) => handleClick(e, "category", category.id)}
                                className={twMerge(
                                    "retro px-4 py-2",
                                    formData.category === category.id ? "bg-green-300" : ""
                                )}
                            >
                                {category.category}
                            </button>
                        ))}
                    </div>
                </div>
                <div className={inputWrapperClass}>
                    <label >Difficulty</label>
                    <div className="flex flex-wrap gap-2">
                        {["Easy", "Medium", "Hard"].map((difficulty) => (
                            <button
                                key={difficulty}
                                type="button"
                                onClick={(e) => handleClick(e, "difficulty", difficulty)}
                                className={twMerge(
                                    "retro px-4 py-2",
                                    formData.difficulty === difficulty ? "bg-green-300" : ""
                                )}      
                            >
                                {difficulty}
                            </button>
                        ))}
                    </div>
                </div>

                <button className="px-4 py-2 bg-black text-white" type="submit">
                    CREATE GAME
                </button>
            </form>

        </MainLayout>
    )
}