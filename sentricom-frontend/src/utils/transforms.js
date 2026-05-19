export function transformZoneResults(data) {
  const zones = Array.isArray(data)
    ? data
    : data.zones || data.results || [];

    // Normalize status values and ensure consistent structure
  return zones.map((item, index) => ({
    id: item.zone_id || index + 1,
    zoneId: item.zone_id || `zone-${index + 1}`,
    zoneName: item.zone_name || item.zone || item.image || `Zone ${index + 1}`,
    count: item.dp_count ?? item.noisy_count ?? 0,
    capacity: item.capacity ?? 0,
    status: normalizeStatus(item.risk_status || item.noisy_decision),
    confidence: item.average_confidence ?? null,
    timestamp: item.timestamp || null,
  }));
  
  function normalizeStatus(value) {
  const status = String(value || "low").toUpperCase();

  if (status.includes("HIGH")) return "HIGH";
  if (status.includes("MEDIUM")) return "MEDIUM";
  if (status.includes("LOW")) return "LOW";

  return "UNKNOWN";
}
}