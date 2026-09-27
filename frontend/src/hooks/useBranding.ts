import { createContext, useContext } from "react";
import type { InfoResponse } from "../api/status";

export const BrandingContext = createContext<InfoResponse | null>(null);

export function useBranding() {
    return useContext(BrandingContext);
}
