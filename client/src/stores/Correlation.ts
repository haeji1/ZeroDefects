import { create } from "zustand";

interface CorrelationStore {

    selectedFacility: string;
    setSelectedFacility: (facility: string) => void;
    selectedParameters: {};
    setSelectedParameters: (parameters: string[]) => void;
    graphData: any[];
    setGraphData: (data: any) => void;
    isFetching: boolean;
    setIsFetching: (fetching: boolean) => void;
    isCollapse: boolean;
    setIsCollapse: (collapse: boolean) => void;
}

export const useCorrelationStore = create<CorrelationStore>()((set) => ({

    selectedFacility: "",
    setSelectedFacility: (facility) => set({ selectedFacility: facility }),
    selectedParameters: {},
    setSelectedParameters: (parameters) => set({ selectedParameters: parameters }),
    graphData: [],
    setGraphData: (val) => set({ graphData: val }),
    isFetching: false,
    setIsFetching: (bool) => set(bool ? { isFetching: true } : { isFetching: false }),
    isCollapse: false,
    setIsCollapse: (bool) => set(bool ? { isCollapse: true } : { isCollapse: false }),
}))





