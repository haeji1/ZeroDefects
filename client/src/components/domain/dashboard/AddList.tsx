import {
    Select,
    SelectContent,
    SelectItem,
    SelectTrigger,
    SelectValue,
} from "@/components/base/select";
import { ScrollArea } from "@/components/base/scroll-area";
import {
    Command,
    CommandEmpty,
    CommandGroup,
    CommandInput,
    CommandItem,
} from "@/components/base/command";
import { Check, ChevronsUpDown } from "lucide-react";
import { cn } from "@/lib/utils";
import { Button } from "@/components/base/button";
import { Popover, PopoverContent, PopoverTrigger } from "@/components/base/popover";
import { useState, useEffect } from "react";
import { Label } from "@/components/base/label";
import { useFacilityStore, Facility, useBatchStore } from "@/stores/Facility"
import { fetchFacilityInfos, getBatches } from "@/apis/api/api";
import { Card } from "@/components/base/card";
import { useBookmarkStore } from "@/stores/Bookmark";
import { useToast } from "@/hooks/use-toast";
import { AxiosResponse } from "axios";

function Addlist() {

    const [selectedFacility, setSelectedFacility] = useState<string>("")
    const [selectedParameter, setSelectedParameter] = useState<string | null>("")
    const [isButtonEnabled, setIsButtonEnabled] = useState<boolean>(false);
    const { facilityList, updateFacilityList } = useFacilityStore();
    const { addBatch } = useBatchStore();
    const { addBookmark } = useBookmarkStore()
    const [open, setOpen] = useState(false)
    const { toast } = useToast()


    // DB에 존재하는 설비 리스트들이랑, 해당 설비의 파라미터들 마운트 시에 가져오기
    useEffect(() => {
        const fetchData = async () => {
            const res: AxiosResponse | undefined = await fetchFacilityInfos();
            const data: Facility = {}
            const result: { [key: string]: string[] } = res?.data.result;
            for (const [facilityName, value] of Object.entries(result)) {
                data[facilityName] = {
                    parameters: value,
                    batches: undefined
                }
            }
            updateFacilityList(data)
            console.log(data);
        };
        fetchData();
    }, []);

    useEffect(() => {
        const handleAddButtonEnability = () => {
            selectedFacility && selectedParameter ? setIsButtonEnabled(true) : setIsButtonEnabled(false)
        }
        handleAddButtonEnability();
    }, [selectedFacility, selectedParameter]);

    const handleAddButton = async () => {

        const newBookmark = {
            facility: selectedFacility,
            parameter: selectedParameter!,
            selectedBatchName: null
        }

        if (facilityList[selectedFacility].batches === undefined) {
            const res: AxiosResponse<any, any> | undefined = await getBatches(selectedFacility)
            addBatch(selectedFacility, res?.data.batches);
            addBookmark(newBookmark);
        }
        else { addBookmark(newBookmark) }
        setSelectedParameter(null);
        toast({
            title: `목록 추가 완료`,
            description: `${selectedFacility} 설비의 ${selectedParameter} 인자를 리스트에 추가하였습니다.`,
        })
    }

    return (
        <Card className="flex flex-col gap-5 my-4 px-5 py-5">
            <Label htmlFor="" className="font-bold text-[20px]">목록 추가</Label>
            <div className="grid grid-cols-5 gap-3">
                <div className="col-span-2 grid w-full items-center gap-1.5">
                    <Label htmlFor="facility">설비명</Label>
                    <Select onValueChange={(val) => {
                        setSelectedFacility(val);
                        setSelectedParameter(null);
                    }}>
                        <SelectTrigger className="w-full self-center">
                            <SelectValue placeholder="설비 선택" />
                        </SelectTrigger>
                        <SelectContent>
                            <ScrollArea className="max-h-[400px] w-full">
                                {Object.keys(facilityList).map(facility => (
                                    <SelectItem key={facility} value={facility} >{facility}</SelectItem>
                                ))}
                            </ScrollArea>
                        </SelectContent>
                    </Select>
                </div>
                <div className="col-span-3 grid w-full  items-center gap-1.5">
                    <Label htmlFor="email">파라미터명</Label>
                    <Popover open={open} onOpenChange={setOpen}>
                        <PopoverTrigger asChild>
                            <Button
                                variant="outline"
                                role="combobox"
                                aria-expanded={open}
                                className="w-full justify-between"
                            >
                                {selectedFacility ? selectedParameter ? selectedParameter : "선택된 파라미터가 없습니다." : "설비를 먼저 선택해주세요."}
                                <ChevronsUpDown className="ml-2 h-4 w-4 shrink-0 opacity-50" />
                            </Button>
                        </PopoverTrigger>
                        <PopoverContent className="w-full p-0">
                            <ScrollArea className="h-[400px] w-full">
                                <Command>
                                    <CommandInput placeholder="파라미터를 검색해주세요." />
                                    <CommandEmpty>검색된 파라미터 없음</CommandEmpty>
                                    <CommandGroup>
                                        {selectedFacility ? facilityList[selectedFacility].parameters.map((param: string) => (
                                            <CommandItem
                                                key={param}
                                                value={param}
                                                onSelect={() => {
                                                    setSelectedParameter(param)
                                                    setOpen(false)
                                                }}
                                            >
                                                <Check
                                                    className={cn(
                                                        "mr-2 h-4 w-4",
                                                        selectedParameter === param ? "opacity-100" : "opacity-0"
                                                    )}
                                                />
                                                {param}
                                            </CommandItem>
                                        )) : null}
                                    </CommandGroup>
                                </Command>
                            </ScrollArea>
                        </PopoverContent>
                    </Popover>

                </div>
            </div>
            <div className="ml-auto">
                <Button disabled={!isButtonEnabled} onClick={handleAddButton}>추가</Button>
            </div>
        </Card >
    )
}

export default Addlist;