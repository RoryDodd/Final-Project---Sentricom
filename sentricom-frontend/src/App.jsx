// Routing components
import { Routes, Route, Navigate } from "react-router-dom";

// Layout wrapper
import MainLayout from "./components/MainLayout";

// Pages
import DashboardPage from "./pages/DashboardPage";
import GenerateReportPage from "./pages/GenerateReportPage";
import ProfilePage from "./pages/ProfilePage";
import LoginPage from "./pages/LoginPage";
import AdminPage from "./pages/AdminPage";

// Route protection
import AdminRoute from "./components/AdminRoute";

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

      {/* Admin page */}
      <Route
        path="/admin"
        element={
          <MainLayout>
            <AdminRoute>
              <AdminPage />
            </AdminRoute>
          </MainLayout>
        }
      />

    </Routes>
  );
}

export default App;