// Import layout wrapper for consistent page structure
import PageContainer from "../components/PageContainer";
import { useEffect, useState } from "react";

// Import services and data transformation utilities
import { getDashboardZones } from "../services/dashboardService";
import { transformZoneResults } from "../utils/transforms";

// Import reusable UI components
import Card from "../components/Card";

// Import dashboard-specific components
import SummaryTable from "../components/SummaryTable";
import Heatmap from "../components/Heatmap";
import AlertPanel from "../components/AlertPanel";

// DashboardPage displays the main overview of system data
export default function DashboardPage() {

  // State for zone data, loading status, and error messages
  const [zones, setZones] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
    // Load dashboard data on component mount
    useEffect(() => {
    async function loadData() {
      try {
        const rawData = await getDashboardZones();
        const transformed = transformZoneResults(rawData);
        setZones(transformed);
      } catch (err) {
        console.error(err);
        setError("Failed to load dashboard data");
      } finally {
        setLoading(false);
      }
    }

    loadData();
  }, []);

    if (loading) {
     return <div style={{ color: "white", padding: "20px" }}>Loading dashboard...</div>;
  }

  if (error) {
    return <div style={{ color: "red", padding: "20px" }}>{error}</div>;
  }
  return (
    // PageContainer provides title, subtitle, and consistent spacing
    <PageContainer
      title="Overview"
      subtitle="Real-time monitoring of crowd density across zones"
    >
      
      {/* Main 2-column dashboard layout */}
      <div className="dashboard-grid-2">

        {/* LEFT COLUMN: Alerts and timeline */}
        <div className="dashboard-stack">

          {/* Warnings / alerts section */}
          <Card title="Warnings">
            <AlertPanel zones={zones} />
          </Card>

          {/* Incident timeline (not implemented yet) */}
          <Card title="Incident Timeline">
            {/* Placeholder content until timeline is built */}
            <div className="placeholder-box">Timeline coming soon</div>
          </Card>

        </div>

        {/* RIGHT COLUMN: Summary and visualisation */}
        <div className="dashboard-stack">

          {/* Summary table of zone data */}
          <Card title="Quick Summary">
            <SummaryTable zones={zones} />
          </Card>

          {/* Heatmap visualisation of zones */}
          <Card title="Zones">
            <Heatmap zones={zones} />
          </Card>

        </div>

      </div>
    </PageContainer>
  );
}