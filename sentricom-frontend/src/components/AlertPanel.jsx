// Alert panel showing current warnings
export default function AlertPanel() {

  // Static alert messages (replace with real data later)
  const alerts = [
    "Zone 5 overcrowded",
    "Zone 2 increasing density",
  ];

  return (
    <div className="alert-panel">
      {/* Render each alert */}
      {alerts.map((alert, index) => (
        <p key={index}>{alert}</p>
      ))}
    </div>
  );
}