import { Button } from "@/components/base/button";
import axios from "axios";
import DragAndDropAni from "./DragandDropFileGif";
import FileDataForRecipe from "@/stores/FileDataForRecipe";
import FileListForRecipe from "./FileListForRecipe";
import { ScrollArea } from "@radix-ui/react-scroll-area";
import { useState } from "react";

function DragAndDropFileRecipe() {
  const { files, addFiles, clearFiles, addOrUpdateFiles } = FileDataForRecipe(
    (state) => ({
      addFiles: state.addFiles,
      files: state.files,
      clearFiles: state.clearFiles,
      addOrUpdateFiles: state.addOrUpdateFiles,
    })
  );

  const [loading, setLoding] = useState(true);

  const handleDragOver = (e) => {
    e.preventDefault(); // 기본 이벤트를 방지합니다.
  };

  const handleDrop = (e) => {
    e.preventDefault();
    const files = e.dataTransfer.files; // 드롭된 파일들을 가져옵니다.
    if (files.length) {
      handleFiles(files);
    }
  };

  const handleFiles = (uploadedFiles) => {
    const validFiles = Array.from(uploadedFiles).filter(
      (file) =>
        file.type === "application/vnd.ms-excel" ||
        file.type ===
          "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    );

    if (validFiles.length < uploadedFiles.length) {
      alert(
        "유효하지 않은 파일 형식이 포함되어 있습니다. xls 혹은 xlsx 파일만 업로드해주세요."
      );
    }

    for (const file of validFiles) {
      // 변경된 부분: 여기서 files는 상태에서 가져온 파일 리스트입니다.
      const hasFile = files.some(
        (existingFile) => existingFile.name === file.name
      );

      if (hasFile) {
        const overwrite = window.confirm(
          `${file.name} 파일이 이미 존재합니다. 덮어쓰시겠습니까?`
        );
        if (overwrite) {
          addOrUpdateFiles([file]);
        }
      } else {
        addOrUpdateFiles([file]);
      }
    }
  };

  const handleFileSelect = (e) => {
    const files = e.target.files;
    if (files.length) {
      handleFiles(files);
    }
  };
  const uploadFiles = (e) => {
    e.preventDefault();

    if (files.length == 0) {
      alert("파일이 없습니다.");
      return;
    }

    let formData = new FormData();

    files.forEach((file) => {
      formData.append("files", file);
    });

    console.log(Array.from(formData));
    console.log("첨부파일 보내기 시작");

    // 수정
    axios
      .post("http://localhost:8000/setting", formData, {
        headers: {
          "Content-Type":
            "application/vnd.ms-excel" ||
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        },
      })
      .then((res) => {
        console.log(res.data);
        console.log("첨부파일 보내기 성공");
        clearFiles(); // 업로드 후 파일 목록 지우기
      })
      .catch((err) => {
        console.error(err);
        console.log("첨부파일 보내기 실패");
      });
  };
  return (
    <div style={{ marginLeft: "100px", marginRight: "100px" }}>
      레시피
      <div
        style={{
          border: "2px dashed #ccc",
          padding: "30px",
          cursor: "pointer",
        }}
        onDragOver={handleDragOver}
        onDrop={handleDrop}
        onClick={() => document.getElementById("fileInput").click()}
      >
        <DragAndDropAni></DragAndDropAni>
        <input
          id="fileInput"
          type="file"
          style={{ display: "none" }}
          onChange={handleFileSelect}
          accept=".xls, .xlsx"
        />
        <h2>여기에 파일을 끌어다 놓거나 클릭하여 선택하세요.</h2>
      </div>
      <div style={{ paddingTop: "20px" }} />
      <FileListForRecipe />
      <div style={{ paddingTop: "20px" }} />
      <Button onClick={uploadFiles}>저장</Button>
    </div>
  );
}

export default DragAndDropFileRecipe;
