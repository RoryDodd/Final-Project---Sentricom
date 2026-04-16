export default function AlertPanel() {
   const alerts = [
    "Zone 5 overcrowded",
     "Zone 2 increasing density",
    ];
  
   return (
  <div className="alert-panel">
    {alerts.map((alert, index) => (
      <p key={index}>“{alert}”</p>
    ))}
  </div>
);
 }
