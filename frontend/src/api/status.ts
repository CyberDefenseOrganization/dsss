import type { PolledAPIResponse } from "./api";

export interface ScoresResponse extends PolledAPIResponse {
    scores: Record<string, number>,
};

export async function getScores(): Promise<ScoresResponse> {
    const res = await fetch("/api/status/scores");
    return res.json();
}

export interface RoundHistoryResponse extends PolledAPIResponse {
    rounds: Record<string, Array<number | null>>,
    roundNumbers?: number[]
}

export async function getRoundHistory(): Promise<RoundHistoryResponse> {
    const res = await fetch("/api/status/round_history");
    return res.json();
}

export async function getRoundHistoryCumulative(): Promise<RoundHistoryResponse> {
    const res = await fetch("/api/status/cumulative_round_history");
    return res.json();
}

export async function getOverview(): Promise<OverviewResponse> {
    const res = await fetch("/api/status/overview");
    if (!res.ok) throw new Error(`Service overview request failed: ${res.status}`);
    return res.json();
}

export async function getInformation(): Promise<InfoResponse> {
    const res = await fetch("/api/status/info");
    if (!res.ok) throw new Error(`Branding request failed: ${res.status}`);
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

export interface OverviewResponse extends PolledAPIResponse {
    overview: Record<string, TeamOverview>
}

export interface InfoResponse extends PolledAPIResponse {
    event_name_long: string,
    event_name_short: string,
    organization_name_long: string,
    organization_name_short: string,
    logo_url?: string | null
}
