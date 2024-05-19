import { Card } from "@/components/base/card";

import { useEffect, useState } from "react";
import BokehPlot from "@/components/common/BokehPlot";

import BookmarkTable from "@/components/domain/dashboard/BookmarkTable";
import Addlist from "@/components/domain/dashboard/AddList";
// import GetTGGraph from "@/components/domain/tglife/GetTGGraph";
import { Sidebar } from "react-pro-sidebar";
import { getTGLife } from "@/apis/api/api";

function Dashboard() {
  const [data, setData] = useState();
  const [tgLifeNum, setTgLifeNum] = useState();

  const fetchData = async () => {
    const model = {
      facility: "MASS07",
      tgLifeNum: "1",
      startTime: "2024-03-10T00:00:00.0Z",
      endTime: "2024-05-20T10:18:57.0Z",
    };

    try {
      console.log("fetch ", model);
      const response = await getTGLife(model);
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
          <Addlist />
          {/* <GetTGGraph /> */}
        </Card>
      </div>
    </>
  );
}

export default Dashboard;
