import { useEffect, useRef } from 'react';
import * as Bokeh from '@bokeh/bokehjs';

BokehPlot.propTypes = {
    data: Object
}

function BokehPlot({ data }) {
    const plotRef = useRef();
    useEffect(() => {
        if (data) {
            Bokeh.embed.embed_item(data, plotRef.current);
        }
    }, [data]);

    return <div ref={plotRef}></div>;
}

export default BokehPlot;


