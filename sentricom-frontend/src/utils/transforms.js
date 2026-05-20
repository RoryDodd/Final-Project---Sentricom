export function transformZoneResults(data) {
  const zones = Array.isArray(data)
    ? data
    : data.zones || data.results || [];

    // Normalize status values and ensure consistent structure
  return zones.map((item, index) => ({
    id: item.zone_id || index + 1,
    readingId: item.reading_id ?? null,
    zoneId: item.zone_id || `zone-${index + 1}`,
    zoneName: item.zone_name || item.zone || item.image || `Zone ${index + 1}`,
    count: item.dp_count ?? item.noisy_count ?? 0,
    capacity: item.capacity ?? 0,
    status: normalizeStatus(item.risk_status || item.noisy_decision),
    confidence: item.average_confidence ?? null,
    timestamp: item.timestamp || null,
  }));
  
 function normalizeStatus(value) {
  const status = String(value || "safe").toUpperCase();

  if (status.includes("EVACUATE") || status.includes("HIGH")) return "EVACUATE";
  if (status.includes("MONITOR") || status.includes("MEDIUM")) return "MONITOR";
  if (status.includes("SAFE") || status.includes("LOW")) return "SAFE";

  return "UNKNOWN";
}
}