import { create } from 'zustand'

export const useStore = create((set) => ({
    count: 1,
    inc: () => set((state) => ({ count: state.count + 1 })),
}))