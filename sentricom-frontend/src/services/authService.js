import { saveSessionToken } from "../utils/auth";

const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL || "https://afert-umber.vercel.app";

// Sends username/password to backend
export async function loginUser(username, password) {
  const response = await fetch(`${API_BASE_URL}/api/v1/auth/login`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      username,
      password,
    }),
  });

  if (!response.ok) {
    throw new Error("Login failed");
  }

  const data = await response.json();

  // Save session token for future API calls
  saveSessionToken(data.session_token);

  return data;
}