import Header from "../components/Header";

function NotFound() {
    return (
        <>
            <Header />
            <div className="flex flex-col w-full h-full items-center bg-gray-950 overflow-y-scroll">
                <b>{"Page not found, nerd"}</b>
            </div>
        </>
    );
}

export default NotFound;
