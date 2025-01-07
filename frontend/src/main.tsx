import ReactDOM from "react-dom/client";
import { BrowserRouter, Routes, Route } from "react-router";
import "./index.css";
import Create from "./pages/Create";
import Game from "./pages/Game";
import Error from "./pages/Error";
import GameOver from "./pages/GameOver";
import Join from "./pages/Join";
import AuthLayout from "./layouts/AuthLayout";

const root = document.getElementById("root");

ReactDOM.createRoot(root!).render(
    <BrowserRouter>
        <Routes>
            <Route path="/" element={<Create />} />
            <Route path="/create" element={<Create />} />
            <Route path="/join/:gameId" element={<Join />} />

            <Route element={<AuthLayout />}>
                <Route path="/game/:gameId" element={<Game />} />
                <Route path="/game/:gameId/over" element={<GameOver />} />
            </Route>

            <Route path="*" element={<Error />} />
        </Routes>
    </BrowserRouter>
);
