import { create } from "zustand";
import { persist } from 'zustand/middleware'


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

interface Batch {
    batchName: string;
    batchStartTime: string;
    batchEndTime: string;
}

interface BatchStore {
    batchList: { [key: string]: Batch[] },
    addBatch: (facility: string, newBatch: Batch[]) => void,
}

interface FacilityStore {
    facilityList: { [key: string]: string[] },
    updateFacility: (data: { [key: string]: string[] }) => void,
}

export const useFacilityStore = create<FacilityStore>()(
    (set) => ({
        facilityList: {},
        updateFacility: (data) => set({ facilityList: data }),
    })
);

export const useBatchStore = create<BatchStore>()(
    persist(
        (set) => ({
            batchList: {},
            addBatch: (facility, newBatch) => {
                set((state: any) => (
                    {
                        batchList: {
                            ...state.batchList,
                            [facility]: newBatch,
                        }
                    }
                ))
            },
        }),
        { name: 'batchStorage' }
    )
)