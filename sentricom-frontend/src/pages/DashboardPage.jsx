import PageContainer from "../components/PageContainer";
import { useEffect, useState, useRef } from "react";

import { getDashboardZones } from "../services/dashboardService";
import { transformZoneResults } from "../utils/transforms";

import Card from "../components/Card";
import SummaryTable from "../components/SummaryTable";
import Heatmap from "../components/Heatmap";
import AlertPanel from "../components/AlertPanel";

import { getSessionToken } from "../utils/auth";

/*** TOKEN HANDLING HELPER 
 * 
 * This helper function retrieves the session token from memory (ref) or storage.
 * It first checks if the token is already cached in the ref. If not, it fetches
 * the token from storage and caches it in the ref for future use.
 * 
***/

/* TODO:
 * - Consider implementing a token refresh mechanism if the API supports it, to handle expired tokens gracefully.
 * - Add error handling for token retrieval failures, such as corrupted storage or missing token scenarios.
 * - Track what data has previously been fetched - likely needs both client-side and server-side support - to optimize API calls and reduce unnecessary data fetching.
*/
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

/*** MAIN DASHBOARD LOGIC ***/
export default function DashboardPage() {

  // Dashboard state
  const [zones, setZones] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const tokenRef = useRef(null);

  // Load dashboard data
  useEffect(() => {
    // Using isMounted flag to prevent state updates on unmounted component during async operations
    let isMounted = true; // while true

    async function loadData() {
      
      const sessionToken = getTokenFromMemoryOrStorage(tokenRef);

      if (!sessionToken) {
        setError("No active session found");
        setLoading(false);
        return;
      }

      // Fetch and transform backend data
      try {
        
        const rawData = await getDashboardZones(sessionToken); // pass token since we've already computed it here
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

    // Simplified polling call
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


  /*** MAIN DASHBOARD PRESENTATION ***/
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