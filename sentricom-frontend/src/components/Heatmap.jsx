// Heatmap component to visualize zone activity levels
export default function Heatmap() {
  // static data for zones and their activity levels
  const zones = [
    { id: 1, level: "low" },
    { id: 2, level: "medium" },
    { id: 3, level: "high" },
    { id: 4, level: "medium" },
    { id: 5, level: "low" },
    { id: 6, level: "high" },
  ];

  // function to get color based on activity level
  const getColor = (level) => {
    if (level === "low") return "#4CAF50";      // green
    if (level === "medium") return "#FFC107";   // yellow
    if (level === "high") return "#F44336";     // red
    return "#ccc";
  };

  return (
    // container for the heatmap
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

      {/* Grid */}
      <div
        style={{
          display: "grid",
          gridTemplateColumns: "repeat(3, 1fr)",
          gap: "15px",
          marginTop: "15px",
        }}
      >
        // loop through zones and display each zone with its corresponding color
        {zones.map((z) => (
          <div
            key={z.id} // unique key for each zone
            style={{
              height: "80px",
              borderRadius: "10px",
              background: getColor(z.level), // set background color based on activity level
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              color: "#fff",
              fontWeight: "bold",
            }}
          >
            // display zone id in the center of the box
            Zone {z.id}
            
          </div>
        ))}
        
        {/* Legend */}
        <div style={{ marginTop: "15px", fontSize: "14px" }}>
        <div><span style={{ color: "#4CAF50" }}>■</span> Low</div>
        <div><span style={{ color: "#FFC107" }}>■</span> Medium</div>
        <div><span style={{ color: "#F44336" }}>■</span> High</div>
</div>
      </div>
    </div>
  );
}