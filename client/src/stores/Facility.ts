import { create } from "zustand";
import { persist } from 'zustand/middleware'

interface Batch {
    batchName: string;
    batchStartTime: Date;
    batchEndTime: Date;
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
    updateBatch: (facilityName: string, batchList: Batch[]) => void,
}

export const useFacilityStore = create<FacilityStore>()(
    persist(
        (set) => ({
            facilityList: {},
            updateFacilityList: (data) => set({ facilityList: data }),
            updateBatch: (facilityName, batchList) => {
                set((state) => ({
                    facilityList: {
                        ...state.facilityList,
                        [facilityName]: {
                            ...state.facilityList[facilityName],
                            batches: batchList
                        }
                    }
                }));
            }
        }), { name: 'facilityStorage' }
    ));


// batchList = {
//     'F1492': [
//                {
//                   "batchName": "batch-F1508-2024-04-16T20:18:40",
//                   "batchStartTime": "2024-04-16T20:18:40+00:00Z",
//                   "batchEndTime": "2024-04-16T21:37:25+00:00Z",],
//                },
//                {
//                   "batchName": "batch-F1508-2024-04-16T20:18:40",
//                   "batchStartTime": "2024-04-16T20:18:40+00:00Z",
//                   "batchEndTime": "2024-04-16T21:37:25+00:00Z",],
//                },
//              ],
//     'F1493': [
//                {
//                   "batchName": "batch-F1508-2024-04-16T20:18:40",
//                   "batchStartTime": "2024-04-16T20:18:40+00:00Z",
//                   "batchEndTime": "2024-04-16T21:37:25+00:00Z",],
//                },
//                {
//                   "batchName": "batch-F1508-2024-04-16T20:18:40",
//                   "batchStartTime": "2024-04-16T20:18:40+00:00Z",
//                   "batchEndTime": "2024-04-16T21:37:25+00:00Z",],
//                },
//              ]
// }