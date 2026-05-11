// Header with navigation and logout
import { useNavigate, useLocation } from "react-router-dom";

export default function Header() {
  const navigate = useNavigate();
  const location = useLocation();

  
 // Navigation tabs
const tabs = [
  { label: "Overview", path: "/dashboard" },
  { label: "Generate Report", path: "/generate" },
  { label: "Profile", path: "/profile" },

  // Admin-only navigation tab
  ...(localStorage.getItem("sentricom_role") === "admin"
    ? [{ label: "Admin", path: "/admin" }]
    : []),
];

  // Logout handler
  const handleLogout = () => {

  localStorage.removeItem("sentricom_session_token");
  localStorage.removeItem("sentricom_role");

  navigate("/login");
};

  return (
    <header className="header">
      <div className="header-inner">
        <div className="logo">Sentricom</div>

        {/* Tabs + logout */}
        <div className="header-actions">
          <nav className="nav-tabs">
            {tabs.map((tab) => {
              const isActive = location.pathname === tab.path;

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

          {/* Logout button */}
          <button className="logout-button" onClick={handleLogout}>
            Logout
          </button>
        </div>
      </div>
    </header>
  );
}