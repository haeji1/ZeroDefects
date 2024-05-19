import { create } from "zustand";
import { persist } from "zustand/middleware";

interface TGLife {
  facility: String;
  tgLifeNum: String;
  startTime: String;
  endTime: String;
}

interface TGLifeStore extends TGLife {
  setFacility: (facility: string) => void;
  setTGLifeNum: (tgLifeNum: string) => void;
  setStartTime: (startTime: string) => void;
  setEndTime: (endTime: string) => void;
}

export const useTGLifeStore = create<TGLifeStore>()(
  persist(
    (set) => ({
      facility: "",
      tgLifeNum: "",
      startTime: "",
      endTime: "",
      setFacility: (facility) => set({ facility }),
      setTGLifeNum: (tgLifeNum) => set({ tgLifeNum }),
      setStartTime: (startTime) => set({ startTime }),
      setEndTime: (endTime) => set({ endTime }),
    }),
    { name: "tgLifeStorage" }
  )
);
