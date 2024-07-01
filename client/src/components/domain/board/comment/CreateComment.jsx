import React, { useState } from "react";
import axios from "axios";
import useCommentStore from "@/stores/Comment";

function CreateComments({ postId }) {
  // 사용자 입력 값을 관리하기 위한 상태
  const [author, setAuthor] = useState("");
  const [content, setContent] = useState("");
  const [password, setPassword] = useState("");

  // Zustand 스토어에서 addComment 함수 추출
  const addComment = useCommentStore((state) => state.addComment);

  // 폼 제출 핸들러
  const handleSubmit = async (e) => {
    e.preventDefault();

    // 유효성 검사 예시
    if (!author || !content || !password) {
      alert("모든 필드를 채워주세요.");
      return;
    }

    try {
      // 서버에 댓글 정보 전송
      const response = await axios.post(
        `http://localhost:8000/post/posts/${postId}/comments`,
        {
          author,
          content,
          password,
        }
      );

      // 응답으로 받은 댓글 정보를 Zustand 스토어에 추가
      if (response.data) {
        addComment(response.data);
        alert("댓글 생성에 성공했습니다.");
        // 입력 필드 초기화
        setAuthor("");
        setContent("");
        setPassword("");
        window.location.reload();
      }
    } catch (error) {
      console.error(error);
      alert("댓글 생성에 실패했습니다.");
    }
  };

  // 폼 렌더링
  return (
    <form
      className="relative overflow-hidden rounded-lg border bg-background focus-within:ring-1 focus-within:ring-ring"
      onSubmit={handleSubmit}
    >
      <label
        className="text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70 sr-only"
        for="message"
      >
        Message
      </label>
      <textarea
        className="flex w-full rounded-md border-input bg-background text-sm ring-offset-background placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50 min-h-12 resize-none border-0 p-3 shadow-none focus-visible:ring-0"
        value={content}
        style={{border:"none"}}
        placeholder="Type your message here..."
        onChange={(e) => setContent(e.target.value)}
        required
      ></textarea>
      <div className="flex items-center p-3 pt-0">
      <input
        type="text"
        value={author}
        onChange={e => setAuthor(e.target.value)}
        placeholder="작성자"
        required
      />
      <input
        type="password"
        value={password}
        onChange={e => setPassword(e.target.value)}
        placeholder="비밀번호"
        required
      />
      
        <button
          className="inline-flex items-center justify-center whitespace-nowrap text-sm font-medium ring-offset-background transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50 bg-primary text-primary-foreground hover:bg-primary/90 h-9 rounded-md px-3 ml-auto gap-1.5"
          type="submit"
        >
          Send Message
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
            className="lucide lucide-corner-down-left size-3.5"
          >
            <polyline points="9 10 4 15 9 20"></polyline>
            <path d="M20 4v7a4 4 0 0 1-4 4H4"></path>
          </svg>
        </button>
      </div>
    </form>
  );
}

export default CreateComments;
