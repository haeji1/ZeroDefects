
import { Card } from "@/components/base/card";
import { ListOrdered as StepIcon, Clock as TimeIcon } from "lucide-react";
import {
    Select,
    SelectContent,
    SelectItem,
    SelectTrigger,
    SelectValue,
} from "@/components/base/select";
import { ScrollArea } from "@/components/base/scroll-area";
import { Button } from "@/components/base/button";
import { useEffect, useState } from "react";
import { useGraphDataStore } from "@/stores/GraphData";
import { useSelectedRowStore, useBookmarkStore } from "@/stores/Bookmark";
import { Label } from "@/components/base/label";
import { getGraph } from "@/apis/api/api";
import { useQueryDateTimeStore, useQueryStepStore, useQueryTypeStore, QueryType } from "@/stores/QueryCondition";
import StepSelect from "@/components/domain/dashboard/StepSelect";
import TimeSelect from "@/components/domain/dashboard/TimeSelect";
import { useFacilityStore } from "@/stores/Facility";
function GetGraph() {

    const [selectedFacility, setSelectedFacility] = useState<string>("")
    const [isButtonEnabled, setIsButtonEnabled] = useState(false);
    const { queryStartDate, queryEndDate, timeValid } = useQueryDateTimeStore();
    const { queryStartStep, queryEndStep, stepValid } = useQueryStepStore();
    const { queryType, setQueryType } = useQueryTypeStore();
    const { bookmark } = useBookmarkStore();
    const { selectedRow } = useSelectedRowStore();
    const { setIsFetching, setGraphData } = useGraphDataStore()

    const { facilityList, updateFacilityList } = useFacilityStore();
    const changeFacility = (value: string) => {
        // setSelectedParameter(null); // 기존 선택되었던 파라미터 값은 이전 설비이었을 때 선택되었던 파라미터이므로 상태를 null 값으로 초기화
        setSelectedFacility(value); // 선택된 설비의 정보를 변경
    }
    // 쿼리 타입 버튼 디자인 변경
    const buttonStyle = (buttonName: QueryType) => ({
        border: queryType === buttonName ? '1px solid black' : '',
    });


    // 시간 및 스텝 선택 유효성 검사 및 조회 버튼 활성화
    useEffect(() => {
        if (Object.keys(selectedRow).length === 0) setIsButtonEnabled(false)
        else {
            if (queryType === 'time') {
                timeValid ? setIsButtonEnabled(true) : setIsButtonEnabled(false)
            }

            else if (queryType === 'step') {
                stepValid ? setIsButtonEnabled(true) : setIsButtonEnabled(false)
            }
        }
    }, [selectedRow, queryType, timeValid, stepValid])




    return (
        <Card className="flex flex-col gap-5 px-5 py-5">

            {/* <Label htmlFor="" className="font-bold text-[20px]">조회</Label> */}
            <div className="grid grid-cols-10 gap-5">
                <div className="col-span-3 flex flex-row gap-2 h-[50px]">

                    <div className="col-span-2 grid w-full items-center gap-1.5">
                        <Label>설비 선택</Label>
                        <Select value={selectedFacility} onValueChange={changeFacility} >
                            <SelectTrigger className="w-full self-center">
                                <SelectValue placeholder="설비 선택" />
                            </SelectTrigger>
                            <SelectContent>
                                <ScrollArea className="max-h-[400px] w-full">
                                    {Object.keys(facilityList).map(facility => <SelectItem key={facility} value={facility} >{facility}</SelectItem>)}
                                </ScrollArea>
                            </SelectContent>
                        </Select>
                    </div>


                    <Button id="time" variant="outline" className="h-full flex-col gap-1" onClick={() => setQueryType('time')}
                        style={buttonStyle('time')}>
                        <TimeIcon />
                        <p>시간대로 조회</p>
                        <TimeSelect />
                    </Button>
                    <Button id="step" variant="outline" className="h-full flex-col gap-1" onClick={() => setQueryType('step')}
                        style={buttonStyle('step')}>
                        <StepIcon />
                        <p>스텝으로 조회</p>
                        <StepSelect />
                    </Button>
                </div>
                <div className="col-span-7 flex flex-row gap-2 h-[100px]">
                </div>
            </div>
            <div className="ml-auto">
                <Button disabled={!isButtonEnabled} >조회</Button>
            </div>
        </Card>
    )
}

export default GetGraph;