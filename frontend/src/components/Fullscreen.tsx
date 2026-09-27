import { useEffect, useRef, useState, type ReactNode } from "react";
import FullscreenButton from "./FullscreenButton";

function Fullscreen({ children, className, keyboard = false, buttonLabel }: {
    children: (active: boolean) => ReactNode;
    className: string;
    keyboard?: boolean;
    buttonLabel?: string;
}) {
    const ref = useRef<HTMLDivElement>(null);
    const [active, setActive] = useState(false);

    useEffect(() => {
        const update = () => setActive(document.fullscreenElement === ref.current);
        document.addEventListener("fullscreenchange", update);
        return () => document.removeEventListener("fullscreenchange", update);
    }, []);

    useEffect(() => {
        if (!keyboard) return;

        const handleKeyDown = (event: KeyboardEvent) => {
            if (event.key !== "F11" || event.altKey || event.ctrlKey || event.metaKey || event.shiftKey) return;
            event.preventDefault();
            if (event.repeat) return;

            const request = document.fullscreenElement
                ? document.exitFullscreen()
                : ref.current?.requestFullscreen();
            request?.catch((error: unknown) => console.error("Unable to toggle fullscreen", error));
        };

        document.addEventListener("keydown", handleKeyDown);
        return () => document.removeEventListener("keydown", handleKeyDown);
    }, [keyboard]);

    const toggle = async () => {
        const element = ref.current;
        if (!element) return;

        if (document.fullscreenElement === element) {
            await document.exitFullscreen();
        } else {
            await element.requestFullscreen();
        }
    };

    return (
        <div ref={ref} className={active ? "flex h-screen w-screen flex-col gap-4 bg-black p-4" : className}>
            {buttonLabel && <FullscreenButton active={active} label={buttonLabel} onClick={() => {
                void toggle().catch((error: unknown) => console.error("Unable to toggle fullscreen", error));
            }} />}
            {children(active)}
        </div>
    );
}

export default Fullscreen;
