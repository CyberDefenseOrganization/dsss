import { useEffect, useState } from "react";
import Login from "../components/Login";
import PageShell from "../components/PageShell";
import { getAdminStatus, logout, pauseScoring, startScoring, type AdminStatus } from "../api/admin";
import { useStatusPollerWithState } from "../hooks/useStatusPoller";

function Admin() {
    const cookieExists = (cookieName: string): boolean =>
        document.cookie.split(";").some((item) => item.trim().startsWith(`${cookieName}=`));

    const [sessionExists, setSessionExists] = useState(cookieExists("session_token_timestamp"));
    const [loggedIn, setLoggedIn] = useState(sessionExists);
    const [adminData, setAdminData] = useState<AdminStatus | null>(null);
    const [pending, setPending] = useState(false);
    const [actionError, setActionError] = useState<string | null>(null);
    useStatusPollerWithState(getAdminStatus, adminData, setAdminData, loggedIn && !pending);

    const handleScoring = async (paused: boolean) => {
        setPending(true);
        setActionError(null);
        try {
            await (paused ? pauseScoring() : startScoring());
            setAdminData((current) => current ? { ...current, paused } : current);
        } catch (error) {
            setActionError(error instanceof Error ? error.message : "Unable to change scoring state.");
        } finally {
            setPending(false);
        }
    };

    useEffect(() => {
        if (!sessionExists) return;

        let active = true;
        getAdminStatus()
            .then((status) => {
                if (active) {
                    setLoggedIn(status.success);
                    if (!status.success) setSessionExists(false);
                }
            })
            .catch(() => {
                if (active) {
                    setLoggedIn(false);
                    setSessionExists(false);
                }
            });

        return () => {
            active = false;
        };
    }, [sessionExists]);

    const handleLogout = async () => {
        await logout();
        setSessionExists(false);
        setLoggedIn(false);
    };

    return (
        <PageShell
            data={adminData}
        >
            {loggedIn ? (
                <>
                    <h1 className="text-xl font-semibold text-white sm:text-2xl">Admin Panel</h1>
                    {adminData ? (
                        <div className="flex flex-col gap-5 border border-white/40 p-5 sm:flex-row sm:items-center sm:justify-between sm:p-7">
                            <div>
                                <p className="mt-2 flex items-center gap-2 text-xl font-semibold text-white">
                                    <span className={`size-2.5 ${adminData.paused ? "bg-black border-white border" : "bg-white"}`} />
                                    Engine {adminData.paused ? "Paused" : "Running"}
                                </p>
                            </div>
                            <div className="flex flex-wrap gap-3">
                                <button
                                    type="button"
                                    disabled={pending}
                                    onClick={() => void handleScoring(!adminData.paused)}
                                    className="min-h-11 border border-white bg-white px-5 text-sm font-bold uppercase tracking-wider text-black hover:bg-[#e0e0e0] disabled:opacity-40"
                                >
                                    {adminData.paused ? "Start scoring" : "Pause scoring"}
                                </button>
                                <button
                                    type="button"
                                    disabled={pending}
                                    className="min-h-11 border border-white/60 px-5 text-sm font-bold uppercase tracking-wider text-white transition-colors hover:bg-white hover:text-black disabled:opacity-40"
                                    onClick={handleLogout}
                                >
                                    Log out
                                </button>
                            </div>
                        </div>
                    ) : (
                        <p className="border border-white/30 p-5 text-sm text-[#E0E0E0]">Checking admin session...</p>
                    )}
                    {actionError && <p role="alert" className="border border-rose-300/50 bg-rose-300/10 p-3 text-sm text-rose-100">{actionError}</p>}
                </>
            ) : sessionExists ? (
                <p className="border border-white/30 p-5 text-sm text-[#E0E0E0]">Checking admin session...</p>
            ) : (
                <Login setLoggedIn={(value) => {
                    setLoggedIn(value);
                    setSessionExists(value);
                }} />
            )}
        </PageShell>
    );
}

export default Admin;
