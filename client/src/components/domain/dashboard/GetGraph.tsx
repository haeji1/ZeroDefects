
import { Card } from "@/components/base/card";
import { ListOrdered as StepIcon, Clock as TimeIcon } from "lucide-react";
import { Button } from "@/components/base/button";
import { useEffect, useState } from "react";
import { useGraphDataStore } from "@/stores/GraphData";
import { useSelectedRowStore, useBookmarkStore } from "@/stores/Bookmark";
import { Label } from "@/components/base/label";
import { getGraph } from "@/apis/api/api";
import { useQueryDateTimeStore, useQueryStepStore, useQueryButtonStore, QueryType } from "@/stores/QueryCondition";
import StepSelect from "@/components/domain/dashboard/StepSelect";
import TimeSelect from "@/components/domain/dashboard/TimeSelect";
function GetGraph() {
    // 그래프 조회에 필요한 인자들

    const { queryTypeButton, setQueryTypeButton } = useQueryButtonStore();

    const {
        queryStartDate, setQueryStartDate,
        queryStartTime, setQueryStartTime,
        queryEndDate, setQueryEndDate,
        queryEndTime, setQueryEndTime
    } = useQueryDateTimeStore();

    const {
        queryStartStep, setQueryStartStep,
        queryEndStep, setQueryEndStep,
    } = useQueryStepStore();

    const [isButtonEnabled, setIsButtonEnabled] = useState(false);
    const { bookmark } = useBookmarkStore();
    const { selectedRow } = useSelectedRowStore();
    const { setIsFetching, setGraphData } = useGraphDataStore()
    const [startStep, setStartStep] = useState<undefined | number>();
    const [endStep, setEndStep] = useState<undefined | number>();
    const [selectedButton, setSelectedButton] = useState('time');
    const [isTimeButtonSelected, setTimeButtonSelected] = useState(true);


    const buttonStyle = (buttonName: QueryType) => ({
        border: queryTypeButton === buttonName ? '1px solid black' : '',
    });


    const handleGetGraph = async () => {

        let queryCondition;

        if (selectedButton === 'time') {
            const startParts = queryStartTime.split(":");
            const endParts = queryEndTime.split(":");
            queryCondition = {
                startTime: new Date(queryStartDate.getFullYear(), queryStartDate.getMonth(), queryStartDate.getDate(), startParts[0], startParts[1]).toISOString(),
                endTime: new Date(queryEndDate.getFullYear(), queryEndDate.getMonth(), queryEndDate.getDate(), endParts[0], endParts[1]).toISOString(),
                step: null,
            }
        }
        else if (selectedButton === 'step' && startStep && endStep) {
            const step: number[] = [];
            for (let i: number = startStep; i <= endStep; i++) {
                step.push(i);
            }
            queryCondition = {
                startTime: null,
                endTime: null,
                step: step,
            }
        }
        const data = {
            queryType: selectedButton,
            queryCondition: queryCondition,
            queryData: Object.keys(selectedRow).map((idx) => {
                console.log(idx);
                const val = bookmark.find((obj) => obj.id == idx);
                console.log(val)
                return {
                    facility: val.facility,
                    parameter: val.parameter,
                    batchName: selectedButton === 'time' ? null : val.selectedBatchName,
                }
            })
        }

        console.log(data);

        setIsFetching(true)
        const res = await getGraph(data)
        console.log(res);
        setGraphData(res?.data);
        setIsFetching(false)
    }




    // useEffect(() => {
    //     // 시간으로 
    //     if (selectedButton === 'time') {
    //         queryStartDate && startTime && endDate && endTime ? setIsButtonEnabled(true) : setIsButtonEnabled(false)
    //     }
    //     else if (selectedButton === 'step') {
    //         startStep && endStep ? setIsButtonEnabled(true) : setIsButtonEnabled(false)
    //     }
    // }, [queryStartDate, startTime, endDate, endTime, selectedButton, startStep, endStep])





    return (
        <Card className="flex flex-col gap-5 px-5 py-5">
            <Label htmlFor="" className="font-bold text-[20px]">조회</Label>
            <div className="grid grid-cols-10 gap-5">
                <div className="col-span-3 flex flex-col gap-2 h-[200px]">
                    <Button id="time" variant="outline" className="h-full flex-col gap-1" onClick={() => setQueryTypeButton('time')}
                        style={buttonStyle('time')}>
                        <TimeIcon />
                        <p>시간대로 조회</p>
                    </Button>
                    <Button id="step" variant="outline" className="h-full flex-col gap-1" onClick={() => setQueryTypeButton('step')}
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