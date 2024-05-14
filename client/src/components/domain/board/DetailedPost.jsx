import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import {
  Card,
  CardContent,
  CardHeader,
  CardTitle,
} from "@/components/base/card";
import BokehPlot from "@/components/common/BokehPlot";
import ReadComment from "./ReadComments";
import CreateComments from "./CreateComment";

function BoardDetail() {
  const { ids } = useParams(); // URL에서 ids 파라미터 가져오기
  const [post, setPost] = useState(null);

  useEffect(() => {
    fetch(`http://localhost:8000/post/posts/${ids}`) // 백엔드 API 엔드포인트에 맞게 수정
      .then((response) => response.json())
      .then((data) => setPost(data))
      .catch((error) => console.error("Fetching post failed", error));
  }, [ids]);

  if (!post) {
    return <div>Loading...</div>;
  }

  return (
    <div>
      <h1>제목: {post.title}</h1>
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
    <CreateComments postId = {ids}/>
    <ReadComment postId = {ids}/>
    </div>
  );
}

export default BoardDetail;
