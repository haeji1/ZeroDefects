import React, { useEffect, useState } from 'react';
import axios from 'axios';

function Posts() {
  const [posts, setPosts] = useState([]);
  const [currentPage, setCurrentPage] = useState(1); // 현재 페이지 상태 추가

  useEffect(() => {
    fetchPosts();
  }, []); // 컴포넌트 마운트 시 첫 페이지의 게시물을 가져옵니다.

  const fetchPosts = async (page = 1) => {
    const response = await axios.get(`http://localhost:8000/post/posts?page=${page}`);
    setPosts(response.data.items);
    setCurrentPage(page); // 페이지를 성공적으로 불러온 후 현재 페이지 상태 업데이트
  };
  
  return (
    <div>
      <h1>게시물 목록</h1>
      {posts.map(post => (
        <div key={post.id}>
          <h2>{post.title}</h2>
          <p>{post.content}</p>
        </div>
      ))}
      {/* 현재 페이지를 기반으로 다음 페이지를 불러오는 버튼 */}
      <button onClick={() => fetchPosts(currentPage + 1)}>다음 페이지</button>
      <button onClick={() => fetchPosts(currentPage - 1)}>이전 페이지</button>
    </div>
  );
}

export default Posts;