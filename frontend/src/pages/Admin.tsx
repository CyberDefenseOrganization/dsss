import { useEffect, useState } from "react";
import Login from "../components/Login";
import PageShell from "../components/PageShell";
import { getAdminStatus, logout } from "../api/admin";
import { useStatusPollerConditionally } from "../hooks/useStatusPoller";

function Admin() {
    const cookieExists = (cookieName: string): boolean =>
        document.cookie.split(";").some((item) => item.trim().startsWith(`${cookieName}=`));

    const [sessionExists, setSessionExists] = useState(cookieExists("session_token_timestamp"));
    const [loggedIn, setLoggedIn] = useState(sessionExists);
    const adminData = useStatusPollerConditionally(getAdminStatus, loggedIn);

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
                    <h1 className="text-xl font-semibold text-white sm:text-2xl">Scoring engine</h1>
                    {adminData ? (
                        <div className="flex flex-col gap-5 border border-white/40 p-5 sm:flex-row sm:items-center sm:justify-between sm:p-7">
                            <div>
                                <p className="mt-2 flex items-center gap-2 text-xl font-semibold text-white">
                                    <span className={`size-2.5 rounded-full ${adminData.paused ? "bg-amber-300" : "bg-emerald-400"}`} />
                                    Engine {adminData.paused ? "Paused" : "Running"}
                                </p>
                            </div>
                            <button
                                type="button"
                                className="min-h-11 border border-white/60 px-5 text-sm font-bold uppercase tracking-wider text-white transition-colors hover:bg-white hover:text-black"
                                onClick={handleLogout}
                            >
                                Log out
                            </button>
                        </div>
                    ) : (
                        <p className="border border-white/30 p-5 text-sm text-[#E0E0E0]">Checking admin session...</p>
                    )}
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
