// Alert panel showing current warnings
export default function AlertPanel({ zones = [] }) {
  // Filter zones that need attention
  const alerts = zones.filter(
    (zone) => zone.status === "MEDIUM" || zone.status === "HIGH"
  );

  return (
    <div
    className="alert-panel"
    style={{
    maxHeight: "400px",
    overflowY: "auto",
      }}
    >
      
      {alerts.length > 0 ? (
        alerts.map((zone) => (
          <p key={zone.id}>
            {zone.zoneName} {zone.status === "HIGH" ? "overcrowded" : "increasing density"}
          </p>
        ))
      ) : (
        <p>No active warnings</p>
      )}
    </div>
  );
}