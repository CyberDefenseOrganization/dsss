import { useEffect, useState } from "react";
import { Link, useLocation } from "react-router";
import { getInformation, type InfoResponse } from "../api/status";

let informationRequest: Promise<InfoResponse> | undefined;

const routes = [
    { name: "Scoreboard", path: "/" },
    { name: "Service overview", path: "/overview" },
    { name: "Admin", path: "/admin" },
];

function Header() {
    const location = useLocation();
    const [open, setOpen] = useState(false);
    const [information, setInformation] = useState<InfoResponse | null>(null);

    useEffect(() => {
        let active = true;
        informationRequest ??= getInformation();
        void informationRequest.then((data) => {
            if (active) setInformation(data);
        }).catch(() => {});
        return () => { active = false; };
    }, []);
    const [failedLogo, setFailedLogo] = useState<string | null>(null);
    const configuredLogo = information?.logo_url;
    const logoSource = configuredLogo && configuredLogo !== failedLogo ? configuredLogo : null;
    const eventName = information?.event_name_long || information?.event_name_short || "Scoreboard";
    const organizationName = information?.organization_name_long || information?.organization_name_short || eventName;

    return (
        <header className="sticky top-0 z-30 mx-auto w-full max-w-5xl border-b border-[#e0e0e0] bg-black/95 backdrop-blur-sm">
            <title>{information?.event_name_short || eventName}</title>
            <link rel="icon" href={information?.logo_url || "data:,"} />
            <div className="flex h-16 items-center justify-between gap-6 px-4 sm:px-6 md:h-18 md:px-4">
                <Link to="/" aria-label={`${eventName} scoreboard`} title={`${eventName} · ${organizationName}`} className="flex min-w-0 items-center gap-3" onClick={() => setOpen(false)}>
                    {logoSource && (
                        <img src={logoSource} alt="" onError={() => setFailedLogo(logoSource)} className="h-10 w-auto shrink-0 md:h-12" />
                    )}
                    <div className="flex min-w-0 flex-col">
                        <span className="truncate text-lg font-bold">{information?.event_name_short || eventName}</span>
                        {information && <span className="truncate text-xs text-[#b8b8b8]">{information.organization_name_short || organizationName}</span>}
                    </div>
                </Link>

                <nav className="hidden items-center gap-8 md:flex" aria-label="Main navigation">
                    {routes.map(({ name, path }) => (
                        <Link
                            key={path}
                            to={path}
                            aria-current={location.pathname === path ? "page" : undefined}
                            className={`text-nowrap text-base font-bold uppercase tracking-wider text-[#e0e0e0] hover:text-white ${location.pathname === path ? "underline underline-offset-4" : ""}`}
                        >
                            {name}
                        </Link>
                    ))}
                </nav>

                <button
                    type="button"
                    className="flex size-11 shrink-0 items-center justify-center text-[#e0e0e0] hover:text-white md:hidden"
                    aria-label={open ? "Close navigation menu" : "Open navigation menu"}
                    aria-controls="mobile-navigation"
                    aria-expanded={open}
                    onClick={() => setOpen((value) => !value)}
                >
                    <span className="relative block h-5 w-7" aria-hidden="true">
                        <span className={`absolute left-0 top-0 h-0.5 w-7 bg-current transition-transform ${open ? "translate-y-[9px] rotate-45" : ""}`} />
                        <span className={`absolute left-0 top-[9px] h-0.5 w-7 bg-current transition-opacity ${open ? "opacity-0" : ""}`} />
                        <span className={`absolute bottom-0 left-0 h-0.5 w-7 bg-current transition-transform ${open ? "-translate-y-[9px] -rotate-45" : ""}`} />
                    </span>
                </button>
            </div>

            {open && (
                <nav id="mobile-navigation" className="absolute inset-x-0 top-full border-b border-[#e0e0e0] bg-black px-4 py-2 shadow-2xl md:hidden" aria-label="Mobile navigation">
                    {routes.map(({ name, path }) => (
                        <Link
                            key={path}
                            to={path}
                            aria-current={location.pathname === path ? "page" : undefined}
                            onClick={() => setOpen(false)}
                            className={`block border-b border-white/15 py-3 text-base font-bold uppercase tracking-wider text-[#e0e0e0] last:border-0 hover:text-white ${location.pathname === path ? "underline underline-offset-4" : ""}`}
                        >
                            {name}
                        </Link>
                    ))}
                </nav>
            )}
        </header>
    );
}

export default Header;
