import { useState } from "react";
import { login } from "../api/admin";

function Login({ setLoggedIn: setLoggedIn }: { setLoggedIn: (value: boolean) => void }) {
    const [message, setMessage] = useState<string | null>(null);

    const tryLogin = async (formData: FormData) => {
        let response = await login(formData.get("username")!.toString(), formData.get("password")!.toString())

        if (response.success != true) {
            setMessage(response.message);
            return;
        }

        setLoggedIn(true);
    };

    return (
        <>
            <div className="flex flex-col gap-4 font-mono">
                <form action={tryLogin} className="bg-gray-950 border-1 border-indigo-400 p-6 flex flex-col items-center gap-4">
                    <div className="flex flex-col text-2xl gap-2 w-full">
                        <label htmlFor="username">Username</label>
                        <input className="p-2 bg-gray-600 " type="text" id="username" name="username"></input>
                    </div>

                    <div className="flex flex-col text-2xl gap-2 w-full">
                        <label htmlFor="password">Password</label>
                        <input className="p-2 bg-gray-600" type="password" id="password" name="password"></input>
                    </div>

                    <div className="w-full pt-4">
                        <button className="text-xl h-12 bg-indigo-400 hover:bg-indigo-500 w-full px-2">
                            {"Login"}
                        </button>
                    </div>
                </form >

                <div className={`flex justify-center items-center w-full bg-red-400 h-12 p-4 ${message ? "" : "hidden"}`}>
                    <div>{message}</div>
                </div>
            </div>
        </>
    )
}

export default Login;
