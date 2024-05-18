import React from "react";
import {
  Card,
  CardContent,
  CardHeader,
  CardTitle,
} from "@/components/base/card";
import BokehPlot from "@/components/common/BokehPlot";
import DeletePostDialog from "./DeletePostDialog";
function PostContent({ post, setAuthor, setPassword, deletePost }) {
  return (
    <>
      <div className="p-6 border border-gray-200 rounded-lg shadow-sm">
        <div className="flex items-center justify-between mb-4">
          <div>
            <h2 className="text-xl font-semibold tracking-tight text-gray-800">
              {post.title}
            </h2>
            <div style={{padding: "3px"}}/>
              <div className="text-sm text-gray-500">닉네임: {post.author}</div>
              <div className="text-sm text-gray-500">날짜: {post.date}</div>
          </div>
          
          <div className="p-2"><DeletePostDialog
                  setAuthor={setAuthor}
                  setPassword={setPassword}
                  deletePost={deletePost}
          /></div>
        </div>
        <div className="flex flex-col">
          <Card className="mr-5 min-h-[100px]">
            <CardHeader>
              <CardTitle>Graph Overview</CardTitle>
            </CardHeader>
            <CardContent>
              {post.graphData.map((data, index) => (
                <div key={index} className="mb-4 last:mb-0">
                  <BokehPlot data={data} />
                </div>
              ))}
            </CardContent>
          </Card>
        </div>
        <div style={{padding:"10px"}}/>
        <p className="mb-4 border-gray-200 pb-2 text-gray-700">
          {post.content}
        </p>

      </div>
    </>
  );
}

export default PostContent;
