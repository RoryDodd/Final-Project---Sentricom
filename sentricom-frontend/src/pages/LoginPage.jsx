import { User, Lock } from "lucide-react";
import { useNavigate } from "react-router-dom";

export default function LoginPage() {
    const navigate = useNavigate();
  return (
    <div className="login-page">
      <div className="login-card">
        <h1 className="login-title">Login</h1>
        <p className="login-subtitle">Please login into your account</p>

        <form className="login-form">
          <div className="login-field">
            <label htmlFor="username">Username</label>
            <div className="input-with-icon">
              <User size={22} />
              <input
                id="username"
                type="text"
                placeholder="Enter username"
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
              />
            </div>
          </div>

          <div className="login-actions">
           <button
             type="button"
             className="login-button"
             onClick={() => navigate("/dashboard")}
            >
            Login
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}