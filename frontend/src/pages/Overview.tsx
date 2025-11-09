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
                        <table className="table-auto font-mono text-gray-200 border-indigo-400 border-1 w-full">
                            <thead>
                                <tr className="border-indigo-400 border-1 p-2">
                                    <th className="border-indigo-400 border-1 p-2">Team</th>
                                    <th className="border-indigo-400 border-1 p-2">Score</th>
                                    {
                                        services.map((service) => (
                                            <th className="border-indigo-400 border-1">
                                                {service}
                                            </th>
                                        ))
                                    }
                                </tr>
                            </thead>
                            <tbody>
                                {
                                    Object.keys(overviewData.overview).map((team) => (
                                        <tr className="text-center">
                                            <td className="border-indigo-400 border-1">{team}</td>
                                            <td className="border-indigo-400 border-1">{overviewData.overview[team].score}</td>
                                            {
                                                Object.values(overviewData.overview[team].services).map((service) => (
                                                    <td className="font-mono border-indigo-400 border-1 p-2 text-4xl ">
                                                        <div className="group w-full h-full flex">
                                                            {
                                                                service.online ?
                                                                    <FontAwesomeIcon icon={faCircleArrowUp} className="text-green-400" />
                                                                    :
                                                                    <FontAwesomeIcon icon={faCircleArrowDown} className="text-red-400" />
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
