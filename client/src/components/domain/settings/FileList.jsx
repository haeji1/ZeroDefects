import React from "react";
import FileDataForSettings from "@/stores/FileDataForSettingStore";
import {
  Table,
  TableBody,
  TableCaption,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
  TableFooter,
} from "@/components/base/table";
import { ScrollArea } from "@/components/base/scroll-area";
import {formatFileSize} from "@/lib/formatFileSize"

const FileList = () => {
  const { files, deleteFile } = FileDataForSettings((state) => ({
    files: state.files,
    deleteFile: state.deleteFile,
  }));

  return (
    <div style={{ width: "100%", height: "300px", textAlign: ""}}>
      <ScrollArea className="h-[100%] w-[100%] rounded-md border">
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead>
                파일 이름
              </TableHead>
              <TableHead>
                크기
              </TableHead>
              <TableHead>
                작업
              </TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {files.map((file, index) => (
              <TableRow key={index}>
                <TableCell>{file.name}</TableCell>
                {/* <TableCell>{`${file.size} bytes`}</TableCell> */}
                <TableCell>{formatFileSize(file.size)}</TableCell>
                <TableCell>
                  <button onClick={() => deleteFile(file.name)}>삭제</button>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </ScrollArea>
    </div>
  );
}; 

export default FileList;
