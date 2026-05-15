// src/pages/SystemInfoPage.jsx

import { useState, useEffect } from "react";
// Shared layout components
import PageContainer from "../components/PageContainer";
import Card from "../components/Card";
// Healthcheck page - could also contain other config
export default function SystemInfoPage() {

  // Store currently selected privacy method
  const [healthData, setHealthData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Get healthcheck
  useEffect(() => {
    fetchHealth()
  }, []);
  
  const fetchHealth = async () => {
    setLoading(true);
    setError(null);

    try {
      //const response = await fetch("/api/v1/health", {
      const response = await fetch("http://localhost:8082/api/v1/health", {
        headers: {
          "X-API-Key": "2a92652f69031a93302e5ec20f0758a9f364e7206b300fa027118f2d71a1e7aa"
        },
      });

      const data = await response.json();
      setHealthData(data);
    }
    catch (err) {
      setError(err.message);
    }
    finally {
      setLoading(false);
    }
  };


  return (
    <PageContainer
      title="System Info"
      subtitle="Live system health and service status"
    >

      <div className="dashboard-grid-2">

        <Card title="API Health">

            <button
              onClick={fetchHealth}
              style={{
                marginBottom: "12px",
                padding: "8px 12px",
                borderRadius: "6px",
                cursor: "pointer",
              }}
            >
              Refresh
            </button>

          {loading && <p>Loading...</p>}

          {error && (
            <p style={{ color: "red" }}>
              Error: {error}
            </p>
          )}

          {healthData && (
            <>
              <p>
                Status:{" "}
                <strong
                  style={{
                    color: healthData?.status?.includes("passed")
                      ? "green"
                      : "red",
                  }}
                >
                  {healthData.status}
                </strong>
              </p>

              <p>
                Privacy Engine:{" "}
                <strong
                  style={{
                    color: healthData?.check_results?.privacy_engine_reachable
                      ? "green"
                      : "red",
                  }}
                >
                  {healthData?.check_results?.privacy_engine_reachable
                    ? "Online"
                    : "Offline"}
                </strong>
              </p>

              <pre
                style={{
                  fontSize: "12px",
                  background: "#f5f5f5",
                  padding: "10px",
                  borderRadius: "8px",
                  overflowX: "auto",
                }}
              >
                {JSON.stringify(healthData, null, 2)}
              </pre>
            </>
          )}

        </Card>
      </div>
    </PageContainer>
  );
}