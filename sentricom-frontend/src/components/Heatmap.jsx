// Heatmap for zone activity
export default function Heatmap({ zones = [] }) {
  // Get color from risk status
  const getColor = (status) => {
    if (status === "SAFE") return "#4CAF50";
    if (status === "MONITOR") return "#FFC107";
    if (status === "EVACUATE") return "#F44336";
    return "#ccc";
  };

  return (
    <div
      style={{
        background: "#fff",
        padding: "15px",
        borderRadius: "10px",
        color: "#000",
        boxShadow: "0 2px 8px rgba(0,0,0,0.1)",
      }}
    >
      <h3>Zone Heatmap</h3>

      <div
        style={{
          display: "grid",
          gridTemplateColumns: "repeat(3, 1fr)",
          gap: "15px",
          marginTop: "15px",
        }}
      >
        {zones.map((zone) => (
          <div
            key={zone.id}
            style={{
              minHeight: "80px",
              borderRadius: "10px",
              background: getColor(zone.status),
              display: "flex",
              flexDirection: "column",
              alignItems: "center",
              justifyContent: "center",
              color: zone.status === "MONITOR" ? "#000" : "#fff",
              fontWeight: "bold",
              textAlign: "center",
            }}
          >
            <div>{zone.zoneName}</div>
            <small>
              {zone.count} / {zone.capacity}
            </small>
          </div>
        ))}
      </div>

      <div style={{ marginTop: "15px", fontSize: "14px" }}>
        <div>
          <span style={{ color: "#4CAF50" }}>■</span> SAFE
        </div>
        <div>
          <span style={{ color: "#FFC107" }}>■</span> MONITOR
        </div>
        <div>
          <span style={{ color: "#F44336" }}>■</span> EVACUATE
        </div>
      </div>
    </div>
  );
}