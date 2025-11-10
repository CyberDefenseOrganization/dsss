import Header from "../components/Header";
import Overview from "../components/Overview";

import { useStatusPoller } from "../hooks/useStatusPoller";
import { getOverview, type OverviewResponse, } from "../api/status";
import Footer from "../components/Footer";

function Home() {
    const overviewData: OverviewResponse | null = useStatusPoller(getOverview);

    return (
        <>
            <Header />
            <div className="bg-gray-950 flex flex-col w-full h-full items-center overflow-y-scroll">
                <div className="flex flex-col items-center w-full lg:p-4 lg:w-6xl h-full pt-6 gap-8 lg:gap-14 md:px-4">
                    {
                        overviewData && <Overview overviewData={overviewData} />
                    }
                </div>
            </div >
            <Footer data={overviewData} />
        </>
    );
}

export default Home;
