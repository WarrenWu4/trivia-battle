import { useState } from "react";
import names from "../assets/data/names.json";

export default function Join() {

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