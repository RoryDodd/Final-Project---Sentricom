export function transformZoneResults(data) {
  const zones = Array.isArray(data)
    ? data
    : data.zones || data.results || [];

  return zones.map((item, index) => ({
    id: item.zone_id || index + 1,
    zoneId: item.zone_id || `zone-${index + 1}`,
    zoneName: item.zone_name || item.zone || item.image || `Zone ${index + 1}`,
    count: item.dp_count ?? item.noisy_count ?? 0,
    capacity: item.capacity ?? 0,
    status: (item.risk_status || item.noisy_decision || "low").toUpperCase(),
    confidence: item.average_confidence ?? null,
    timestamp: item.timestamp || null,
  }));
}