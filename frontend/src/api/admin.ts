import type { PolledAPIResponse } from "./api";

export interface LoginResponse {
    success: boolean,
    message: string | null,
}

export async function login(username: string, password: string): Promise<LoginResponse> {
    const res = await fetch("/api/admin/login", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({
            username: username,
            password: password,
        }),
    });

    return res.json();
}

export interface LogoutResponse {
    success: boolean,
    message: string | null,
}

export async function logout(): Promise<LogoutResponse> {
    const res = await fetch("/api/admin/logout", {
        method: "POST",
        credentials: "include",
    });

    return res.json();
}

export interface AdminStatus extends PolledAPIResponse {
    success: boolean,
    message: string | null,
    paused: boolean,
}

export async function getAdminStatus(): Promise<AdminStatus> {
    const res = await fetch("/api/admin/get_status", {
        credentials: "include",
    });

    return res.json();
}
