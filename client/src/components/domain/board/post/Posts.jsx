import React, { useEffect, useState } from "react";
import axios from "axios";
import { Link, useNavigate } from "react-router-dom";
import {
  Pagination,
  PaginationContent,
  PaginationEllipsis,
  PaginationItem,
  PaginationLink,
  PaginationNext,
  PaginationPrevious,
} from "@/components/base/pagination";
import {
  Card,
  CardContent,
  CardHeader,
  CardTitle,
} from "@/components/base/card";
import BokehPlot from "@/components/common/BokehPlot";
function Posts() {
  const [posts, setPosts] = useState([]);
  const [currentPage, setCurrentPage] = useState(1); // 현재 페이지 상태 추가
  const [totalPages, setTotalPages] = useState(0);
  const [pageRangeStart, setPageRangeStart] = useState(1);
  const navigate = useNavigate();

  const updatePageRange = (newCurrentPage) => {
    const newStartPage = Math.floor((newCurrentPage - 1) / 5) * 5 + 1;
    if (newStartPage !== pageRangeStart) {
      setPageRangeStart(newStartPage);
    }
  };
  useEffect(() => {
    fetchPosts();
  }, []); // 컴포넌트 마운트 시 첫 페이지의 게시물을 가져옵니다.

  const fetchPosts = async (page = 1) => {
    const response = await axios.get(
      `http://localhost:8000/post/posts?page=${page}`
    );
    setPosts(response.data.items);
    setCurrentPage(page); // 페이지를 성공적으로 불러온 후 현재 페이지 상태 업데이트
    setTotalPages(response.data.pages);
    updatePageRange(page); // 페이지 업데이트 함수에 현재 페이지 전달
  };
  const handleRowClick = (postId) => {
    navigate(`/board/${postId}`); // 'history' 대신 'navigate' 사용
  };

  return (
    <div>
      <h2 className="scroll-m-20 pb-2 text-3xl font-semibold tracking-tight first:mt-0">
        게시물 목록
      </h2>
      <div
        className="posts-container"
        style={{
          display: "flex",
          flexDirection: "column",
          justifyContent: "space-between",
          height: "100%",
        }}
      >
        <div
          className="my-6 w-full overflow-y-auto"
          style={{ height: "800px" }}
        >
          <table className="w-full">
            <colgroup>
              <col style={{ width: "5%" }} />
              <col style={{ width: "50%" }} />
              <col style={{ width: "15%" }} />
              <col style={{ width: "30%" }} />
            </colgroup>
            <thead>
              <tr className="m-0 border-t p-0 even:bg-muted">
                <th className="border px-4 py-2 text-center font-bold">ID</th>
                <th className="border px-4 py-2 text-center font-bold">
                  게시글 제목
                </th>
                <th className="border px-4 py-2 text-center font-bold">
                  작성자
                </th>
                <th className="border px-4 py-2 text-center font-bold">날짜</th>
              </tr>
            </thead>
            <tbody>
              {posts.map((post) => (
                <tr
                  className="m-0 border-t p-0 even:bg-muted"
                  key={post.id}
                  onClick={() => handleRowClick(post.id)}
                  style={{ cursor: "pointer" }}
                >
                  <td className="border px-4 py-2 text-center">{post.id}</td>
                  <td className="border px-4 py-2 text-center">{post.title}</td>
                  <td className="border px-4 py-2 text-center">
                    {post.author}
                  </td>
                  <td className="border px-4 py-2 text-center">{post.date}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
      <div>
        <Pagination>
          <PaginationContent>
            <PaginationItem>
              <PaginationPrevious
                onClick={() => fetchPosts(Math.max(currentPage - 5, 1))}
                disabled={currentPage - 5 < 1}
                style={{ cursor: "pointer" }}
              />
            </PaginationItem>
            {[...Array(5)].map((_, index) => {
              const pageNumber = pageRangeStart + index;
              return pageNumber <= totalPages ? (
                <PaginationItem key={pageNumber}>
                  <PaginationLink
                    onClick={() => fetchPosts(pageNumber)}
                    style={{
                      backgroundColor:
                        pageNumber === currentPage ? "#334155" : "#fff",
                      color: pageNumber === currentPage ? "#fff" : "#334155",
                      cursor: "pointer",
                    }}
                  >
                    {pageNumber}
                  </PaginationLink>
                </PaginationItem>
              ) : null;
            })}
            <PaginationItem>
              <PaginationNext
                onClick={() =>
                  fetchPosts(Math.min(currentPage + 5, totalPages))
                }
                disabled={currentPage + 5 > totalPages}
                style={{ cursor: "pointer"}}
              />
            </PaginationItem>
          </PaginationContent>
        </Pagination>
      </div>
    </div>
  );
}

export default Posts;
