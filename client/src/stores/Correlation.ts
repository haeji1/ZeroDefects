import { create } from "zustand";
import { Batch } from "./Facility";

interface CorrelationStore {

    selectedFacility: string;
    setSelectedFacility: (facility: string) => void;
    selectedBatch: Batch | null
    setSelectedBatch: (batch: Batch) => void;
    selectedParameters: [];
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
    selectedBatch: null,
    setSelectedBatch: (batch) => set({ selectedBatch: batch }),
    selectedParameters: [],
    setSelectedParameters: (parameters) => set({ selectedParameters: parameters }),
    graphData: [],
    setGraphData: (val) => set({ graphData: val }),
    isFetching: false,
    setIsFetching: (bool) => set(bool ? { isFetching: true } : { isFetching: false }),
    isCollapse: false,
    setIsCollapse: (bool) => set(bool ? { isCollapse: true } : { isCollapse: false }),
}))





