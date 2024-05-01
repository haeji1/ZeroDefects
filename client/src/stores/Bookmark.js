import axios from 'axios';
import { create } from 'zustand'
import { persist } from 'zustand/middleware'

const initialState = [
    {
        "id": 1,
        "facility": "F1490",
        "parameter": "No6_P2_Vdc[V]",
        "startTime": '1995-12-17T03:24:00',
        "endTime": '1995-12-17T03:24:00',
        "cycles": [
            {
                "cycleName": "cycle1",
                "cycleStartTime": '1995-12-17T03:24:00',
                "cycleEndTime": '1995-12-17T03:24:00',
            },
            {
                "cycleName": "cycle2",
                "cycleStartTime": '1995-12-17T03:24:00',
                "cycleEndTime": '1995-12-17T03:24:00',
            }
        ],
        "cycleName": "cycle-F1496-240311-101751",
        "step": 8,
    },
    {
        "id": 2,
        "facility": "F1491",
        "parameter": "No6_P2_Vdc[V]",
        "startTime": '1995-12-17T03:24:00',
        "endTime": '1995-12-17T03:24:00',
        "cycles": [
            {
                "cycleName": "cycle3",
                "cycleStartTime": '1995-12-17T03:24:00',
                "cycleEndTime": '1995-12-17T03:24:00',
            },
            {
                "cycleName": "cycle4",
                "cycleStartTime": '1995-12-17T03:24:00',
                "cycleEndTime": '1995-12-17T03:24:00',
            }
        ],
        "cycleName": null,
        "step": null,
    }
]


export const useBookmark = create(
    persist(
        (set) => ({
            bookmark: initialState,
            // addBookmark: (data) => set((state) => ({
            //     bookmark: [
            //         ...state.bookmark,
            //         {
            //             id: state.bookmark.length > 0 ? state.bookmark.at(-1).id + 1 : 1,
            //             facility: data.facility,
            //             parameter: data.parameter,
            //             startTime: data.startTime,
            //             endTime: data.endTime,
            //         }
            //     ]
            // })),
            addBookmark: async (data) => {
                // const res = await axios({
                //     method: 'post',
                //     url: '/api/section',
                //     data: {
                //         facility: data.facility,
                //         parameter: data.parameter,
                //         startTime: data.startTime.toISOString(), // 확인 필요
                //         endTime: data.endTime.toISOString(),
                //     }
                // })
                // set((state) => ({
                //     bookmark: [
                //         ...state.bookmark,
                //         {
                //             id: state.bookmark.length > 0 ? state.bookmark.at(-1).id + 1 : 1,
                //             facility: data.facility,
                //             parameter: data.parameter,
                //             startTime: data.startTime,
                //             endTime: data.endTime,
                //             cycles: res.data.cycles,
                //         }
                //     ]
                // }))
            },
            deleteBookmark: (id) => set((state) => ({ bookmark: state.bookmark.filter((e) => e.id !== id) })),
            updateBookmark: (data) => set((state) => ({
                bookmark: [
                    ...state.bookmark.filter((e) => e.id !== data.id),
                    {
                        id: data.id,
                        facility: data.facility,
                        parameter: data.parameter,
                        startTime: data.startTime,
                        endTime: data.endTime,
                        cycles: data.cycles,
                        cycleName: data.cycleName,
                        step: data.step,
                    }
                ]
            })),
        }),
        { name: 'bookmarkStorage' }
    )
);