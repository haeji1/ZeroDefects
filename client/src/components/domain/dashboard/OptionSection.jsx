import ParameterSelection from "./ParameterSelection";
import StepSelection from "./StepSelection";
import BookmarkSection from "./BookmarkSection";
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
            <BookmarkSection />
            <div className="grid grid-cols-2 space-x-5">
                <ParameterSelection />
                <StepSelection />
            </div>

        </div>
    )
}

export default OptionSection;