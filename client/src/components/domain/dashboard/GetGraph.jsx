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
import { Calendar as CalendarIcon, ListOrdered as StepIcon, Clock as TimeIcon } from "lucide-react";
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
import { fetchFacilityInfos } from "@/apis/api/api";
import { Label } from "@/components/base/label";

function GetGraph() {
    // 그래프 조회에 필요한 인자들
    const [facility, setFacility] = useState()
    const [parameter, setParameter] = useState()
    const [startDate, setStartDate] = useState()
    const [startTime, setStartTime] = useState()
    const [endDate, setEndDate] = useState()
    const [endTime, setEndTime] = useState()
    const [startStep, setStartStep] = useState();
    const [endStep, setEndStep] = useState();

    const { facilityList, updateFacility } = useFacilityStore();
    const { bookmark, addBookmark } = useBookmark();
    const { setGraphData, setIsFetching } = useGraphDataStore()


    // 시작 및 종료 시간을 설정하는 Input 핸들러
    const handleTime = (e) => {
        if (e.target.id === "startTime") {
            setStartTime(e.target.value)
        }
        else if (e.target.id === "endTime") {
            setEndTime(e.target.value)
        }
    }

    const handleStep = (e) => {
        if (e.target.id === "startStep") {
            setStartStep(e.target.value)
        }
        else if (e.target.id === "endStep") {
            setEndStep(e.target.value)
        }
    }


    return (
        <Card className="flex flex-col m-3 gap-5 px-5 py-5">
            <Label htmlFor="" className="font-bold text-[20px]">조회</Label>
            <div className="grid grid-cols-10 gap-5">
                <div className="col-span-3 flex flex-col gap-2 h-[200px]">
                    <Button variant="outline" className="h-full flex-col gap-1">
                        <TimeIcon />
                        <p>시간대로 조회</p>
                    </Button>
                    <Button variant="outline" className="h-full flex-col gap-1">
                        <StepIcon />
                        <p>스텝으로 조회</p>
                    </Button>
                </div>
                <div className="col-span-7 flex flex-col gap-2 h-[200px]">
                    <div className="h-full w-full flex flex-col gap-2 justify-center">
                        <div className="flex flex-row gap-3 items-center">
                            <p>
                                시작 구간 :
                            </p>
                            <Popover>
                                <PopoverTrigger asChild>
                                    <Button
                                        variant={"outline"}
                                        className={cn(
                                            "w-[180px] justify-start text-left font-normal",
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
                        </div>
                        <div className="flex flex-row gap-3 items-center">
                            <p>
                                종료 구간 :
                            </p>
                            <Popover>
                                <PopoverTrigger asChild>
                                    <Button
                                        variant={"outline"}
                                        className={cn(
                                            "w-[180px] justify-start text-left font-normal",
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
                        </div>

                    </div>
                    <div className="h-full flex flex-col gap-2 justify-center">
                        <div className="flex flex-row gap-3">
                            <div>
                                <Label>시작 스텝</Label>
                                <Input id="startStep" onChange={handleStep} />
                            </div>
                            <div>
                                <Label>종료 스텝</Label>
                                <Input id="endStep" onChange={handleStep} />
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <div className="ml-auto">
                <Button onClick={() => {

                    console.log(startStep);
                    console.log(endStep);
                    console.log()
                }}>조회</Button>
            </div>

            {/* <div className="col-span-2 grid w-full items-center gap-1.5">
                <Label htmlFor="facility">임의 시간</Label>
                <div className="flex flex-col">
                    <Popover>
                        <PopoverTrigger asChild>
                            <Button
                                variant={"outline"}
                                className={cn(
                                    "w-[180px] justify-start text-left font-normal",
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
                    <Popover>
                        <PopoverTrigger asChild>
                            <Button
                                variant={"outline"}
                                className={cn(
                                    "w-[180px] justify-start text-left font-normal",
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

                </div>

            </div>
            <div className="col-span-2 grid w-full items-center gap-1.5">
                <Label htmlFor="facility">스텝 구간</Label>
                <div className="flex flex-row">
                    <Select onValueChange={setFacility}>
                        <SelectTrigger className="w-full self-center">
                            <SelectValue placeholder="시작 스텝" />
                        </SelectTrigger>
                        <SelectContent>
                            {Object.keys(facilityList).map(facility => (
                                <SelectItem key={facility} value={facility} >{facility}</SelectItem>
                            ))}
                        </SelectContent>
                    </Select>
                    ~
                    <Select onValueChange={setFacility}>
                        <SelectTrigger className="w-full self-center">
                            <SelectValue placeholder="종료 스텝" />
                        </SelectTrigger>
                        <SelectContent>
                            {Object.keys(facilityList).map(facility => (
                                <SelectItem key={facility} value={facility} >{facility}</SelectItem>
                            ))}
                        </SelectContent>
                    </Select>
                </div>
            </div>
            <div className="ml-auto">
                <Button onClick={() => { }}>조회</Button>
            </div> */}
        </Card>
    )
}

export default GetGraph;