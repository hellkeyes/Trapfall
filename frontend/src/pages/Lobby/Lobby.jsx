import { useState, useEffect } from "react";
import { useParams, useNavigate } from "react-router-dom";

import { getRoom, startGame } from "../../services/api";
import Button from "../../components/Button/Button";
import "./Lobby.css";
import Notification from "../../components/Notification/Notification";

function Lobby(){
    const navigate = useNavigate();
    const { roomCode } = useParams();
    const [room, setRoom] = useState(null);
    const [showRules, setShowRules] = useState(false);
    const [notification, setNotification] = useState(null);

    function showNotification(message) {
        setNotification(message);

        setTimeout(() => {
            setNotification(null);
        }, 2000);
    }

    async function handleCopyCode(){
        await navigator.clipboard.writeText(room.room_code);
        showNotification("ROOM CODE COPIED!");
    }

    async function handleStartGame(){
        try {
            const token = localStorage.getItem("token");
            const response = await startGame(roomCode, token);

            if(!response.ok){
            const error = await response.json();
            showNotification(error.detail);
            }
        }
        catch(error){
            showNotification("Unable to start the game.");
        }
    }


    useEffect(() => {

        const token = localStorage.getItem("token");

        // Fetch initial room data
        async function fetchRoom(){
            try {
                const response = await getRoom(roomCode, token);
                if(response.ok){
                    const data = await response.json();
                    setRoom(data);
                }
                else {
                    const error = await response.json();
                    showNotification(error.detail);
                }
            }
            catch(error){
                showNotification("Unable to get the game.");
            }
        }

        fetchRoom();

        // WebSocket connection
        const socket = new WebSocket(
            `ws://127.0.0.1:8000/ws/rooms/${roomCode}?token=${token}`
        );

        socket.onopen = () => {
        };

        socket.onmessage = (event) => {
            const data = JSON.parse(event.data);

            if(data.type === "ROOM_UPDATED"){
                setRoom(data.room);
            }

            if(data.type === "GAME_STARTED"){
                navigate(`/rooms/${roomCode}/game`);
            }
        };

        socket.onclose = () => {
        };

        return () => {
            socket.close();
        };

    }, [roomCode]);


return (
    <div className="lobby-container">

        <Notification message={notification} />

        {room && (
            <div className="lobby-card">

                <h1>TRAPFALL</h1>

                <p className="lobby-subtitle">
                    WAITING FOR PLAYERS
                </p>

                <div className="room-box">

                    <p>ROOM CODE</p>

                    <div className="room-code">
                        {room.room_code}
                    </div>

                    <div className="copy-button">
                        <Button
                            text="COPY CODE"
                            onClick={handleCopyCode}
                            small={true}
                        />
                    </div>

                </div>


                <div className="player-box">

                    <div className="player-row">

                        <span className="player-label">
                            PLAYER A
                        </span>

                        <span className="player-name">
                            {room.player_a}
                        </span>

                    </div>


                    <div className="player-row">

                        <span className="player-label">
                            PLAYER B
                        </span>

                        <span className="player-name">
                            {room.player_b || "WAITING..."}
                        </span>

                    </div>

                </div>

                <div className="status-box">

                    <p>STATUS</p>

                    <div className="status-value">
                        {room.phase}
                    </div>

                </div>


                {/* ACTIONS */}

                <div className="lobby-actions">

                    <Button
                        text="HOW TO PLAY"
                        onClick={() => setShowRules(true)}
                    />

                    <Button
                        text="START GAME"
                        onClick={handleStartGame}
                    />

                </div>

            </div>
        )}


        {showRules && (
            <div className="rules-overlay">

                <div className="rules-modal">

                    <h2>HOW TO PLAY</h2>


                    {/* OBJECTIVE */}

                    <div className="rules-section">

                        <h3>OBJECTIVE</h3>

                        <p>
                            Reach the opponent's side before they reach yours.
                        </p>

                    </div>


                    {/* TRAPS */}

                    <div className="rules-section">

                        <h3>TRAPS</h3>

                        <p>• 8 traps per player.</p>
                        <p>• Trap placement lasts 60 seconds.</p>
                        <p>• Traps are hidden during movement.</p>
                        <p>• A triggered trap activates only once.</p>
                        <p>• Trap hit costs 1 life.</p>
                        <p>• Trap hit knocks you back 2 tiles.</p>

                    </div>


                    {/* LIVES */}

                    <div className="rules-section">

                        <h3>LIVES</h3>

                        <p>• Each player starts with ♥ ♥ ♥.</p>
                        <p>• Lose all 3 lives and you are eliminated.</p>
                        <p>• Your opponent wins.</p>

                    </div>


                    {/* PHASES */}

                    <div className="rules-section">

                        <h3>PHASES</h3>

                        <p>• Trap Placement — 60 seconds</p>
                        <p>• Memorize — 15 seconds</p>
                        <p>• Movement — Turn based</p>

                    </div>


                    <div className="rules-close">

                        <Button
                            text="CLOSE"
                            onClick={() => setShowRules(false)}
                        />

                    </div>

                </div>

            </div>
        )}

    </div>
    );
}


export default Lobby;