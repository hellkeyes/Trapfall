import { useState } from 'react';
import { Link } from "react-router-dom";

import Button from "../../components/Button/Button";
import "./Register.css";

function Register() {
  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");

    return (
        <div className="register-container">

            <div className="register-card">
                <h1>TRAPFALL</h1>

                <label htmlFor="username">Username</label>

                <input
                    id="username"
                    type="text"
                    value={username}
                    onChange={(event)=>setUsername(event.target.value)}
                />


                <label htmlFor="email">Email</label>

                <input
                    id="email"
                    type="email"
                    value={email}
                    onChange={(event)=>setEmail(event.target.value)}
                />


                <label htmlFor="password">Password</label>

                <input
                    id="password"
                    type="password"
                    value={password}
                    onChange={(event)=>setPassword(event.target.value)}
                />


                <label htmlFor="confirm-password">Confirm Password</label>

                <input
                    id="confirm-password"
                    type="password"
                    value={confirmPassword}
                    onChange={(event)=>setConfirmPassword(event.target.value)}
                />


                <Button text="REGISTER" />

                <p className="login-text">Already a player? <Link to="/">Login</Link></p>


            </div>

        </div>
    );
}


export default Register;