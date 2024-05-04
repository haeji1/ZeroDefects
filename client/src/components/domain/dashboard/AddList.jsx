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
import { useFacilityStore } from "@/stores/Facility"
import { fetchFacilityInfos } from "@/apis/api/api";
import { Card } from "@/components/base/card";


function Addlist() {

    // 그래프 조회에 필요한 인자들
    const [facility, setFacility] = useState()
    const [parameter, setParameter] = useState()

    const { facilityList, updateFacility } = useFacilityStore();

    const [open, setOpen] = useState(false)

    // DB에 존재하는 설비 리스트들이랑, 해당 설비의 파라미터들 마운트 시에 가져오기
    useEffect(() => {
        const fetchData = async () => {
            const res = await fetchFacilityInfos();
            updateFacility(res.data.result)
        };
        fetchData();
    }, []);
    return (
        <Card className="flex flex-col m-3 gap-5 px-5 py-5">
            <Label htmlFor="" className="font-bold text-[20px]">목록 추가</Label>
            <div className="grid grid-cols-5 gap-3">
                <div className="col-span-2 grid w-full items-center gap-1.5">
                    <Label htmlFor="facility">설비명</Label>
                    <Select onValueChange={setFacility}>
                        <SelectTrigger className="w-full self-center">
                            <SelectValue placeholder="설비명" />
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
                                {facility ? facilityList[facility].find((param) => param === parameter) ? "있다" : " 없다"
                                    : "설비를 먼저 선택해주세요."}
                                <ChevronsUpDown className="ml-2 h-4 w-4 shrink-0 opacity-50" />
                            </Button>
                        </PopoverTrigger>
                        <PopoverContent className="w-[full] p-0">
                            <Command>
                                <CommandInput placeholder="파라미터를 검색해주세요." />
                                <CommandEmpty>검색된 파라미터 없음</CommandEmpty>
                                <CommandGroup>

                                    {facility ? facilityList[facility].map((param) => (
                                        <CommandItem
                                            key={param}
                                            value={param}
                                            onSelect={(currentValue) => {
                                                setParameter(currentValue)
                                                setOpen(false)
                                            }}
                                        >
                                            <Check
                                                className={cn(
                                                    "mr-2 h-4 w-4",
                                                    parameter === param ? "opacity-100" : "opacity-0"
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
                <Button onClick={() => { console.log(facility); console.log(parameter) }}>추가</Button>
            </div>
        </Card >
    )
}

export default Addlist;