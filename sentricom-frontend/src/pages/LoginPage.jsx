// Import icons for input fields
import { User, Lock } from "lucide-react";

// Import navigation hook for programmatic routing
import { useNavigate } from "react-router-dom";

// LoginPage handles user authentication UI (frontend only for now)
export default function LoginPage() {

  // Hook used to navigate between routes
  const navigate = useNavigate();

  return (
    // Main login page container
    <div className="login-page">

      {/* Login card container */}
      <div className="login-card">

        {/* Page title and subtitle */}
        <h1 className="login-title">Login</h1>
        <p className="login-subtitle">Please login into your account</p>

        {/* Login form (not yet connected to backend) */}
        <form className="login-form">

          {/* Username input field */}
          <div className="login-field">
            <label htmlFor="username">Username</label>
            <div className="input-with-icon">
              <User size={22} /> {/* User icon */}
              <input
                id="username"
                type="text"
                placeholder="Enter username"
              />
            </div>
          </div>

          {/* Password input field */}
          <div className="login-field">
            <label htmlFor="password">Password</label>
            <div className="input-with-icon">
              <Lock size={22} /> {/* Lock icon */}
              <input
                id="password"
                type="password"
                placeholder="Enter password"
              />
            </div>
          </div>

          {/* Login button */}
          <div className="login-actions">
            <button
              type="button" // Prevents default form submission
              className="login-button"
              onClick={() => navigate("/dashboard")} // Temporary navigation (no auth yet)
            >
              Login
            </button>
          </div>

        </form>
      </div>
    </div>
  );
}