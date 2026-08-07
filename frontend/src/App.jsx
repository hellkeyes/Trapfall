import { BrowserRouter, Routes, Route } from "react-router-dom";

import Login from "./pages/Login/Login";
import Register from "./pages/Register/Register";
import Home from "./pages/Home/Home";
import Lobby from "./pages/Lobby/Lobby";


function App() {

  return (
    <BrowserRouter>

      <Routes>

        <Route path="/" element={<Login />} />

        <Route path="/register" element={<Register />} />

        <Route path="/home" element={<Home />} />

        <Route path="/rooms/:roomCode" element={<Lobby />} />

      </Routes>

    </BrowserRouter>
  );
}


export default App;