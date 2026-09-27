import RoundGraph from "../components/RoundGraph";
import ScoreGraph from "../components/ScoreGraph";
import Fullscreen from "../components/Fullscreen";
import PageShell from "../components/PageShell";
import { getRoundHistoryCumulative, getScores, type RoundHistoryResponse, type ScoresResponse } from "../api/status";
import { useStatusPoller } from "../hooks/useStatusPoller";

function Home() {
    const scoreData: ScoresResponse | null = useStatusPoller(getScores);
    const roundData: RoundHistoryResponse | null = useStatusPoller(getRoundHistoryCumulative);

    return (
        <PageShell data={scoreData}>
            {scoreData && roundData ? (
                <Fullscreen keyboard className="flex flex-col gap-9 sm:gap-12">
                    {(isFullscreen) => {
                        const sectionClass = isFullscreen ? "flex min-h-0 flex-1 flex-col" : "";
                        const chartClass = isFullscreen
                            ? "min-h-0 flex-1 border border-white/40 p-3"
                            : "h-80 border border-white/40 bg-black p-3 sm:h-96 sm:p-5";

                        return (
                            <>
                                <section className={sectionClass}>
                                    {!isFullscreen && <h1 className="mb-4 text-xl font-semibold text-white sm:text-2xl">Competition leaderboard</h1>}
                                    <Fullscreen buttonLabel="Competition leaderboard" className={`flex flex-col gap-2 ${chartClass}`}>
                                        {() => (
                                            <div className="min-h-0 flex-1">
                                                <ScoreGraph scoreData={scoreData.scores} />
                                            </div>
                                        )}
                                    </Fullscreen>
                                </section>
                                <section className={sectionClass}>
                                    {!isFullscreen && <h2 className="mb-4 text-xl font-semibold text-white sm:text-2xl">Score by round</h2>}
                                    <Fullscreen buttonLabel="Score by round" className={`flex flex-col gap-2 ${chartClass}`}>
                                        {() => (
                                            <div className="min-h-0 flex-1">
                                                <RoundGraph numRounds={roundData.currentRound} roundData={roundData.rounds} />
                                            </div>
                                        )}
                                    </Fullscreen>
                                </section>
                            </>
                        );
                    }}
                </Fullscreen>
            ) : (
                <p className="text-sm text-center text-[#E0E0E0]">
                    Loading data...
                </p>
            )}
        </PageShell>
    );
}

export default Home;
