import DragAndDropFileFacility from "@/components/domain/settings/DragAndDropFileFacility";
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
      <div style={{ padding: 3 }} />
      <div className="text-center">
        <div style={{ padding: 10 }} />
        <Tabs defaultValue="facilityData">
          <TabsList>
            <TabsTrigger value="facilityData">설계 데이터</TabsTrigger>
            <TabsTrigger value="receipeData">레시피 데이터</TabsTrigger>
          </TabsList>
          <TabsContent value="facilityData">
          <DragAndDropFileFacility></DragAndDropFileFacility>
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
