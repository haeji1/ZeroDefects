import { create } from 'zustand'

export const useGraphDataStore = create((set) => ({
    graphData: [],
    parameterData: [],
    setGraphData: (val) => set({ graphData: val }),
    setParameterData: (val) => set({ parameterData: val }),
}))