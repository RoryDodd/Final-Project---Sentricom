// Import React hook for managing component state
import { useState } from "react";

// Import reusable layout and card components
import PageContainer from "../components/PageContainer";
import Card from "../components/Card";

// Import API service for fetching dashboard zones 
import { useEffect } from "react";
import { getDashboardZones } from "../services/dashboardService";

// GenerateReportPage allows users to configure and preview report options
export default function GenerateReportPage() {
  // Store form input values for report generation
  const [formData, setFormData] = useState({
  
    startDate: "",
    endDate: "",
    zone: "all",
    reportType: "occupancy",
    format: "pdf",
  });

  const [zones, setZones] = useState([]);
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

  // Handle form submission
  const handleGenerate = (event) => {
    event.preventDefault(); // Prevent page reload on submit

    // Placeholder logic until backend integration is added
    console.log("Generate report with:", formData);
    alert("Report generation will be connected to the backend later.");
  };

  return (
    // Page layout wrapper with heading and subtitle
    <PageContainer
      title="Generate Report"
      subtitle="Create downloadable occupancy and incident reports by date, zone, and format"
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
               <option
               key={`${zone.id}-${zone.zoneName}`}
               value={zone.id}
                >
              {zone.zoneName}
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
                <option value="incident">Incident Report</option>
                <option value="evacuation">Evacuation Summary</option>
                <option value="full">Full System Report</option>
              </select>
            </div>

            {/* Output format selection */}
            <div className="form-group">
              <label htmlFor="format">Output Format</label>
              <select
                id="format"
                name="format"
                value={formData.format}
                onChange={handleChange}
              >
                <option value="pdf">PDF</option>
                <option value="csv">CSV</option>
                <option value="json">JSON</option>
              </select>
            </div>

            {/* Submit button */}
            <button type="submit" className="primary-button">
              Generate Report
            </button>
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
              <span className="preview-label">Format</span>
              <span className="preview-value">{formData.format}</span>
            </div>

            <div className="preview-item">
              <span className="preview-label">Date Range</span>
              <span className="preview-value">
                {formData.startDate && formData.endDate
                  ? `${formData.startDate} to ${formData.endDate}`
                  : "Not selected"}
              </span>
            </div>

            {/* Placeholder note for future backend preview functionality */}
            <div className="report-note">
              This panel can later show a backend-generated summary, estimated file size, or a mini preview before download.
            </div>
          </div>
        </Card>

      </div>
    </PageContainer>
  );
}