import { create } from "zustand";

// 상태 인터페이스 정의
interface FileDataForSettingsState {
  files: any[];
  addFiles: (newFiles: any[]) => void;
  deleteFile: (fileName: string) => void;
  clearFiles: () => void;
  addOrUpdateFiles: (newFiles: any[]) => void;
}

const FileDataForSettings = create<FileDataForSettingsState>((set) => ({
  files: [],
  addFiles: (newFiles) =>
    set((state) => ({ files: [...state.files, ...newFiles] })),
  deleteFile: (fileName: string) =>
    set((state) => ({
      files: state.files.filter((file) => file.name !== fileName),
    })),
  clearFiles: () => set({ files: [] }),
  addOrUpdateFiles: (newFiles) =>
    set((state) => {
      const updatedFiles = [...state.files];

      newFiles.forEach((newFile) => {
        const index = updatedFiles.findIndex(
          (file) => file.name === newFile.name
        );
        if (index !== -1) {
          // 파일 이름이 이미 존재하면 업데이트 (이 경우, confirm 로직은 컴포넌트에서 처리)
          updatedFiles[index] = newFile;
        } else {
          // 새 파일 추가
          updatedFiles.push(newFile);
        }
      });

      return { files: updatedFiles };
    }),
}));

export default FileDataForSettings;
