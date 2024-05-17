// import { Button } from "@/components/base/button";
// import { useGraphDataStore } from "@/stores/GraphData";
// import React, { useState } from "react";
// import Modal from "react-modal";
// import {
//   Card,
//   CardTitle,
//   CardHeader,
//   CardContent,
// } from "@/components/base/card";
// import Lottie from "lottie-react";
// import ChartLoadingGIF from "@/assets/chartloading.json";
// import BokehPlot from "@/components/common/BokehPlot";
// import SamsungLogo from "@/assets/images/Logo_BLUE.png";
// import { navigate } from "react-router-dom";
// import axios from "axios";

// function ModifyPost() {
//   const [post, setPost] = useState(null);

//   const updatePost = () => {
//     axios
//       .put(`http://localhost:8000/post/posts/${ids}`, {
//         title: post.title, // 수정된 제목
//         content: post.content, // 수정된 내용
//         // 필요한 다른 필드들...
//       })
//       .then((response) => {
//         if (response.status === 200) {
//           alert("게시글이 수정되었습니다.");
//           navigate("/board"); // 수정 후 목록 페이지로 리디렉션
//         } else {
//           alert("게시글 수정에 실패했습니다.");
//         }
//       })
//       .catch((error) => {
//         console.error("Updating post failed", error);
//         alert("게시글 수정 중 오류가 발생했습니다.");
//       });
//   };
//   return (
//     <div>
//       <input
//         type="text"
//         value={post.title}
//         onChange={(e) => setPost({ ...post, title: e.target.value })}
//       />
//       <textarea
//         value={post.content}
//         onChange={(e) => setPost({ ...post, content: e.target.value })}
//       />
//       <button onClick={updatePost}>게시글 수정</button>
//     </div>
//   );
// }

// export default ModifyPost;
