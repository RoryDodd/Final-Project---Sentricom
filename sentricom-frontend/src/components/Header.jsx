import { useNavigate, useLocation } from "react-router-dom";

export default function Header() {
  const navigate = useNavigate();
  const location = useLocation();

  const tabs = [
    { label: "Overview", path: "/dashboard" },
    { label: "Generate Report", path: "/generate" },
    { label: "Profile", path: "/profile" },
  ];

  const handleLogout = () => {
    navigate("/login");
  };

  return (
    <header className="header">
      <div className="header-inner">
        <div className="logo">Sentricom</div>

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

          <button className="logout-button" onClick={handleLogout}>
            Logout
          </button>
        </div>
      </div>
    </header>
  );
}