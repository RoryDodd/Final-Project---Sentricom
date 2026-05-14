import PageContainer from "../components/PageContainer";
import { useEffect, useState, useRef } from "react";

import { getDashboardZones } from "../services/dashboardService";
import { transformZoneResults } from "../utils/transforms";

import Card from "../components/Card";
import SummaryTable from "../components/SummaryTable";
import Heatmap from "../components/Heatmap";
import AlertPanel from "../components/AlertPanel";

import { getSessionToken } from "../utils/auth";

// DEBUG HELPER
function getTokenFromMemoryOrStorage(tokenRef) {
  if (tokenRef.current) {
    return tokenRef.current;
  }

  const storedToken = getSessionToken();

  if (storedToken) {
    tokenRef.current = storedToken;
  }

  return storedToken;
}

// Main dashboard page
export default function DashboardPage() {

  // Dashboard state
  const [zones, setZones] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  //const [token, setToken] = useState("");
  const tokenRef = useRef(null);

  // Prevent duplicate API calls in React StrictMode
  //const hasLoaded = useRef(false);

  // Lets make sure we have a session token first
  //const sessionToken = getSessionToken();
  //setToken(sessionToken);

  // Load dashboard data
  useEffect(() => {
    //debug
    let isMounted = true; // while true
    //if (hasLoaded.current) return;
    //hasLoaded.current = true;
    
    // Cache the token in a ref to prevent stale closures in setInterval
    //tokenRef.current = getSessionToken();

    async function loadData() {
      
      const sessionToken = getTokenFromMemoryOrStorage(tokenRef);

      if (!sessionToken) {
        setError("No active session found");
        setLoading(false);
        return;
      }
      
      try {
        /*
        if (!token) {
          setError("No active session found");
          setLoading(false);
          return;
        }
        */
        // Fetch and transform backend data
        const rawData = await getDashboardZones(sessionToken);
        const transformed = transformZoneResults(rawData);

        if (isMounted) {
          setZones(transformed);
          setError("");
        }
      } catch (err) {
        console.error(err);

        if (isMounted) {
          if (err.message?.includes("401")) {
            setError("Session expired. Please login again.");
          } else {
            setError("Failed to load dashboard data");
          }
        }
      } finally {
        if (isMounted) {
        setLoading(false);
      }
    }
  }

    // Initial load
    loadData();

    // Auto refresh every 10 seconds
    /*
    const interval = setInterval(() => {
      loadData();
    }, 10000);
    */
    const interval = setInterval(loadData, 5000);

    return () => {
      isMounted = false;
      clearInterval(interval);
    };
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