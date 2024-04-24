import {
    Select,
    SelectContent,
    SelectGroup,
    SelectItem,
    SelectLabel,
    SelectTrigger,
    SelectValue,
} from "@/components/base/select"
import { Button } from "@/components/base/button";
import {
    Dialog,
    DialogContent,
    DialogDescription,
    DialogFooter,
    DialogHeader,
    DialogTitle,
    DialogTrigger,
    DialogClose,
} from "@/components/base/dialog"
import { Input } from "@/components/base/input"
import { Label } from "@/components/base/label"

import {
    Card
} from "@/components/base/card"

import { useState } from "react";
import axios from "axios";
import { useImage } from "./ImageContext";
import { format } from "date-fns";
import { Calendar as CalendarIcon } from "lucide-react";
import { Calendar } from "@/components/base/calendar";
import {
    Popover,
    PopoverContent,
    PopoverTrigger,
} from "@/components/base/popover";
import { cn } from "@/lib/utils"





function Navbars() {

    const [date, setDate] = useState()

    const { setImage } = useImage();
    const [files, setFiles] = useState([]);

    const handleFilesChange = (e) => {
        setFiles(Array.from(e.target.files));
    }

    const uploadFiles = (e) => {
        e.preventDefault();
        let formData = new FormData();

        files.map((file) => {
            formData.append("file", file);
        });

        console.log(Array.from(formData));
        console.log('첨부파일 보내기 시작');

        // 수정
        axios.post('http://localhost:8000/upload', formData, {
            headers: {
                'Content-Type': 'multipart/form-data'
            }
        })
            .then((res) => {
                console.log(res.data);
                console.log('첨부파일 보내기 성공');
                const imageBase64 = res.data.img_data64;
                console.log(imageBase64);
                setImage(`data:image/png;base64,${imageBase64}`);
                setImage(sample)
            }).catch((err) => {
                console.error(err);
                console.log('첨부파일 보내기 실패');
            });
    }







    return (
        <Card className='flex flex-row justify-between my-6 p-4'>
            <Select>
                <SelectTrigger className="w-[180px]">
                    <SelectValue placeholder="설비를 선택해주세요." />
                </SelectTrigger>
                <SelectContent>
                    <SelectGroup>
                        <SelectItem value="1번 설비">1번 설비</SelectItem>
                        <SelectItem value="2번 설비">2번 설비</SelectItem>
                        <SelectItem value="3번 설비">3번 설비</SelectItem>
                        <SelectItem value="4번 설비">4번 설비</SelectItem>
                        <SelectItem value="5번 설비">5번 설비</SelectItem>
                        <SelectItem value="6번 설비">6번 설비</SelectItem>
                        <SelectItem value="7번 설비">7번 설비</SelectItem>
                        <SelectItem value="8번 설비">8번 설비</SelectItem>
                    </SelectGroup>
                </SelectContent>
            </Select>
            <Popover>
                <PopoverTrigger asChild>
                    <Button
                        variant={"outline"}
                        className={cn(
                            "w-[280px] justify-start text-left font-normal",
                            !date && "text-muted-foreground"
                        )}
                    >
                        <CalendarIcon className="mr-2 h-4 w-4" />
                        {date ? format(date, "PPP") : <span>데이터 날짜를 선택하세요.</span>}
                    </Button>
                </PopoverTrigger>
                <PopoverContent className="w-auto p-0">
                    <Calendar
                        mode="single"
                        selected={date}
                        onSelect={setDate}
                        initialFocus
                    />
                </PopoverContent>
            </Popover>
            <Popover>
                <PopoverTrigger asChild>
                    <Button
                        variant={"outline"}
                        className={cn(
                            "w-[280px] justify-start text-left font-normal",
                            !date && "text-muted-foreground"
                        )}
                    >
                        <CalendarIcon className="mr-2 h-4 w-4" />
                        {date ? format(date, "PPP") : <span>데이터 날짜를 선택하세요.</span>}

                    </Button>

                </PopoverTrigger>
                <PopoverContent className="w-auto p-0">
                    <Calendar
                        mode="single"
                        selected={date}
                        onSelect={setDate}
                        initialFocus
                    />
                </PopoverContent>
            </Popover>

            <Dialog>
                <DialogTrigger asChild>
                    <Button>새로운 설비 추가</Button>
                </DialogTrigger>
                <DialogContent className="sm:max-w-[425px]">
                    <DialogHeader>
                        <DialogTitle>설비 추가</DialogTitle>
                        <DialogDescription>현재는 엑셀 단일파일 하나만 지원함</DialogDescription>
                    </DialogHeader>
                    <div className="grid gap-4 py-4">
                        <div className="space-y-1">
                            <Label htmlFor="name">설비명</Label>
                            <Input id="name" defaultValue="설비의 이름을 입력해주세요" />
                        </div>
                        <div className="space-y-1">
                            <Label htmlFor="file">데이터 파일</Label>
                            <Input
                                id="file"
                                type="file"
                                onChange={handleFilesChange}
                                accept='csv'
                            />
                        </div>
                    </div>
                    <DialogFooter>
                        <Button type="button" onClick={uploadFiles}>설비 추가</Button>
                    </DialogFooter>

                </DialogContent>
            </Dialog>


        </Card>
    )
}

export default Navbars;