import {
    Select,
    SelectContent,
    SelectItem,
    SelectTrigger,
    SelectValue,
} from "@/components/base/select";
import { ScrollArea } from "@/components/base/scroll-area";
import { Card } from "@/components/base/card";
import { Label } from "@/components/base/label";
import { useFacilityStore } from "@/stores/Facility";
import { useTargetLifeStore } from "@/stores/Targetlife";
import { Button } from "@/components/base/button";
import { ListOrdered as StepIcon, Clock as TimeIcon } from "lucide-react";
import { useQueryTypeStore, QueryType, useQueryDateTimeStore, useQueryLifeCntStore } from "@/stores/QueryCondition";
import TimeSelect from "@/components/common/TimeSelect";
import { useEffect, useState } from "react";
import useHandleQueryTgLife from "@/hooks/useHandleQueryTgLife";
import LifeCntSelect from "@/components/common/LifeCntSelect";


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
                <Button id="step" variant="outline" className="h-full flex-col gap-1" onClick={() => setQueryType('lifeCnt')}
                    style={buttonStyle('lifeCnt')}>
                    <StepIcon />
                    <p>카운트로 조회</p>
                </Button>
            </div>
        </div>
    )
}




function FacilitySelect() {
    const { facilityList } = useFacilityStore();
    const { selectedFacility, setSelectedFacility } = useTargetLifeStore();
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


function TgLifeNumSelect() {

    const { setSelectedTgLifeNum } = useTargetLifeStore();

    const lifeNum = ["1", "2", "4", "5"]

    return (
        <div className="col-span-3 m-auto gap-1.5 w-full">
            <Label>LifeNum 선택</Label>
            <Select onValueChange={setSelectedTgLifeNum}>
                <SelectTrigger className="self-center">
                    <SelectValue placeholder="LifeNum 선택" />
                </SelectTrigger>
                <SelectContent>
                    <ScrollArea className="max-h-[400px]">
                        {lifeNum.map((num) => <SelectItem key={num} value={num}>{num}</SelectItem>)}
                    </ScrollArea>
                </SelectContent>
            </Select>
        </div >
    )
}




function QueryInput() {
    const { queryType } = useQueryTypeStore();
    if (queryType === 'time') return <TimeSelect />
    else if (queryType === 'lifeCnt') return <LifeCntSelect />
}

function QueryTargetLifeButton() {

    const [isButtonEnabled, setIsButtonEnabled] = useState(false);
    const { selectedFacility, selectedTgLifeNum } = useTargetLifeStore();
    const { queryType } = useQueryTypeStore();
    const { timeValid } = useQueryDateTimeStore();
    const { lifeCntValid } = useQueryLifeCntStore();
    const handleQueryTgLife = useHandleQueryTgLife();

    // 시간 및 스텝 선택 유효성 검사 및 조회 버튼 활성화
    useEffect(() => {
        if (!selectedFacility) setIsButtonEnabled(false)
        else if (!selectedTgLifeNum) setIsButtonEnabled(false)
        else {
            if (queryType === 'time') {
                timeValid ? setIsButtonEnabled(true) : setIsButtonEnabled(false)
            }

            else if (queryType === 'lifeCnt') {
                lifeCntValid ? setIsButtonEnabled(true) : setIsButtonEnabled(false)
            }
        }
    }, [selectedFacility, selectedTgLifeNum, queryType, timeValid, lifeCntValid])


    return (
        <Button disabled={!isButtonEnabled} onClick={handleQueryTgLife}>
            조회
        </Button>
    )
}

export default function QueryTypeSection() {

    return (
        <Card className="flex flex-col gap-5 p-5">
            <Label className="font-bold text-[20px]">조회 조건 선택</Label>
            <QueryTypeButton />
            <div className="flex flex-row gap-5">
                <FacilitySelect />
                <TgLifeNumSelect />
            </div>
            <QueryInput />
            <div className="ml-auto">
                <QueryTargetLifeButton />
            </div>
        </Card>
    )
}