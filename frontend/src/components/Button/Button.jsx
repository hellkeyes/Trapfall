import "./Button.css";


function Button({ text, onClick, small }){
    return(
        <button  className={small ? 'game-button small' : 'game-button'} onClick={onClick}>{text}</button>
    );
}

export default Button;