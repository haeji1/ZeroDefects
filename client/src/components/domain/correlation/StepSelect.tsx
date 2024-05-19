import { Label } from "@/components/base/label";
import { Input } from "@/components/base/input";
import { useQueryStepStore, useQueryTypeStore } from "@/stores/QueryCondition";
import { useEffect } from "react";

export default function StepSelect() {

    const { queryStartStep, setQueryStartStep, queryEndStep, setQueryEndStep, setStepValid } = useQueryStepStore();
    const { queryType } = useQueryTypeStore();

    // 숫자 이외의 입력 값들을 제거하고, Number 타입으로 변환하여 전역값으로 저장
    const handleStepChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        const filteredValue = e.target.value.replace(/\D/g, '');
        if (e.target.id === 'startStep') setQueryStartStep(Number(filteredValue));
        else if (e.target.id === 'endStep') setQueryEndStep(Number(filteredValue));
    };

    useEffect(() => {
        if (queryStartStep - queryEndStep > 0) setStepValid(false);
        else setStepValid(true)
    }, [queryStartStep, queryEndStep])


    return (
        <div className="h-full flex flex-col gap-2 justify-center">
            <div className="flex flex-row gap-3">
                <div className="w-full">
                    <Label>시작 스텝</Label>
                    <Input id="startStep" type="number" min={0} value={queryStartStep} onChange={handleStepChange} disabled={queryType !== "step"} />
                </div>
                <div className="w-full">
                    <Label>종료 스텝</Label>
                    <Input id="endStep" type="number" min={0} value={queryEndStep} onChange={handleStepChange} disabled={queryType !== "step"} />
                </div>
            </div>
            {queryStartStep - queryEndStep > 0 ?
                <p className="ml-auto text-sm text-red-500">시작 스텝은 종료 스텝보다 늦을 수 없습니다.</p>
                :
                <p className="ml-auto text-sm text-white">null</p>
            }

        </div>
    )
}