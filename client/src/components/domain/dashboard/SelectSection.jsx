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

import { useState, useEffect } from "react";
import { Calendar } from "@/components/base/calendar";
import { Input } from "@/components/base/input";
import { useFacilityStore } from "@/stores/Facility"
import { useGraphDataStore } from "@/stores/GraphData";
import { useBookmark } from "@/stores/Bookmark";
import axios from "axios";

function SelectSection() {

    // 그래프 조회에 필요한 인자들
    const [facility, setFacility] = useState()
    const [parameter, setParameter] = useState()
    const [startDate, setStartDate] = useState()
    const [startTime, setStartTime] = useState()
    const [endDate, setEndDate] = useState()
    const [endTime, setEndTime] = useState()


    const { facilityList, updateFacility } = useFacilityStore();
    const { bookmark, addBookmark } = useBookmark();
    // 시작 및 종료 시간을 설정하는 Input 핸들러
    const handleTime = (e) => {
        if (e.target.id === "startTime") {
            setStartTime(e.target.value)
        }
        else if (e.target.id === "endTime") {
            setEndTime(e.target.value)
        }
    }

    // DB에 존재하는 설비 리스트들이랑, 해당 설비의 파라미터들 마운트 시에 가져오기
    useEffect(() => {
        const fetchData = async () => {
            try {
                console.log('DB에 존재하는 설비 및 파라미터 리스트 가져오기 시작')
                const response = await axios.get('http://localhost:8000/facility/info');
                // 응답 데이터 설비 리스트에 업데이트
                //   updateFacility(data)
            } catch (error) {
                console.error('Error fetching data:', error);
            }
        };
        fetchData(); // 데이터를 가져오는 함수 호출
    }, []);

    // 그래프 조회 
    const getGraphData = async () => {
        const startParts = startTime.split(":");
        const endParts = endTime.split(":");
        axios.post('http://localhost:8000/facility/info', {
            facility: facility,
            parameter: parameter,
            startTime: new Date(startDate.getFullYear(), startDate.getMonth(), startDate.getDate(), startParts[0], startParts[1]).toISOString(),
            endTime: new Date(endDate.getFullYear(), endDate.getMonth(), endDate.getDate(), endParts[0], endParts[1]).toISOString(),
            cycle: null,
            step: null,
        })
            .then(response => {
                console.log(response.data);
            })
            .catch(error => {
                console.log(error, "그래프 받아오는 것 실패");
            })
    }

    return (
        <div>
            <Card className="h-[80px] mr-5 mb-5 items-center flex flex-row px-3 space-x-3">
                <Select onValueChange={setFacility}>
                    <SelectTrigger className="w-[180px] self-center">
                        <SelectValue placeholder="설비명" />
                    </SelectTrigger>
                    <SelectContent>
                        {Object.keys(facilityList).map(facility => (
                            <SelectItem key={facility} value={facility} >{facility}</SelectItem>
                        ))}
                    </SelectContent>
                </Select>

                <Select onValueChange={setParameter}>
                    <SelectTrigger className="w-[180px] self-center">
                        <SelectValue placeholder="" />
                    </SelectTrigger>
                    <SelectContent>
                        {facilityList[facility] !== undefined ? facilityList[facility].map((param) => (
                            <SelectItem key={param} value={param}>{param}</SelectItem>
                        )) : null}
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
                <Button onClick={getGraphData}>그래프 조회</Button>
                <Button
                    onClick={() => {

                        const startParts = startTime.split(":");
                        const endParts = endTime.split(":");
                        console.log(new Date(startDate.getFullYear(), startDate.getMonth(), startDate.getDate(), startParts[0], startParts[1]))

                        addBookmark(
                            {
                                facility: facility,
                                parameter: parameter,
                                startTime: new Date(startDate.getFullYear(), startDate.getMonth(), startDate.getDate(), startParts[0], startParts[1]),
                                endTime: new Date(endDate.getFullYear(), endDate.getMonth(), endDate.getDate(), endParts[0], endParts[1]),
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