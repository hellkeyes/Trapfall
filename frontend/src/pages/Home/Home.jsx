import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";

import { createRoom, joinRoom } from '../../services/api';
import Button from "../../components/Button/Button";
import Notification from "../../components/Notification/Notification";
import "./Home.css";


function Home() {
    const navigate = useNavigate();
    const [roomCode, setRoomCode] = useState("");
    const [createdRoomCode, setCreatedRoomCode] = useState("");
    const [notification, setNotification] = useState(null);

    function showNotification(message) {
        setNotification(message);

        setTimeout(() => {
            setNotification(null);
        }, 2000);
    }

    useEffect(() => {
        const token = localStorage.getItem('token');
        if (token === null) {
            // console.log("No token, redirecting");
            navigate("/");
        }
    }, []);

    async function handleCreateRoom(){
        try {
            const token = localStorage.getItem('token');
            const response = await createRoom(token);

            if(response.ok){
                const data = await response.json();
                navigate(`/rooms/${data.room_code}`);
            }
        }
         catch(error){
            showNotification('Cannot create room!');
        }
    }

    async function handleJoinRoom(){
        try {
            const token = localStorage.getItem('token');
            const response = await joinRoom(roomCode, token)

            if(response.ok){
                const data = await response.json();
                console.log("JOIN RESPONSE:", data);

                if (data.message === "Reconnected") {
                    navigate(`/rooms/${roomCode}/game`);
                } else {
                    navigate(`/rooms/${roomCode}`);
                }
            }
            else {
            const error = await response.json();
            showNotification(error.detail);
            }
        }
         catch(error){
            showNotification('Cannot join room!');
        }
    }


    return (

        <div className="home-container">
            <Notification message={notification} />

            <div className="home-card">

                <h1>TRAPFALL</h1>

                <h2>PLAYER MENU</h2>

                <Button text="CREATE ROOM" onClick={handleCreateRoom}/>

                <div className="divider">OR</div>


                <label>ROOM CODE</label>


                <input
                    type="text"
                    value={roomCode}
                    onChange={(event)=>setRoomCode(event.target.value)}
                />

                <Button text="JOIN ROOM" onClick={handleJoinRoom} />

            </div>

        </div>

    );
}

export default Home;