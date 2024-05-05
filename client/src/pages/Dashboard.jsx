import { Card } from "@/components/base/card";
import GraphSection from "@/components/domain/dashboard/GraphSection";
import BookmarkTable from "@/components/domain/dashboard/BookmarkTable";
import Addlist from "@/components/domain/dashboard/AddList";
import GetGraph from "@/components/domain/dashboard/GetGraph";

function Dashboard() {

    return (
        <div className="grid grid-cols-3 m-5">
            <div className="col-span-2">
                <GraphSection />
            </div>
            <Card className="p-4">
                <BookmarkTable />
                <Addlist />
                <GetGraph />
            </Card>
        </div>
    )
}

export default Dashboard;