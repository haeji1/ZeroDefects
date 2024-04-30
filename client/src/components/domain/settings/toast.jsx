import {
    AlertDialog,
    AlertDialogAction,
    AlertDialogCancel,
    AlertDialogContent,
    AlertDialogDescription,
    AlertDialogFooter,
    AlertDialogHeader,
    AlertDialogTitle,
    AlertDialogTrigger,
  } from "@/components/ui/alert-dialog"
  import { Button } from "@/components/ui/button"
  
  export function AlertDialogDemo() {
    return (
      <AlertDialog>
        <AlertDialogTrigger asChild>
          <Button variant="outline">Show Dialog</Button>
        </AlertDialogTrigger>
        <AlertDialogContent>
          <AlertDialogHeader>
            <AlertDialogTitle>Are you absolutely sure?</AlertDialogTitle>
            <AlertDialogDescription>
              This action cannot be undone. This will permanently delete your
              account and remove your data from our servers.
            </AlertDialogDescription>
          </AlertDialogHeader>
          <AlertDialogFooter>
            <AlertDialogCancel>Cancel</AlertDialogCancel>
            <AlertDialogAction>Continue</AlertDialogAction>
          </AlertDialogFooter>
        </AlertDialogContent>
      </AlertDialog>
    )
  }
  import { useState } from "react";
import axios from "axios";
import { Button } from "@/components/base/button";
import { Input } from "@/components/base/input";
import {
  AlertDialog,
  AlertDialogAction,
  AlertDialogCancel,
  AlertDialogContent,
  AlertDialogDescription,
  AlertDialogFooter,
  AlertDialogHeader,
  AlertDialogTitle,
  AlertDialogTrigger,
} from "@/components/base/alert-dialog";

function UploadedFileSection() {
  const [files, setFiles] = useState([]);

  const handleFilesChange = (e) => {
    setFiles(Array.from(e.target.files));
  };

  const deleteFile = (fileName) => {
    setFiles(files.filter((file) => file.name !== fileName));
  };

  const onReset = () => {
    setFiles([]);
  };

  const uploadFiles = (e) => {
    e.preventDefault();

    if (files.length == 0) {
        alert("파일이 없습니다.")
      return;
    }

    let formData = new FormData();

    files.map((file) => {
      formData.append("file", file);
    });

    console.log(Array.from(formData));
    console.log("첨부파일 보내기 시작");

    // 수정
    axios
      .post("http://localhost:8000/upload/csv", formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      })
      .then((res) => {
        console.log(res.data);
        console.log("첨부파일 보내기 성공");
      })
      .catch((err) => {
        console.error(err);
        console.log("첨부파일 보내기 실패");
      });
  };

  return (
    <>
      <div
        style={{
          display: "flex",
          justifyContent: "center", // 가로 방향으로 중앙 정렬
          alignItems: "center", // 세로 방향으로 중앙 정렬
          height: "100vh", // 부모 컨테이너의 높이를 화면 높이와 동일하게 설정
          flexDirection: "column", // 자식 요소들을 세로로 배열
        }}
      >
        <form
          style={{
            display: "flex",
            justifyContent: "center",
            alignItems: "center",
            gap: "10px",
            width: "60%",
          }}
          onSubmit={uploadFiles}
        >
          <Input
            id="fileInput"
            type="file"
            // multiple={true}
            onChange={handleFilesChange}
            accept=".csv"
          />
          <Button onClick={uploadFiles}>분석!!</Button>
        </form>
        <div>
          {files.map((file, index) => (
            <div
              key={index}
              style={{ display: "flex", alignItems: "center", gap: "10px" }}
            >
              {file.name}
              <button onClick={() => deleteFile(file.name)}>삭제</button>
            </div>
          ))}
        </div>
        <Button onClick={onReset}> 전체 삭제 </Button>
      </div>
    </>
  );
}
export default UploadedFileSection;
