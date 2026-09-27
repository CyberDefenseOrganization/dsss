import { useEffect, useRef, useState, type ReactNode } from "react";
import Footer from "./Footer";
import Header from "./Header";
import type { PolledAPIResponse } from "../api/api";

function PageShell({
    data,
    children,
}: {
    data?: PolledAPIResponse | null;
    children: ReactNode;
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
            <Header />

            <main className="mx-auto flex w-full max-w-5xl flex-1 flex-col gap-9 px-4 py-4 sm:gap-12 sm:px-6 sm:py-6">
                {children}
            </main>

            <Footer data={data ?? null} fullscreenTarget={fullscreenTarget} />
        </div>
    );
}

export default PageShell;
