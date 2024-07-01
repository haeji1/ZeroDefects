import { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import axios from "axios";
import Loading from "@/components/domain/settings/Loading";
import PostContent from "./PostContent";
import DeletePostDialog from "./DeletePostDialog";
import ReadComment from "../comment/ReadComments";
import CreateComments from "../comment/CreateComment";

function BoardDetail() {
  const { ids } = useParams();
  const [post, setPost] = useState(null);
  const navigate = useNavigate();
  const [author, setAuthor] = useState("");
  const [password, setPassword] = useState("");

  useEffect(() => {
    fetch(`http://localhost:8000/post/posts/${ids}`)
      .then((response) => response.json())
      .then((data) => setPost(data))
      .catch((error) => console.error("Fetching post failed", error));
  }, [ids]);

  const deletePost = () => {
    axios
      .delete(`http://localhost:8000/post/posts/${ids}`, {
        data: { author, password },
      })
      .then((response) => {
        if (response.status === 200) {
          alert("게시글이 삭제되었습니다.");
          navigate("/board");
        } else {
          alert("게시글 삭제에 실패했습니다.");
        }
      })
      .catch((error) => {
        console.error("Deleting post failed", error);
        alert("게시글 삭제 중 오류가 발생했습니다.");
      });
  };

  if (!post) {
    return (
      <div>
        <Loading />
      </div>
    );
  }

  return (
    <div style={{ marginLeft: "5%", marginRight: "5%", marginBottom: "5%" }}>
      <div style={{ padding: "20px" }} />
      <PostContent post={post}
        setAuthor={setAuthor}
        setPassword={setPassword}
        deletePost={deletePost} />
      <ReadComment postId={ids} />
      <div style={{ padding: "5px" }} />
      <CreateComments postId={ids} />
    </div>
  );
}

export default BoardDetail;
