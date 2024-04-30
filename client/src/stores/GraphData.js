import { create } from 'zustand'

export const useGraphDataStore = create((set) => ({
    graphData: [],
    setGraphData: (val) => set({ graphData: val }),
}))