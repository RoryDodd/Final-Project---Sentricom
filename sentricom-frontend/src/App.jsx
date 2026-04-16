// Import routing components from react-router-dom
import { Routes, Route, Navigate } from "react-router-dom";

// Import main layout component that wraps around page components
import MainLayout from "./components/MainLayout";

// Import page components for different routes
import DashboardPage from "./pages/DashboardPage";
import GenerateReportPage from "./pages/GenerateReportPage";
import ProfilePage from "./pages/ProfilePage";
import LoginPage from "./pages/LoginPage";

// Main App component that defines the routing structure of the application
function App() {
  return (
    <Routes>

      // Route for the login page
      <Route path="/login" element={<LoginPage />} />

      // Redirect root path to login page
      <Route path="/" element={<Navigate to="/login" />} />

      {/* App pages */}

      // Route for the dashboard page, wrapped in the main layout
      <Route
        path="/dashboard"
        element={
          <MainLayout>
            <DashboardPage />
          </MainLayout>
        }
      />

      // Route for the generate report page
      <Route
        path="/generate"
        element={
          <MainLayout>
            <GenerateReportPage />
          </MainLayout>
        }
      />
      // Route for the profile page
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

// Export App as the root component.
export default App;