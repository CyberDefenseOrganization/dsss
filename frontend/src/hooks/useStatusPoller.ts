import { useEffect, useState } from "react";
import { type StatusResponse } from "../api/status.ts";

export function useStatusPoller<T extends StatusResponse>(apiCall: () => Promise<T>): T | null {
    const [data, setData] = useState<T | null>(null);

    let timeoutId: ReturnType<typeof setTimeout>;

    useEffect(() => {
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

    }, []);

    return data;
}

