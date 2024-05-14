import React, { useEffect } from 'react';
import axios from 'axios';
import Comment from './Comment';
import useCommentStore from '@/stores/Comment';

function ReadComments({ postId }) {
  const comments = useCommentStore(state => state.comments);
  const setComments = useCommentStore(state => state.setComments);

  useEffect(() => {
    const fetchComments = async () => {
      try {
        const response = await axios.get(`http://localhost:8000/post/posts/${postId}/comments`);
        setComments(response.data.comments);
        console.log(response.data.comments);
      } catch (error) {
        console.error("댓글을 가져오는데 실패했습니다.", error);
      }
    };

    fetchComments();
  }, [postId, setComments]);

  return (
    <div>
      {comments.length > 0 ? (
        <ul>
          {comments.map((comment, index) => (
            <li key={index}>
              <p>{comment.author}: {comment.content}</p>
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
