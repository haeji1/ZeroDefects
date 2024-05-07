import {
    Select,
    SelectContent,
    SelectItem,
    SelectTrigger,
    SelectValue,
} from "@/components/base/select";
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
import { useBatchStore, useFacilityStore } from "@/stores/Facility"
import { fetchFacilityInfos, getBatches } from "@/apis/api/api";
import { Card } from "@/components/base/card";
import { useBookmarkStore } from "@/stores/Bookmark";

function Addlist() {

    const [selectedFacility, setSelectedFacility] = useState()
    const [selectedParameter, setSelectedParameter] = useState()
    const [isButtonEnabled, setIsButtonEnabled] = useState(false);
    const { facilityList, updateFacility } = useFacilityStore();
    const { batchList, addBatch } = useBatchStore();
    const { addBookmark } = useBookmarkStore()
    const [open, setOpen] = useState(false)

    // DB에 존재하는 설비 리스트들이랑, 해당 설비의 파라미터들 마운트 시에 가져오기
    useEffect(() => {
        const fetchData = async () => {
            const res = await fetchFacilityInfos();
            updateFacility(res.data.result)
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
            parameter: selectedParameter,
        }

        if (batchList[selectedFacility] === undefined) {
            const res = await getBatches(selectedFacility)
            addBatch(selectedFacility, res.data.batches);
            addBookmark(newBookmark);
        }
        else { addBookmark(newBookmark) }
        setSelectedFacility(null);
        setSelectedParameter(null);
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
                            {Object.keys(facilityList).map(facility => (
                                <SelectItem key={facility} value={facility} >{facility}</SelectItem>
                            ))}
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
                        <PopoverContent className="w-[full] p-0">
                            <Command>
                                <CommandInput placeholder="파라미터를 검색해주세요." />
                                <CommandEmpty>검색된 파라미터 없음</CommandEmpty>
                                <CommandGroup>

                                    {selectedFacility ? facilityList[selectedFacility].map((param) => (
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