import {
    Card,
    CardContent,
    CardHeader,
    CardTitle,
} from "@/components/base/card"
import { Chart } from 'chart.js'
import zoomPlugin from 'chartjs-plugin-zoom'
import { useState, useEffect } from 'react'
import { useGraphDataStore } from "@/stores/GraphData";
import BokehPlot from "@/components/common/BokehPlot";
import Lottie from "lottie-react";
import ChartLoadingGIF from "@/assets/chartloading.json"
import { div } from "@bokeh/bokehjs/build/js/lib/core/dom";
import SamsungLogo from "@/assets/images/Logo_BLUE.png"

Chart.register(zoomPlugin);

function GraphSection() {

    const { graphData, isFetching } = useGraphDataStore()

    useEffect(() => {
        const fetchData = async () => {
            try {
                // const response = await fetch('http://localhost:8000/draw_all_graph_2'); // 서버에 요청을 보냄
                const response = await fetch('http://localhost:8000/draw_all_tg_graph');
                // console.log("==========응답===========")
                // console.log(response.data)
                const data = await response.json(); // JSON 데이터를 응답으로부터 추출
                // console.log("==========data=============")
                console.log(data)
                // const response2 =  await fetch('http://localhost:8000/draw_all_graph_2');
                // const data2 = await response2.json();

                const parameterList = data.map((data, index) => ({
                    index: index,
                }))

                setParameterData(parameterList)

                setGraphData(data); // 받아온 JSON 데이터를 상태에 설정
                // console.log("===========graph===========")
                // console.log(graphData)
                // setGraphData(data2); // 받아온 JSON 데이터를 상태에 설정
                // console.log("data11111111111111111")
                // console.log(data)
                // console.log("data222222222222222222222")
                // console.log(data2)
                console.log(graphData);
            } catch (error) {
                console.error('Error fetching data:', error);
            }
        };

        fetchData(); // 데이터를 가져오는 함수 호출
    }, []); // 빈 배열을 전달하여 컴포넌트가 마운트될 때만 실행되도록 함

    return (
        <div className="flex flex-col ">
            <Card className='mr-5 min-h-[800px]'>
                <CardHeader>
                    <CardTitle>Graph Overview</CardTitle>
                </CardHeader>
                <CardContent className="">
                    {graphData.length != 0 ?
                        graphData.map((data, index) => (
                            <div key={index}>
                                <h2>Plot {index + 1}</h2>
                                <BokehPlot data={graphData} />
                            </div>
                        )) : isFetching ?
                            <div className="flex flex-col items-center">
                                <Lottie animationData={ChartLoadingGIF} style={{ width: 400 }} />
                                <p className="text-[42px]">그래프를 조회하고 있습니다.</p>
                            </div> :
                            <div className="flex flex-col items-center my-[100px]">
                                <img src={SamsungLogo} width={800} alt="" />
                                <p className="text-[40px]">GLOBAL TECHNOLOGY RESEARCH</p>
                                <p className="text-[40px] my-[50px]">그래프를 조회해주세요.</p>
                            </div>
                    }
                </CardContent>
            </Card >
        </div >
    )
}

export default GraphSection;