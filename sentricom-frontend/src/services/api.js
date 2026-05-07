import { getSessionToken } from "../utils/auth";

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;
const API_KEY = import.meta.env.VITE_API_KEY;

export async function apiFetch(endpoint, options = {}) {

  // Get current session token
  const token = getSessionToken();

  // Prevent API calls without authentication
  if (!token) {
    throw new Error("Missing session token");
  }

  const response = await fetch(`${API_BASE_URL}${endpoint}`, {
    ...options,
    headers: {
      "Content-Type": "application/json",
      "X-Session-Token": token,
      "X-API-Key": API_KEY,
      ...(options.headers || {}),
    },
  });

  // Handle failed API requests
  if (!response.ok) {
    throw new Error(`API request failed: ${response.status}`);
  }

  return response.json();
}