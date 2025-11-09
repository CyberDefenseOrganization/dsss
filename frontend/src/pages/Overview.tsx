import Header from "../components/Header";
import { useStatusPoller } from "../hooks/useStatusPoller";
import { getOverview, type OverviewResponse, } from "../api/status";
import { faArrowCircleUp, faCircleArrowDown, faCircleArrowUp } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";

function Home() {
    const overviewData: OverviewResponse | null = useStatusPoller(getOverview);
    let services;
    if (overviewData) {
        services = Object.keys(overviewData!.overview[Object.keys(overviewData!.overview)[0]].services)
    }
    return (
        <>
            <Header />
            <div className="bg-gray-950 flex flex-col w-full h-full items-center overflow-y-scroll">
                <div className="flex flex-col items-center w-full lg:p-4 lg:w-6xl h-full pt-6 gap-8 lg:gap-14 md:px-4">
                    {
                        overviewData &&
                        <table className="table-auto font-mono text-gray-200 w-full text-lg mt-40">
                            <thead>
                                <tr>
                                    <th className="py-4"></th>
                                    {
                                        services.map((service) => (
                                            <th className="">
                                                <div className="-rotate-50 -translate-y-27 -translate-x-5 absolute">
                                                    <div className="text-lg text-nowrap text-left w-64 overflow-hidden">
                                                        {service}
                                                    </div>
                                                </div>
                                            </th>
                                        ))
                                    }
                                </tr>
                            </thead>
                            <tbody>
                                {
                                    Object.keys(overviewData.overview).map((team) => (
                                        <tr>
                                            <td>
                                                <div className="font-mono font-bold text-2xl p-4">
                                                    {team}
                                                </div>
                                            </td>
                                            {
                                                Object.values(overviewData.overview[team].services).map((service) => (
                                                    <td className="font-mono border-indigo-300 border-3">
                                                        <div className="group flex justify-center align-middle p-2">
                                                            {
                                                                service.online ?
                                                                    <FontAwesomeIcon icon={faCircleArrowUp} className="text-green-400 text-4xl" />
                                                                    :
                                                                    <FontAwesomeIcon icon={faCircleArrowDown} className="text-red-400 text-4xl" />
                                                            }
                                                            <div
                                                                className="hover:hidden hidden group-hover:block bg-gray-950 absolute -translate-y-9 translate-x-12 z-10 p-1 border-indigo-400 border-1 text-lg">
                                                                {service.message}
                                                            </div>
                                                        </div>
                                                    </td>
                                                ))
                                            }
                                        </tr>
                                    ))
                                }
                            </tbody>
                        </table>
                    }
                </div>
            </div >
        </>
    );
}

export default Home;
