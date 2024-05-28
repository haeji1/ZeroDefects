import { create } from "zustand";

export type TgLifeNum = "1" | "2" | "4" | "5";


interface TargetLifeStore {

    cycleList: any[];
    setCycleList: (cycle: any) => void;
    selectedParam: string;
    setSelectedParam: (param: string) => void;
    selectedCycleList: any[];
    setSelectedCycleList: (selectedCycles: any[]) => void;
    selectedStat: string;
    setSelectedStat: (stat: string) => void;
    selectedFacility: string;
    setSelectedFacility: (facility: string) => void;
    selectedTgLifeNum?: TgLifeNum
    setSelectedTgLifeNum: (TgLifeNum: TgLifeNum) => void;
    graphData: any[];
    setGraphData: (data: any) => void;
    isFetching: boolean;
    setIsFetching: (fetching: boolean) => void;
    isCollapse: boolean;
    setIsCollapse: (collapse: boolean) => void;
}

export const useTargetLifeStore = create<TargetLifeStore>()((set) => ({

    cycleList: [],
    setCycleList: (val) => set({ cycleList: val }),
    selectedCycleList: [],
    setSelectedCycleList: (selectedCycles) => set({ selectedCycleList: selectedCycles }),
    selectedParam: "",
    setSelectedParam: (param) => set({ selectedParam: param }),
    selectedStat: "",
    setSelectedStat: (stat) => set({ selectedStat: stat }),
    selectedFacility: "",
    setSelectedFacility: (facility) => set({ selectedFacility: facility }),
    selectedTgLifeNum: undefined,
    setSelectedTgLifeNum: (TgLifeNum) => set({ selectedTgLifeNum: TgLifeNum }),
    graphData: [],
    setGraphData: (val) => set({ graphData: val }),
    isFetching: false,
    setIsFetching: (bool) => set(bool ? { isFetching: true } : { isFetching: false }),
    isCollapse: false,
    setIsCollapse: (bool) => set(bool ? { isCollapse: true } : { isCollapse: false }),
}))