import { useMemo } from "react";
import { CartesianGrid, Legend, Line, LineChart, Tooltip, XAxis, YAxis, type TooltipContentProps } from "recharts";

const axisStyle = { fontSize: 12, fill: "#b8b8b8" };
const teamColors = [
    "#FF4C4C", "#FF9F1C", "#FFD23F", "#75FF33", "#33FFC1", "#33A1FD", "#7F3CFF",
    "#FF33EC", "#FF6B6B", "#00E5FF", "#B6FF00", "#FFB5E8", "#FF8C00", "#00FF99", "#9D4EDD",
];

const RoundTooltip = ({ active, payload, label }: TooltipContentProps<string | number, string>) => {
    const isVisible = active && payload && payload.length > 0;

    return (
        <div className="border border-white/50 bg-black px-3 py-2 text-sm text-white shadow-xl" style={{ visibility: isVisible ? "visible" : "hidden" }}>
            {isVisible && (
                <div className="p-2 font-mono">
                    {payload.map((team) => (
                        <p key={team.dataKey}>
                            <span style={{ color: team.color }}>{team.name}</span>
                            <span>{` ${team.value}`}</span>
                        </p>
                    ))}
                    <p>{`Round ${label}`}</p>
                </div>
            )}
        </div>
    );
};

function RoundGraph({ numRounds, roundData }: { numRounds: number; roundData: Record<string, number[]> }) {
    const formattedRoundData = useMemo(() => {
        const rounds: Array<Record<string, number>> = Array.from({ length: numRounds }, () => ({}));

        for (const [team, scores] of Object.entries(roundData)) {
            scores.forEach((score, index) => {
                if (rounds[index]) rounds[index][team] = (rounds[index][team] ?? 0) + score;
            });
        }

        return rounds;
    }, [numRounds, roundData]);

    const lineElements = useMemo(() =>
        Object.keys(formattedRoundData[0] ?? {}).map((teamName, index) => (
            <Line
                key={teamName}
                type="monotone"
                dataKey={teamName}
                stroke={teamColors[index % teamColors.length]}
                isAnimationActive={false}
                dot={false}
            />
        )), [formattedRoundData]);

    const interval = numRounds < 20 ? 0 : numRounds < 50 ? 1 : numRounds < 100 ? 4 : numRounds < 200 ? 9 : 99;

    return (
        <LineChart
            className="h-full w-full"
            responsive
            data={formattedRoundData}
            margin={{ top: 12, right: 12, bottom: 8, left: 0 }}
        >
            <CartesianGrid stroke="#ffffffff" vertical={false} />
            <XAxis tick={axisStyle} tickLine={false} axisLine={{ stroke: "#ffffff55" }} interval={interval} />
            <YAxis width="auto" tick={axisStyle} tickLine={false} axisLine={false} />
            <Tooltip content={RoundTooltip} wrapperStyle={{ zIndex: 50 }} />
            <Legend wrapperStyle={{ color: "#e0e0e0", fontSize: 12 }} />
            {lineElements}
        </LineChart>
    );
}

export default RoundGraph;
