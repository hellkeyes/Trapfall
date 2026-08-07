import { useState, useEffect } from "react";
import { useParams } from "react-router-dom";

import { getRoom } from "../../services/api";
import Button from "../../components/Button/Button";
import "./Lobby.css";


function Lobby(){

    const { roomCode } = useParams();
    const [room, setRoom] = useState(null);

    async function handleCopyCode(){
        await navigator.clipboard.writeText(room.room_code);
        alert("Room Code Copied!");
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

            socket.send(JSON.stringify({
                type:"JOIN_LOBBY"
            }));
        };

        socket.onmessage = (event) => {
            const data = JSON.parse(event.data);
            console.log("Received:", data);

            if(data.type === "ROOM_UPDATED"){
                setRoom(data.room);
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
                                PLAYER 1
                            </span>


                            <span className="player-name">
                                {room.player_a}
                            </span>

                        </div>


                        <div className="player-row">

                            <span className="player-label">
                                PLAYER 2
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

                        <Button text="START GAME" />

                    </div>

                </div>

            )}

        </div>

    );

}


export default Lobby;