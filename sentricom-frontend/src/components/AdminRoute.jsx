// React Router navigation
import { Navigate } from "react-router-dom";

// Auth utilities
import { isAdmin } from "../utils/auth";

// Protect admin-only pages
export default function AdminRoute({ children }) {

  return isAdmin()
    ? children
    : <Navigate to="/dashboard" />;
}