import { useState, useEffect } from "react";
import { useParams, useNavigate } from "react-router-dom";

import { getRoom, startGame } from "../../services/api";
import Button from "../../components/Button/Button";
import "./Lobby.css";


function Lobby(){
    const navigate = useNavigate();
    const { roomCode } = useParams();
    const [room, setRoom] = useState(null);

    async function handleCopyCode(){
        await navigator.clipboard.writeText(room.room_code);
        alert("Room Code Copied!");
    }

    async function handleStartGame(){
        try {
            const token = localStorage.getItem("token");
            const response = await startGame(roomCode, token);

            if(!response.ok){
            const error = await response.json();
            alert(error.detail);
            }
        }
        catch(error){
            console.error(error);
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
                    alert(error.detail);
                }
            }
            catch(error){
                console.error(error);
            }
        }

        fetchRoom();

        // WebSocket connection
        console.log("SETTING UP SOCKET");
        const socket = new WebSocket(
            `ws://127.0.0.1:8000/ws/rooms/${roomCode}?token=${token}`
        );

        socket.onopen = () => {
            console.log("WebSocket connected");
        };

        socket.onmessage = (event) => {
            const data = JSON.parse(event.data);
            console.log("Received:", data);

            if(data.type === "ROOM_UPDATED"){
                setRoom(data.room);
            }

            if(data.type === "GAME_STARTED"){
                navigate(`/rooms/${roomCode}/game`);
            }
        };

        socket.onclose = () => {
            console.log("WebSocket disconnected");
        };

        return () => {
            socket.close();
        };

    }, [roomCode]);


    return (

        <div className="lobby-container">

            {room && (
                <div className="lobby-card">

                    <h1>TRAPFALL</h1>

                    <p className="lobby-subtitle">WAITING FOR PLAYERS</p>

                    <div className="room-box">

                        <p>ROOM CODE</p>

                        <div className="room-code">{room.room_code}</div>

                        <div className="copy-button">

                            <Button text="COPY CODE" onClick={handleCopyCode} small={true} />

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

                        <div className="status-value">{room.phase}</div>

                    </div>


                    <div className="start-button">

                        <Button text="START GAME" onClick={handleStartGame}/>

                    </div>

                </div>

            )}

        </div>

    );

}


export default Lobby;