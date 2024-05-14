import React, { useEffect, useState } from 'react';
import { getAllOfBoard as fetchAllOfBoard } from "@/apis/api/board"; // 이름 변경으로 충돌 방지

function BoardList() {
    const [boardList, setBoardList] = useState([]);

    useEffect(() => {
        const fetchBoardList = async () => { // 함수 이름 변경
            try {
                const res = await fetchAllOfBoard(); // 수정된 함수 이름 사용
                console.log(res)
                if (res.data && res.data.message) {
                    setBoardList([res.data.message]); // 메시지를 배열에 넣어 상태 업데이트
                }
            } catch (error) {
                console.error("게시판 목록을 불러오는데 실패했습니다.", error);
            }
        };

        fetchBoardList();
    }, []);

    return (
        <div>
            {boardList.map((message, index) => (
                <div key={index}>{message}</div> // 각 메시지를 렌더링
            ))}
        </div>
    );
}

export default BoardList;
