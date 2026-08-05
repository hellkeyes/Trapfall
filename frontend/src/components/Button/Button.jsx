import "./Button.css";


function Button({ text }){
    return(
        <button  className="game-button">{text}</button>
    );
}

export default Button;