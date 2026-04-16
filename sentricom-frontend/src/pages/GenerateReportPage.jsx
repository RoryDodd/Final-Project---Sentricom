import { useState } from "react";
import PageContainer from "../components/PageContainer";
import Card from "../components/Card";

export default function GenerateReportPage() {
  const [formData, setFormData] = useState({
    startDate: "",
    endDate: "",
    zone: "all",
    reportType: "occupancy",
    format: "pdf",
  });

  const handleChange = (event) => {
    const { name, value } = event.target;

    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  const handleGenerate = (event) => {
    event.preventDefault();

    console.log("Generate report with:", formData);
    alert("Report generation will be connected to the backend later.");
  };

  return (
    <PageContainer
      title="Generate Report"
      subtitle="Create downloadable occupancy and incident reports by date, zone, and format"
    >
      <div className="report-grid">
        <Card title="Report Settings">
          <form className="report-form" onSubmit={handleGenerate}>
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

            <div className="form-group">
              <label htmlFor="zone">Zone</label>
              <select
                id="zone"
                name="zone"
                value={formData.zone}
                onChange={handleChange}
              >
                <option value="all">All Zones</option>
                <option value="zone1">Zone 1</option>
                <option value="zone2">Zone 2</option>
                <option value="zone3">Zone 3</option>
                <option value="zone4">Zone 4</option>
                <option value="zone5">Zone 5</option>
              </select>
            </div>

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

            <button type="submit" className="primary-button">
              Generate Report
            </button>
          </form>
        </Card>

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

            <div className="report-note">
              This panel can later show a backend-generated summary, estimated file size, or a mini preview before download.
            </div>
          </div>
        </Card>
      </div>
    </PageContainer>
  );
}