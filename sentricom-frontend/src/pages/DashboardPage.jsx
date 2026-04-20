// Import layout wrapper for consistent page structure
import PageContainer from "../components/PageContainer";

// Import reusable UI components
import Card from "../components/Card";

// Import dashboard-specific components
import SummaryTable from "../components/SummaryTable";
import Heatmap from "../components/Heatmap";
import AlertPanel from "../components/AlertPanel";

// DashboardPage displays the main overview of system data
export default function DashboardPage() {
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
            <AlertPanel />
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
            <SummaryTable />
          </Card>

          {/* Heatmap visualisation of zones */}
          <Card title="Zones">
            <Heatmap />
          </Card>

        </div>

      </div>
    </PageContainer>
  );
}