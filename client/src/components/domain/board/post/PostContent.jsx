import React from "react";
import {
  Card,
  CardContent,
  CardHeader,
  CardTitle,
} from "@/components/base/card";
import BokehPlot from "@/components/common/BokehPlot";

function PostContent({ post }) {
  return (
    <>
      <h2 className="scroll-m-20 border-b pb-2 text-2xl font-semibold tracking-tight first:mt-0">
        {post.title}
      </h2>
      <p>유저 이름: {post.author}</p>
      <p>날짜: {post.date}</p>
      <p>글: {post.content}</p>
      <div className="flex flex-col ">
        <Card className="mr-5 min-h-[100px]">
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
    </>
  );
}

export default PostContent;
