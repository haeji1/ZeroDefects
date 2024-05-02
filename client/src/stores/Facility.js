import { create } from "zustand";

const initialState = {
    "F1490": ["L.PiG301Press[Pa]", "L.PiG402Press[Pa]", "P.PiG201Press[Pa]", "P.PiG202Press[Pa]", "P.PEG201Press[Pa]", "P.DG201Press[Pa]", "PFC.T(In)[C]", "PFC.T(Out)[C]", "Im_1[Times]", "dU_1[Times]", "Im_2[Times]", "dU_2[Times]", "Im_4[Times]", "No4_A1[sccm]", "No4_A2[sccm]", "No4_A3[sccm]"],
    "F1491": ["dU_4[Times]", "Im_5[Times]", "dU_5[Times]", "No1_P[V]", "No1_P[A]", "No1_P[kW]", "No2_P[V]", "No2_P[A]", "No2_P[kW]", "No4_P[V]", "No4_P[A]", "No4_P[kW]", "No5_P[V]", "No5_P[A]", "No5_P[kW]", "No6_P1_Fwd[kW]", "No6_P1_Ref[KW]", "No6_P1_Vpp[V]", "No6_P1_Vdc[V]", "No6_P2_Fwd[kW]"],
    "F1492": ["No6_P2_Ref[KW]", "No6_P2_Vpp[V]", "No6_P2_Vdc[V]", "No6_P3_Fwd[kW]", "No6_P3_Ref[KW]", "No6_P3_Vpp[V]", "No6_P3_Vdc[V]", "No6_P4_Fwd[kW]", "No6_P4_Ref[KW]", "No6_P4_Vpp[V]", "No6_P4_Vdc[V]", "No6_A1[sccm]", "No6_O1[sccm]", "No6_O2[sccm]", "No6_N1[sccm]", "No1_A1[sccm]", "No1_A2[sccm]", "No1_A3[sccm]", "No1_A4[sccm]", "No2_A1[sccm]", "No2_A2[sccm]", "No2_A3[sccm]", "No2_A4[sccm]", "No4_A4[sccm]", "No5_A1[sccm]", "No5_A2[sccm]", "No5_A3[sccm]", "No5_A4[sccm]"]
}

export const useFacilityStore = create(
    (set) => ({
        facilityList: initialState,
        updateFacility: (data) => set({ facilityList: data })
    }),

);