import { saveSessionToken } from "../utils/auth";


const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL || "https://afert-umber.vercel.app";

const API_KEY = import.meta.env.VITE_API_KEY; // put this in .env

console.log("API KEY:", API_KEY);

export async function loginUser(identifier, password) {
  const response = await fetch(`${API_BASE_URL}/api/v1/auth/login`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-API-Key": API_KEY,
    },
    body: JSON.stringify({
      identifier, // <-- IMPORTANT CHANGE
      password,
    }),
  });

  if (!response.ok) {
    throw new Error("Login failed");
  }

  const data = await response.json();

  saveSessionToken(data.session_token);

  return data;
}