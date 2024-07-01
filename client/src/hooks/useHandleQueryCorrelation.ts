import { getCorrelationGraph } from "@/api/api";
import { useCorrelationStore } from "@/stores/Correlation";
import { useQueryTypeStore, useQueryDateTimeStore, useQueryStepStore } from "@/stores/QueryCondition";
import { QueryType } from "@/stores/QueryCondition";

type Data = {
    queryType: QueryType,
    queryCondition: {
        startTime: null | string,
        endTime: null | string,
        step: null | number[],
    },
    queryData: {
        facility: string,
        parameter: string[],
        batchName: null | string,
    }
}

const useHandleQueryCorrelation = () => {
    const { queryType } = useQueryTypeStore();
    const { queryStartDate, queryEndDate } = useQueryDateTimeStore();
    const { queryStartStep, queryEndStep } = useQueryStepStore();
    const { selectedFacility, selectedParameters, selectedBatch, setIsFetching, setGraphData } = useCorrelationStore();

    const handleQueryCorrelation = async () => {

        const data: Data = {
            queryType: queryType,
            queryCondition: {
                startTime: null,
                endTime: null,
                step: [],
            },
            queryData: {
                facility: selectedFacility,
                parameter: selectedParameters,
                batchName: null,
            }
        }

        if (queryType === 'time') {
            data.queryCondition = {
                startTime: queryStartDate.toISOString(),
                endTime: queryEndDate.toISOString(),
                step: null,
            }
        } else if (queryType === 'step') {
            const step = [];
            for (let i = queryStartStep; i <= queryEndStep; i++) {
                step.push(i);
            }
            data.queryCondition = {
                startTime: null,
                endTime: null,
                step: step,
            }
            data.queryData.batchName = selectedBatch!.batchName
        }

        console.log(data);
        setIsFetching(true)
        const res = await getCorrelationGraph(data)
        if (res) {
            setGraphData(res.data);
            setIsFetching(false)
        }
        else {
            setIsFetching(false);
        }
    }

    return handleQueryCorrelation;
}

export default useHandleQueryCorrelation;
