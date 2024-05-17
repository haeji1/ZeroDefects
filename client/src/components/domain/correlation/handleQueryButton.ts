import {
    useQueryTypeStore,
    useQueryDateTimeStore,
    useQueryStepStore,
    useCorrelationStore,
} from "@/stores/Correlation";


const { queryType, setQueryType } = useQueryTypeStore();
const { queryStartDate, queryEndDate, timeValid } = useQueryDateTimeStore();
const { queryStartStep, queryEndStep, stepValid } = useQueryStepStore();


export const handleQueryButton = async () => {

    let queryCondition;

    if (queryType === 'time') {
        queryCondition = {
            startTime: queryStartDate.toISOString(),
            endTime: queryEndDate.toISOString(),
            step: null,
        }
    }
    else if (queryType === 'step') {
        const step: number[] = [];
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
        queryData: Object.keys(selectedRow).map((idx) => {
            const val = bookmark.find((obj) => obj.id === Number(idx));
            if (!val) return
            return {
                facility: val.facility,
                parameter: val.parameter,
                batchName: queryType === 'time' ? null : val.selectedBatchName,
            }
        })
    }

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