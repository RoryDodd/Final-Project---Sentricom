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
      <div style={{ display: "flex", justifyContent: "center" }}>
        <div style={{ width: "100%", maxWidth: "800px" }}>

          {/* Sentricom System Health-Check */}
          <Card title="Sentricom System Health-Check">

            {error && (
              <p style={{ color: "red" }}>
                Error: {error}
              </p>
            )}

            {/* Health-Check Results */}
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

                <table
                  className="summary-table"
                  style={{ width: "100%", marginTop: "8px" }}
                >
                  <thead>
                    <tr>
                      <th>Check</th>
                      <th>Status</th>
                    </tr>
                  </thead>

                  <tbody> 
                    {/* Populate table dynamically based on booleand health checks */}
                    {Object.entries(healthData.check_results)
                      .filter(([, value]) => typeof value === "boolean")
                      .map(([key, value]) => (
                        <tr key={key}>
                          <td>{key}</td>
                          <td>
                            <strong style={{ color: value ? "green" : "red" }}>
                              {value ? "PASS" : "FAIL"}
                            </strong>
                          </td>
                        </tr>
                      ))}
                  </tbody>
                </table>

                {/* Expanded privacy engine health and status */}
                {healthData.check_results.privacy_engine && (
                  <div style={{ marginTop: "8px" }}>
                    <h3>Privacy Engine App</h3>

                    <table
                      className="summary-table"
                      style={{ width: "100%"}}
                    >
                      <tbody>
                        {/* Dynamically filter results specific to privacy engine */}
                        {Object.entries(
                          healthData.check_results.privacy_engine
                        ).map(([key, value]) => (
                          <tr key={key}>
                            <td>{key}</td>
                            <td>
                              {typeof value === "boolean" 
                                ? value
                                  ? "true"
                                  : "false"
                                : String(value)}
                            </td>
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>
                )}

                {/* Manually refresh healthcheck data */}
                <div style={{ marginTop: "8px" }}>
                  <button
                    onClick={fetchHealth}
                    style={{
                      padding: "8px 12px",
                      borderRadius: "6px",
                      cursor: "pointer",
                    }}
                  >
                    Refresh
                  </button>

                  {loading && (
                    <span style={{ marginLeft: "10px", fontSize: "13px", color: "#666" }}>
                      Loading...
                    </span>
                  )}
                </div>
              </>
            )}
          </Card>
        </div>
      </div>
    </PageContainer>
  );
}