// AlertPanel component that displays important alerts related to zone overcrowding and density
export default function AlertPanel() {
   const alerts = [
    "Zone 5 overcrowded",
     "Zone 2 increasing density",
    ];
    
  // Render the alert panel with the list of alerts
   return (
  <div className="alert-panel">
    {alerts.map((alert, index) => (
      <p key={index}>“{alert}”</p>
    ))}
  </div>
);
 }
