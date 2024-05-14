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


    // 설비명과 파라미터명 모두 선택되었을 때만 추가 버튼 활성화
    useEffect(() => {
        const handleAddButtonEnability = () => {
            selectedFacility && selectedParameter ? setIsButtonEnabled(true) : setIsButtonEnabled(false)
        }
        handleAddButtonEnability();
    }, [selectedFacility, selectedParameter]);



    // 설비 선택란 컴포넌트
    function FacilitySelect() {

        const changeFacility = (value: string) => {
            setSelectedParameter(null); // 기존 선택되었던 파라미터 값은 이전 설비이었을 때 선택되었던 파라미터이므로 상태를 null 값으로 초기화
            setSelectedFacility(value); // 선택된 설비의 정보를 변경
        }

        return (
            <div className="col-span-2 grid w-full items-center gap-1.5">
                <Label htmlFor="facility">설비명</Label>
                <Select value={selectedFacility} onValueChange={changeFacility} >
                    <SelectTrigger className="w-full self-center">
                        <SelectValue placeholder="설비 선택" />
                    </SelectTrigger>
                    <SelectContent>
                        <ScrollArea className="max-h-[400px] w-full">
                            {Object.keys(facilityList).map(facility => <SelectItem key={facility} value={facility} >{facility}</SelectItem>)}
                        </ScrollArea>
                    </SelectContent>
                </Select>
            </div>
        )
    }

    // 파라미터 선택란 컴포넌트
    function ParameterSelect() {

        const [open, setOpen] = useState(false)

        return (
            <div className="col-span-3 grid w-full  items-center gap-1.5">
                <Label htmlFor="email">파라미터명</Label>
                <Popover open={open} onOpenChange={setOpen}>
                    <PopoverTrigger asChild>
                        <Button
                            disabled={selectedFacility ? false : true}
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
        )
    }

    const handleAddButton = async () => {

        const res: AxiosResponse<any, any> | undefined = await getBatches(selectedFacility); // 추가하고자 하는 설비의 최신 배치 정보 가져오기

        if (res !== undefined) {
            addBatch(selectedFacility, res?.data.batches);
            addBookmark({
                facility: selectedFacility,
                parameter: selectedParameter!,
                selectedBatchName: null
            });
            setSelectedParameter(null); // 선택된 파라미터 초기화
            toast({
                title: `목록 추가 완료`,
                description: `${selectedFacility} 설비의 ${selectedParameter} 인자를 리스트에 추가하였습니다.`,
            })
        }

        else {
            toast({
                variant: "destructive",
                title: `목록 추가 실패`,
                description: `오류가 발생하였습니다. 네트워크 및 서버 상태를 점검해주세요.`,
            })
        }
    }

    return (
        <Card className="flex flex-col gap-5 my-4 px-5 py-5">
            <Label htmlFor="" className="font-bold text-[20px]">목록 추가</Label>
            <div className="grid grid-cols-5 gap-3">
                <FacilitySelect />
                <ParameterSelect />
            </div>
            <div className="ml-auto">
                <Button disabled={!isButtonEnabled} onClick={handleAddButton}>추가</Button>
            </div>
        </Card >
    )
}

export default Addlist;