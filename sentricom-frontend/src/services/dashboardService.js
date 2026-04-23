import { apiFetch } from "./api";

export async function getDashboardZones() {
  return apiFetch("/api/v1/zones/latest");
}