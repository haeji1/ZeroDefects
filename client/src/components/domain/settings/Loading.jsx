import React from "react";
import Lottie from "lottie-react";
import DragAndDropGif from "../../../assets/loading2.json";

// 업로드 이미지
function DragAndDropAni() {
  return (
    <div className="fixed inset-0 flex items-center justify-center z-50">
      <div className="absolute inset-0 bg-black opacity-50"></div>
      <Lottie animationData={DragAndDropGif} style={{ width: 250 }} />
    </div>
  );
}

export default DragAndDropAni;
