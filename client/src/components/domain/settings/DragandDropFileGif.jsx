import React from "react";
import Lottie from "lottie-react";
import DragAndDropGif from "../../../assets/draganddrop.json";

function DragAndDropAni() {
    return (
        <div style={{ display: 'grid', placeItems: 'center', height: "auto" }}>
        <Lottie animationData={DragAndDropGif} style={{ width: 400 }} />
    </div>
    );
  }
  
  export default DragAndDropAni;