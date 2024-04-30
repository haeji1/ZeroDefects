import DragAndDropFileUpload from "@/components/domain/settings/DragAndDrop";
function Settings() {
  return (
    <>
      <div style={{ padding: 10 }} />
      <div className="text-center">
        <h1 className="scroll-m-20 text-4xl font-extrabold tracking-tight lg:text-5xl">
          설비 데이터 관리
        </h1>
        <div style={{ padding: 20 }} />
        <DragAndDropFileUpload></DragAndDropFileUpload>
      </div>
    </>
  );
}

export default Settings;
