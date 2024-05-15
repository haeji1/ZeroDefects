import { create } from 'zustand'

type QueryType = "time" | "step";

interface QueryDateTime {
    queryStartDate: Date;
    setQueryStartDate: (date: Date) => void;
    queryStartTime: string;
    setQueryStartTime: (time: string) => void;
    queryEndDate: Date;
    setQueryEndDate: (date: Date) => void;
    queryEndTime: string;
    setQueryEndTime: (time: string) => void;
    timeValid: boolean;
    setTimeValid: () => void;
}

interface QueryStep {
    queryStartStep: number;
    setQueryStartStep: (step: number) => void;
    queryEndStep: number;
    setQueryEndStep: (step: number) => void;
    stepValid: boolean;
    setStepValid: () => void;
}


interface QueryButton {
    queryTypeButton: QueryType;
    setQueryTypeButton: (type: QueryType) => void;
}

export const useQueryDateTimeStore = create<QueryDateTime>((set) => ({
    queryStartDate: new Date(),
    setQueryStartDate: (date) => set({ queryStartDate: date }),
    queryStartTime: "",
    setQueryStartTime: (time) => set({ queryStartTime: time }),
    queryEndDate: new Date(),
    setQueryEndDate: (date) => set({ queryEndDate: date }),
    queryEndTime: "",
    setQueryEndTime: (time) => set({ queryEndTime: time }),
    timeValid: false,
    setTimeValid: () => set((state) => ({ timeValid: !state.timeValid })),
}));

export const useQueryStepStore = create<QueryStep>((set) => ({
    queryStartStep: 0,
    setQueryStartStep: (step) => set({ queryStartStep: step }),
    queryEndStep: 0,
    setQueryEndStep: (step) => set({ queryEndStep: step }),
    stepValid: false,
    setStepValid: () => set((state) => ({ stepValid: !state.stepValid })),
}));

export const useQueryButtonStore = create<QueryButton>((set) => ({
    queryTypeButton: "time",
    setQueryTypeButton: (type) => set({ queryTypeButton: type })
}))