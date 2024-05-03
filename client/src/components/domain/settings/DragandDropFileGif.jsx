import React from "react";
import Lottie from "lottie-react";
import DragAndDropGif from "../../../assets/draganddrop.json";

// 업로드 이미지
function DragAndDropAni() {
    return (
        <div style={{ display: 'grid', placeItems: 'center', height: "auto" }}>
        <Lottie animationData={DragAndDropGif} style={{ width: 250 }} />
    </div>
    );
  }
  
  export default DragAndDropAni;