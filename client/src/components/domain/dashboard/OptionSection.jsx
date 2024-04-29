import ParameterSelection from "./ParameterSelection";
import StepSelection from "./StepSelection";
import DataList from "./DataList";
function OptionSection() {



    //     <>
    //     <div style={{
    //         display: 'grid',
    //         gridTemplateColumns: '8fr 4fr',
    //         padding: '20px'
    //     }}>
    //         <GraphSection />
    //         <OptionSection />
    //     </div>
    // </>
    return (
        <div>
            <DataList />
            <div className="grid grid-cols-2 space-x-5">
                <ParameterSelection />
                <StepSelection />
            </div>

        </div>
    )
}

export default OptionSection;