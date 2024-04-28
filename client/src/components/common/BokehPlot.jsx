import React, { useEffect, useRef } from 'react';
import * as Bokeh from '@bokeh/bokehjs';

function BokehPlot({ data }) {
    const plotRef = useRef();
    let plotModel = null;

    useEffect(() => {
        if (data) {
            // 데이터가 존재하는 경우에만 그래프 생성
            // console.log("============data값=========")
            // console.log(data.value)
            plotModel = Bokeh.embed.embed_item(data, plotRef.current);
        }

        // 컴포넌트가 언마운트될 때 호출되는 cleanup 함수
        return () => {
            if (plotModel) {
                // 그래프 리소스를 해제
                const plotElement = plotRef.current;
                while (plotElement.firstChild) {
                    plotElement.removeChild(plotElement.firstChild);
                }
            }
        };
    }, [data]);

    return <div ref={plotRef}></div>;
}

export default BokehPlot;


