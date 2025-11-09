export interface StatusResponse {
    currentRound: number,
    timeToNextRound: number,
}

export interface ScoresResponse extends StatusResponse {
    scores: Record<string, number>,
};

export async function getScores(): Promise<ScoresResponse> {
    const res = await fetch("/api/status/get_scores");
    return res.json();
}

export interface RoundHistoryResponse extends StatusResponse {
    rounds: Record<string, Array<number>>
}

export async function getRoundHistory(): Promise<RoundHistoryResponse> {
    const res = await fetch("/api/status/get_round_history");
    return res.json();
}

export async function getRoundHistoryCumulative(): Promise<RoundHistoryResponse> {
    const res = await fetch("/api/status/get_cumulative_round_history");
    return res.json();
}

export async function getOverview(): Promise<OverviewResponse> {
    const res = await fetch("/api/status/get_overview");
    return res.json();
}

interface TeamOverview {
    score: number,
    services: Record<string, ServiceStatus>
}

interface ServiceStatus {
    online: boolean
    message: string
}

export interface OverviewResponse extends StatusResponse {
    overview: Record<string, TeamOverview>
}

