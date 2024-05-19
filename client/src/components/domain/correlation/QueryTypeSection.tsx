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
import { useFacilityStore } from "@/stores/Facility";
import { useCorrelationStore } from "@/stores/Correlation";
import { useQueryTypeStore, QueryType } from "@/stores/QueryCondition";
import CorrelationTable from "@/components/domain/correlation/CorrelationTable";
import StepSelect from "./StepSelect";
import TimeSelect from "../dashboard/TimeSelect";
import useHandleQueryCorrelation from "@/hooks/useHandleQueryCorrelation";

function QueryTypeButton() {
    const { queryType, setQueryType } = useQueryTypeStore();
    const buttonStyle = (buttonName: QueryType) => ({
        border: queryType === buttonName ? '1px solid black' : '',
    });
    return (
        <div className="m-auto max-w-[200px]">
            <Label>조회 타입</Label>
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
        <div className="m-auto gap-1.5 max-w-[200px]">
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

function QueryInput() {
    const { queryType } = useQueryTypeStore();
    if (queryType === 'time') return <TimeSelect />
    else if (queryType === 'step') return <StepSelect />
}



function QueryTypeSection() {

    const handleQueryCorrelation = useHandleQueryCorrelation();

    return (
        <Card className="p-5">
            <QueryTypeButton />
            <FacilitySelect />
            <CorrelationTable />
            <QueryInput />
            <div className="ml-auto">
                <Button
                    // disabled={!isButtonEnabled} 
                    onClick={handleQueryCorrelation}
                >조회</Button>
            </div>
        </Card>
    )
}

export default QueryTypeSection;