import {
    Select,
    SelectContent,
    SelectItem,
    SelectTrigger,
    SelectValue,
} from "@/components/base/select";
import { Card } from "@/components/base/card";
import { format } from "date-fns"
import { Calendar as CalendarIcon } from "lucide-react";
import { cn } from "@/lib/utils";
import { Button } from "@/components/base/button";
import { Popover, PopoverContent, PopoverTrigger } from "@/components/base/popover";
import { useState } from "react";
import { Calendar } from "@/components/base/calendar";
import { Input } from "@/components/base/input";
import { Label } from "@/components/base/label";
import { useParameterStore } from "@/stores/ParameterList"
import { useGraphDataStore } from "@/stores/GraphData";

function SelectSection() {
    const [date, setDate] = useState()

    const [startDate, setStartDate] = useState()
    const [startTime, setStartTime] = useState()
    const [endDate, setEndDate] = useState()
    const [endTime, setEndTime] = useState()




    const [facility, setFacility] = useState()
    const [parameter, setParameter] = useState()
    const [times, setTimes] = useState()


    const facilityList = ["F1490", "F1491", "F1492"]


    const { graphData, parameterData, setGraphData, setParameterData } = useGraphDataStore()


    const { addParameter } = useParameterStore();

    return (
        <div>
            <Card className="h-[80px] mr-5 mb-5 items-center flex flex-row px-3 space-x-3">
                <Select>
                    <SelectTrigger className="w-[180px] self-center">
                        <SelectValue placeholder="설비명" />
                    </SelectTrigger>
                    <SelectContent>
                        {facilityList.map(facility => (
                            <SelectItem key={facility} value={facility}>{facility}</SelectItem>
                        ))}

                    </SelectContent>
                </Select>

                <Select>
                    <SelectTrigger className="w-[180px] self-center">
                        <SelectValue placeholder="파라미터 명" />
                    </SelectTrigger>
                    <SelectContent>
                        {parameterData.map((param) => (
                            <SelectItem key={param.index} value={param.index}>{param.index}</SelectItem>
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
                            {startDate ? format(startDate, "PPP") : <span>시작 날짜</span>}
                        </Button>
                    </PopoverTrigger>
                    <PopoverContent className="w-auto p-0">
                        <Calendar
                            mode="single"
                            selected={startDate}
                            onSelect={setStartDate}
                            initialFocus
                        />
                    </PopoverContent>
                </Popover>
                <Input className="w-[130px]" type={"time"} />
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
                            {endDate ? format(endDate, "PPP") : <span>종료 날짜</span>}
                        </Button>
                    </PopoverTrigger>
                    <PopoverContent className="w-auto p-0">
                        <Calendar
                            mode="single"
                            selected={endDate}
                            onSelect={setEndDate}
                            initialFocus
                        />
                    </PopoverContent>
                </Popover>
                <Input className="w-[130px]" type={"time"} />
                <Button>그래프 조회</Button>
                <Button
                // onClick={addParameter(
                //     {
                //         facility:facility,
                //         parameter:parameter,
                //     }
                // )}
                >
                    비교 목록 추가</Button>
                <div className=" max-w-sm items-center gap-1.5">
                    {/* <Input type="file" onChange={ } /> */}
                </div>
            </Card>

        </div>
    )
}

export default SelectSection;