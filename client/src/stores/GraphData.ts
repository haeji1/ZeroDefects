import { create } from 'zustand'


interface GraphDataStore {
    graphData: any;
    isFetching: boolean;
    setIsFetching: (fetching: boolean) => void;
    setGraphData: (data: any) => void;
}


export const useGraphDataStore = create<GraphDataStore>((set) => ({
    graphData: [],
    isFetching: false,
    setIsFetching: (bool) => set(bool ? { isFetching: true } : { isFetching: false }),
    setGraphData: (val) => set({ graphData: val }),
}))