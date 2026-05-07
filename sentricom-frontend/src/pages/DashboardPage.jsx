// Layout wrapper and React hooks
import PageContainer from "../components/PageContainer";
import { useEffect, useState, useRef } from "react";

// API services and data transformation utilities
import { getDashboardZones } from "../services/dashboardService";
import { transformZoneResults } from "../utils/transforms";

// Reusable UI components
import Card from "../components/Card";
import SummaryTable from "../components/SummaryTable";
import Heatmap from "../components/Heatmap";
import AlertPanel from "../components/AlertPanel";

import { getSessionToken } from "../utils/auth";

// Main dashboard page
export default function DashboardPage() {

  // Dashboard state
  const [zones, setZones] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  // Prevent duplicate API calls in React StrictMode
  const hasLoaded = useRef(false);

  // Load dashboard data on page load
  useEffect(() => {

  // Prevent duplicate API calls in React StrictMode
  if (hasLoaded.current) return;

  hasLoaded.current = true;

  async function loadData() {
    try {

      // Fetch and transform backend zone data
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

  // Initial dashboard load
  loadData();
    const token = getSessionToken();

    if (!token) return;

  // Refresh dashboard data every 10 seconds
  const interval = setInterval(loadData, 10000);

  // Cleanup interval when component unmounts
  return () => clearInterval(interval);

}, []);

  // Loading screen
  if (loading) {
    return (
      <div style={{ color: "white", padding: "20px" }}>
        Loading dashboard...
      </div>
    );
  }

  // Error screen
  if (error) {
    return (
      <div style={{ color: "red", padding: "20px" }}>
        {error}
      </div>
    );
  }

  return (

    // Main dashboard layout
    <PageContainer
      title="Overview"
      subtitle="Real-time monitoring of crowd density across zones"
    >

      <div className="dashboard-grid-2">

        {/* Left dashboard column */}
        <div className="dashboard-stack">

          <Card title="Warnings">
            <AlertPanel zones={zones} />
          </Card>

          <Card title="Incident Timeline">
            <div className="placeholder-box">
              Timeline coming soon
            </div>
          </Card>

        </div>

        {/* Right dashboard column */}
        <div className="dashboard-stack">

          <Card title="Quick Summary">
            <SummaryTable zones={zones} />
          </Card>

          <Card title="Zones">
            <Heatmap zones={zones} />
          </Card>

        </div>

      </div>

    </PageContainer>
  );
}