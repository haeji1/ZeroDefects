import { getTargetLifeGraph } from "@/apis/api/api";
import { useQueryTypeStore, useQueryDateTimeStore, useQueryLifeCntStore } from "@/stores/QueryCondition";
import { QueryType } from "@/stores/QueryCondition";
import { useTargetLifeStore } from "@/stores/Targetlife";

type Data = {
    queryType: QueryType,
    queryCondition: {
        startTime: null | string,
        endTime: null | string,
        startCnt: null | number,
        endCnt: null | number,
    },
    queryData: {
        facility: string,
        tgLifeNum: undefined | number,
    }
}

const useHandleQueryTgLife = () => {
    const { queryType } = useQueryTypeStore();
    const { queryStartDate, queryEndDate } = useQueryDateTimeStore();
    const { queryStartCnt, queryEndCnt } = useQueryLifeCntStore();
    const { selectedFacility, selectedTgLifeNum, setIsFetching, setGraphData } = useTargetLifeStore();

    const handleQueryTgLife = async () => {

        const data: Data = {
            queryType: queryType,
            queryCondition: {
                startTime: null,
                endTime: null,
                startCnt: null,
                endCnt: null,
            },
            queryData: {
                facility: selectedFacility,
                tgLifeNum: selectedTgLifeNum,
            }
        }

        if (queryType === 'time') {
            data.queryCondition.startTime = queryStartDate.toISOString();
            data.queryCondition.endTime = queryEndDate.toISOString();
        } else if (queryType === 'lifeCnt') {
            data.queryCondition.startCnt = queryStartCnt;
            data.queryCondition.endCnt = queryEndCnt;
        }

        console.log(data);
        setIsFetching(true)
        const res = await getTargetLifeGraph(data)
        if (res) {
            setGraphData(res.data);
            setIsFetching(false)
        }
        else {
            setIsFetching(false);
        }
    }

    return handleQueryTgLife;
}

export default useHandleQueryTgLife;
