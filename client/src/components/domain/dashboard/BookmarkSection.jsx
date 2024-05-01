import { useState } from "react";
import { format } from "date-fns";
import {
    flexRender,
    getCoreRowModel,
    getFilteredRowModel,
    getPaginationRowModel,
    getSortedRowModel,
    useReactTable,
} from "@tanstack/react-table"
import { MoreHorizontal } from "lucide-react"
import { useBookmark } from "@/stores/Bookmark";
import { Checkbox } from "@/components/base/checkbox"
import {
    DropdownMenu,
    DropdownMenuContent,
    DropdownMenuItem,
    DropdownMenuTrigger,
} from "@/components/base/dropdown-menu"
import {
    Card,
    CardHeader,
    CardTitle,
    CardContent,
} from "@/components/base/card";
import { ScrollArea } from "@radix-ui/react-scroll-area";
import { Separator } from "@/components/base/separator";
import { RadioGroup, RadioGroupItem } from "@/components/base/radio-group";
import { Label } from "@/components/base/label";
import { Input } from "@/components/base/input"
import { Button } from "@/components/base/button";
import {
    Table,
    TableBody,
    TableCell,
    TableHead,
    TableHeader,
    TableRow,
} from "@/components/base/table"
import useDidMountEffect from "@/hooks/useDidMountEffect";

function BookmarkSection() {

    const { bookmark, deleteBookmark, updateBookmark } = useBookmark();

    // 테이블 관련 hook
    // ==============================
    const data = bookmark
    const [sorting, setSorting] = useState([])
    const [columnFilters, setColumnFilters] = useState([])
    const [columnVisibility, setColumnVisibility] = useState({})
    const [rowSelection, setRowSelection] = useState({})
    const [pagination, setPagination] = useState({
        pageIndex: 0,
        pageSize: 7,
    });
    // ==============================
    const [cycles, setCycles] = useState([])
    const stepList = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19]
    const [selectedBlock, setSelectedBlock] = useState({});
    const [selectedCycleName, setSelectedCycleName] = useState(null);
    const [selectedStep, setSelectedStep] = useState(null);

    const handleBlockClick = (data) => {
        setSelectedBlock(data) // 선택한 블럭으로 교체
        setCycles(data.cycles) // 블럭의 사이클 리스트로 교체
        setSelectedCycleName(data.cycleName)
        setSelectedStep(data.step)
    }

    useDidMountEffect(() => {
        updateBookmark(
            {
                ...selectedBlock,
                cycleName: selectedCycleName,
                step: selectedStep,
            }
        )

    }, [selectedCycleName, selectedStep])

    const columns = [
        {
            id: "select",
            header: ({ table }) => (
                <Checkbox
                    checked={
                        table.getIsAllPageRowsSelected() ||
                        (table.getIsSomePageRowsSelected() && "indeterminate")
                    }
                    onCheckedChange={(value) => table.toggleAllPageRowsSelected(!!value)}
                    aria-label="Select all"
                />
            ),
            cell: ({ row }) => (
                <Checkbox
                    checked={row.getIsSelected()}
                    onCheckedChange={(value) => row.toggleSelected(!!value)}
                    aria-label="Select row"
                />
            ),
            enableSorting: false,
            enableHiding: false,
        },
        {
            accessorKey: "facility",
            header: () => <div className="text-center">설비명</div>,
            cell: ({ row }) => {

                const facility = row.getValue("facility")

                return <div className="text-center">{facility}</div>
            }
        },
        {
            accessorKey: "parameter",
            header: () => <div className="text-center">파라미터</div>,
            cell: ({ row }) => {

                const parameter = row.getValue("parameter")

                return <div className="text-center">{parameter}</div>
            }
        },
        {
            accessorKey: "times",
            header: () => <div className="text-center">시간대</div>,
            cell: ({ row }) => {
                const data = row.original
                return <div className="text-center font-medium">
                    {format(data.startTime, "yy-MM-dd hh:mm") + " ~ " + format(data.endTime, "yy-MM-dd hh:mm")}
                </div>
            },
        },
        {
            id: "actions",
            enableHiding: false,
            cell: ({ row }) => {
                const payment = row.original

                return (
                    <DropdownMenu>
                        <DropdownMenuTrigger asChild>
                            <Button variant="ghost" className="h-8 w-8 p-0">
                                <span className="sr-only">Open menu</span>
                                <MoreHorizontal className="h-4 w-4" />
                            </Button>
                        </DropdownMenuTrigger>
                        <DropdownMenuContent align="end">
                            <DropdownMenuItem onClick={() => deleteBookmark(payment.id)}>세팅값 삭제</DropdownMenuItem>
                        </DropdownMenuContent>
                    </DropdownMenu >
                )
            },
        },
    ]

    const table = useReactTable({
        data,
        columns,
        onSortingChange: setSorting,
        onColumnFiltersChange: setColumnFilters,
        getCoreRowModel: getCoreRowModel(),
        getPaginationRowModel: getPaginationRowModel(),
        getSortedRowModel: getSortedRowModel(),
        getFilteredRowModel: getFilteredRowModel(),
        onColumnVisibilityChange: setColumnVisibility,
        onRowSelectionChange: setRowSelection,
        onPaginationChange: setPagination,
        state: {
            sorting,
            columnFilters,
            columnVisibility,
            rowSelection,
            pagination,
        },
    })

    return (
        <div className="w-full">
            <div className="flex items-center py-4">
                <Input
                    placeholder="설비명으로 검색"
                    value={(table.getColumn("facility")?.getFilterValue()) ?? ""}
                    onChange={(event) =>
                        table.getColumn("facility")?.setFilterValue(event.target.value)
                    }
                    className="max-w-sm"
                />

                <div className="space-x-2 ml-auto">
                    <Button
                        variant="outline"
                        size="sm"
                        onClick={() => table.previousPage()}
                        disabled={!table.getCanPreviousPage()}
                    >
                        이전
                    </Button>
                    <Button
                        variant="outline"
                        size="sm"
                        onClick={() => table.nextPage()}
                        disabled={!table.getCanNextPage()}
                    >
                        다음
                    </Button>
                </div>
            </div>
            <div className="rounded-md border">
                <Table>
                    <TableHeader>
                        {table.getHeaderGroups().map((headerGroup) => (
                            <TableRow key={headerGroup.id}>
                                {headerGroup.headers.map((header) => {
                                    return (
                                        <TableHead key={header.id}>
                                            {header.isPlaceholder
                                                ? null
                                                : flexRender(
                                                    header.column.columnDef.header,
                                                    header.getContext()
                                                )}
                                        </TableHead>
                                    )
                                })}
                            </TableRow>
                        ))}
                    </TableHeader>
                    <TableBody>
                        {table.getRowModel().rows?.length ? (
                            table.getRowModel().rows.map((row) => (
                                <TableRow
                                    key={row.id}
                                    data-state={row.getIsSelected() && "selected"}
                                    onClick={() => handleBlockClick(row.original)}
                                >
                                    {row.getVisibleCells().map((cell) => (
                                        <TableCell key={cell.id}>
                                            {flexRender(
                                                cell.column.columnDef.cell,
                                                cell.getContext()
                                            )}
                                        </TableCell>
                                    ))}
                                </TableRow>
                            ))
                        ) : (
                            <TableRow>
                                <TableCell
                                    colSpan={columns.length}
                                    className="h-24 text-center"
                                >
                                    저장된 설정이 없습니다.
                                </TableCell>
                            </TableRow>
                        )}
                    </TableBody>
                </Table>
            </div>
            {/* <div className="flex items-center justify-end space-x-2 py-4">
                <div className="flex-1 text-sm text-muted-foreground">
                    총 {table.getFilteredRowModel().rows.length}개 중{" "}
                    {table.getFilteredSelectedRowModel().rows.length}개 선택됨.
                </div>
            </div> */}
            <div className="grid grid-cols-2 space-x-5 py-4">
                <Card className="mb-3">
                    <CardHeader>
                        <CardTitle>
                            Cycle Selection
                        </CardTitle>
                    </CardHeader>
                    <ScrollArea className="h-48">
                        <div className="p-4">
                            <RadioGroup defalutValue={cycles[0]}>
                                {cycles.map((cycle) => (
                                    <>
                                        <div key={cycle.cycleName} className="flex flex-row text-sm justify-between"
                                            onClick={() => setSelectedCycleName(cycle.cycleName)}>
                                            <Label htmlFor={cycle.cycleName}>{cycle.cycleName}</Label>
                                            <RadioGroupItem value={cycle.cycleName} id={cycle.cycleName} />
                                        </div>
                                        <Separator className="my-2" />
                                    </>
                                ))}
                            </RadioGroup>
                        </div>
                    </ScrollArea>
                </Card>
                <Card>
                    <CardHeader>
                        <CardTitle>
                            Step Selection
                        </CardTitle>
                    </CardHeader>
                    <CardContent>
                        <div className="grid grid-cols-5">
                            {stepList.map((step) =>
                                <Button key={step} className="m-[2px]" variant="outline" onClick={() => setSelectedStep(step)}>{step}</Button>
                            )}

                        </div>
                        <Button variant="outline" className='w-full' onClick={() => setSelectedStep(null)}>전체</Button>
                    </CardContent>
                </Card>
            </div>
            <div className="space-x-2">
                <Button
                    className="ml-auto"
                    onClick={() => {
                        const selectedRows = table.getFilteredRowModel().rows
                        const selectedRowData = selectedRows.map(row => row.original)
                        console.log(selectedRowData)
                    }}
                >
                    비교하기
                </Button>
            </div>
        </div>
    )
}

export default BookmarkSection;