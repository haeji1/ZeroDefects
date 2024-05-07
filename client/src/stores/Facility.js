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
//}


export const useFacilityStore = create(
    (set) => ({
        facilityList: {},
        updateFacility: (data) => set({ facilityList: data }),
        batchList: {},

        addBatch: (facility, newBatch) => {

            console.log({ [facility]: newBatch })
            set((state) => (


                {
                    batchList: {
                        ...state.batchList,
                        [facility]: newBatch,
                    }
                }
            ))
        },
    })
);

export const useBatchStore = create(
    persist(
        (set) => ({
            batchList: {},
            addBatch: (facility, newBatch) => {
                set((state) => (
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