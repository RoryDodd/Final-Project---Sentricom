// Table showing zone status
export default function SummaryTable({ zones = [] }) {
  const getStatusStyle = (status) => {
    switch (status) {
      case "LOW":
        return { background: "#4CAF50", color: "#fff" };
      case "MEDIUM":
        return { background: "#FFC107", color: "#000" };
      case "HIGH":
        return { background: "#F44336", color: "#fff" };
      default:
        return { background: "#ccc", color: "#000" };
    }
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
      <h3>Zone Summary</h3>

      {/* Table */}
      <table
        style={{
          width: "100%",
          borderCollapse: "collapse",
          marginTop: "10px",
        }}
      >
        {/* Header */}
        <thead>
  <tr>
    <th style={{ padding: "8px", borderBottom: "1px solid #ddd", textAlign: "left" }}>
      Zone
    </th>
    <th style={{ padding: "8px", borderBottom: "1px solid #ddd", textAlign: "left" }}>
      Occupancy
    </th>
    <th style={{ padding: "8px", borderBottom: "1px solid #ddd", textAlign: "left" }}>
      Capacity
    </th>
    <th style={{ padding: "8px", borderBottom: "1px solid #ddd", textAlign: "left" }}>
      Status
    </th>
  </tr>
</thead>

        {/* Rows */}
         <tbody>
          {zones.map((zone) => (
            <tr key={zone.id}>
              <td style={{ padding: "8px" }}>{zone.zoneName}</td>
              <td style={{ padding: "8px" }}>{zone.count}</td>
              <td style={{ padding: "8px" }}>{zone.capacity}</td>

              <td style={{ padding: "8px" }}>
                <span
                  style={{
                    padding: "4px 10px",
                    borderRadius: "8px",
                    fontSize: "12px",
                    fontWeight: "bold",
                    ...getStatusStyle(zone.status),
                  }}
                >
                  {zone.status}
                </span>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}