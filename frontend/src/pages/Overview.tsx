import PageShell from "../components/PageShell";
import OverviewTable from "../components/Overview";
import Fullscreen from "../components/Fullscreen";
import { getOverview, type OverviewResponse } from "../api/status";
import { useStatusPoller } from "../hooks/useStatusPoller";

function Overview() {
    const overviewData: OverviewResponse | null = useStatusPoller(getOverview);

    return (
        <PageShell data={overviewData}>
            {overviewData ? (
                <Fullscreen keyboard className="flex min-w-0 flex-col gap-4">
                    {(isFullscreen) => <OverviewTable overviewData={overviewData} fullscreen={isFullscreen} />}
                </Fullscreen>
            ) : (
                <p className="text-sm text-center text-[#E0E0E0]">
                    Loading data...
                </p>
            )}
        </PageShell>
    );
}

export default Overview;
