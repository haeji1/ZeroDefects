import {
    Card,
    CardContent,
    CardHeader,
    CardTitle,
} from "@/components/base/card";
import Lottie from "lottie-react";
import { Switch } from "@/components/base/switch";
import { Label } from "@/components/base/label";
import BokehPlot from "@/components/common/BokehPlot";
import SamsungLogo from "@/assets/images/Logo_BLUE.png";
import { useEffect, useState } from "react";
import ChartLoadingGIF from "@/assets/chartloading.json"


function GraphSection() {

    let isFetching = false;
    const [isCollapse, setIsCollapse] = useState(false);
    const graphData: any = [];

    return (
        <div className="flex flex-col ">
            <Card className='mr-5 min-h-[800px]'>
                <CardHeader className="flex flex-row">
                    <CardTitle>Graph Overview</CardTitle>
                    <div className="ml-auto flex items-center space-x-2">
                        <Label htmlFor="airplane-mode">그래프 전체 보기</Label>
                        <Switch id="airplane-mode" onClick={() => setIsCollapse(!isCollapse)} />
                    </div>
                </CardHeader>
                <CardContent>
                    {isFetching ? <div className="flex flex-col items-center">
                        <Lottie animationData={ChartLoadingGIF} style={{ width: 400 }} />
                        <p className="text-[42px]">그래프를 조회하고 있습니다.</p>
                    </div> : graphData.length !== 0 ?
                        graphData.map((data: any, index: number) => (
                            <div key={index}>
                                <BokehPlot data={data} />
                            </div>
                        )) : <div className="flex flex-col items-center my-[100px]">
                            <img src={SamsungLogo} width={800} alt="" />
                            <p className="text-[40px]">GLOBAL TECHNOLOGY RESEARCH</p>
                        </div>
                    }
                </CardContent>
            </Card >
        </div >
    );
}

export default GraphSection;