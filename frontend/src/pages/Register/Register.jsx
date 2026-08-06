import { useState } from 'react';
import { Link, useNavigate } from "react-router-dom";
import { registerUser } from "../../services/api";
import Button from "../../components/Button/Button";
import "./Register.css";

function Register() {
  const navigate = useNavigate();
  
  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");


    async function handleRegister(){
        if (password !== confirmPassword){
            alert('Passwords do not match');
            return;
        }

        try {
            const response = await registerUser({
                username,
                email,
                password,
            });

            if (response.ok) {
                alert('Registration successful!');
                navigate("/")
            }
            else {
                const error = await response.json();
                alert(error.detail);
            }
        }

        catch(error) {
            console.error(error);
            alert('server error.');
        }
    }

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


                <Button text="REGISTER"  onClick={handleRegister} />

                <p className="login-text">Already a player? <Link to="/">Login</Link></p>


            </div>

        </div>
    );
}


export default Register;

