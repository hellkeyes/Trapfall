import { useState } from "react";

import Button from "../../components/Button/Button";
import "./Home.css";


function Home() {

    const [roomCode, setRoomCode] = useState("");

    return (

        <div className="home-container">

            <div className="home-card">

                <h1>TRAPFALL</h1>

                <h2>PLAYER MENU</h2>

                <Button text="CREATE ROOM" />

                <div className="divider">OR</div>


                <label>ROOM CODE</label>


                <input
                    type="text"
                    value={roomCode}
                    onChange={(event)=>setRoomCode(event.target.value)}
                />


                <Button text="JOIN ROOM" />

            </div>

        </div>

    );
}


export default Home;