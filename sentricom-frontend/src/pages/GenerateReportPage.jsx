// Import React hook for managing component state
import { useState } from "react";

// Import reusable layout and card components
import PageContainer from "../components/PageContainer";
import Card from "../components/Card";

// Import API service for fetching dashboard zones 
import { useEffect } from "react";
import { getDashboardZones } from "../services/dashboardService";

import { apiFetch } from "../services/api";

// GenerateReportPage allows users to configure and preview report options
export default function GenerateReportPage() {

  
  
// Store form input values for report generation
 const [formData, setFormData] = useState({
  startDate: "",
  endDate: "",
  zone: "all",
  reportType: "occupancy",
});

  const [zones, setZones] = useState([]);
  const [report, setReport] = useState(null);
  const [error, setError] = useState("");
  const [isGenerating, setIsGenerating] = useState(false);
  useEffect(() => {

  async function loadZones() {
    try {

      const data = await getDashboardZones();
      setZones(data);

    } catch (err) {

      console.error(err);

    }
  }

  loadZones();

}, []);
  // Update form state when any input field changes
  const handleChange = (event) => {
    const { name, value } = event.target;

    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  const handleGenerate = async (event) => {
  event.preventDefault();

  setError("");
  setReport(null);
  setIsGenerating(true);

  try {
    const params = new URLSearchParams();

    if (formData.startDate) {
      params.set("from_timestamp", `${formData.startDate}T00:00:00`);
    }

    if (formData.endDate) {
      params.set("to_timestamp", `${formData.endDate}T23:59:59`);
    }

    if (formData.zone !== "all") {
      params.set("zone_id", formData.zone);
    }

    const data = await apiFetch(`/api/v1/reports/occupancy/history?${params}`, {
     includeContentType: false,
    });

   setReport(data);

    const jsonBlob = new Blob([JSON.stringify(data, null, 2)], {
      type: "application/json",
    });

    const downloadUrl = URL.createObjectURL(jsonBlob);
    const downloadLink = document.createElement("a");

    downloadLink.href = downloadUrl;
    downloadLink.download = "occupancy-report.json";
    downloadLink.click();

    URL.revokeObjectURL(downloadUrl);

      console.log("Generated report:", data);
  } catch (err) {
    console.error(err);

    if (err.status === 401) {
      setError("Session expired. Please log in again.");
    } else {
      setError("Failed to generate report. Please try again.");
    }
    } finally {
    setIsGenerating(false);
      }
    };

  return (
    // Page layout wrapper with heading and subtitle
    <PageContainer
      title="Generate Report"
      subtitle="Generate reports by date range and zone"

    >
      {/* Two-column layout: form settings + live preview */}
      <div className="report-grid">

        {/* Report settings form */}
        <Card title="Report Settings">
          <form className="report-form" onSubmit={handleGenerate}>

            {/* Date range inputs */}
            <div className="form-row">
              <div className="form-group">
                <label htmlFor="startDate">Start Date</label>
                <input
                  id="startDate"
                  name="startDate"
                  type="date"
                  value={formData.startDate}
                  onChange={handleChange}
                />
              </div>

              <div className="form-group">
                <label htmlFor="endDate">End Date</label>
                <input
                  id="endDate"
                  name="endDate"
                  type="date"
                  value={formData.endDate}
                  onChange={handleChange}
                />
              </div>
            </div>

            {/* Zone selection */}
               <div className="form-group">
                <label htmlFor="zone">Zone</label>
                <select
                 id="zone"
                 name="zone"
                 value={formData.zone}
                 onChange={handleChange}
               >

             <option value="all">All Zones</option>

              {zones.map((zone) => (
                <option key={zone.zone_id} value={zone.zone_id}>
                {zone.zone_name}
                </option>
              ))}

            </select> </div>
            {/* Report type selection */}
            <div className="form-group">
              <label htmlFor="reportType">Report Type</label>
              <select
                id="reportType"
                name="reportType"
                value={formData.reportType}
                onChange={handleChange}
              >
                <option value="occupancy">Occupancy Report</option>
               
              </select>
            </div>

            {/* Submit button */}
              <button type="submit" className="primary-button" disabled={isGenerating}>
                {isGenerating ? "Generating..." : "Generate Report"}
              </button>

                {error && <p style={{ color: "red" }}>{error}</p>}

          </form>
        </Card>

        {/* Live preview of selected report settings */}
        <Card title="Report Preview">
          <div className="report-preview">

            <div className="preview-item">
              <span className="preview-label">Selected Zone</span>
              <span className="preview-value">{formData.zone}</span>
            </div>

            <div className="preview-item">
              <span className="preview-label">Report Type</span>
              <span className="preview-value">{formData.reportType}</span>
            </div>

            <div className="preview-item">
              <span className="preview-label">Export Type</span>
              <span className="preview-value">JSON Report</span>
            </div>

            <div className="preview-item">
              <span className="preview-label">Date Range</span>
              <span className="preview-value">
                {formData.startDate && formData.endDate
                  ? `${formData.startDate} to ${formData.endDate}`
                  : "Not selected"}
              </span>
            </div>

            {report && (
              <pre className="report-note">
                {JSON.stringify(report, null, 2)}
              </pre>
            )}

          </div>
        </Card>

      </div>
    </PageContainer>
  );
}