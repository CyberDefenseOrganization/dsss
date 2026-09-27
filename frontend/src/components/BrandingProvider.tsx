import { useEffect, type ReactNode } from "react";
import { getInformation } from "../api/status";
import { BrandingContext } from "../hooks/useBranding";
import { useStatusPoller } from "../hooks/useStatusPoller";

function BrandingProvider({ children }: { children: ReactNode }) {
    const information = useStatusPoller(getInformation);

    useEffect(() => {
        document.title = information?.event_name_short || information?.event_name_long || "Scoreboard";
        const icon = document.querySelector<HTMLLinkElement>('link[rel="icon"]');
        if (icon) icon.href = information?.logo_url || "data:,";
    }, [information]);

    return <BrandingContext value={information}>{children}</BrandingContext>;
}

export default BrandingProvider;
