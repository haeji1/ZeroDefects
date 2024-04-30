import { create } from 'zustand'

export const useBookmark = create((set) => ({
    bookmark: [],
    addBookmark: (data) =>
        set((state) => ({
            bookmark: [
                ...state.bookmark,
                {
                    id: state.bookmark.length > 0 ? state.bookmark.at(-1).id + 1 : 1,
                    facility: data.facility,
                    parameter: data.parameter,
                    startDate: data.startDate,
                    startTime: data.startTime,
                    endDate: data.endDate,
                    endTime: data.endTime,
                }
            ]
        })),
    deleteBookmark: (id) =>
        set((state) => ({ bookmark: state.bookmark.filter((e) => e.id !== id) })),
    updateBookmark: (data) =>
        set((state) => ({
            bookmark: [
                ...state.bookmark.filter((e) => e.id !== data.id),
                {
                    id: data.id,
                    facility: data.facility,
                    parameter: data.parameter,
                    startDate: data.startDate,
                    startTime: data.startTime,
                    endDate: data.endDate,
                    endTime: data.endTime,
                }
            ]
        })),

}))