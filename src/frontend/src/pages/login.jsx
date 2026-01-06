import React, { useState } from "react";
import "../styles/login.css";
import bellis_logo from "../assets/bellis-logo.svg";

function Login() {
  const [email, set_email] = useState("");
  const [password, set_password] = useState("");

  const handle_submit = (e) => {
    e.preventDefault();
    console.log("Login attempt:", { email, password });
    //Add API call later
  };

  return (
    <div className="LoginContainer">
      <div className="LoginBox">
        <img src={bellis_logo} alt="Bellis Logo" className="LoginLogo" />
        <form onSubmit={handle_submit} className="LoginForm">
          <input
            type="email"
            placeholder="E-Mail"
            value={email}
            onChange={(e) => set_email(e.target.value)}
            required
          />
          <input
            type="password"
            placeholder="Passwort"
            value={password}
            onChange={(e) => set_password(e.target.value)}
            required
          />
          <a href="#" className="ForgotPassword">Passwort vergessen?</a>
          <button type="submit">Login</button>
        </form>
      </div>
    </div>
  );
}

export default Login;