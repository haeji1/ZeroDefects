import DragAndDropFileUpload from "@/components/domain/settings/DragAndDrop";
import {
  Tabs,
  TabsContent,
  TabsList,
  TabsTrigger,
} from "@/components/base/tabs";
import DragAndDropFileRecipe from "@/components/domain/settings/DragAndDropRecipe";

function Settings() {
  return (
    <>
      <div style={{ padding: 10 }} />
      <div className="text-center">
        <h1 className="scroll-m-20 text-4xl font-extrabold tracking-tight lg:text-5xl">
          데이터 관리
        </h1>
        <div style={{ padding: 15 }} />
        <Tabs defaultValue="tabs">
          <TabsList>
            <TabsTrigger value="facilityData">설계 데이터</TabsTrigger>
            <TabsTrigger value="receipeData">레시피 데이터</TabsTrigger>
          </TabsList>
          <TabsContent value="facilityData">
          <DragAndDropFileUpload></DragAndDropFileUpload>
          </TabsContent>
          <TabsContent value="receipeData">
            <DragAndDropFileRecipe></DragAndDropFileRecipe>
          </TabsContent>
        </Tabs>
      </div>
    </>
  );
}

export default Settings;
