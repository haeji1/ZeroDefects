import { Label } from "@/components/base/label";
import { Input } from "@/components/base/input";
import { useQueryLifeCntStore, useQueryTypeStore } from "@/stores/QueryCondition";
import { useEffect } from "react";

export default function LifeCntSelect() {

    const { queryStartCnt, setQueryStartCnt, queryEndCnt, setQueryEndCnt, setLifeCntValid } = useQueryLifeCntStore();
    const { queryType } = useQueryTypeStore();

    // 숫자 이외의 입력 값들을 제거하고, Number 타입으로 변환하여 전역값으로 저장
    const handleCntChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        const filteredValue = e.target.value.replace(/\D/g, '');
        if (e.target.id === 'startCnt') setQueryStartCnt(Number(filteredValue));
        else if (e.target.id === 'endCnt') setQueryEndCnt(Number(filteredValue));
    };

    useEffect(() => {
        if (queryStartCnt - queryEndCnt > 0) setLifeCntValid(false);
        else setLifeCntValid(true)
    }, [queryStartCnt, queryEndCnt])


    return (
        <div className="h-full flex flex-col gap-2 justify-center">
            <div className="flex flex-row gap-3">
                <div className="w-full">
                    <Label>시작 카운트</Label>
                    <Input id="startCnt" type="number" min={0} value={queryStartCnt} onChange={handleCntChange} disabled={queryType !== "lifeCnt"} />
                </div>
                <div className="w-full">
                    <Label>종료 카운트</Label>
                    <Input id="endCnt" type="number" min={0} value={queryEndCnt} onChange={handleCntChange} disabled={queryType !== "lifeCnt"} />
                </div>
            </div>
            {queryStartCnt - queryEndCnt > 0 ?
                <p className="ml-auto text-sm text-red-500">시작 카운트는 종료 카운트보다 늦을 수 없습니다.</p>
                :
                <p className="ml-auto text-sm text-white">null</p>
            }

        </div>
    )
}