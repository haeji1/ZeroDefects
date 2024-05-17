import { Sidebar } from 'react-pro-sidebar';
import GraphSection from '@/components/domain/correlation/GraphSection';
import GetGraph from '@/components/domain/correlation/GetGraph';
import CorrelationTable from '@/components/domain/correlation/CorrelationTable';



function Correlation() {

    let isCollapse = false;

    return (
        <>
            <div className='m-5'>
                <GetGraph />
            </div>
            <div className="flex flex-row-reverse m-5">
                <Sidebar
                    collapsed={isCollapse}
                    width="20%"
                    collapsedWidth="0%"
                    backgroundColor="null"
                >
                    <CorrelationTable />
                </Sidebar>
                <div className="w-full">
                    <GraphSection />
                </div>
            </div>
        </>
    )
}

export default Correlation;