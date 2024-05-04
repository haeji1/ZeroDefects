import SelectSection from "@/components/domain/dashboard/SelectSection";
import GraphSection from "@/components/domain/dashboard/GraphSection";
import BookmarkSection from "@/components/domain/dashboard/BookmarkSection";
import BookmarkTable from "@/components/domain/dashboard/BookmarkTable";
import { Card } from "@/components/base/card";
import Addlist from "@/components/domain/dashboard/AddList";
import GetGraph from "@/components/domain/dashboard/GetGraph";

function Dashboard() {

    return (
        <div className="grid grid-cols-3 m-5">
            <div className="col-span-2">
                <SelectSection />
                <GraphSection />
            </div>
            <Card>
                <Addlist />
                <BookmarkTable />
                <GetGraph />
            </Card>
        </div>
    )
}

export default Dashboard;