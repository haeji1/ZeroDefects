import { create } from 'zustand'
import { persist } from 'zustand/middleware'


interface Bookmark {
    id?: number;
    facility: string;
    parameter: string;
    selectedBatchName?: string | null;
}

interface BookmarkStore {
    bookmark: Bookmark[];
    addBookmark: (facilInfo: Bookmark) => void;
    deleteBookmark: (id: number) => void;
    updateBookmark: (data: Bookmark) => void;
}

interface SelectedBookmarkStore {
    selectedBookmark: Bookmark[],
    setSelectedBookmark: (data: Bookmark[]) => void,
}



export const useBookmarkStore = create<BookmarkStore>()(
    persist(
        (set) => ({
            bookmark: [],
            addBookmark: (facilInfo) => set((state) => ({
                bookmark: [
                    ...state.bookmark,
                    {
                        id: state.bookmark.length > 0 ? state.bookmark.at(-1).id + 1 : 1,
                        facility: facilInfo.facility,
                        parameter: facilInfo.parameter,
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
                        selectedBatchName: data.selectedBatchName,
                    }
                ]
            })),
        }),
        { name: 'bookmarkStorage' }
    )
);

export const useSelectedBookmarkStore = create<SelectedBookmarkStore>()((set) => ({
    selectedBookmark: [],
    setSelectedBookmark: (data) => set({ selectedBookmark: data }),
}))