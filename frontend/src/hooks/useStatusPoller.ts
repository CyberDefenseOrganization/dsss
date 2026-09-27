import { useEffect, useState } from "react";
import type { PolledAPIResponse } from "../api/api";

const MIN_POLL_DELAY_MS = 1000;

function nextPollDelay(timeToNextRound: number): number {
    const delay = timeToNextRound * 1000;
    return Number.isFinite(delay) ? Math.max(MIN_POLL_DELAY_MS, delay) : MIN_POLL_DELAY_MS;
}

export function useStatusPoller<T extends PolledAPIResponse>(apiCall: () => Promise<T>): T | null {
    const [data, setData] = useState<T | null>(null);
    return useStatusPollerWithState(apiCall, data, setData, true);
}

export function useStatusPollerConditionally<T extends PolledAPIResponse>(apiCall: () => Promise<T>, shouldRun: boolean): T | null {
    const [data, setData] = useState<T | null>(null);
    return useStatusPollerWithState(apiCall, data, setData, shouldRun);
}

export function useStatusPollerWithState<T extends PolledAPIResponse>(
    apiCall: () => Promise<T>,
    data: T | null,
    setData: React.Dispatch<React.SetStateAction<T | null>>,
    shouldRun: boolean): T | null {

    useEffect(() => {
        if (!shouldRun) {
            return;
        }

        let timeoutId: ReturnType<typeof setTimeout>;
        let active = true;
        async function poll() {
            try {
                const status = await apiCall();
                if (!active) return;
                setData(status);
                timeoutId = setTimeout(poll, nextPollDelay(status.timeToNextRound));
            } catch {
                if (active) timeoutId = setTimeout(poll, 5000);
            }
        }

        void poll();
        return () => {
            active = false;
            clearTimeout(timeoutId);
        };

    }, [apiCall, setData, shouldRun]);

    return data;
}
