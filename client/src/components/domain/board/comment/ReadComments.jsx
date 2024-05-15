import React, { useEffect, useState } from "react";
import axios from "axios";
import useCommentStore from "@/stores/Comment";
import CommentDeleteModal from "./CommentDeleteModal";

function ReadComments({ postId }) {
  const comments = useCommentStore((state) => state.comments);
  const setComments = useCommentStore((state) => state.setComments);
  const [showModal, setShowModal] = useState(false);
  const [currentCommentId, setCurrentCommentId] = useState(null);

  useEffect(() => {
    const fetchComments = async () => {
      try {
        const response = await axios.get(
          `http://localhost:8000/post/posts/${postId}/comments`
        );
        setComments(response.data.comments);
        console.log(response.data.comments);
      } catch (error) {
        console.error("댓글을 가져오는데 실패했습니다.", error);
      }
    };

    fetchComments();
  }, [postId, setComments]);

  // 삭제 버튼 클릭 이벤트 핸들러
  const handleDeleteClick = (commentId) => {
    setCurrentCommentId(commentId);
    setShowModal(true); // 모달을 보여줍니다.
  };

  return (
    <div>
      {comments.length > 0 ? (
        <ul>
          {comments.map((comment, index) => (
            <li key={index}>
              <p>
                {comment.author}: {comment.content}
              </p>
              <button onClick={() => handleDeleteClick(comment.id)}>
                삭제
              </button>
            </li>
          ))}
        </ul>
      ) : (
        <p>No comments yet.</p>
      )}
      <CommentDeleteModal
        showModal={showModal}
        handleClose={() => setShowModal(false)}
        commentId={currentCommentId}
        setComments={setComments} // 댓글 상태 업데이트 함수 전달
        comments={comments} // 현재 댓글 목록 전달
      />
    </div>
  );
}

export default ReadComments;
