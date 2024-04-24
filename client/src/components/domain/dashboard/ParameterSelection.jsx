import {
    Card,
    CardHeader,
    CardTitle,
} from "@/components/base/card"

import { ScrollArea } from "../../base/scroll-area";
import { Separator } from "../../base/separator";
import { RadioGroup, RadioGroupItem } from "../../base/radio-group";
import { Label } from "../../base/label";



// 파라미터 더미 데이터
const parameters = ["No_1_P", "No_2_P", "No_3_P", "No_4_P", "No_5_P", "No_6_P", "No_7_P",]



function ParameterSelection() {

    return (
        <Card className="mb-3">
            <CardHeader>
                <CardTitle>
                    Parameter Selection
                </CardTitle>
            </CardHeader>
            <ScrollArea className="h-48">
                <div className="p-4">
                    <RadioGroup defalutValue={parameters[0]}>
                        {parameters.map((param) => (
                            <>
                                <div key={param} className="flex flex-row text-sm justify-between">
                                    <Label htmlFor={param}>{param}</Label>
                                    <RadioGroupItem value={param} id={param} />
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