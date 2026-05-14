import { apiFetch } from "./api";

/*
export async function getDashboardZones() {
  try {
    return await apiFetch("/api/v1/zones/latest");
  } catch (error) {
    console.error("API failed:", error);
    throw new Error("Failed to load API");
  }
}
*/

export async function getDashboardZones(token) {
  try {
    const response = await fetch(`${import.meta.env.VITE_API_BASE_URL}/api/v1/zones/latest`, {
      headers: {
        //"Content-Type": "application/json",
        //Authorization: `Bearer ${token}`,
        "X-Session-Token": token,
      },
    });

    if (!response.ok) {
      throw new Error(`API request failed: ${response.status}`);
    }
    return await response.json();
  }
  catch (error) {
    console.error("API unknown error:", error);
    throw new Error("Failed to load API");
  }
}