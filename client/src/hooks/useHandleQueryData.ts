import { getGraph } from "@/apis/api/api";
import { useQueryTypeStore, useQueryDateTimeStore, useQueryStepStore } from "@/stores/QueryCondition";
import { useSelectedRowStore } from "@/stores/Bookmark";
import { useGraphDataStore } from "@/stores/GraphData";
import { useBookmarkStore } from "@/stores/Bookmark";

const useHandleQueryData = () => {

    const { queryType } = useQueryTypeStore();
    const { queryStartDate, queryEndDate } = useQueryDateTimeStore();
    const { queryStartStep, queryEndStep } = useQueryStepStore();
    const { selectedRow } = useSelectedRowStore();
    const { setIsFetching, setGraphData } = useGraphDataStore()
    const { bookmark } = useBookmarkStore();

    const handleQueryData = async () => {
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

        setIsFetching(true)
        const res = await getGraph(data)
        if (res) {
            setGraphData(res.data);
            setIsFetching(false)
        }
        else {
            setIsFetching(false);
        }
    }

    return handleQueryData;

}

export default useHandleQueryData;