import Header from "../components/Header";
import Login from "../components/Login";

function Home() {

    return (
        <>
            <Header />
            <div className="bg-gray-950 flex flex-col w-full h-full items-center overflow-y-scroll">
                <div className="flex flex-col items-center w-full lg:p-4 lg:w-6xl h-full pt-6 gap-8 lg:gap-14 md:px-4">
                    <Login />
                </div>
            </div >
        </>
    );
}

export default Home;
