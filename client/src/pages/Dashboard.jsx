import GraphSection from "@/components/domain/dashboard/GraphSection";
import OptionSection from "@/components/domain/dashboard/OptionSection";

function Dashboard() {

    return (
        <>
            <div style={{
                display: 'grid',
                gridTemplateColumns: '9fr 3fr',
                padding: '20px'
            }}>
                <GraphSection />
                <OptionSection />
            </div>
        </>
    )
}

export default Dashboard;