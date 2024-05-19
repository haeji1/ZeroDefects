import {
    Select,
    SelectContent,
    SelectItem,
    SelectTrigger,
    SelectValue,
} from "@/components/base/select";
import { Card } from "@/components/base/card";
import { Label } from "@/components/base/label";
import { Button } from "@/components/base/button";
import { ScrollArea } from "@/components/base/scroll-area";
import { ListOrdered as StepIcon, Clock as TimeIcon } from "lucide-react";
import { Batch, useBatchStore, useFacilityStore } from "@/stores/Facility";
import { useCorrelationStore } from "@/stores/Correlation";
import { useQueryTypeStore, QueryType, useQueryDateTimeStore, useQueryStepStore } from "@/stores/QueryCondition";
import CorrelationTable from "@/components/domain/correlation/CorrelationTable";
import StepSelect from "@/components/common/StepSelect";
import TimeSelect from "@/components/common/TimeSelect";
import useHandleQueryCorrelation from "@/hooks/useHandleQueryCorrelation";
import useDidMountEffect from "@/hooks/useDidMountEffect";
import { useEffect, useState } from "react";
import { getBatches } from "@/api/api";
import { AxiosResponse } from "axios";

function QueryTypeButton() {
    const { queryType, setQueryType } = useQueryTypeStore();
    const buttonStyle = (buttonName: QueryType) => ({
        border: queryType === buttonName ? '1px solid black' : '',
    });
    return (
        <div className="m-auto max-w-[200px]">
            <div className="flex flex-rows gap-2">
                <Button id="time" variant="outline" className="h-full flex-col gap-1" onClick={() => setQueryType('time')}
                    style={buttonStyle('time')} >
                    <TimeIcon />
                    <p>시간대로 조회</p>
                </Button>
                <Button id="step" variant="outline" className="h-full flex-col gap-1" onClick={() => setQueryType('step')}
                    style={buttonStyle('step')}>
                    <StepIcon />
                    <p>스텝으로 조회</p>
                </Button>
            </div>
        </div>
    )
}

function FacilitySelect() {
    const { facilityList } = useFacilityStore();
    const { selectedFacility, setSelectedFacility } = useCorrelationStore();
    return (
        <div className="col-span-2 m-auto gap-1.5 w-full">
            <Label>설비 선택</Label>
            <Select value={selectedFacility} onValueChange={setSelectedFacility} >
                <SelectTrigger className="self-center">
                    <SelectValue placeholder="설비 선택" />
                </SelectTrigger>
                <SelectContent>
                    <ScrollArea className="max-h-[400px]">
                        {Object.keys(facilityList).map(facility => <SelectItem key={facility} value={facility} >{facility}</SelectItem>)}
                    </ScrollArea>
                </SelectContent>
            </Select>
        </div >
    )
}

function BatchSelect() {

    const { selectedFacility, setSelectedBatch } = useCorrelationStore();
    const [batches, setBatches] = useState<Batch[]>();
    const { queryType } = useQueryTypeStore();
    const { addBatch, batchList } = useBatchStore();

    useDidMountEffect(async () => {
        if (!batchList[selectedFacility]) {
            const res: AxiosResponse<any, any> | undefined = await getBatches(selectedFacility); // 추가하고자 하는 설비의 최신 배치 정보 가져오기
            setBatches(res?.data.batches)
            addBatch(selectedFacility, res?.data.batches);
        }
        else setBatches(batchList[selectedFacility])

    }, [selectedFacility])


    const handleBatchChange = (batchStartTime: string) => {
        const selectedBatch = batches!.find((batch) => batch.batchStartTime === batchStartTime);
        setSelectedBatch(selectedBatch!);
    }

    return (
        <div className="col-span-3 m-auto gap-1.5 w-full">
            <Label>배치 시작 시간 선택</Label>
            <Select onValueChange={handleBatchChange} disabled={queryType !== 'step'}>
                <SelectTrigger className="self-center">
                    <SelectValue placeholder="배치 선택" />
                </SelectTrigger>
                <SelectContent>
                    <ScrollArea className="max-h-[400px]">
                        {batches?.map((batch) =>
                            <SelectItem
                                key={batch.batchStartTime}
                                value={batch.batchStartTime}
                            >
                                {batch.batchStartTime}
                            </SelectItem>)}
                    </ScrollArea>
                </SelectContent>
            </Select>
        </div >
    )
}

function QueryInput() {
    const { queryType } = useQueryTypeStore();
    if (queryType === 'time') return <TimeSelect />
    else if (queryType === 'step') return <StepSelect />
}


function QueryCorrelationButton() {

    const [isButtonEnabled, setIsButtonEnabled] = useState(false);
    const { selectedParameters } = useCorrelationStore();
    const { queryType } = useQueryTypeStore();
    const { timeValid } = useQueryDateTimeStore();
    const { stepValid } = useQueryStepStore();
    const handleQueryCorrelation = useHandleQueryCorrelation();

    // 시간 및 스텝 선택 유효성 검사 및 조회 버튼 활성화
    useEffect(() => {
        if (selectedParameters.length === 0) setIsButtonEnabled(false)
        else if (selectedParameters.length > 8) setIsButtonEnabled(false)
        else {
            if (queryType === 'time') {
                timeValid ? setIsButtonEnabled(true) : setIsButtonEnabled(false)
            }

            else if (queryType === 'step') {
                stepValid ? setIsButtonEnabled(true) : setIsButtonEnabled(false)
            }
        }
    }, [selectedParameters, queryType, timeValid, stepValid])


    return (
        <Button disabled={!isButtonEnabled} onClick={handleQueryCorrelation}>
            조회
        </Button>
    )
}


function QueryTypeSection() {

    return (
        <Card className="flex flex-col gap-5 p-5">
            <Label className="font-bold text-[20px]">조회 조건 선택</Label>
            <QueryTypeButton />
            <div className="grid grid-cols-5 gap-5">
                <FacilitySelect />
                <BatchSelect />
            </div>
            <CorrelationTable />
            <QueryInput />
            <div className="ml-auto">
                <QueryCorrelationButton />
            </div>
        </Card>
    )
}

export default QueryTypeSection;