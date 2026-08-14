import { useState } from 'react';
import { Link, useNavigate } from "react-router-dom";

import { loginUser } from '../../services/api';
import Button from "../../components/Button/Button";
import Notification from "../../components/Notification/Notification";
import "./Login.css";


function Login() {
  const navigate = useNavigate();

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const [notification, setNotification] = useState(null);

  function showNotification(message) {
      setNotification(message);

      setTimeout(() => {
          setNotification(null);
      }, 2000);
  }

  async function handleLogin(){
    try{
      const response = await loginUser({
        email,
        password,
      });

      if (response.ok) {
          const data = await response.json();
          localStorage.setItem("token", data.access_token);
          showNotification('Login successful!');
          navigate("/home");
        }
        else {
          const error = await response.json();
          showNotification(error.detail);
        }
    }
    catch(error) {
        console.error(error);
        showNotification('server error.');
      }
    } 

  return (
    <div className="login-container">
      <Notification message={notification} />

      <div className="login-card">

        <h1>TRAPFALL</h1>

        <label htmlFor="email">Email</label>

        <input
          id="email"
          type="email"
          value={email}
          onChange={(event) => setEmail(event.target.value)}
        />

        <label htmlFor="password">Password</label>

        <input
          id="password"
          type="password"
          value={password}
          onChange={(event) => setPassword(event.target.value)}
        />

        <Button text="LOGIN" onClick={handleLogin} />

        <p className="register-text">New Player? <Link to="/register">Register Now</Link></p>

      </div>

    </div>
  );
}

export default Login;