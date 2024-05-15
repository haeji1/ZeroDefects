import { useState } from "react";
import { Button } from "@/components/base/button";
import { Popover, PopoverContent, PopoverTrigger } from "@/components/base/popover";
import { Input } from "@/components/base/input";
import { Calendar } from "@/components/base/calendar";
import { Calendar as CalendarIcon } from "lucide-react";
import { format } from "date-fns"
import { ko } from "date-fns/locale"
import { cn } from "@/lib/utils";
import { useQueryDateTimeStore, useQueryButtonStore } from "@/stores/QueryCondition";

export default function TimeSelect() {

    const [startDateOpen, setStartDateOpen] = useState(false);
    const [endDateOpen, setEndDateOpen] = useState(false);

    const {
        queryStartDate, setQueryStartDate, queryEndDate, setQueryEndDate,
        setQueryStartTime, setQueryEndTime
    } = useQueryDateTimeStore();

    const { queryTypeButton } = useQueryButtonStore();

    // 시작 및 종료 시간을 설정하는 Input 핸들러
    const handleTime = (e: React.ChangeEvent<HTMLInputElement>) => {
        if (e.target.id === "startTime") {
            setQueryStartTime(e.target.value)
        }
        else if (e.target.id === "endTime") {
            setQueryEndTime(e.target.value)
        }
    }

    return (
        <div className="h-full w-full flex flex-col gap-2 justify-center">
            <div className="flex flex-row gap-3 items-center">
                <p>시작 :</p>
                <Popover open={startDateOpen}>
                    <PopoverTrigger asChild>
                        <Button
                            variant={"outline"}
                            className={cn(
                                "w-[180px] justify-start text-left font-normal",
                                !queryStartDate && "text-muted-foreground"
                            )}
                            onClick={() => setStartDateOpen(true)}
                            disabled={queryTypeButton !== "time"}
                        >
                            <CalendarIcon className="mr-2 h-4 w-4" />
                            {queryStartDate ? format(queryStartDate, "yyyy년 MM월 dd일") : <span>시작 날짜</span>}
                        </Button>
                    </PopoverTrigger>
                    <PopoverContent
                        className="w-auto p-0"
                        onPointerDownOutside={() => setStartDateOpen(false)}>
                        <Calendar
                            mode="single"
                            defaultMonth={queryStartDate}
                            selected={queryStartDate}
                            onSelect={(date) => { if (date) setQueryStartDate(date); setStartDateOpen(false); }}
                            locale={ko}
                            initialFocus
                        />
                    </PopoverContent>
                </Popover>
                <Input className="w-[130px]" type={"time"} id="startTime" onChange={handleTime} disabled={queryTypeButton !== "time"} />
            </div>


            <div className="flex flex-row gap-3 items-center">
                <p>종료 :</p>
                <Popover open={endDateOpen}>
                    <PopoverTrigger asChild>
                        <Button
                            variant={"outline"}
                            className={cn(
                                "w-[180px] justify-start text-left font-normal",
                                !queryEndDate && "text-muted-foreground"
                            )}
                            onClick={() => setEndDateOpen(true)}
                            disabled={queryTypeButton !== "time"}
                        >
                            <CalendarIcon className="mr-2 h-4 w-4" />
                            {queryEndDate ? format(queryEndDate, "yyyy년 MM월 dd일") : <span>종료 날짜</span>}
                        </Button>
                    </PopoverTrigger>
                    <PopoverContent
                        className="w-auto p-0"
                        onPointerDownOutside={() => setEndDateOpen(false)}>
                        <Calendar
                            mode="single"
                            defaultMonth={queryEndDate}
                            selected={queryEndDate}
                            onSelect={(date) => { if (date) setQueryEndDate(date); setEndDateOpen(false) }}
                            locale={ko}
                            initialFocus
                        />
                    </PopoverContent>
                </Popover>
                <Input className="w-[130px]" type="time" id="endTime" onChange={handleTime} disabled={queryTypeButton !== "time"} />
            </div>
        </div>
    )
};