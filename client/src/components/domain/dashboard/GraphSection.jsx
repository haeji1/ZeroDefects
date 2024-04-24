import {
    Card,
    CardContent,
    CardHeader,
    CardTitle,
} from "@/components/base/card"
import { useImage } from "./ImageContext";
import CSVReader from './CSVReader'
import ChartComponent from './ChartComponent'
import { Chart } from 'chart.js'
import zoomPlugin from 'chartjs-plugin-zoom'
import { useState } from 'react'

Chart.register(zoomPlugin);

function GraphSection() {
    const [kwData, setkwData] = useState(null);
    const column = "No4_P[kW]";

    const { image } = useImage();

    return (
        <Card className='mr-5'>
            <CardHeader>
                <CardTitle>Graph Overview</CardTitle>
            </CardHeader>
            <CardContent>
                <CSVReader column={column} setkwData={setkwData}></CSVReader>

                {kwData ?
                    <ChartComponent title={column} start_index={0} data_set={kwData} /> :
                    <p style={{
                        marginTop: '30vh',
                        textAlign: 'center',
                        fontSize: '42px',
                    }}>먼저 데이터를 첨부해주십시오.</p>
                }
                {/* {image ? <img src={image} alt="Uploaded" /> : <h1>먼저 데이터를 첨부해주세요</h1>} */}
            </CardContent>
        </Card >
    )
}

export default GraphSection;