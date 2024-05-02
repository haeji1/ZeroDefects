import { create } from "zustand";

export const useParameterStore = create((set) => ({
    parameterList: [],
    addParameter: (val) =>
        set((prev) => ({
            // id 이상한걸로 설정해서 수정 필요
            parameterList: [
                ...prev.parameterList,
                { id: new Date().getMilliseconds(), facility: val.facility, parameter: val.parameter },
            ],
        })),
    removeParameter: (id) =>
        set((prev) => ({ parameterList: prev.parameterList.filter((e) => e.id !== id) })),

}))