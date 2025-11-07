import Header from "../components/Header";
import { BarChart, Bar, CartesianGrid, XAxis, YAxis, Tooltip, Legend, Rectangle, type TooltipContentProps, LineChart, Line } from 'recharts';
import RoundGraph from "../components/RoundGraph";
import ScoreGraph from "../components/ScoreGraph";
import { useStatusPoller } from "../hooks/useStatusPoller";
import { getRoundHistory, getRoundHistoryCumulative, getScores, type RoundHistoryResponse, type ScoresResponse } from "../api/status";

const roundData = [
    {
        "Team1": 1000,
        "Team2": 1000,
        "Team3": 1000,
    },
    {
        "Team1": 1200,
        "Team2": 1000,
        "Team3": 1400,
    },
    {
        "Team1": 1300,
        "Team2": 1100,
        "Team3": 1800,
    },
    {
        "Team1": 1500,
        "Team2": 1300,
        "Team3": 2200,
    },
    {
        "Team1": 1700,
        "Team2": 1500,
        "Team3": 2300,
    },
    {
        "Team1": 1900,
        "Team2": 1800,
        "Team3": 2500,
    },

];

const scoreData = [
    {
        name: 'Team1',
        score: 4000,
    },
    {
        name: 'Team2',
        score: 3000,
    },
    {
        name: 'Team3',
        score: 2000,
    },
    {
        name: 'Team4',
        score: 2780,
    },
    {
        name: 'Team5',
        score: 1890,
    },
    {
        name: 'Team6',
        score: 2390,
    },
    {
        name: 'Team7',
        score: 3490,
    },
];


function Home() {
    const scoreData: ScoresResponse | null = useStatusPoller(getScores);
    const roundData: RoundHistoryResponse | null = useStatusPoller(getRoundHistoryCumulative);

    return (
        <>
            <Header />
            <div className="bg-gray-950 flex flex-col w-full h-full items-center overflow-y-scroll">
                <div className="flex flex-col items-center w-full lg:p-4 lg:w-6xl h-full pt-6 gap-8 lg:gap-14 md:px-4">
                    {/* {scoreData && <ScoreGraph scoreData={scoreData!.scores} />} */}
                    {roundData && <RoundGraph numRounds={roundData!.currentRound} roundData={roundData!.rounds} />}
                </div>
            </div >
        </>
    );
}

export default Home;
