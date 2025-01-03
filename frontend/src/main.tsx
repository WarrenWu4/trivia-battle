import ReactDOM from "react-dom/client";
import { BrowserRouter, Routes, Route } from "react-router";
import "./index.css";
import Create from "./pages/Create";
import Game from "./pages/Game";
import Error from "./pages/Error";

const root = document.getElementById("root");

ReactDOM.createRoot(root!).render(
  <BrowserRouter>
    <Routes>
      <Route path="/" element={<Create />} />
      <Route path="/create" element={<Create />} />
      <Route path="/game/:gameId" element={<Game />}/>
      <Route path="*" element={<Error />} />
    </Routes>
  </BrowserRouter>
);
