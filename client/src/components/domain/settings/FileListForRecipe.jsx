import React from "react";
import FileDataForRecipe from "@/stores/FileDataForRecipe";
import {
    Table,
    TableBody,
    TableCaption,
    TableCell,
    TableHead,
    TableHeader,
    TableRow,
  } from "@/components/base/table"
  

const FileListForRecipe = () => {
  const { files, deleteFile } = FileDataForRecipe((state) => ({
    files: state.files,
    deleteFile: state.deleteFile,
  }));

  return (
    <Table>
    <TableHeader>
      <TableRow>
        <TableHead>파일 이름</TableHead>
        <TableHead>크기</TableHead>
        <TableHead>작업</TableHead>
      </TableRow>
    </TableHeader>
    <TableBody>
      {files.map((file, index) => (
        <TableRow key={index}>
          <TableCell>{file.name}</TableCell>
          <TableCell>{`${file.size} bytes`}</TableCell>
          <TableCell>
            <button onClick={() => deleteFile(file.name)}>삭제</button>
          </TableCell>
        </TableRow>
      ))}
    </TableBody>
  </Table>
  );
};

export default FileListForRecipe;
