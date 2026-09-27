import { useState } from "react";
import { login } from "../api/admin";

function Login({ setLoggedIn }: { setLoggedIn: (value: boolean) => void }) {
    const [message, setMessage] = useState<string | null>(null);

    const tryLogin = async (formData: FormData) => {
        const username = formData.get("username")?.toString() ?? "";
        const password = formData.get("password")?.toString() ?? "";
        const response = await login(username, password);

        if (!response.success) {
            setMessage(response.message ?? "Unable to sign in. Check your credentials and try again.");
            return;
        }

        setMessage(null);
        setLoggedIn(true);
    };

    return (
        <section className="mx-auto w-full max-w-xl">
            <form action={tryLogin} className="flex flex-col gap-5 border border-white/40 p-5 sm:p-7">
                <label className="flex flex-col gap-2 text-sm font-semibold text-[#e0e0e0]">
                    Username
                    <input
                        className="min-h-11 border border-white/40 bg-white/5 px-3 text-base text-white outline-none transition-colors focus:border-white"
                        type="text"
                        name="username"
                        autoComplete="username"
                        required
                    />
                </label>

                <label className="flex flex-col gap-2 text-sm font-semibold text-[#e0e0e0]">
                    Password
                    <input
                        className="min-h-11 border border-white/40 bg-white/5 px-3 text-base text-white outline-none transition-colors focus:border-white"
                        type="password"
                        name="password"
                        autoComplete="current-password"
                        required
                    />
                </label>

                <button className="min-h-11 border border-white bg-white px-5 text-sm font-bold uppercase tracking-wider text-black transition-colors hover:bg-[#e0e0e0]">
                    Sign in
                </button>

                {message && <p className="border p-3 text-sm bg-black" role="alert">{message}</p>}
            </form>
        </section>
    );
}

export default Login;
