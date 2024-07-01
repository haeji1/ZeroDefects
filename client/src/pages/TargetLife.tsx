import QueryTypeSection from '@/components/domain/targetlife/QueryTypeSection';
import TargetLifeGraphSection from '@/components/domain/targetlife/TargetLifeGraphSection';
import { useTargetLifeStore } from '@/stores/Targetlife';
import { Sidebar } from 'react-pro-sidebar';

function TargetLife() {

    const { isCollapse } = useTargetLifeStore();
    return (
        <div className="flex flex-row-reverse m-5">
            <Sidebar
                collapsed={isCollapse}
                width="30%"
                collapsedWidth="0%"
                backgroundColor="null"
            >
                <QueryTypeSection />
            </Sidebar>
            <div className='w-full'>
                <TargetLifeGraphSection />
            </div>

        </div>
    )
}

export default TargetLife;