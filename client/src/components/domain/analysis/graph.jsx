import React, { useState, useEffect } from 'react';
import BokehPlot from '@/components/common/BokehPlot';
import { useGraphDataStore } from '@/stores/GraphData';

function Graph() {

    const { graphData, setGraphData } = useGraphDataStore()


    useEffect(() => {
        const fetchData = async () => {
            try {
                // const response = await fetch('http://localhost:8000/draw_all_graph_2'); // 서버에 요청을 보냄
                const response = await fetch('http://localhost:8000/draw_all_tg_graph');
                // console.log("==========응답===========")
                // console.log(response.data)
                const data = await response.json(); // JSON 데이터를 응답으로부터 추출
                // console.log("==========data=============")
                // console.log(data)
                // const response2 =  await fetch('http://localhost:8000/draw_all_graph_2');
                // const data2 = await response2.json();
                setGraphData(data); // 받아온 JSON 데이터를 상태에 설정
                // console.log("===========graph===========")
                // console.log(setGraphData(data))
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
        <div>
            <h1>Bokeh Plots</h1>
            {graphData.map((data, index) => (
                <div key={index}>
                    <h2>Plot {index + 1}</h2>
                    <BokehPlot data={data} /> {/* BokehPlot 컴포넌트에 JSON 데이터를 전달 */}
                </div>
            ))}
        </div>
    );
} export default Graph;

