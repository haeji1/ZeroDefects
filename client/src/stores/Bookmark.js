import { create } from 'zustand'
import { persist } from 'zustand/middleware'

export const useBookmarkStore = create(
    persist(
        (set) => ({
            bookmark: [],
            addBookmark: (newData) => set((state) => ({
                bookmark: [
                    ...state.bookmark,
                    {
                        id: state.bookmark.length > 0 ? state.bookmark.at(-1).id + 1 : 1,
                        facility: newData.facility,
                        parameter: newData.parameter,
                        selectedBatchName: null,
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

export const useSelectedBookmarkStore = create((set) => ({
    selectedBookmark: [],
    setSelectedBookmark: (data) => set({ selectedBookmark: data }),
}))