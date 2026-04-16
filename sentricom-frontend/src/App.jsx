// Routing components
import { Routes, Route, Navigate } from "react-router-dom";

// Layout wrapper
import MainLayout from "./components/MainLayout";

// Pages
import DashboardPage from "./pages/DashboardPage";
import GenerateReportPage from "./pages/GenerateReportPage";
import ProfilePage from "./pages/ProfilePage";
import LoginPage from "./pages/LoginPage";

// App routes
function App() {
  return (
    <Routes>

      {/* Login page */}
      <Route path="/login" element={<LoginPage />} />

      {/* Redirect root to login */}
      <Route path="/" element={<Navigate to="/login" />} />

      {/* Dashboard */}
      <Route
        path="/dashboard"
        element={
          <MainLayout>
            <DashboardPage />
          </MainLayout>
        }
      />

      {/* Generate report */}
      <Route
        path="/generate"
        element={
          <MainLayout>
            <GenerateReportPage />
          </MainLayout>
        }
      />

      {/* Profile */}
      <Route
        path="/profile"
        element={
          <MainLayout>
            <ProfilePage />
          </MainLayout>
        }
      />

    </Routes>
  );
}

export default App;