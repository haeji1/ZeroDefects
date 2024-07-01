import { Sidebar } from 'react-pro-sidebar';
import GraphSection from "@/components/domain/dashboard/GraphSection";
import BookmarkTable from "@/components/domain/dashboard/BookmarkTable";
import Addlist from "@/components/domain/dashboard/AddList";
import QueryConditionSection from "@/components/domain/dashboard/QueryConditionSection";
import { useGraphDataStore } from "@/stores/GraphData";


function Dashboard() {

    const { isCollapse } = useGraphDataStore();

    return (
        <div className="flex flex-row-reverse m-5">
            <Sidebar
                collapsed={isCollapse}
                width="40%"
                collapsedWidth="0%"
                backgroundColor="null"
            >
                <BookmarkTable />
                <Addlist />
                <QueryConditionSection />
            </Sidebar>
            <div className="w-full">
                <GraphSection />
            </div>
        </div>


    )
}

export default Dashboard;