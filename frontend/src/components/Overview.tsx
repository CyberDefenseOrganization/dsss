import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import type { OverviewResponse } from "../api/status";
import { faCircleArrowDown, faCircleArrowUp } from "@fortawesome/free-solid-svg-icons";

function Overview({ overviewData }: { overviewData: OverviewResponse }) {
    let services = Object.keys(overviewData.overview[Object.keys(overviewData.overview)[0]].services);

    return (
        <div className="flex flex-col justify-center">
            <div className="text-5xl font-bold font-mono text-center pt-4">
                {"Scoring Overview"}
            </div>
            <table className="table-auto font-mono text-gray-200 w-full text-lg mt-26 border-collapse">
                <thead>
                    <tr>
                        <th className="py-4"></th>
                        {
                            services.map((service) => (
                                <th className="">
                                    <div className="-rotate-50 -translate-y-27 -translate-x-5 fixed">
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
                                        <td className="font-mono border-dashed border-gray-100 border-1">
                                            <div className="group flex justify-center align-middle p-2">
                                                {
                                                    <FontAwesomeIcon
                                                        icon={service.online ? faCircleArrowUp : faCircleArrowDown}
                                                        className={`text-4xl ${service.online ? "text-green-400" : "text-red-400"}`} />
                                                }
                                                <div
                                                    className="hidden -translate-y-10 group-hover:block bg-gray-950 absolute z-10 p-1 border-indigo-400 border-1 text-lg whitespace-pre bootom-0">
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
        </div>
    )
}

export default Overview;
