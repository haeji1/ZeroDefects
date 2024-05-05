import { create } from "zustand";

export const useFacilityStore = create(
    (set) => ({
        facilityList: {},
        updateFacility: (data) => set({ facilityList: data }),
        batchList: {},
        addBatch: (newBatch) => set((state) => ({
            batchList: {
                ...state.batchList,
                newBatch,
            }
        })),
    })
);