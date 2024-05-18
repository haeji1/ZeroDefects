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
import { Button } from "react-day-picker";

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
    <div style={{ minHeight: "840px" }}>
      <h2 className="scroll-m-20 pb-2 text-3xl font-semibold tracking-tight first:mt-0">
        게시물 목록
      </h2>
      
      <div style={{ padding: "5px" }} />
      <div className="relative ml-auto flex-1 md:grow-0">
        <svg
          xmlns="http://www.w3.org/2000/svg"
          width="24"
          height="24"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          stroke-width="2"
          stroke-linecap="round"
          stroke-linejoin="round"
          className="lucide lucide-search absolute left-2.5 top-2.5 h-4 w-4 text-muted-foreground"
        >
          <circle cx="11" cy="11" r="8"></circle>
          <path d="m21 21-4.3-4.3"></path>
        </svg>
        <input
          type="search"
          className="flex h-10 border border-input px-3 py-2 text-sm ring-offset-background file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50 w-full rounded-lg bg-background pl-8 md:w-[200px] lg:w-[336px]"
          placeholder="Search..."
        ></input>
      </div>
      <div style={{padding:"5px"}}/>
      <div
        className="posts-container"
        style={{
          display: "flex",
          flexDirection: "column",
          justifyContent: "space-between",
          height: "600px",
        }}
      >
        <div
          className="relative overflow-x-auto"
          // style={{ height: "800px" }}
        >
          <table className="w-full text-sm text-center rtl:text-center text-gray-900 dark:text-gray-400">
            <colgroup>
              <col style={{ width: "3%" }} />
              <col style={{ width: "50%" }} />
              <col style={{ width: "15%" }} />
              <col style={{ width: "20%" }} />
            </colgroup>
            <thead
              style={{
                color: "black",
                backgroundColor: "#fcfcfc", // 아주 연한 회색 배경
                textTransform: "uppercase",
                borderTop: "2px solid #333", // 진한 선 (위쪽)
                borderBottom: "1px solid #ccc", // 일반 표의 선처럼 (아래쪽)
              }}
              className="text-l text-gray-900 uppercase dark:bg-gray-700"
            >
              <tr>
                <th className="px-6 py-4"></th>
                <th className="px-6 py-4">제목</th>
                <th className="px-6 py-4">작성자</th>
                <th className="px-6 py-4">작성일</th>
              </tr>
            </thead>
            <tbody>
              {posts.map((post) => (
                <tr
                  className="bg-white border-b dark:bg-gray-900 dark:border-gray-700"
                  key={post.id}
                  onClick={() => handleRowClick(post.id)}
                  style={{ cursor: "pointer" }}
                >
                  <td className="px-6 py-4">{post.id}</td>
                  <td className="px-6 py-4 text-left">
                    {post.title.length > 30
                      ? post.title.substring(0, 35) + "..."
                      : post.title}
                  </td>
                  <td className="px-6 py-4">{post.author}</td>
                  <td className="px-6 py-4 ">{post.date}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
      <div style={{ padding: "20px" }} />
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
                style={{ cursor: "pointer" }}
              />
            </PaginationItem>
          </PaginationContent>
        </Pagination>
      </div>
    </div>
  );
}

export default Posts;
