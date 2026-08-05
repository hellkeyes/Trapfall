import { useState } from 'react';
import { Link } from "react-router-dom";

import Button from "../../components/Button/Button";
import "./Login.css";


function Login() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  return (
    <div className="login-container">

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

        <Button text="LOGIN" />

        <p className="register-text">New Player? <Link to="/register">Register Now</Link></p>

      </div>

    </div>
  );
}

export default Login;