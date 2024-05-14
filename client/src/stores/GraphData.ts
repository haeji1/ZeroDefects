import { create } from 'zustand'


interface GraphDataStore {
    graphData: any[];
    isFetching: boolean;
    isCollapse: boolean;
    setIsFetching: (fetching: boolean) => void;
    setGraphData: (data: any) => void;
    setIsCollapse: (collapse: boolean) => void;

}


export const useGraphDataStore = create<GraphDataStore>((set) => ({
    graphData: [],
    isFetching: false,
    isCollapse: false,
    setIsFetching: (bool) => set(bool ? { isFetching: true } : { isFetching: false }),
    setGraphData: (val) => set({ graphData: val }),
    setIsCollapse: (bool) => set(bool ? { isCollapse: true } : { isCollapse: false }),
}))