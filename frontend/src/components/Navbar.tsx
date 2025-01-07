import { useState } from "react";
import { MdDarkMode } from "react-icons/md";
import { MdLightMode } from "react-icons/md";

interface NavbarProps {
    title: string;
}

export default function Navbar({ title }: NavbarProps) {

    const [theme, setTheme] = useState<string>(
        localStorage.getItem("theme") || "light"
    );

    function changeTheme(e: React.MouseEvent<HTMLButtonElement>) {
        e.preventDefault();
        if (document.documentElement.classList.contains("dark")) {
            document.documentElement.classList.remove("dark");
            localStorage.setItem("theme", "light");
            setTheme("light");
        } else {
            document.documentElement.classList.add("dark");
            localStorage.setItem("theme", "dark");
            setTheme("dark");
        }
    }

    return (
        <nav className="flex items-center justify-between pb-2 border-b-4 border-black dark:border-white mb-4">
            <a href="/" className="text-lg font-bold">
                {title}
            </a>
            <button
                type="button"
                className="text-lg cursor-pointer" 
                onClick={changeTheme}
            >
                {theme === 'light' ?
                <MdDarkMode />
                :
                <MdLightMode /> 
                }
            </button>
        </nav>
    )
}