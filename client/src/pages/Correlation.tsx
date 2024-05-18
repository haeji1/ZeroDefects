import { Sidebar } from 'react-pro-sidebar';
import GraphSection from '@/components/domain/correlation/GraphSection';
import QueryTypeSection from '@/components/domain/correlation/QueryTypeSection';
import CorrelationTable from '@/components/domain/correlation/CorrelationTable';



function Correlation() {

    let isCollapse = false;

    return (
        <>
            <div className="flex flex-row-reverse m-5">
                <Sidebar
                    collapsed={isCollapse}
                    width="30%"
                    collapsedWidth="0%"
                    backgroundColor="null"
                >
                    <QueryTypeSection />
                </Sidebar>
                <div className="w-full">
                    <GraphSection />
                </div>
            </div>
        </>
    )
}

export default Correlation;