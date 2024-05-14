import axios from "axios";

// DB에 저장된 설비의 이름들과 각각의 설비들의 파라미터들을 받는 요청
export const getAllOfBoard = async () => {
  try {
    console.log("DB 내 설비 게시판 리스트 가져오기 시작");
    const res = await axios.get("http://localhost:8000/board");
    console.log("DB 내 설비 게시판 리스트 가져오기 완료");
    return res;
  } catch (err) {
    console.log("게시판 정보 리스트를 가져오는 데에 실패하였습니다.", err);
  }
};