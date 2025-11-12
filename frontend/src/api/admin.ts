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
