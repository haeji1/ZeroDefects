import UploadedFileSection from "@/components/domain/settings/UploadedFilesSection";

function Settings() {
  return (
    <>
      <h1 className="scroll-m-20 text-4xl font-extrabold tracking-tight lg:text-5xl" style={{display: "flex", justifyContent: "center"}}>
        파일 CRUD
      </h1>
      <UploadedFileSection></UploadedFileSection>
    </>
  );
}

export default Settings;
