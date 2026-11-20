import { useLayoutEffect, useRef, useState } from "react";
import type { OverviewResponse } from "../api/status";

function Overview({ overviewData, fullscreen }: { overviewData: OverviewResponse; fullscreen: boolean }) {
    const teams = Object.entries(overviewData.overview);
    const groups = overviewData.hosts;
    // configs without any `host` get a single header row, as before
    const grouped = groups.some(group => group.name !== null);
    const services = groups.flatMap(group => group.services.map((service, index) => ({
        ...service, host: group.name, startsGroup: index === 0,
    })));
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
            <h1 className="mx-auto mb-4 w-full max-w-7xl text-xl font-semibold text-white sm:text-2xl">Service status</h1>
            <div className={`overview-scrollbar isolate mx-auto w-full max-w-7xl overflow-auto border border-white/40 bg-black ${fullscreen ? "min-h-0" : ""}`}>
                <table className="w-full table-fixed border-separate border-spacing-0 text-left text-sm" style={{ minWidth: `min(calc(6rem + ${services.length * 4}rem), max(100%, 64rem))` }}>
                    <colgroup><col className="w-24" /></colgroup>
                    {groups.map(group => <colgroup key={group.services[0].id} span={group.services.length} />)}
                    <thead className={`bg-black ${fullscreen ? "sticky top-0 z-20" : ""}`}>
                        <tr>
                            <th scope="col" rowSpan={grouped ? 2 : 1} className="sticky left-0 z-10 border-b border-white/30 bg-black px-4 py-3 text-sm font-semibold">
                                Team
                            </th>
                            {grouped && groups.map(group => (
                                <th key={group.services[0].id} colSpan={group.services.length} scope="colgroup" className="border-b border-l border-white/20 px-2 py-2 text-center text-sm font-semibold [overflow-wrap:anywhere]">
                                    {group.name ?? "Services"}
                                </th>
                            ))}
                            {!grouped && services.map(service => <th key={service.id} scope="col" className="border-b border-l border-white/20 px-1 py-2 text-center text-xs [overflow-wrap:anywhere]">{service.name}</th>)}
                        </tr>
                        {grouped && <tr>
                            {services.map(service => (
                                <th key={service.id} scope="col" className={`border-b border-white/30 px-1 py-2 text-center text-xs font-medium text-[#b8b8b8] [overflow-wrap:anywhere] ${service.startsGroup ? "border-l border-l-white/20" : ""}`}>
                                    {service.name}
                                </th>
                            ))}
                        </tr>}
                    </thead>
                    <tbody>
                        {teams.map(([team, data]) => (
                            <tr key={team} className="group hover:bg-white/[0.06] focus-within:bg-white/[0.06]">
                                <th scope="row" className="sticky left-0 z-10 border-b border-white/10 bg-black px-4 py-1 text-left font-semibold [overflow-wrap:anywhere] group-hover:bg-[#101010] group-focus-within:bg-[#101010]">
                                    {team}
                                </th>
                                {services.map((service) => {
                                    const status = data.services[service.id];
                                    const title = [team, service.host, service.name].filter(Boolean).join(" - ");

                                    return (
                                        <td
                                            key={service.id}
                                            className={`cursor-pointer border-b border-white/10 px-1 py-1 text-center ${service.startsGroup ? "border-l border-l-white/20" : ""}`}
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
                                                className="inline-flex size-7 cursor-pointer items-center justify-center outline-offset-1 focus-visible:outline focus-visible:outline-white"
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
                    className="pointer-events-none fixed z-50 max-w-[min(20rem,calc(100vw-1rem))] border border-white/50 bg-black px-3 py-2 text-sm text-white shadow-xl"
                    style={{ left: 8, top: 8 }}
                >
                    <p className="font-semibold">{tooltip.title}</p>
                    <p className="mt-1 text-[#E0E0E0]">{tooltip.message}</p>
                </div>
            )}
        </section>
    );
}

export default Overview;
