import { getSessionToken } from "../utils/auth";

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;
const API_KEY = import.meta.env.VITE_API_KEY;

export async function apiFetch(endpoint, options = {}, tokenOverride = null) {

  try {
    // Use provided token or fallback to storage
    const token = tokenOverride || getSessionToken();

    // Prevent API calls without authentication
    if (!token) {
      throw new Error("Missing session token");
    }

    // Define options - not all calls need all options
    const {
      includeApiKey = true, // default include
      includeContentType = true, // default include
      headers: customHeaders = {},
      ...restOptions
    } = options;

    const response = await fetch(`${API_BASE_URL}${endpoint}`, {
      ...restOptions,
      headers: {
        ...(includeContentType && { "Content-Type": "application/json" }),
        "X-Session-Token": token,
        ...(includeApiKey && { "X-API-Key": API_KEY}),
        ...customHeaders,
      },
    });

    // Handle failed API requests
    if (!response.ok) {
      throw new Error(`API request failed: ${response.status}`);
    }

    return response.json();
  } 
  catch (error) {
    console.error("Fetch error:", error);
    throw new Error("Failed to fetch API data");
  }
}