<<<<<<< HEAD
import MainSection from "@/components/domain/dashboard/MainSection";
import OptionSection from "@/components/domain/dashboard/OptionSection";
=======
import SelectSection from "@/components/domain/dashboard/SelectSection";
import GraphSection from "@/components/domain/dashboard/GraphSection";
import BookmarkSection from "@/components/domain/dashboard/BookmarkSection";
>>>>>>> 784dd6c01622c4837f02cb266b29ef278350c91c

function Dashboard() {

    return (
<<<<<<< HEAD
        <>
            <div style={{
                display: 'grid',
                gridTemplateColumns: '8fr 4fr',
                padding: '20px'
            }}>
                <MainSection />
                <OptionSection />
=======
        <div className="grid grid-cols-3 m-5">
            <div className="col-span-2">
                <SelectSection />
                <GraphSection />
>>>>>>> 784dd6c01622c4837f02cb266b29ef278350c91c
            </div>
            <BookmarkSection />
        </div>
    )
}

export default Dashboard;