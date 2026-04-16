// Header component that displays the app logo, navigation tabs, and logout button
import { useNavigate, useLocation } from "react-router-dom";

// Importing necessary hooks from react-router-dom for navigation and location tracking
export default function Header() {
  const navigate = useNavigate();
  const location = useLocation();

  // Define the navigation tabs with their labels and corresponding paths
  const tabs = [
    { label: "Overview", path: "/dashboard" },
    { label: "Generate Report", path: "/generate" },
    { label: "Profile", path: "/profile" },
  ];

  // Function to handle logout action, which redirects the user to the login page
  const handleLogout = () => {
    navigate("/login");
  };

  // Render the header with logo, navigation tabs, and logout button
  return (

    // Main header container
    <header className="header">
      <div className="header-inner">
        <div className="logo">Sentricom</div>


        // Navigation tabs and logout button container
        <div className="header-actions">
          <nav className="nav-tabs">
            {tabs.map((tab) => {
              const isActive = location.pathname === tab.path;
              
              // Render each navigation tab with an active state based on the current location
              return (
                <button
                  key={tab.label}
                  onClick={() => navigate(tab.path)}
                  className={`nav-tab ${isActive ? "active" : ""}`}
                >
                  {tab.label}
                </button>
              );
            })}
          </nav>

            // Logout button that triggers the handleLogout function when clicked
          <button className="logout-button" onClick={handleLogout}>
            Logout
          </button>
        </div>
      </div>
    </header>
  );
}