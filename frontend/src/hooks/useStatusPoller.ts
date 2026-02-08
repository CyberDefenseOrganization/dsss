import { useEffect, useState } from "react";
import type { PolledAPIResponse } from "../api/api";

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
    shouldRun: Boolean): T | null {

    let timeoutId: ReturnType<typeof setTimeout>;

    useEffect(() => {
        if (shouldRun == false) {
            return;
        }

        async function poll() {
            try {
                const status = await apiCall();
                setData(status);
                const timeToNextRound = status.timeToNextRound;
                timeoutId = setTimeout(poll, timeToNextRound * 1000);
            } catch (err: any) {
                return;
            }
        }

        poll();
        return () => {
            clearTimeout(timeoutId);
        };

    }, [shouldRun]);

    return data;
}
