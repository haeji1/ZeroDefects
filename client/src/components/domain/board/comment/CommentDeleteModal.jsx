// Modal.js
import React, { useState } from 'react';
import axios from "axios";
import { useParams, useNavigate } from 'react-router-dom';

function CommentDeleteModal({ showModal, handleClose, commentId, deleteCommentFunction, setComments, comments }) {
  const [author, setAuthor] = useState("");
  const [password, setPassword] = useState("");
  const { ids } = useParams();

  console.log(ids, commentId)
  const navigate = useNavigate(); // useHistory 대신 useNavigate를 사용
  const deletePost = () => {
    axios.delete(`http://localhost:8000/post/posts/${ids}/comments/${commentId}`, { data: { author, password } })
      .then((response) => {
        if (response.status === 200) {
          alert("댓글이 삭제되었습니다.");
          navigate(0);
        } else {
          alert("댓글 삭제에 실패했습니다.");
        }
      })
      .catch((error) => {
        console.error("Deleting post failed", error);
        alert("게시글 삭제에 실패했습니다.");
      });
  };

  return (
    <div style={{ display: showModal ? "block" : "none" }}>
      <span onClick={handleClose}>X</span>
      <form onSubmit={(e) => e.preventDefault()}>
        <input
          type="text"
          placeholder="Username"
          value={author}
          onChange={(e) => setAuthor(e.target.value)}
        />
        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />
        <button onClick={deletePost}>댓글 삭제</button>
      </form>
    </div>
  );
}

export default CommentDeleteModal;
