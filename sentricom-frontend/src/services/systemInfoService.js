import { apiFetch } from "./api";

// Send dashboard zone request with API base and previously computed token
export async function getPrivEngHealth() {
  try {
    return await apiFetch("/api/v1/health", {
      includeApiKey: true
    }); 
  }  
  catch (error) {
    console.error("API unknown error:", error);
    throw new Error("Failed to load API");
  }   
}

// TODO - add get scenario sim health