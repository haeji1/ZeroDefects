import {
    Card,
    CardHeader,
    CardTitle,
} from "@/components/base/card"

import { ScrollArea } from "../../base/scroll-area";
import { Separator } from "../../base/separator";
import { RadioGroup, RadioGroupItem } from "../../base/radio-group";
import { Label } from "../../base/label";



// 데이터 더미 데이터
const datas = [
    {
        id: "m5gr84i9",
        times: "24-02-01 11:03 ~ 24-02-01 13:03",
        parameter: "No_1_P",
        facility: "F1490",
    },
    {
        id: "3u1reuv4",
        times: "24-02-02 14:03 ~ 24-02-02 15:03",
        parameter: "No_2_P",
        facility: "F1491",
    },
    {
        id: "derv1ws0",
        times: "24-02-02 14:03 ~ 24-02-02 15:03",
        parameter: "No_3_P",
        facility: "F1422",
    },
    {
        id: "5kma53ae",
        times: "24-02-02 14:03 ~ 24-02-02 15:03",
        parameter: "No_4_P",
        facility: "F1221",
    },
    {
        id: "bhqecj4p",
        times: "24-02-02 14:03 ~ 24-02-02 15:03",
        parameter: "No_5_A",
        facility: "F1111",
    },
]

function ParameterSelection() {

    return (
        <Card className="mb-3">
            <CardHeader>
                <CardTitle>
                    Cycle Selection
                </CardTitle>
            </CardHeader>
            <ScrollArea className="h-48">
                <div className="p-4">
                    <RadioGroup defalutValue={datas[0]}>
                        {datas.map((data) => (
                            <>
                                <div key={data.id} className="flex flex-row text-sm justify-between">
                                    <Label htmlFor={data.id}>{data.times}</Label>
                                    <RadioGroupItem value={data.id} id={data.id} />
                                </div>
                                <Separator className="my-2" />
                            </>
                        ))}
                    </RadioGroup>
                </div>
            </ScrollArea>
        </Card>
    )
}

export default ParameterSelection;