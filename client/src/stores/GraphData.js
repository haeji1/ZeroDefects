import { create } from 'zustand'

export const useGraphDataStore = create((set) => ({
    graphData: [],
    isFetching: false,
    setIsFetching: (bool) => set(bool ? { isFetching: true } : { isFetching: false }),
    setGraphData: (val) => set({ graphData: val }),
}))