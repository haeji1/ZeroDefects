import {
    Select,
    SelectContent,
    SelectItem,
    SelectTrigger,
    SelectValue,
} from "@/components/base/select";
import { Card } from "@/components/base/card";
import { format } from "date-fns"
import { ko } from "date-fns/locale"
import { Calendar as CalendarIcon } from "lucide-react";
import { cn } from "@/lib/utils";
import { Button } from "@/components/base/button";
import { Popover, PopoverContent, PopoverTrigger } from "@/components/base/popover";
import { useState } from "react";
import { Calendar } from "@/components/base/calendar";
import { Input } from "@/components/base/input";
import { useParameterStore } from "@/stores/ParameterList"
import { useGraphDataStore } from "@/stores/GraphData";
import { useBookmark } from "@/stores/Bookmark";

function SelectSection() {

    // 그래프 조회에 필요한 인자들
    const [facility, setFacility] = useState()
    const [parameter, setParameter] = useState()
    const [startDate, setStartDate] = useState()
    const [startTime, setStartTime] = useState()
    const [endDate, setEndDate] = useState()
    const [endTime, setEndTime] = useState()


    const { graphData, parameterData, setGraphData, setParameterData } = useGraphDataStore()
    const { addParameter } = useParameterStore();
    const { addBookmark } = useBookmark();
    // 시작 및 종료 시간을 설정하는 Input 핸들러
    const handleTime = (e) => {
        if (e.target.id === "startTime") {
            setStartTime(e.target.value)
        }
        else if (e.target.id === "endTime") {
            setEndTime(e.target.value)
        }
    }

    // 설비 목록
    const facilityList = ["F1490", "F1491", "F1492"]
    // 파라미터 목록
    const paramList = ["L.PiG301Press[Pa]", "L.PiG402Press[Pa]", "P.PiG201Press[Pa]", "P.PiG202Press[Pa]", "P.PEG201Press[Pa]", "P.DG201Press[Pa]"
        , "PFC.T(In)[C]", "PFC.T(Out)[C]", "Im_1[Times]", "dU_1[Times]", "Im_2[Times]", "dU_2[Times]", "Im_4[Times]",
        "dU_4[Times]", "Im_5[Times]", "dU_5[Times]", "No1_P[V]", "No1_P[A]", "No1_P[kW]", "No2_P[V]", "No2_P[A]", "No2_P[kW]", "No4_P[V]", "No4_P[A]",
        "No4_P[kW]", "No5_P[V]", "No5_P[A]", "No5_P[kW]", "No6_P1_Fwd[kW]", "No6_P1_Ref[KW]", "No6_P1_Vpp[V]", "No6_P1_Vdc[V]",
        "No6_P2_Fwd[kW]", "No6_P2_Ref[KW]", "No6_P2_Vpp[V]", "No6_P2_Vdc[V]", "No6_P3_Fwd[kW]", "No6_P3_Ref[KW]", "No6_P3_Vpp[V]", "No6_P3_Vdc[V]", "No6_P4_Fwd[kW]", "No6_P4_Ref[KW]", "No6_P4_Vpp[V]", "No6_P4_Vdc[V]", "No6_A1[sccm]", "No6_O1[sccm]", "No6_O2[sccm]",
        "No6_N1[sccm]", "No1_A1[sccm]", "No1_A2[sccm]", "No1_A3[sccm]", "No1_A4[sccm]", "No2_A1[sccm]", "No2_A2[sccm]", "No2_A3[sccm]", "No2_A4[sccm]",
        "No4_A1[sccm]", "No4_A2[sccm]", "No4_A3[sccm]", "No4_A4[sccm]", "No5_A1[sccm]", "No5_A2[sccm]", "No5_A3[sccm]", "No5_A4[sccm]"]




    return (
        <div>
            <Card className="h-[80px] mr-5 mb-5 items-center flex flex-row px-3 space-x-3">
                <Select onValueChange={setFacility}>
                    <SelectTrigger className="w-[180px] self-center">
                        <SelectValue placeholder="설비명" />
                    </SelectTrigger>
                    <SelectContent>
                        {facilityList.map(facility => (
                            <SelectItem key={facility} value={facility}>{facility}</SelectItem>
                        ))}
                    </SelectContent>
                </Select>

                <Select onValueChange={setParameter}>
                    <SelectTrigger className="w-[180px] self-center">
                        <SelectValue placeholder="파라미터 명" />
                    </SelectTrigger>
                    <SelectContent>
                        {paramList.map((param) => (
                            <SelectItem key={param} value={param}>{param}</SelectItem>
                        ))}
                    </SelectContent>
                </Select>

                <Popover>
                    <PopoverTrigger asChild>
                        <Button
                            variant={"outline"}
                            className={cn(
                                "w-[200px] justify-start text-left font-normal",
                                !startDate && "text-muted-foreground"
                            )}
                        >
                            <CalendarIcon className="mr-2 h-4 w-4" />
                            {startDate ? format(startDate, "yyyy년 MM월 dd일") : <span>시작 날짜</span>}
                        </Button>
                    </PopoverTrigger>
                    <PopoverContent className="w-auto p-0">
                        <Calendar
                            mode="single"
                            selected={startDate}
                            onSelect={setStartDate}
                            locale={ko}
                            initialFocus
                        />
                    </PopoverContent>
                </Popover>
                <Input className="w-[130px]" type={"time"} id="startTime" onChange={handleTime} />
                <h1>
                    ~
                </h1>
                <Popover>
                    <PopoverTrigger asChild>
                        <Button
                            variant={"outline"}
                            className={cn(
                                "w-[200px] justify-start text-left font-normal",
                                !endDate && "text-muted-foreground"
                            )}
                        >
                            <CalendarIcon className="mr-2 h-4 w-4" />
                            {endDate ? format(endDate, "yyyy년 MM월 dd일") : <span>종료 날짜</span>}
                        </Button>
                    </PopoverTrigger>
                    <PopoverContent className="w-auto p-0">
                        <Calendar
                            mode="single"
                            selected={endDate}
                            onSelect={setEndDate}
                            locale={ko}
                            initialFocus
                        />
                    </PopoverContent>
                </Popover>
                <Input className="w-[130px]" type={"time"} id="endTime" onChange={handleTime} />
                <Button>그래프 조회</Button>
                <Button
                    onClick={() => {
                        addBookmark(
                            {
                                facility: facility,
                                parameter: parameter,
                                startDate: startDate,
                                startTime: startTime,
                                endDate: endDate,
                                endTime: endTime,
                            }
                        )
                    }}
                >
                    비교 목록 추가</Button>
            </Card>

        </div>
    )
}

export default SelectSection;