import { apiFetch } from "./api";

export async function getDashboardZones() {
  try {
    return await apiFetch("/api/v1/zones/latest");
  } catch (error) {
    console.error("API failed:", error);
    throw new Error("Failed to load API");
  }
}