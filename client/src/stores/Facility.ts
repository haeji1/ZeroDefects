import { create } from "zustand";
import { persist } from 'zustand/middleware'

export interface Batch {
    batchName: string;
    batchStartTime: string;
    batchEndTime: string;
    stepsCnt: number;
}

interface BatchStore {
    batchList: { [key: string]: Batch[] };
    addBatch: (facilityName: string, batches: Batch[]) => void;
}


export interface Facility {
    [key: string]: {
        parameters: string[];
        batches?: Batch[];
    };
}

interface FacilityStore {
    facilityList: Facility,
    updateFacilityList: (data: Facility) => void,
}

export const useFacilityStore = create<FacilityStore>()(
    persist(
        (set) => ({
            facilityList: {},
            updateFacilityList: (data) => set({ facilityList: data }),
        }), { name: 'facilityStorage' }
    ));

export const useBatchStore = create<BatchStore>()(
    persist(
        (set) => ({
            batchList: {},
            addBatch: (facilityName, batches) => {
                set((state) => ({
                    batchList: {
                        ...state.batchList,
                        [facilityName]: batches
                    }
                }))
            }
        }), { name: 'batchStorage' })
)