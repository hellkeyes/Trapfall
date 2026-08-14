import "./Notification.css";

function Notification({ message }) {

    if (!message) {
        return null;
    }

    return (
        <div className="game-notification">
            <span className="notification-icon">⚠</span>

            <span className="notification-message">
                {message}
            </span>
        </div>
    );
}

export default Notification;