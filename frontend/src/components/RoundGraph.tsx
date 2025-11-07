import { useMemo } from "react";
import { CartesianGrid, Legend, Line, LineChart, Tooltip, XAxis, YAxis, type TooltipContentProps } from "recharts";

const RoundTooltip = ({ active, payload, label }: TooltipContentProps<string | number, string>) => {
    const isVisible = active && payload && payload.length;

    return (
        <div className="bg-gray-950 border-indigo-400 border-solid border-1" style={{ visibility: isVisible ? 'visible' : 'hidden' }}>
            {isVisible && (
                <>
                    <div className="p-2 font-mono">
                        {payload.map((team) => (
                            <p>
                                <span style={{ color: team.color }}>{`${team.name}`}</span>
                                <span>{` ${team.value}`}</span>
                            </p>
                        ))}
                        <p>{`Round ${label}`}</p>
                    </div>
                </>
            )}
        </div>
    );
};


function RoundGraph({ numRounds, roundData }: { numRounds: number, roundData: Record<string, Array<number>> }) {
    const teamColors = [
        "#FF4C4C",
        "#FF9F1C",
        "#FFD23F",
        "#75FF33",
        "#33FFC1",
        "#33A1FD",
        "#7F3CFF",
        "#FF33EC",
        "#FF6B6B",
        "#00E5FF",
        "#B6FF00",
        "#FFB5E8",
        "#FF8C00",
        "#00FF99",
        "#9D4EDD"
    ];

    let formattedRoundData: Array<Record<string, number>> = [];
    for (let index = 0; index < numRounds; index++) {
        formattedRoundData.push({});
    }

    for (const [team, rounds] of Object.entries(roundData)) {
        let index = 0;
        for (const round of rounds) {
            formattedRoundData[index][team] =
                formattedRoundData[index][team] ? formattedRoundData[index][team] : 0;

            formattedRoundData[index][team] += round;
            index += 1;
        }
    }

    const lineElements = useMemo(() => (
        Object.keys(formattedRoundData[0] ?? {}).map((teamName, i) => (
            <Line
                key={teamName}
                type="monotone"
                dataKey={teamName}
                stroke={teamColors[i % teamColors.length]}
                isAnimationActive={false}
                dot={false}
            />
        ))
    ), [formattedRoundData, teamColors]);

    let interval;
    if (numRounds < 10) {
        interval = 0;
    }
    else if (numRounds < 50) {
        interval = 1;
    }
    else if (numRounds < 100) {
        interval = 9;
    }
    else {
        interval = 99;
    }

    return (
        <>
            <LineChart
                className="h-full w-full"
                responsive
                data={formattedRoundData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis tick={{ className: "font-mono fill-gray-200" }} interval={interval} />
                <YAxis width="auto" tick={{ className: "font-mono fill-gray-200" }} />
                <Tooltip content={RoundTooltip} />
                <Legend />
                {lineElements}
            </LineChart >
        </>
    )
}

export default RoundGraph;
