import Header from "../components/Header";
import RoundGraph from "../components/RoundGraph";
import ScoreGraph from "../components/ScoreGraph";
import { useStatusPoller } from "../hooks/useStatusPoller";
import { getRoundHistoryCumulative, getScores, type RoundHistoryResponse, type ScoresResponse } from "../api/status";

function Home() {
    const scoreData: ScoresResponse | null = useStatusPoller(getScores);
    const roundData: RoundHistoryResponse | null = useStatusPoller(getRoundHistoryCumulative);

    return (
        <>
            <Header />
            <div className="bg-gray-950 flex flex-col w-full h-full items-center overflow-y-scroll">
                <div className="flex flex-col items-center w-full lg:p-4 lg:w-6xl h-full pt-6 gap-8 lg:gap-14 md:px-4">
                    {
                        scoreData && roundData &&
                        <>
                            {<ScoreGraph scoreData={scoreData!.scores} />}
                            {<RoundGraph numRounds={roundData!.currentRound} roundData={roundData!.rounds} />}
                        </>
                    }
                </div>
            </div >
        </>
    );
}

export default Home;
