import SelectSection from "@/components/domain/dashboard/SelectSection";
import GraphSection from "@/components/domain/dashboard/GraphSection";
import BookmarkSection from "@/components/domain/dashboard/BookmarkSection";

function Dashboard() {

    return (
        <div className="grid grid-cols-3 m-5">
            <div className="col-span-2">
                <SelectSection />
                <GraphSection />
            </div>
            <BookmarkSection />
        </div>
    )
}

export default Dashboard;