import FileDataForRecipe from "@/stores/FileDataForRecipe";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/base/table";
import { ScrollArea } from "@/components/base/scroll-area";
import { formatFileSize } from "@/lib/formatFileSize";


const FileListForRecipe = () => {
  const { files, deleteFile } = FileDataForRecipe((state) => ({
    files: state.files,
    deleteFile: state.deleteFile,
  }));

  return (
    <div style={{ width: "100%", height: "300px" }}>
      <ScrollArea className="h-[100%] w-[100%] rounded-md border">
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead>
                <div className="text-center">파일 이름</div>
              </TableHead>
              <TableHead>
                <div className="text-center">크기</div>
              </TableHead>
              <TableHead>
                <div className="text-center">작업</div>
              </TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {files.map((file, index) => (
              <TableRow key={index}>
                <TableCell>{file.name}</TableCell>
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

export default FileListForRecipe;
