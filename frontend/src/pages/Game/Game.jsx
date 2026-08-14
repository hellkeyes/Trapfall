import { useParams, useNavigate } from "react-router-dom";
import { useState, useEffect, useRef  } from "react";
import "./Game.css";
import Tile from "../../components/Tile/Tile";
import Button from "../../components/Button/Button";


function Game(){
    const navigate = useNavigate();    
    const { roomCode } = useParams();
    const tiles = Array.from({length:100});
    const socketRef = useRef(null);

    const [players, setPlayers] = useState({
        player_a: {id: null, x: 0, y: 0 },  //position of a
        player_b: {id: null, x: 9, y: 9 },  //position of b
        current_turn: null,
        you_are: null  // player state
    });      
    
    const [traps, setTraps] = useState([]); // collect all traps

    const [winner, setWinner] = useState(null); 

    const [timer, setTimer] = useState(60);

    const [phaseEndsAt, setPhaseEndsAt] = useState(null);

    const [triggeredTrap, setTriggeredTrap] = useState(null);

    const [phase, setPhase] = useState("TRAP_PLACEMENT");

    const myPlayerSide = players.current_turn;

    useEffect(() => {

            const token = localStorage.getItem("token");

            socketRef.current = new WebSocket(
                `ws://127.0.0.1:8000/ws/rooms/${roomCode}?token=${token}`
            );

            socketRef.current.onopen = () => {
                console.log("WebSocket connected");

                socketRef.current.send(JSON.stringify({
                    type: "GET_GAME_STATE"
                }));
            };

            socketRef.current.onmessage = (event) => {
            const data = JSON.parse(event.data);
            console.log("RECEIVED FROM SERVER:", data);

            if (data.type === "GAME_STATE") {
                console.log("SETTING INITIAL PLAYERS");
                setPlayers({
                    player_a: data.player_a,
                    player_b: data.player_b,
                    current_turn: data.current_turn,
                    you_are: data.you_are
                });

                setTraps(data.traps);
                setPhase(data.phase);

                console.log("GAME STATE DEADLINE:", data.phase_ends_at);
                setPhaseEndsAt(data.phase_ends_at);

                return;
            }

            if (data.type === "PLAYER_MOVED") {

                console.log("PLAYER MOVED ID:", data.player_id);

                setPlayers(prev => {

                    console.log("CURRENT A:", prev.player_a);
                    console.log("CURRENT B:", prev.player_b);

                    if (data.player_id === prev.player_a.id) {

                        console.log("MATCHED PLAYER A");

                        return {
                            ...prev,
                            player_a: {
                                ...prev.player_a,
                                x: data.position.x,
                                y: data.position.y
                            }
                        };
                    }

                    if (data.player_id === prev.player_b.id) {

                        console.log("MATCHED PLAYER B");

                        return {
                            ...prev,
                            player_b: {
                                ...prev.player_b,
                                x: data.position.x,
                                y: data.position.y
                            }
                        };
                    }

                    console.log("NO PLAYER MATCH");

                    return prev;
                });
            }

            if (data.type === "TRAP_PLACED") {
                console.log("Trap placement");
                setTraps(prev => [
                    ...prev,
                    {
                        x: data.position.x,
                        y: data.position.y,
                        owner: data.player_id
                    }
                ]) 
            }

            if (data.type === 'TRAP_TRIGGERED') {
                setTriggeredTrap(data.position);
                setTimeout(() => {
                    setTriggeredTrap(null);
                }, 1000);

                console.log("PLAYER MOVED ID:", data.player_id);

                setPlayers(prev => {

                    console.log("CURRENT A:", prev.player_a);
                    console.log("CURRENT B:", prev.player_b);

                    if (data.player_id === prev.player_a.id) {

                        console.log("MATCHED PLAYER A");

                        return {
                            ...prev,
                            player_a: {
                                ...prev.player_a,
                                x: data.position.x,
                                y: data.position.y
                            }
                        };
                    }

                    if (data.player_id === prev.player_b.id) {

                        console.log("MATCHED PLAYER B");

                        return {
                            ...prev,
                            player_b: {
                                ...prev.player_b,
                                x: data.position.x,
                                y: data.position.y
                            }
                        };
                    }

                    console.log("NO PLAYER MATCH");

                    return prev;
                });               
            }

            if (data.type === "GAME_WON") {
                setWinner(data.winner);
                return;
            }

            if (data.type === "ERROR") {
                alert(data.message);
            }

            if (data.type === "PHASE_CHANGED") {
                setPhase(data.phase);
                setPhaseEndsAt(data.phase_ends_at);
            }

            if (data.phase === "MOVEMENT") {
                setTraps([]);
            }

            if (data.type === "ROOM_TERMINATED") {
                console.log("ROOM TERMINATED RECEIVED");
                navigate('/home');
                return;
            }

            if (data.type === "ROOM_NOT_FOUND") {
                alert(data.message);
                navigate("/home");
                return;
            }


            }

            socketRef.current.onclose = () => {
                console.log("WebSocket disconnected");
            };

            return () => {
                console.log("GAME JSX UNMOUNTING — CLOSING SOCKET");
                socketRef.current.close();
            };
        

        
    }, []);

    function handleTileClick(row, col){
        try {
            socketRef.current.send(JSON.stringify({
                type: "PLACE_TRAP",
                position: {
                    x: col,
                    y: row
                }
            }));

        }
         catch(error){
            console.error(error);
        }  
    }

    useEffect(() => {                 // see which key is pressed
        function handleKeyDown(event) {
            console.log(event.key);
            let direction = null;

             switch (event.key) {
                case "ArrowUp":
                    direction = "UP";
                    break;

                case "ArrowDown":
                    direction = "DOWN";
                    break;

                case "ArrowLeft":
                    direction = "LEFT";
                    break;

                case "ArrowRight":
                    direction = "RIGHT";
                    break;

                default:
                    return;   // ignore every other key
            }

            if ( socketRef.current &&
                socketRef.current.readyState === WebSocket.OPEN) {
                    console.log("SENDING:", direction);

                    socketRef.current.send(JSON.stringify({
                        type: "MOVE",
                        direction: direction
                    }));
            }
                                

        }


        window.addEventListener("keydown", handleKeyDown);

        return () => {
            window.removeEventListener("keydown", handleKeyDown);
        };


    }, []);

    useEffect(() => {

        console.log("TIMER EFFECT RAN");
        console.log("PHASE ENDS AT:", phaseEndsAt);

        if (!phaseEndsAt) {
            console.log("NO PHASE END TIME YET");
            return;
        }


        const interval = setInterval(() => {

            const remaining = Math.ceil(
                phaseEndsAt - Date.now() / 1000
            );

            console.log("REMAINING:", remaining);

            setTimer(Math.max(0, remaining));

        }, 1000);

        return () => clearInterval(interval);

    }, [phaseEndsAt]);


  return (
        <div className="game-container">

            <div className="game-card">

                <h1 className="game-title">TRAPFALL</h1>

                <div className="game-info">

                    <span>ROOM : {roomCode}</span>
                    
                    <span>PHASE : {phase} </span>

                    {/* <span>TIMER : {timer}</span> */}

                </div>

                <div className="game-layout">

                    {/* GAME BOARD */}
                    <div className="board">
                        {
                            tiles.map((_,index)=>(
                                <Tile key={index}
                                    index={index}
                                    player_a={players.player_a}
                                    player_b={players.player_b}
                                    onClick={handleTileClick}
                                    traps={traps}
                                    phase={phase}
                                    triggeredTrap={triggeredTrap} />             // giving index so react knows which tile changes
                            ))
                        }
                    </div>


                    {/* SIDE PANEL */}
                    <div className="sidebar">

                        <div className="sidebar-box">

                            <div className="sidebar-title">
                                You are: {players.you_are}
                            </div>

                            <div className="sidebar-text">
                                Lives : ♥ ♥ ♥
                            </div>

                            <div className="sidebar-text">
                                Turn: {players.current_turn === players.you_are ? "YOU" : "OPPONENT"}
                            </div>

                        </div>


                        <div className="sidebar-box">

                            <div className="sidebar-title">
                                TRAPS
                            </div>

                            <div className="sidebar-text">
                                Placed : {traps.length}
                            </div>

                            {/* <div className="sidebar-text">
                                Selected : NORMAL
                            </div> */}

                        </div>


                        <div className="sidebar-box">

                            <div className="sidebar-title">
                                STATUS
                            </div>

                            <div className="sidebar-text">
                                    {phase === "TRAP_PLACEMENT"
                                        ? "Place your traps."
                                        : phase === "MEMORIZE"
                                        ? "Memorize your traps. They will disappear soon."
                                        : "Get ready to move!"
                                    }
                            </div>

                        </div>


                        <div className="sidebar-box">

                            <div className="sidebar-title">
                                TIMER
                            </div>

                            <div className="timer">
                                {phase === 'MOVEMENT' ? 'NA': timer}
                            </div>

                        </div>


                        {/* <div className="sidebar-box">

                            <div className="sidebar-title">
                                ROOM CODE
                            </div>

                            <div className="timer">
                                {timer}
                            </div>

                        </div> */}



                    </div>

                </div>

            </div>

            {winner && (
                <div className="winner-overlay">
                    <div className="winner-dialog">

                        <div className="winner-warning">GAME COMPLETE</div>

                        {/* <div className="winner-icon">
                            🏆
                        </div> */}

                        <h2>PLAYER {winner} WINS</h2>

                        <div className="winner-line"></div>

                        <p>THE OPPONENT HAS BEEN DEFEATED</p>

                        <button onClick={() => navigate("/home")}>
                            RETURN HOME
                        </button>

                    </div>
                </div>
            )}

        </div>
    );
}

export default Game;