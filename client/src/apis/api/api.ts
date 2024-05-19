import axios from "axios";

// DB에 저장된 설비의 이름들과 각각의 설비들의 파라미터들을 받는 요청
export const fetchFacilityInfos = async () => {
  try {
    console.log("DB 내 설비 정보 리스트 가져오기 시작");
    const res = await axios.get("http://localhost:8000/facility/info");
    console.log("DB 내 설비 정보 리스트 가져오기 완료");
    return res;
  } catch (err) {
    console.log("설비 정보 리스트를 가져오는 데에 실패하였습니다.", err);
  }
};

// 조회하고자 하는 설비명, 파라미터명, 조회 구간, 사이클명(Option), 스탭번호(Option)을 통해 해당하는 Bokeh 그래프 데이터를 받아오는 요청
// 단일 조회와 다중 비교 조회 둘 다 가능 
export const getGraph = async (data: object) => {
  try {
    console.log("그래프 데이터를 요청합니다.");
    const res = await axios.post("http://localhost:8000/api/draw-graph", data)
    console.log("그래프 데이터를 가져오기 완료");
    return res;
  } catch (err) {
    console.log("그래프 데이터를 가져오는 데에 실패하였습니다.", err);
    // 에러 처리
  }
}

// 설비명, 파라미터명, 조회 구간을 통해 해당 구간 내에 배치 정보들을 받아오는 요청
export const getBatches = async (facilityInfo: any) => {
  try {
    console.log("배치 데이터를 요청합니다.");
    const res = await axios.post("http://localhost:8000/api/batches", { facility: facilityInfo })
    console.log("배치 데이터 가져오기 완료.");
    return res;
  } catch (err) {
    console.log("배치 데이터를 가져오는 데에 실패하였습니다.", err);
    // 에러 처리
  }
}


export const getCorrelationGraph = async (data: object) => {
  try {
    console.log("그래프 데이터를 요청합니다.");
    const res = await axios.post("http://localhost:8000/api/correlation", data)
    console.log("그래프 데이터를 가져오기 완료");
    return res;
  } catch (err) {
    console.log("그래프 데이터를 가져오는 데에 실패하였습니다.", err);
    // 에러 처리
  }
}