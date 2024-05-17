import { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom"; // useHistory 대신 useNavigate를 사용
import {
  Card,
  CardContent,
  CardHeader,
  CardTitle,
} from "@/components/base/card";
import BokehPlot from "@/components/common/BokehPlot";
import ReadComment from "../comment/ReadComments";
import CreateComments from "../comment/CreateComment";
import axios from "axios"; // 상단에 엑시오스 import
import Loading from "@/components/domain/settings/Loading";

function BoardDetail() {
  const { ids } = useParams();
  const [post, setPost] = useState(null);
  const navigate = useNavigate(); // useHistory 대신 useNavigate를 사용
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
    return <div><Loading/></div>;
  }

  return (
    <div style={{ marginLeft: "20%", marginRight: "20%" }}>
      <div style={{ padding: "20px" }} />
      <h2 className="scroll-m-20 border-b pb-2 text-2xl font-semibold tracking-tight first:mt-0">
        {post.title}
      </h2>
      <p>유저 이름: {post.author}</p>
      <p>날짜: {post.date}</p>
      <p>글: {post.content}</p>
      <div className="flex flex-col ">
        <Card className="mr-5 min-h-[800px]">
          <CardHeader>
            <CardTitle>Graph Overview</CardTitle>
          </CardHeader>
          <CardContent>
            {post.graphData.map((data, index) => (
              <div key={index}>
                <BokehPlot data={data} />
              </div>
            ))}
          </CardContent>
        </Card>
      </div>
      <CreateComments postId={ids} />
      <ReadComment postId={ids} />
      <div>
        <input
          type="text"
          placeholder="작성자"
          value={author}
          onChange={(e) => setAuthor(e.target.value)}
        />
        <input
          type="password"
          placeholder="비밀번호"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />
        <button onClick={deletePost}>게시글 삭제</button>
      </div>
      
    </div>
    
  );
}

export default BoardDetail;
