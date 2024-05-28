import { getTargetLifeGraph } from "@/api/api";
import { useTargetLifeStore, TgLifeNum } from "@/stores/Targetlife";

const parameterMap: { [key: string]: string } = {
    "전압 V [V]": "V",
    "전류 I [A]": "I",
    "전력 Pwr [kW]": "P",
};

const statisticsMap: { [key: string]: string } = {
    "평균": "mean",
    "최대": "max",
    "최소": "min",
    "분산": "variance",
    "표준편차": "standard_deviation",
};

type Data = {
    queryConditions: any[],
    queryData: {
        facility: string,
        tgLifeNum: string,
        parameter: string,
        statistics: string,
    }
}

const useHandleQueryTgLife = () => {
    const { selectedFacility, selectedTgLifeNum, selectedParam, selectedStat, selectedCycleList, setIsFetching, setGraphData } = useTargetLifeStore();

    const handleQueryTgLife = async () => {
        // Transform the parameter and statistics values using the mapping objects
        const transformedParameter = parameterMap[selectedParam] || selectedParam;
        const transformedStatistics = statisticsMap[selectedStat] || selectedStat;

        const data: Data = {
            queryConditions: selectedCycleList,
            queryData: {
                facility: selectedFacility,
                tgLifeNum: selectedTgLifeNum as TgLifeNum,
                parameter: transformedParameter,
                statistics: transformedStatistics,
            }
        }

        console.log(data);
        setIsFetching(true);
        const res = await getTargetLifeGraph(data);
        if (res) {
            setGraphData(res.data);
            setIsFetching(false);
        } else {
            setIsFetching(false);
        }
    }

    return handleQueryTgLife;
}

export default useHandleQueryTgLife;
