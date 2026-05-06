import { useState } from "react";
import { User, Lock } from "lucide-react";
import { useNavigate } from "react-router-dom";
import { loginUser } from "../services/authService";

// LoginPage handles user authentication and session creation
export default function LoginPage() {
  const navigate = useNavigate();

  // Form state
  const [identifier, setIdentifier] = useState("");
  const [password, setPassword] = useState("");

  // Error message state
  const [error, setError] = useState("");

  // Handles login request to backend
  async function handleLogin(e) {
    e.preventDefault();

    try {
      // Send credentials → receive session token
      await loginUser(identifier, password);

      // Only navigate if login succeeds
      navigate("/dashboard");
    } catch (err) {
      setError("Invalid username or password");
    }
  }

  return (
    <div className="login-page">
      <div className="login-card">
        <h1 className="login-title">Login</h1>
        <p className="login-subtitle">Please login into your account</p>

        {/* Login form */}
        <form className="login-form" onSubmit={handleLogin}>
          <div className="login-field">
            <label htmlFor="identifier">Username or Email</label>
            <div className="input-with-icon">
              <User size={22} />
              <input
                id="identifier"
                type="text"
                placeholder="Enter username or email"
                value={identifier}
                onChange={(e) => setIdentifier(e.target.value)}
              />
            </div>
          </div>

          <div className="login-field">
            <label htmlFor="password">Password</label>
            <div className="input-with-icon">
              <Lock size={22} />
              <input
                id="password"
                type="password"
                placeholder="Enter password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
              />
            </div>
          </div>

          {/* Display error if login fails */}
          {error && <p style={{ color: "red" }}>{error}</p>}

          <div className="login-actions">
            <button type="submit" className="login-button">
              Login
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}