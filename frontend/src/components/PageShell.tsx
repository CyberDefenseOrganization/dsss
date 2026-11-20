import { useEffect, useRef, useState, type ReactNode } from "react";
import Footer from "./Footer";
import Header from "./Header";
import type { PolledAPIResponse } from "../api/api";

const viewportMaxWidth = "max-w-[calc(100dvh*16/9)]";

function PageShell({
    data,
    children,
    viewportWidthLimit = false,
}: {
    data?: PolledAPIResponse | null;
    children: ReactNode;
    viewportWidthLimit?: boolean;
}) {
    const shellRef = useRef<HTMLDivElement>(null);
    const [fullscreenTarget, setFullscreenTarget] = useState<Element | null>(null);

    useEffect(() => {
        const update = () => {
            const element = document.fullscreenElement;
            setFullscreenTarget(element && shellRef.current?.contains(element) ? element : null);
        };
        document.addEventListener("fullscreenchange", update);
        return () => document.removeEventListener("fullscreenchange", update);
    }, []);

    return (
        <div ref={shellRef} className="flex min-h-screen w-full flex-col bg-black text-[#e0e0e0]">
            <Header maxWidthClass={viewportMaxWidth} />

            <main className={`mx-auto flex w-full flex-1 flex-col gap-2 px-4 py-4 sm:gap-4 sm:px-6 sm:py-6 ${viewportWidthLimit ? viewportMaxWidth : "max-w-5xl"}`}>
                {children}
            </main>

            <Footer data={data ?? null} fullscreenTarget={fullscreenTarget} maxWidthClass={viewportMaxWidth} />
        </div>
    );
}

export default PageShell;
