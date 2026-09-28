import { useEffect, useState } from "react";
import { createPortal } from "react-dom";
import type { PolledAPIResponse } from "../api/api";

function Footer({ data, fullscreenTarget }: {
    data: (PolledAPIResponse & { paused?: boolean }) | null;
    fullscreenTarget?: Element | null;
}) {
    const [timeLeft, setTimeLeft] = useState(0);
    const timeToNextRound = data?.timeToNextRound;

    useEffect(() => {
        if (timeToNextRound === undefined) return;

        const roundEndsAt = Date.now() + timeToNextRound * 1000;
        const update = () => setTimeLeft(Math.max(0, (roundEndsAt - Date.now()) / 1000));
        update();
        const intervalId = window.setInterval(update, 500);
        return () => window.clearInterval(intervalId);
    }, [timeToNextRound]);

    const content = (
        <footer className={`mt-auto flex w-full shrink-0 flex-col items-center ${fullscreenTarget ? "" : "px-4 sm:px-6"}`}>
            <div className={`h-px w-full bg-[#e0e0e0] ${fullscreenTarget ? "" : "max-w-5xl"}`} />
            <div className={`flex w-full items-center justify-between gap-2 py-4 font-semibold text-[#e0e0e0] sm:gap-4 sm:py-5 ${fullscreenTarget ? "flex-row text-lg sm:text-2xl" : "max-w-5xl flex-col text-xs sm:flex-row sm:text-sm"}`}>
                <span>{data ? `Round ${String(data.currentRound).padStart(2, "0")}` : "Competition scoring"}</span>
                <span>
                    {data
                        ? data.paused
                            ? "Scoring paused"
                            : `Next round in ${Math.ceil(timeLeft)} seconds`
                        : "Waiting for scoring data"}
                </span>
            </div>
        </footer>
    );

    return fullscreenTarget ? createPortal(content, fullscreenTarget) : content;
}

export default Footer;
