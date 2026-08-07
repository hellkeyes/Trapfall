import { useParams } from "react-router-dom";
import "./Game.css";


function Game(){

    const { roomCode } = useParams();


    return (
        <div className="game-container">

            <div className="game-card">

                <h1>TRAPFALL</h1>

                <p>GAME STARTED</p>

                <p>
                    ROOM: {roomCode}
                </p>

            </div>

        </div>
    );
}


export default Game;