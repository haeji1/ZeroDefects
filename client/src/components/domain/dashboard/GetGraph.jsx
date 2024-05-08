
import { Card } from "@/components/base/card";
import { format } from "date-fns"
import { ko } from "date-fns/locale"
import { Calendar as CalendarIcon, ListOrdered as StepIcon, Clock as TimeIcon } from "lucide-react";
import { cn } from "@/lib/utils";
import { Button } from "@/components/base/button";
import { Popover, PopoverContent, PopoverTrigger } from "@/components/base/popover";
import { useEffect, useState } from "react";
import { Calendar } from "@/components/base/calendar";
import { Input } from "@/components/base/input";
import { useGraphDataStore } from "@/stores/GraphData";
import { useSelectedBookmarkStore } from "@/stores/Bookmark";
import { Label } from "@/components/base/label";
import { getGraph } from "@/apis/api/api";

function GetGraph() {
    // 그래프 조회에 필요한 인자들
    const [startDate, setStartDate] = useState()
    const [startTime, setStartTime] = useState()
    const [endDate, setEndDate] = useState()
    const [endTime, setEndTime] = useState()
    const [startStep, setStartStep] = useState();
    const [endStep, setEndStep] = useState();
    const [isButtonEnabled, setIsButtonEnabled] = useState(false);
    const { selectedBookmark } = useSelectedBookmarkStore();
    const { setIsFetching, setGraphData } = useGraphDataStore()

    const [selectedButton, setSelectedButton] = useState('time');


    const [isTimeButtonSelected, setTimeButtonSelected] = useState(true);


    const handleButtonClick = (id) => {
        setSelectedButton(id)
        setTimeButtonSelected(id === 'time')
    };

    const buttonStyle = (buttonName) => ({
        border: selectedButton === buttonName ? '1px solid black' : '',
    });


    const handleGetGraph = async () => {

        let queryCondition;

        if (selectedButton === 'time') {
            const startParts = startTime.split(":");
            const endParts = endTime.split(":");
            queryCondition = {
                startTime: new Date(startDate.getFullYear(), startDate.getMonth(), startDate.getDate(), startParts[0], startParts[1]).toISOString(),
                endTime: new Date(endDate.getFullYear(), endDate.getMonth(), endDate.getDate(), endParts[0], endParts[1]).toISOString(),
                step: null,
            }
        }
        else if (selectedButton === 'step') {
            const step = [];
            for (let i = startStep; i <= endStep; i++) {
                step.push(i);
            }
            queryCondition = {
                startTime: null,
                endTime: null,
                step: step,
            }
        }

        setIsFetching(true)
        const data = {
            queryType: selectedButton,
            queryCondition: queryCondition,
            queryData: selectedBookmark.map((val) => {
                console.log(val)
                return {
                    facility: val.facility,
                    parameter: val.parameter,
                    batchName: selectedButton === 'time' ? null : val.selectedBatchName,
                }
            })
        }
        const res = await getGraph(data)
        setGraphData(res.data);
        setIsFetching(false)
    }


    useEffect(() => {
        // 시간으로 
        if (selectedButton === 'time') {
            startDate && startTime && endDate && endTime ? setIsButtonEnabled(true) : setIsButtonEnabled(false)
        }
        else {
            startStep && endStep ? setIsButtonEnabled(true) : setIsButtonEnabled(false)
        }
    }, [startDate, startTime, endDate, endTime, selectedButton, startStep, endStep])



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
            setStartStep(Number(e.target.value))
        }
        else if (e.target.id === "endStep") {
            setEndStep(e.target.value)
        }
    }


    return (
        <Card className="flex flex-col gap-5 px-5 py-5">
            <Label htmlFor="" className="font-bold text-[20px]">조회</Label>
            <div className="grid grid-cols-10 gap-5">
                <div className="col-span-3 flex flex-col gap-2 h-[200px]">
                    <Button id="time" variant="outline" className="h-full flex-col gap-1" onClick={() => handleButtonClick('time')}
                        style={buttonStyle('time')}>
                        <TimeIcon />
                        <p>시간대로 조회</p>
                    </Button>
                    <Button id="step" variant="outline" className="h-full flex-col gap-1" onClick={() => handleButtonClick('step')}
                        style={buttonStyle('step')}>
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
                                        disabled={!isTimeButtonSelected}
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
                            <Input className="w-[130px]" type={"time"} id="startTime" onChange={handleTime} disabled={!isTimeButtonSelected} />
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
                                        disabled={!isTimeButtonSelected}
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
                            <Input className="w-[130px]" type="time" id="endTime" onChange={handleTime} disabled={!isTimeButtonSelected} />
                        </div>

                    </div>
                    <div className="h-full flex flex-col gap-2 justify-center">
                        <div className="flex flex-row gap-3">
                            <div>
                                <Label>시작 스텝</Label>
                                <Input id="startStep" type="number" onChange={handleStep} disabled={isTimeButtonSelected} />
                            </div>
                            <div>
                                <Label>종료 스텝</Label>
                                <Input id="endStep" type="number" onChange={handleStep} disabled={isTimeButtonSelected} />
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            <div className="ml-auto">
                <Button disabled={!isButtonEnabled} onClick={handleGetGraph}>조회</Button>
            </div>
        </Card>
    )
}

export default GetGraph;