// Table showing zone status
export default function SummaryTable() {

  // Get style from status
  const getStatusStyle = (status) => {
    switch (status) {
      case "NORMAL":
        return { background: "#4CAF50", color: "#fff" };
      case "BUSY":
        return { background: "#FFC107", color: "#000" };
      case "CROWDED":
        return { background: "#FF9800", color: "#fff" };
      case "MAX_CAPACITY":
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
            <th style={{ padding: "8px", borderBottom: "1px solid #ddd" }}>
              Zone
            </th>
            <th style={{ padding: "8px", borderBottom: "1px solid #ddd" }}>
              Occupancy
            </th>
            <th style={{ padding: "8px", borderBottom: "1px solid #ddd" }}>
              Status
            </th>
          </tr>
        </thead>

        {/* Rows */}
        <tbody>
          {[
            // Static data (replace with API later)
            { zone: "Zone 1", occupancy: 20, status: "NORMAL" },
            { zone: "Zone 2", occupancy: 35, status: "BUSY" },
            { zone: "Zone 3", occupancy: 50, status: "CROWDED" },
          ].map((z, index) => (
            <tr key={index}>
              <td style={{ padding: "8px" }}>{z.zone}</td>
              <td style={{ padding: "8px" }}>{z.occupancy}</td>

              <td style={{ padding: "8px" }}>
                <span
                  style={{
                    padding: "4px 10px",
                    borderRadius: "8px",
                    fontSize: "12px",
                    fontWeight: "bold",
                    ...getStatusStyle(z.status),
                  }}
                >
                  {z.status}
                </span>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}