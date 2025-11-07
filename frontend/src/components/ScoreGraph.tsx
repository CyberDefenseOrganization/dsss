import { Bar, BarChart, CartesianGrid, Tooltip, XAxis, YAxis, type TooltipContentProps } from "recharts";


const ScoreTooltip = ({ active, payload, label }: TooltipContentProps<string | number, string>) => {
    const isVisible = active && payload && payload.length;
    return (
        <div className="custom-tooltip bg-gray-950 border-indigo-400 border-solid border-1" style={{ visibility: isVisible ? 'visible' : 'hidden' }}>
            {isVisible && (
                <>
                    <div className="p-2 font-mono">
                        <p className="label">{`${label} : ${payload[0].value}`}</p>

                    </div>
                </>
            )}
        </div>
    );
};

function ScoreGraph({ scoreData }: { scoreData: Record<string, number> }) {
    let formattedScoredData = []

    for (const [teamName, score] of Object.entries(scoreData)) {
        formattedScoredData.push({ teamName, score });
    }

    console.log(formattedScoredData);

    return (
        <>
            <BarChart
                className="h-full w-full"
                responsive
                data={formattedScoredData}
                margin={{
                    top: 5,
                    right: 0,
                    left: 0,
                    bottom: 5,
                }}
            >
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="teamName" tick={{ className: "font-mono fill-gray-200" }} />
                <YAxis width="auto" tick={{ className: "font-mono fill-gray-200" }} />
                <Tooltip content={ScoreTooltip} />
                <Bar dataKey="score" name="test" className="fill-indigo-400 stroke-indigo-400" />
            </BarChart>
        </>
    )
}

export default ScoreGraph;
