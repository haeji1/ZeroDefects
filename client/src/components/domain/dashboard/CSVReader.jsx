import React, { useState } from "react";
import Papa from "papaparse";

function CSVReader({ setkwData }) {
  const [data, setData] = useState([]);
  // No1_P[kW]
  // const [kWData, setkWData] = useState([]);

  const handleFileChange = (event) => {
    const file = event.target.files[0];

    Papa.parse(file, {
      header: true, // 첫 번째 행을 필드명으로 사용
      skipEmptyLines: true,
      complete: function (results) {
        setData(results.data);
        // setkWData(results.data.map((item) => item["No1_P[kW]"]));
        setkwData(results.data.map((item) => item["No1_P[kW]"]));
        console.log(results.data); // 파싱된 데이터를 콘솔에 출력
        console.log(results.data.map((item) => item["No1_P[kW]"]));
      },
    });

    console.log("data", data);
  };

  return (
    <div>
      <input type="file" accept=".csv" onChange={handleFileChange} />
      {/* <div>
        {data.map((item, index) => (
          <div key={index}>{JSON.stringify(item)}</div>
        ))}
      </div> */}
    </div>
  );
}

export default CSVReader;
