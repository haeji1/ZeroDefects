import { create } from 'zustand'

export type QueryType = "time" | "step" | "lifeCnt";

interface QueryDateTime {
    queryStartDate: Date;
    setQueryStartDate: (date: Date) => void;
    queryEndDate: Date;
    setQueryEndDate: (date: Date) => void;
    timeValid: boolean;
    setTimeValid: (valid: boolean) => void;
}

interface QueryStep {
    queryStartStep: number;
    setQueryStartStep: (step: number) => void;
    queryEndStep: number;
    setQueryEndStep: (step: number) => void;
    stepValid: boolean;
    setStepValid: (valid: boolean) => void;
}

interface QueryLifeCnt {
    queryStartCnt: number;
    setQueryStartCnt: (cnt: number) => void;
    queryEndCnt: number;
    setQueryEndCnt: (cnt: number) => void;
    lifeCntValid: boolean;
    setLifeCntValid: (valid: boolean) => void;
}

interface QueryTypeStore {
    queryType: QueryType;
    setQueryType: (type: QueryType) => void;
}

export const useQueryDateTimeStore = create<QueryDateTime>((set) => ({
    queryStartDate: new Date(),
    setQueryStartDate: (date) => set({ queryStartDate: date }),
    queryEndDate: new Date(),
    setQueryEndDate: (date) => set({ queryEndDate: date }),
    timeValid: false,
    setTimeValid: (valid) => set({ timeValid: valid }),
}));

export const useQueryStepStore = create<QueryStep>((set) => ({
    queryStartStep: 0,
    setQueryStartStep: (step) => set({ queryStartStep: step }),
    queryEndStep: 0,
    setQueryEndStep: (step) => set({ queryEndStep: step }),
    stepValid: true,
    setStepValid: (valid) => set({ stepValid: valid }),
}));

export const useQueryLifeCntStore = create<QueryLifeCnt>((set) => ({
    queryStartCnt: 0,
    setQueryStartCnt: (cnt) => set({ queryStartCnt: cnt }),
    queryEndCnt: 0,
    setQueryEndCnt: (cnt) => set({ queryEndCnt: cnt }),
    lifeCntValid: true,
    setLifeCntValid: (valid) => set({ lifeCntValid: valid }),
}))

export const useQueryTypeStore = create<QueryTypeStore>((set) => ({
    queryType: "time",
    setQueryType: (type) => set({ queryType: type })
}))
