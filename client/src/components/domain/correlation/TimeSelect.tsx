import { useEffect, useState } from "react";
import { Button } from "@/components/base/button";
import { Popover, PopoverContent, PopoverTrigger } from "@/components/base/popover";
import { Input } from "@/components/base/input";
import { Label } from "@/components/base/label";
import { Calendar } from "@/components/base/calendar";
import { Calendar as CalendarIcon } from "lucide-react";
import { format } from "date-fns"
import { ko } from "date-fns/locale"
import { cn } from "@/lib/utils";
import { useQueryDateTimeStore, useQueryTypeStore } from "@/stores/QueryCondition";

export default function TimeSelect() {

    // 캘린더 팝오버 상태 저장
    const [startDateOpen, setStartDateOpen] = useState(false);
    const [endDateOpen, setEndDateOpen] = useState(false);

    // 선택한 날짜 및 시간 각각 저장
    const [queryStartDay, setQueryStartDay] = useState<Date>(new Date());
    const [queryEndDay, setQueryEndDay] = useState<Date>(new Date());
    const [queryStartTime, setQueryStartTime] = useState<string>("00:00");
    const [queryEndTime, setQueryEndTime] = useState<string>("00:00");

    const { queryType } = useQueryTypeStore();
    const { queryStartDate, setQueryStartDate, queryEndDate, setQueryEndDate, setTimeValid } = useQueryDateTimeStore();


    // 시/분 을 설정하는 Input 핸들러
    const handleTime = (e: React.ChangeEvent<HTMLInputElement>) => {
        if (e.target.id === "startTime") {
            setQueryStartTime(e.target.value)
        }
        else if (e.target.id === "endTime") {
            setQueryEndTime(e.target.value)
        }
    }

    // 선택된 일자와 선택된 시간을 조합하여 전역 상태 저장
    useEffect(() => {
        const [startHours, startMinutes] = queryStartTime.split(':').map(Number);
        const date = new Date(queryStartDay);
        date.setHours(startHours, startMinutes);
        setQueryStartDate(date);
    }, [queryStartDay, queryStartTime])

    useEffect(() => {
        const [endHours, endMinutes] = queryEndTime.split(':').map(Number);
        const date = new Date(queryEndDay);
        date.setHours(endHours, endMinutes);
        setQueryEndDate(date);
    }, [queryEndDay, queryEndTime])

    // 시작 시간이 종료 시간보다 일렀을 때만 유효성 통과
    useEffect(() => {
        if (queryStartDate < queryEndDate) setTimeValid(true);
        else setTimeValid(false);
    }, [queryStartDate, queryEndDate])


    return (
        <div className={`h-full w-full flex flex-row gap-2 justify-center`}>
            <div className="flex flex-row gap-3 items-center">
                <Label>시작 : </Label>
                <Popover open={startDateOpen}>
                    <PopoverTrigger asChild>
                        <Button
                            variant={"outline"}
                            className={cn(
                                "w-[180px] justify-start text-left font-normal",
                                !queryStartDay && "text-muted-foreground"
                            )}
                            onClick={() => setStartDateOpen(true)}
                            disabled={queryType !== "time"}
                        >
                            <CalendarIcon className="mr-2 h-4 w-4" />
                            {queryStartDay ? format(queryStartDay, "yyyy년 MM월 dd일") : <span>시작 날짜</span>}
                        </Button>
                    </PopoverTrigger>
                    <PopoverContent
                        className="w-auto p-0"
                        onPointerDownOutside={() => setStartDateOpen(false)}>
                        <Calendar
                            mode="single"
                            defaultMonth={queryStartDay}
                            selected={queryStartDay}
                            onSelect={(date) => { if (date) setQueryStartDay(date); setStartDateOpen(false); }}
                            locale={ko}
                            initialFocus
                        />
                    </PopoverContent>
                </Popover>
                <Input className="w-[130px]" type={"time"} id="startTime" onChange={handleTime} disabled={queryType !== "time"} />
            </div>


            <div className="flex flex-row gap-3 items-center">
                <Label>종료 : </Label>
                <Popover open={endDateOpen}>
                    <PopoverTrigger asChild>
                        <Button
                            variant={"outline"}
                            className={cn(
                                "w-[180px] justify-start text-left font-normal",
                                !queryEndDay && "text-muted-foreground"
                            )}
                            onClick={() => setEndDateOpen(true)}
                            disabled={queryType !== "time"}
                        >
                            <CalendarIcon className="mr-2 h-4 w-4" />
                            {queryEndDay ? format(queryEndDay, "yyyy년 MM월 dd일") : <span>종료 날짜</span>}
                        </Button>
                    </PopoverTrigger>
                    <PopoverContent
                        className="w-auto p-0"
                        onPointerDownOutside={() => setEndDateOpen(false)}>
                        <Calendar
                            mode="single"
                            defaultMonth={queryEndDay}
                            selected={queryEndDay}
                            onSelect={(date) => { if (date) setQueryEndDay(date); setEndDateOpen(false) }}
                            locale={ko}
                            initialFocus
                        />
                    </PopoverContent>
                </Popover>
                <Input className="w-[130px]" type="time" id="endTime" onChange={handleTime} disabled={queryType !== "time"} />
            </div>
        </div>
    )
};