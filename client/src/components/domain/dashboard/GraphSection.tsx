import {
    Card,
    CardContent,
    CardHeader,
    CardTitle,
} from "@/components/base/card"
import { Switch } from "@/components/base/switch";
import { Label } from "@/components/base/label";
import { Chart } from 'chart.js'
import zoomPlugin from 'chartjs-plugin-zoom'
import { useGraphDataStore } from "@/stores/GraphData";
import BokehPlot from "@/components/common/BokehPlot";
import Lottie from "lottie-react";
import ChartLoadingGIF from "@/assets/chartloading.json"
import SamsungLogo from "@/assets/images/Logo_BLUE.png"
import { useEffect } from "react";
import CreatePostModal from "@/components/domain/board/post/CreatePost";

Chart.register(zoomPlugin);

function GraphSection() {

    const { graphData, isFetching, isCollapse, setIsCollapse } = useGraphDataStore()

    useEffect(() => {
    }, [isFetching])

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
                                <CreatePostModal />
                            </div>
                        )) : <div className="flex flex-col items-center my-[100px]">
                            <img src={SamsungLogo} width={800} alt="" />
                            <p className="text-[40px]">GLOBAL TECHNOLOGY RESEARCH</p>
                            {/* <p className="text-[40px] my-[50px]">그래프를 조회해주세요.</p> */}
                        </div>
                    }
                </CardContent>
            </Card >
        </div >
    )
}

export default GraphSection;