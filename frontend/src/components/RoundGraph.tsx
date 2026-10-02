import { useMemo } from "react";
import { CartesianGrid, Legend, Line, LineChart, Tooltip, XAxis, YAxis, type TooltipContentProps } from "recharts";

const axisStyle = { fontSize: 12, fill: "#b8b8b8" };
type RoundPoint = { round: number; scores: Record<string, number | null> };
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
                        <p key={team.name}>
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

function RoundGraph({ numRounds, roundData, roundNumbers }: { numRounds: number; roundData: Record<string, (number | null)[]>; roundNumbers?: number[] }) {
    const formattedRoundData = useMemo(() => {
        const numbers = roundNumbers ?? Array.from({ length: numRounds }, (_, index) => index + 1);
        const rounds: RoundPoint[] = numbers.map((round) => ({ round, scores: {} }));

        for (const [team, scores] of Object.entries(roundData)) {
            scores.forEach((score, index) => {
                if (rounds[index]) rounds[index].scores[team] = score;
            });
        }

        return rounds;
    }, [numRounds, roundData, roundNumbers]);

    const lineElements = useMemo(() =>
        Object.keys(roundData).map((teamName, index) => (
            <Line
                key={teamName}
                type="monotone"
                dataKey={(point: RoundPoint) => point.scores[teamName]}
                name={teamName}
                stroke={teamColors[index % teamColors.length]}
                isAnimationActive={false}
                dot={false}
            />
        )), [roundData]);

    return (
        <LineChart
            className="h-full w-full"
            responsive
            data={formattedRoundData}
            margin={{ top: 12, right: 12, bottom: 8, left: 0 }}
        >
            <CartesianGrid stroke="#ffffffff" vertical={false} />
            <XAxis type="number" domain={["dataMin", "dataMax"]} dataKey="round" tickCount={10} tick={axisStyle} tickLine={false} axisLine={{ stroke: "#ffffff55" }} />
            <YAxis width="auto" tick={axisStyle} tickLine={false} axisLine={false} />
            <Tooltip content={RoundTooltip} wrapperStyle={{ zIndex: 50 }} />
            <Legend wrapperStyle={{ color: "#e0e0e0", fontSize: 12 }} />
            {lineElements}
        </LineChart>
    );
}

export default RoundGraph;
