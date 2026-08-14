import "./Tile.css";

function Tile({ index, player_a, player_b, onClick, traps, phase, triggeredTrap  }) {

    const row = Math.floor(index / 10);    // giving tiles number 
    const col = index % 10;

    let player = null

    if (player_a.x === col && player_a.y === row) {
        player = 'A';
    }

    if (player_b.x === col && player_b.y === row) {
        player = 'B';
    }

    const trap = traps.find(
        trap => trap.x === col && trap.y === row);

    const showTrap = trap && (phase === "TRAP_PLACEMENT" || phase === "MEMORIZE");

    const showExplosion = triggeredTrap && triggeredTrap.x === col && triggeredTrap.y === row;

    return (
        <div className ={` tile ${player === 'A' ? 'player' : ''} 
                                ${player === 'B' ? 'enemy' : ''}
                                ${showTrap ? 'trap' : ''}
                                ${showExplosion ? 'explosion': ''}`}
                            onClick={() => onClick(row, col)}>
            {player}
        </div>
    );
}

export default Tile;