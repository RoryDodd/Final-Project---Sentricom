import PageContainer from "../components/PageContainer";
import { useEffect, useState, useRef } from "react";

import { getDashboardZones } from "../services/dashboardService";
import { transformZoneResults } from "../utils/transforms";

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

  // Load dashboard data
  useEffect(() => {

    if (hasLoaded.current) return;

    hasLoaded.current = true;

    async function loadData() {

      try {

        // Check for valid session token
        const token = getSessionToken();

        if (!token) {
          setError("No active session found");
          setLoading(false);
          return;
        }

        // Fetch and transform backend data
        const rawData = await getDashboardZones();
        const transformed = transformZoneResults(rawData);

        setZones(transformed);
        setError("");

      } catch (err) {

        console.error(err);

        if (err.message?.includes("401")) {
          setError("Session expired. Please login again.");
        } else {
          setError("Failed to load dashboard data");
        }

      } finally {

        setLoading(false);

      }
    }

    // Initial load
    loadData();

    // Auto refresh every 10 seconds
    const interval = setInterval(() => {
      loadData();
    }, 10000);

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

    <PageContainer
      title="Overview"
      subtitle="Real-time monitoring of crowd density across zones"
    >

      <div className="dashboard-grid-2">

        {/* Left column */}
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

        {/* Right column */}
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