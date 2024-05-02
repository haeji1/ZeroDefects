import axios from 'axios';
import { create } from 'zustand'
import { persist } from 'zustand/middleware'

export const useBookmark = create(
    persist(
        (set) => ({
            bookmark: [],
            addBookmark: async (data) => {
                console.log("북마크 추가 시작")
                const res = await axios({
                    method: 'post',
                    url: 'http://localhost:8000/api/section',
                    data: {
                        facility: data.facility,
                        parameter: data.parameter,
                        startTime: data.startTime.toISOString(), // 확인 필요
                        endTime: data.endTime.toISOString(),
                    }
                })
                console.log("끝")
                set((state) => ({
                    bookmark: [
                        ...state.bookmark,
                        {
                            id: state.bookmark.length > 0 ? state.bookmark.at(-1).id + 1 : 1,
                            facility: data.facility,
                            parameter: data.parameter,
                            startTime: data.startTime,
                            endTime: data.endTime,
                            cycles: res.data.cycles,
                        }
                    ]
                }))
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