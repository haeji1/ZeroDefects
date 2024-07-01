import { Button } from "@/components/base/button";
import axios from "axios";
import DragAndDropAni from "./DragandDropFileGif";
import FileDataForSettings from "@/stores/FileDataForSettingStore";
import FileList from "./FileList";
import { useState } from "react";
import Loading from "./Loading";

function DragAndDropFileFacility() {
  const { files ,addFiles, clearFiles, addOrUpdateFiles } = FileDataForSettings(
    (state) => ({
      addFiles: state.addFiles,
      files: state.files,
      clearFiles: state.clearFiles,
      addOrUpdateFiles: state.addOrUpdateFiles,
    })
  );
  const [isLoading, setIsLoading] = useState(false);
  
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
      (file) => file.type === "text/csv"
    );

    if (validFiles.length < uploadedFiles.length) {
      alert(
        "유효하지 않은 파일 형식이 포함되어 있습니다. CSV 파일만 업로드해주세요."
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
        addFiles([file]);
      }
    }
  };

  const handleFileSelect = (e) => {
    const files = e.target.files;
    if (files.length) {
      handleFiles(files);
    }
    // 파일이 업로드 하고 삭제하고 또 업로드 할 때 반영 안되는 거 오류 해결 코드
    e.target.value = '';
  };
  const uploadFiles = (e) => {
    e.preventDefault();

    if (files.length == 0) {
      alert("파일이 없습니다.");
      return;
    }

    let formData = new FormData();

    files.forEach((file) => {
      formData.append("files", file); // 이제 file은 실제 File 객체를 포함하고 있습니다.
    });
    setIsLoading(true);
    console.log(Array.from(formData));
    console.log("첨부파일 보내기 시작");

    // 수정
    axios
      .post("http://localhost:8000/facility/write", formData, {
        headers: {
          "Content-Type": "text/csv",
        },
      })
      .then((res) => {
        console.log(res.data);
        console.log("첨부파일 보내기 성공");
        clearFiles(); // 업로드 후 파일 목록 지우기
        alert( files.length + "개 파일 업로드 완료")
        setIsLoading(false);
      })
      .catch((err) => {
        console.error(err);
        console.log("첨부파일 보내기 실패");
        alert("실패")
        setIsLoading(false);
      });
  };
  return (
    <div style={{ marginLeft: "100px", marginRight: "100px" }}>
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
          multiple={true}
          style={{ display: "none" }}
          onChange={handleFileSelect}
          accept=".csv"
        />
        <h2>여기에 파일을 끌어다 놓거나 클릭하여 선택하세요.</h2>
      </div>
      <div style={{ paddingTop: "20px" }} />
      <FileList/>
      <div>{files.length}개의 파일</div>

      <div style={{ paddingTop: "20px" }} />
      {isLoading ? (
        // 로딩 중일 때 로딩 컴포넌트 렌더링
        <div>
          <Loading/>
        </div>
      ) : (
        // 로딩 완료 후 버튼 렌더링
        <Button onClick={uploadFiles}>저장</Button>
      )}
    </div>
  );
}

export default DragAndDropFileFacility;
