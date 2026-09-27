import { useLayoutEffect, useRef, useState } from "react";
import type { OverviewResponse } from "../api/status";

function Overview({ overviewData, fullscreen }: { overviewData: OverviewResponse; fullscreen: boolean }) {
    const teams = Object.entries(overviewData.overview);
    const services = [...new Set(teams.flatMap(([, team]) => Object.keys(team.services)))];
    const [tooltip, setTooltip] = useState<{ title: string; message: string; center: number; top: number; bottom: number } | null>(null);
    const tooltipRef = useRef<HTMLDivElement>(null);

    useLayoutEffect(() => {
        if (!tooltip || !tooltipRef.current) return;

        const card = tooltipRef.current;
        const width = card.offsetWidth;
        const height = card.offsetHeight;
        card.style.left = `${Math.max(8, Math.min(tooltip.center - width / 2, window.innerWidth - width - 8))}px`;
        const below = tooltip.bottom + 8;
        const above = tooltip.top - height - 8;
        card.style.top = `${below + height <= window.innerHeight - 8 ? below : Math.max(8, above)}px`;
    }, [tooltip]);

    const tooltipFor = (element: HTMLElement, title: string, message: string) => {
        const rect = element.getBoundingClientRect();
        return {
            title,
            message,
            center: rect.left + rect.width / 2,
            top: rect.top,
            bottom: rect.bottom,
        };
    };

    if (teams.length === 0) {
        return (
            <section className={fullscreen ? "flex min-h-0 flex-1 flex-col" : ""}>
                {!fullscreen && <h1 className="mb-4 text-xl font-semibold text-white sm:text-2xl">Service status</h1>}
                <p className="border border-white/20 p-5 text-sm text-[#E0E0E0]">
                    Service results will appear after the first scoring round.
                </p>
            </section>
        );
    }

    return (
        <section className={fullscreen ? "flex min-h-0 min-w-0 w-full flex-1 flex-col items-center justify-center" : "min-w-0 w-full"}>
            <div className={`overview-scrollbar isolate w-fit max-w-full border border-white/40 ${fullscreen ? "min-h-0 overflow-auto" : "overflow-x-auto"}`}>
                <table className="w-max border-separate border-spacing-0 text-left text-sm [&_tr>:nth-child(2)]:border-l-0">
                    <thead className="bg-black">
                        <tr>
                            <th scope="col" className={`sticky left-0 z-30 w-px whitespace-nowrap border-b border-r border-white/40 border-r-[#666] bg-black shadow-[-1px_0_0_#000] px-4 py-3 text-xs font-bold tracking-wider text-[#e0e0e0] ${fullscreen ? "top-0" : ""}`}>
                                Team
                            </th>
                            {services.map((service) => (
                                <th key={service} scope="col" className={`w-20 min-w-20 max-w-40 border-b border-l border-white/40 bg-black px-4 py-3 text-center text-xs font-bold text-[#e0e0e0] ${fullscreen ? "sticky top-0 z-20" : ""}`}>
                                    <span className="block break-words">
                                        {service}
                                    </span>
                                </th>
                            ))}
                        </tr>
                    </thead>
                    <tbody>
                        {teams.map(([team, data]) => (
                            <tr key={team} className="group hover:bg-white/[0.04]">
                                <th scope="row" className="sticky left-0 z-10 w-px whitespace-nowrap border-b border-r border-white/20 border-r-[#666] bg-black shadow-[-1px_0_0_#000] px-4 py-3 text-left font-semibold text-[#e0e0e0] group-hover:bg-[#101010]">
                                    {team}
                                </th>
                                {services.map((service) => {
                                    const status = data.services[service];
                                    const title = `${team} - ${service}`;

                                    return (
                                        <td
                                            key={service}
                                            className="cursor-pointer border-b border-l border-white/10 px-4 py-3 text-center"
                                            onPointerEnter={(event) => {
                                                if (event.pointerType !== "touch") setTooltip(tooltipFor(event.currentTarget, title, status?.message));
                                            }}
                                            onPointerLeave={(event) => {
                                                if (event.pointerType !== "touch") setTooltip(null);
                                            }}
                                            onClick={(event) => {
                                                const nextTooltip = tooltipFor(event.currentTarget, title, status?.message);
                                                setTooltip((current) => current?.title === title ? null : nextTooltip);
                                            }}
                                        >
                                            <button
                                                type="button"
                                                aria-label={`${title}: ${status ? (status.online ? "online" : "offline") : "no result"}`}
                                                aria-expanded={tooltip?.title === title}
                                                className="inline-flex size-7 cursor-pointer items-center justify-center rounded-full outline-offset-2 focus-visible:outline focus-visible:outline-white"
                                                onFocus={(event) => {
                                                    if (event.currentTarget.matches(":focus-visible")) setTooltip(tooltipFor(event.currentTarget.closest("td")!, title, status?.message));
                                                }}
                                                onBlur={() => setTooltip(null)}
                                                onKeyDown={(event) => {
                                                    if (event.key === "Escape") setTooltip(null);
                                                }}
                                            >
                                                <span aria-hidden="true" className={`size-3.5 rounded-full ${status ? (status.online ? "bg-green-400" : "bg-red-400") : "bg-white/40"}`} />
                                            </button>
                                        </td>
                                    );
                                })}
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>
            {tooltip && (
                <div
                    ref={tooltipRef}
                    role="tooltip"
                    className="pointer-events-none fixed z-50 max-w-[min(20rem,calc(100vw-1rem))] border border-white/50 bg-black px-3 py-2 text-sm text-[#e0e0e0] shadow-xl"
                    style={{ left: 8, top: 8 }}
                >
                    <p className="font-semibold border-b border-white/40">{tooltip.title}</p>
                    <p className="mt-1 text-[#E0E0E0]">{tooltip.message}</p>
                </div>
            )}
        </section>
    );
}

export default Overview;
