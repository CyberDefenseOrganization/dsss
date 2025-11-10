import { useEffect, useState } from "react";
import type { StatusResponse } from "../api/status";

function Footer({ data }: { data: StatusResponse | null }) {
    if (!data) {
        return (<></>);
    }

    const [originalTimeLeft, setOriginalTimeLeft] = useState(data.timeToNextRound);
    const [timeLeft, setTimeLeft] = useState(data.timeToNextRound);

    useEffect(() => {
        const intervalId = setInterval(() => {
            if (originalTimeLeft != data.timeToNextRound) {
                setTimeLeft(data.timeToNextRound);
                setOriginalTimeLeft(data.timeToNextRound);
            }
            setTimeLeft((t) => t - 0.5);
        }, 500);
        return () => clearInterval(intervalId);
    }, [originalTimeLeft, timeLeft]);

    return (
        <div className="text-xl font-mono font-bold flex justify-between pt-4 bg-gray-950 border-indigo-400 border-t-1 p-2">
            <div>{`Current round: ${data.currentRound}`}</div >
            <div>{`Time to next round: ${timeLeft > 0 ? timeLeft.toFixed(0) : 0} seconds`}</div>
        </div>
    )
}

export default Footer;
