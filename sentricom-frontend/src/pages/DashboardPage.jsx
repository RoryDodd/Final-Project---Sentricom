import PageContainer from "../components/PageContainer";
import Card from "../components/Card";

import SummaryTable from "../components/SummaryTable";
import Heatmap from "../components/Heatmap";
import AlertPanel from "../components/AlertPanel";

export default function DashboardPage() {
  return (
    <PageContainer
      title="Overview"
      subtitle="Real-time monitoring of crowd density across zones"
    >
      <div className="dashboard-grid-2">

        {/* LEFT COLUMN */}
        <div className="dashboard-stack">

          <Card title="Warnings">
            <AlertPanel />
          </Card>

          <Card title="Incident Timeline">
            {/* placeholder for now */}
            <div className="placeholder-box">Timeline coming soon</div>
          </Card>

        </div>

        {/* RIGHT COLUMN */}
        <div className="dashboard-stack">

          <Card title="Quick Summary">
            <SummaryTable />
          </Card>

          <Card title="Zones">
            <Heatmap />
          </Card>

        </div>

      </div>
    </PageContainer>
  );
}