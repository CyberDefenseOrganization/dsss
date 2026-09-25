import { useState } from "react";

import Header from "../components/Header";
import Login from "../components/Login";

import { getAdminStatus, logout } from "../api/admin";
import { useStatusPollerConditionally } from "../hooks/useStatusPoller";
import Footer from "../components/Footer";

function Admin() {
    const cookieExists = (cookieName: string): boolean => {
        return document.cookie.split(";").some(
            item => item
                .trim()
                .startsWith(cookieName + "=")
        )
    }

    const [sessionExists, setSessionExists] = useState(cookieExists("session_token_timestamp"));
    const [loggedIn, setLoggedIn] = useState(sessionExists);
    const adminData = useStatusPollerConditionally(getAdminStatus, loggedIn);


    const handleLogout = async () => {
        await logout();
        setSessionExists(false);
        setLoggedIn(false);
    }

    if (sessionExists) {
        getAdminStatus().then((adminStatus) => {
            setLoggedIn(adminStatus.success);
        })
    }

    return (
        <>
            <Header />
            <div className="bg-black flex flex-col w-full h-full items-center overflow-y-scroll">
                <div className="flex flex-col items-center w-full lg:p-4 lg:w-6xl h-full pt-6 gap-8 lg:gap-14 md:px-4">
                    {loggedIn ? adminData &&
                        <div className="border-[#E0E0E0] border-1 p-6 w-3xl flex flex-col font-mono">
                            <div className="text-2xl">
                                Admin Panel
                            </div>
                            <div>
                                Engine Status: {adminData.paused ? "paused" : "running"}
                            </div>

                            <button className="bg-[#e0e0e0] hover:bg-white" onClick={handleLogout}> LOGOUT </button>
                        </div>
                        : <Login setLoggedIn={setLoggedIn} />
                    }
                </div>
            </div >
            <Footer data={adminData} />
        </>
    );
}

export default Admin;
