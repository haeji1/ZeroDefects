import MainSection from "@/components/domain/dashboard/MainSection";
import OptionSection from "@/components/domain/dashboard/OptionSection";

function Dashboard() {

    return (
        <>
            <div style={{
                display: 'grid',
                gridTemplateColumns: '8fr 4fr',
                padding: '20px'
            }}>
                <MainSection />
                <OptionSection />
            </div>
        </>
    )
}

export default Dashboard;