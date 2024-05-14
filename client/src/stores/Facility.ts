import { create } from "zustand";
import { persist } from 'zustand/middleware'

interface Batch {
    batchName: string;
    batchStartTime: Date;
    batchEndTime: Date;
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