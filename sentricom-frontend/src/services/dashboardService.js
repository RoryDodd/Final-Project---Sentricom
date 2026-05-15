import { apiFetch } from "./api";

// Send dashboard zone request with API base and previously computed token
export async function getDashboardZones(token) {
  try {
    return await apiFetch("/api/v1/zones/latest", {
      includeContentType: false,
      includeApiKey: false,
    }, token);
  }  
  catch (error) {
    console.error("API unknown error:", error);
    throw new Error("Failed to load API");
  }   
}