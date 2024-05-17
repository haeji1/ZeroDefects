
import { Card } from "@/components/base/card";
import { ListOrdered as StepIcon, Clock as TimeIcon } from "lucide-react";
import { Button } from "@/components/base/button";
import { useEffect, useState } from "react";
import { useGraphDataStore } from "@/stores/GraphData";
import { useSelectedRowStore, useBookmarkStore } from "@/stores/Bookmark";
import { Label } from "@/components/base/label";
import { getGraph } from "@/apis/api/api";
import { useQueryDateTimeStore, useQueryStepStore, useQueryTypeStore, QueryType } from "@/stores/QueryCondition";
import StepSelect from "@/components/domain/dashboard/StepSelect";
import TimeSelect from "@/components/domain/dashboard/TimeSelect";
function GetGraph() {

    const [isButtonEnabled, setIsButtonEnabled] = useState(false);
    const { queryStartDate, queryEndDate, timeValid } = useQueryDateTimeStore();
    const { queryStartStep, queryEndStep, stepValid } = useQueryStepStore();
    const { queryType, setQueryType } = useQueryTypeStore();
    const { bookmark } = useBookmarkStore();
    const { selectedRow } = useSelectedRowStore();
    const { setIsFetching, setGraphData } = useGraphDataStore()


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


    const handleGetGraph = async () => {

        let queryCondition;

        if (queryType === 'time') {
            queryCondition = {
                startTime: queryStartDate.toISOString(),
                endTime: queryEndDate.toISOString(),
                step: null,
            }
        }
        else if (queryType === 'step') {
            const step: number[] = [];
            for (let i = queryStartStep; i <= queryEndStep; i++) {
                step.push(i);
            }
            queryCondition = {
                startTime: null,
                endTime: null,
                step: step,
            }
        }
        const data = {
            queryType: queryType,
            queryCondition: queryCondition,
            queryData: Object.keys(selectedRow).map((idx) => {
                const val = bookmark.find((obj) => obj.id === Number(idx));
                if (!val) return
                return {
                    facility: val.facility,
                    parameter: val.parameter,
                    batchName: queryType === 'time' ? null : val.selectedBatchName,
                }
            })
        }

        setIsFetching(true)
        const res = await getGraph(data)
        if (res) {
            setGraphData(res.data);
            setIsFetching(false)
        }
        else {
            setIsFetching(false);
        }
    }

    return (
        <Card className="flex flex-col gap-5 px-5 py-5">
            <Label htmlFor="" className="font-bold text-[20px]">조회</Label>
            <div className="grid grid-cols-10 gap-5">
                <div className="col-span-3 flex flex-col gap-2 h-[200px]">
                    <Button id="time" variant="outline" className="h-full flex-col gap-1" onClick={() => setQueryType('time')}
                        style={buttonStyle('time')}>
                        <TimeIcon />
                        <p>시간대로 조회</p>
                    </Button>
                    <Button id="step" variant="outline" className="h-full flex-col gap-1" onClick={() => setQueryType('step')}
                        style={buttonStyle('step')}>
                        <StepIcon />
                        <p>스텝으로 조회</p>
                    </Button>
                </div>
                <div className="col-span-7 flex flex-col gap-2 h-[200px]">
                    <TimeSelect />
                    <StepSelect />
                </div>
            </div>
            <div className="ml-auto">
                <Button disabled={!isButtonEnabled} onClick={handleGetGraph}>조회</Button>
            </div>
        </Card>
    )
}

export default GetGraph;