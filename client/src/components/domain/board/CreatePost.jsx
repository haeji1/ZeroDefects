import React, { useState } from 'react';
import axios from 'axios';

function CreatePost() {
  const [title, setTitle] = useState('');
  const [content, setContent] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    const post = { title, content };
    await axios.post('http://localhost:8000/posts', post);
    setTitle('');
    setContent('');
    // 게시글 목록을 다시 불러오는 로직 추가 가능
  };

  return (
    <div>
      <h1>게시물 생성</h1>
      <form onSubmit={handleSubmit}>
        <div>
          <label>제목</label>
          <input type="text" value={title} onChange={(e) => setTitle(e.target.value)} />
        </div>
        <div>
          <label>내용</label>
          <textarea value={content} onChange={(e) => setContent(e.target.value)}></textarea>
        </div>
        <button type="submit">게시물 생성</button>
      </form>
    </div>
  );
}

export default CreatePost;
