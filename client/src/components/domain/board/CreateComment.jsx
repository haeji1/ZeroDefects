import React, { useState } from 'react';
import axios from 'axios';
import useCommentStore from '@/stores/Comment';

function CreateComments({ postId }) {
  // 사용자 입력 값을 관리하기 위한 상태
  const [author, setAuthor] = useState('');
  const [content, setContent] = useState('');
  const [password, setPassword] = useState('');

  // Zustand 스토어에서 addComment 함수 추출
  const addComment = useCommentStore(state => state.addComment);

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
      const response = await axios.post(`http://localhost:8000/post/posts/${postId}/comments`, {
        author,
        content,
        password,
      });
      
      // 응답으로 받은 댓글 정보를 Zustand 스토어에 추가
      if (response.data) {
        addComment(response.data);
        alert("댓글 생성에 성공했습니다.");
        // 입력 필드 초기화
        setAuthor('');
        setContent('');
        setPassword('');
        window.location.reload();
      }
    } catch (error) {
      console.error(error);
      alert("댓글 생성에 실패했습니다.");
    }
  };

  // 폼 렌더링
  return (
    <form onSubmit={handleSubmit}>
      <input
        type="text"
        value={author}
        onChange={e => setAuthor(e.target.value)}
        placeholder="작성자"
        required
      />
      <textarea
        value={content}
        onChange={e => setContent(e.target.value)}
        placeholder="댓글 내용"
        required
      ></textarea>
      <input
        type="password"
        value={password}
        onChange={e => setPassword(e.target.value)}
        placeholder="비밀번호"
        required
      />
      <button type="submit">댓글 작성</button>
    </form>
  );
}

export default CreateComments;