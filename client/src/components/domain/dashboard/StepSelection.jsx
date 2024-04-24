import {
    Card,
    CardHeader,
    CardTitle,
    CardContent
} from "@/components/base/card"

import { ScrollArea } from "../../base/scroll-area";
import { Separator } from "../../base/separator";
import { RadioGroup, RadioGroupItem } from "../../base/radio-group";
import { Label } from "../../base/label";
import { Button } from "../../base/button";
import { useRef } from "react";



// 파라미터 더미 데이터
const parameters = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19]


function StepSelection() {

    const buttonRef = useRef(null)

    const handleStep = () => {
        console.log(buttonRef.current)
        buttonRef.current.setAttribute('variant', 'aasdf')

    }


    return (
        <Card>
            <CardHeader>
                <CardTitle>
                    Step Selection
                </CardTitle>
            </CardHeader>

            <CardContent>
                <div className="grid grid-cols-5">
                    {parameters.map((param) => (
                        <>
                            <Button ref={buttonRef} key={param} className="m-[2px]" variant="outline">{param}</Button>
                        </>
                    ))}
                </div>
                <Button variant="outline" className='w-full' ref={buttonRef}

                    onClick={handleStep}

                >total</Button>

            </CardContent>
        </Card>
    )
}

export default StepSelection;