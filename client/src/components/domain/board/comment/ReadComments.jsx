import React, { useEffect, useState } from "react";
import axios from "axios";
import useCommentStore from "@/stores/Comment";
import { useParams, useNavigate } from "react-router-dom";
import {
  Card,
  CardHeader,
  CardContent,
  CardFooter,
} from "@/components/base/card";
import CommentDeleteDialog from "./CommentDeleteDialog";

function ReadComments({ postId }) {
  const comments = useCommentStore((state) => state.comments);
  const setComments = useCommentStore((state) => state.setComments);
  const [deleteFormData, setDeleteFormData] = useState({
    id: "",
    password: "",
  });
  const { ids } = useParams();
  const navigate = useNavigate();
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

  const deletePost = (commentId, author, password) => {
    axios
      .delete(
        `http://localhost:8000/post/posts/${postId}/comments/${commentId}`,
        {
          data: {
            author: author, // 이 부분이 실제로 댓글 작성자의 이름이라면 그대로 두고, 아니라면 적절히 수정해야 합니다.
            password: password,
          },
        }
      )
      .then((response) => {
        if (response.status === 200) {
          alert("댓글이 삭제되었습니다.");
          navigate(0); // 페이지를 새로고침합니다.
        } else {
          alert("댓글 삭제에 실패했습니다.");
        }
      })
      .catch((error) => {
        console.error("Deleting post failed", error);
        alert("댓글 삭제에 실패했습니다.");
      });
  };
  return (
    <div>
      <div style={{ padding: "10px", borderBottom: "solid 1px" }}>
        <h2 className="text-xl font-semibold tracking-tight text-gray-800">
          Comments ({comments.length})
        </h2>
      </div>
      {comments.length > 0 ? (
        <ul>
          {comments.map((comment, index) => (
            <li key={index}>
              <div
                style={{
                  paddingLeft: "20px",
                  paddingRight: "20px",
                  paddingTop: "10px",
                  paddingBottom: "10px",
                  borderBottom: "solid 1px #e3e3e3",
                }}
              >
                <div className="flex items-center justify-between">
                  <div className="flex items-center space-x-4">
                    <p className="scroll-m-20 text-xl font-semibold tracking-tight">
                      {comment.author}
                    </p>
                    <p className="text-sm text-gray-500">{comment.date}</p>
                  </div>
                  <CommentDeleteDialog
                    commentId={comment.id}
                    onDelete={deletePost}
                  />
                </div>
                <div style={{ padding: "3px" }}></div>
                <div>{comment.content}</div>
              </div>
            </li>
          ))}
        </ul>
      ) : (
        <p className="text-gray-500" style={{paddingLeft: "10px",paddingTop: "10px"}}>No comments yet.</p>
      )}
    </div>
  );
}

export default ReadComments;
