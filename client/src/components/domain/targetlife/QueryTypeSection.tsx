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
import { useQueryTypeStore, useQueryDateTimeStore, useQueryLifeCntStore } from "@/stores/QueryCondition";
import { useEffect, useState } from "react";
import useHandleQueryTgLife from "@/hooks/useHandleQueryTgLife";
import { getTargetLifeCycle } from "@/api/api";
import { AxiosResponse } from "axios";
import TGLifeTable from "@/components/domain/targetlife/TGLifeTable";
import { useToast } from "@/hooks/use-toast";


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


function ParamSelect() {
    const { selectedParam, setSelectedParam } = useTargetLifeStore();

    const params = ["전압 V [V]", "전류 I [A]", "전력 Pwr [kW]"]

    return (
        <div className="col-span-2 m-auto gap-1.5 w-full">
            <Label>파라미터</Label>
            <Select value={selectedParam} onValueChange={setSelectedParam} >
                <SelectTrigger className="self-center">
                    <SelectValue placeholder="파라미터 선택" />
                </SelectTrigger>
                <SelectContent>
                    <ScrollArea className="max-h-[400px]">
                        {params.map((param) => <SelectItem key={param} value={param}>{param}</SelectItem>)}
                    </ScrollArea>
                </SelectContent>
            </Select>
        </div >
    )
}


function StatSelect() {
    const { selectedStat, setSelectedStat } = useTargetLifeStore();

    const stats = ["평균", "최대", "최소", "분산", "표준편차"]

    return (
        <div className="col-span-2 m-auto gap-1.5 w-full">
            <Label>통계</Label>
            <Select value={selectedStat} onValueChange={setSelectedStat} >
                <SelectTrigger className="self-center">
                    <SelectValue placeholder="통계 선택" />
                </SelectTrigger>
                <SelectContent>
                    <ScrollArea className="max-h-[400px]">
                        {stats.map((stat) => <SelectItem key={stat} value={stat}>{stat}</SelectItem>)}
                    </ScrollArea>
                </SelectContent>
            </Select>
        </div >
    )
}


function GetTargetLifeCycleButton() {
    
    const [isButtonEnabled, setIsButtonEnabled] = useState(false);
    const { selectedFacility, selectedTgLifeNum } = useTargetLifeStore();
    const { toast } = useToast()

    // 유효성 검사 및 조회 버튼 활성화
    useEffect(() => {
        if (!selectedFacility) setIsButtonEnabled(false)
        else if (!selectedTgLifeNum) setIsButtonEnabled(false)
        else setIsButtonEnabled(true)
    }, [selectedFacility, selectedTgLifeNum])

    const handleAddButton = async () => {
        console.log("selectedFacility:", selectedFacility)
        console.log("selectedTgLifeNum:", selectedTgLifeNum)

        const data = {
            facility: selectedFacility,
            tgLifeNum: selectedTgLifeNum
        }
        
        const res: AxiosResponse<any, any> | undefined = await getTargetLifeCycle(data);

        if (res !== undefined) {
            console.log("res.data:", res.data)
            useTargetLifeStore.setState((state) => ({
                ...state,
                cycleList: Array.isArray(res.data) ? res.data : []
            }));
        }
        else {
            toast({
                variant: "destructive",
                title: `목록 추가 실패`,
                description: `오류가 발생하였습니다. 네트워크 및 서버 상태를 점검해주세요.`,
            })
        }
    }

    return (
        <div className="mt-6">
            <Button disabled={!isButtonEnabled} onClick={handleAddButton}>
                불러오기
            </Button>
        </div>
    )
}


function QueryTargetLifeButton() {

    const [isButtonEnabled, setIsButtonEnabled] = useState(false);
    const { selectedParam, selectedStat, selectedFacility, selectedTgLifeNum } = useTargetLifeStore();
    const { queryType } = useQueryTypeStore();
    const { timeValid } = useQueryDateTimeStore();
    const { lifeCntValid } = useQueryLifeCntStore();
    const handleQueryTgLife = useHandleQueryTgLife();

    // 유효성 검사 및 조회 버튼 활성화
    useEffect(() => {
        if (!selectedFacility) setIsButtonEnabled(false)
        else if (!selectedTgLifeNum) setIsButtonEnabled(false)
        else if (!selectedParam) setIsButtonEnabled(false)
        else if (!selectedStat) setIsButtonEnabled(false)
        else setIsButtonEnabled(true)
    }, [selectedParam, selectedStat, selectedFacility, selectedTgLifeNum, queryType, timeValid, lifeCntValid])


    return (
        <Button disabled={!isButtonEnabled} onClick={handleQueryTgLife}>
            조회
        </Button>
    )
}


export default function QueryTypeSection() {

    return (
        <div>
            <Card className="flex flex-col gap-5 p-5">
                <Label className="font-bold text-[20px]">사이클 목록</Label>
                <div className="flex flex-row gap-5">
                    <FacilitySelect />
                    <TgLifeNumSelect />
                    <GetTargetLifeCycleButton />
                </div>
                <TGLifeTable />
            </Card>
            <Card className="flex flex-col gap-5 p-5">
                <Label className="font-bold text-[20px]">조회</Label>
                <div className="flex flex-row gap-5">
                    <ParamSelect />
                    <StatSelect />
                </div>
                <div className="ml-auto">
                    <QueryTargetLifeButton />
                </div>
            </Card>
        </div>
    )
}
