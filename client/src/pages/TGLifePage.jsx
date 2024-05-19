import { Card } from "@/components/base/card";

import { useEffect, useState } from "react";
import BokehPlot from "@/components/common/BokehPlot";

import BookmarkTable from "@/components/domain/dashboard/BookmarkTable";
import Addlist from "@/components/domain/dashboard/AddList";
import GetGraph from "@/components/domain/dashboard/GetGraph";
import GetTGGraph from "@/components/domain/dashboard/GetTGGraph";
import { getTGLifeJson } from "@/apis/api/api";

function Dashboard() {
  const [data, setData] = useState();
  const [tgLifeNum, setTgLifeNum] = useState();

  const fetchData = async () => {
    const model = {
      facility: "MASS07",
      tg_life_num: "2",
      startTime: "1970-01-01T00:00:00.0Z",
      endTime: "2024-03-14T10:18:57.0Z",
      statistics_list: ["AVG"],
    };

    try {
      const response = await getTGLifeJson(model);
      // console.log("response ...", response);
      // const data = await response.json();
      console.log("res", response);
      setData(response.data.msg);
      // console.log(graphData);
      // console.log("data .... ", data);
    } catch (error) {
      console.error("Error fetching data:", error);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  return (
    <>
      <div className="grid grid-cols-3 m-5">
        <BokehPlot data={data} />
        <Card className="p-4">
          {/* <BookmarkTable /> */}
          {/* <Addlist /> */}
          <GetTGGraph />
        </Card>
      </div>
    </>
  );
}

export default Dashboard;
