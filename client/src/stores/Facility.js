import { create } from "zustand";


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

        addBatch: (newBatch) => set((state) => ({
            batchList: {
                ...state.batchList,
                newBatch
            }
        })),
    })
);