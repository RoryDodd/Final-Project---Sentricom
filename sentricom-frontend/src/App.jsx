import { Routes, Route, Navigate } from "react-router-dom";
import MainLayout from "./components/MainLayout";

import DashboardPage from "./pages/DashboardPage";
import GenerateReportPage from "./pages/GenerateReportPage";
import ProfilePage from "./pages/ProfilePage";
import LoginPage from "./pages/LoginPage";

function App() {
  return (
    <Routes>
      {/* Login page */}
      <Route path="/login" element={<LoginPage />} />

      {/* Redirect root → login */}
      <Route path="/" element={<Navigate to="/login" />} />

      {/* App pages */}
      <Route
        path="/dashboard"
        element={
          <MainLayout>
            <DashboardPage />
          </MainLayout>
        }
      />

      <Route
        path="/generate"
        element={
          <MainLayout>
            <GenerateReportPage />
          </MainLayout>
        }
      />

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