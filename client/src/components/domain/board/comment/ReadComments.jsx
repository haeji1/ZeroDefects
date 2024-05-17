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
import CommentDeleteDialog from './CommentDeleteDialog';

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
      {comments.length > 0 ? (
        <ul>
          {comments.map((comment, index) => (
            <li key={index}>
              <Card>
                <CardHeader>{comment.author}</CardHeader>
                <CardContent>{comment.content}</CardContent>
                <CardFooter>
                <CommentDeleteDialog commentId={comment.id} onDelete={deletePost} />
                </CardFooter>
              </Card>
            </li>
          ))}
        </ul>
      ) : (
        <p>No comments yet.</p>
      )}
    </div>
  );
}

export default ReadComments;
