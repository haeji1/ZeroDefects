import { useCorrelationStore } from "@/stores/Correlation";
import { useQueryTypeStore, useQueryDateTimeStore, useQueryStepStore } from "@/stores/QueryCondition";

const useHandleQueryCorrelation = () => {
    const { queryType } = useQueryTypeStore();
    const { queryStartDate, queryEndDate, timeValid } = useQueryDateTimeStore();
    const { queryStartStep, queryEndStep, stepValid } = useQueryStepStore();
    const { selectedFacility, selectedParameters, setIsFetching } = useCorrelationStore();

    const handleQueryCorrelation = async () => {
        let queryCondition;

        if (queryType === 'time') {
            queryCondition = {
                startTime: queryStartDate.toISOString(),
                endTime: queryEndDate.toISOString(),
                step: null,
            }
        } else if (queryType === 'step') {
            const step = [];
            for (let i = queryStartStep; i <= queryEndStep; i++) {
                step.push(i);
            }
            queryCondition = {
                startTime: null,
                endTime: null,
                step: step,
            }
        }

        const data = {
            queryType: queryType,
            queryCondition: queryCondition,
            queryData: {
                facility: selectedFacility,
                parameter: selectedParameters,
            }
        }

        console.log(data);
        // setIsFetching(true)
        // const res = await getGraph(data)
        // if (res) {
        //     setGraphData(res.data);
        //     setIsFetching(false)
        // }
        // else {
        //     setIsFetching(false);
        // }
    }

    return handleQueryCorrelation;
}

export default useHandleQueryCorrelation;
