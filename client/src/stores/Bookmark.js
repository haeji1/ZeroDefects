import { create } from 'zustand'
import { persist } from 'zustand/middleware'

export const useBookmark = create(
    persist(
        (set) => ({
            bookmark: [],
            addBookmark: (data) => set((state) => ({
                bookmark: [
                    ...state.bookmark,
                    {
                        id: state.bookmark.length > 0 ? state.bookmark.at(-1).id + 1 : 1,
                        facility: data.facility,
                        parameter: data.parameter,
                        startTime: data.startTime,
                        endTime: data.endTime,
                    }
                ]
            })),
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
                    }
                ]
            })),
        }),
        { name: 'bookmarkStorage' }
    )
);