import {
    Bar,
    BarChart,
    CartesianGrid,
    Tooltip,
    XAxis,
    YAxis,
    type TooltipContentProps,
} from "recharts";

const axisStyle = { fontSize: 12, fill: "#b8b8b8" };

const ScoreTooltip = ({ active, payload, label }: TooltipContentProps<string | number, string>) => {
    if (!active || !payload?.length) return null;

    return (
        <div className="border border-white/50 bg-black px-3 py-2 text-sm text-white shadow-xl">
            <p className="font-semibold">{label}</p>
            <p className="mt-1 text-[#E0E0E0]">{payload[0].value} points</p>
        </div>
    );
};

function ScoreGraph({ scoreData }: { scoreData: Record<string, number> }) {
    const data = Object.entries(scoreData).map(([teamName, score]) => ({ teamName, score }));

    return (
        <BarChart
            responsive
            className="h-full w-full bg-black"
            data={data}
            margin={{ top: 12, right: 12, bottom: 8, left: 0 }}
        >
            <CartesianGrid stroke="#ffffff20" vertical={false} />
            <XAxis dataKey="teamName" tick={axisStyle} tickLine={false} axisLine={{ stroke: "#ffffff55" }} />
            <YAxis width="auto" tick={axisStyle} tickLine={false} axisLine={false} />
            <Tooltip content={ScoreTooltip} cursor={{ fill: "#ffffff10" }} />
            <Bar dataKey="score" fill="#e0e0e0" maxBarSize={46} />
        </BarChart>
    );
}

export default ScoreGraph;
