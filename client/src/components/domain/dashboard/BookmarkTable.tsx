import { useEffect, useState } from "react";
import { cn } from "@/lib/utils";
import {
    ColumnDef,
    ColumnFiltersState,
    SortingState,
    flexRender,
    getCoreRowModel,
    getFilteredRowModel,
    getPaginationRowModel,
    getSortedRowModel,
    useReactTable,
} from "@tanstack/react-table";
import { ScrollArea } from "@/components/base/scroll-area";
import {
    Command,
    CommandEmpty,
    CommandGroup,
    CommandInput,
    CommandItem,
} from "@/components/base/command"
import {
    Popover,
    PopoverContent,
    PopoverTrigger,
} from "@/components/base/popover";
import { Check, ChevronsUpDown, MoreHorizontal } from "lucide-react"
import { Bookmark, useBookmarkStore, useSelectedRowStore } from "@/stores/Bookmark";
import { Checkbox } from "@/components/base/checkbox";
import {
    DropdownMenu,
    DropdownMenuContent,
    DropdownMenuItem,
    DropdownMenuTrigger,
} from "@/components/base/dropdown-menu"
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
import { useBatchStore } from "@/stores/Facility";
import useDidMountEffect from "@/hooks/useDidMountEffect";

function BookmarkTable() {

    const { bookmark, deleteBookmark, updateBookmark } = useBookmarkStore();
    const { setSelectedRow } = useSelectedRowStore();
    const { batchList } = useBatchStore();


    // Tanstack Table 세팅에 필요한 Hook 들
    const data: Bookmark[] = bookmark.sort((a: Bookmark, b: Bookmark) => a.id! - b.id!)
    const [sorting, setSorting] = useState<SortingState>([])
    const [columnFilters, setColumnFilters] = useState<ColumnFiltersState>([])
    const [columnVisibility, setColumnVisibility] = useState({})
    const [rowSelection, setRowSelection] = useState({})
    const [pagination, setPagination] = useState({
        pageIndex: 0,
        pageSize: 5,
    });


    // zustand에 선택된 row 정보 저장
    useEffect(() => {
        setSelectedRow(rowSelection)
    }, [rowSelection])

    const columns: ColumnDef<Bookmark>[] = [
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

                const facility: string = row.getValue("facility")

                return <div className="text-center">{facility}</div>
            }
        },
        {
            accessorKey: "parameter",
            header: () => <div className="text-center">파라미터</div>,
            cell: ({ row }) => {

                const parameter: string = row.getValue("parameter")

                return <div className="text-center">{parameter}</div>
            }
        },
        {
            accessorKey: "batches",
            header: () => <div className="text-center">배치</div>,
            cell: ({ row }) => {

                const [open, setOpen] = useState(false);
                const [selectedBatchData, setSelectedBatchData] = useState({
                    id: row.original.id,
                    facility: row.original.facility,
                    parameter: row.original.parameter,
                    selectedBatchName: "",
                });
                const batches = batchList[row.original.facility];

                useDidMountEffect(() => {
                    updateBookmark(selectedBatchData)
                }, [selectedBatchData])


                return <div className="flex flex-row text-center font-medium w-auto">

                    <Popover open={open} onOpenChange={setOpen}>
                        <PopoverTrigger asChild>
                            <Button
                                variant="outline"
                                role="combobox"
                                aria-expanded={open}
                                className="w-full justify-between"
                            >
                                {bookmark.find((e) => e.id === row.original.id)?.selectedBatchName || "배치를 선택해 주세요."}
                                <ChevronsUpDown className="ml-2 h-4 w-4 shrink-0 opacity-50" />
                            </Button>
                        </PopoverTrigger>
                        <PopoverContent className="w-auto p-0">
                            <ScrollArea className="h-[400px] w-full">
                                <Command>
                                    <CommandInput placeholder="배치명을 검색해주세요." />
                                    <CommandEmpty>검색된 배치 없음</CommandEmpty>
                                    <CommandGroup>
                                        {batches?.map((batch) =>
                                            <CommandItem
                                                key={batch.batchName}
                                                value={batch.batchName}
                                                onSelect={() => {
                                                    setSelectedBatchData(prevState => ({
                                                        ...prevState,
                                                        selectedBatchName: batch.batchName,
                                                    }));
                                                    setOpen(false);
                                                    console.log(batch.stepsCnt)
                                                }}>
                                                {batch.batchName}
                                                <Check
                                                    className={cn(
                                                        "mr-2 h-4 w-4",
                                                        bookmark.find((e) => e.id === row.original.id)?.selectedBatchName === batch.batchName ? "opacity-100" : "opacity-0"
                                                    )}
                                                />
                                            </CommandItem>
                                        )}
                                    </CommandGroup>
                                </Command>
                            </ScrollArea>
                        </PopoverContent>
                    </Popover>
                </div >
            },
        },
        {
            id: "actions",
            enableHiding: false,
            cell: ({ row }) => {
                return (
                    <DropdownMenu>
                        <DropdownMenuTrigger asChild>
                            <Button variant="ghost" className="h-8 w-8 p-0">
                                <span className="sr-only">Open menu</span>
                                <MoreHorizontal className="h-4 w-4" />
                            </Button>
                        </DropdownMenuTrigger>
                        <DropdownMenuContent align="end">
                            <DropdownMenuItem onClick={() => deleteBookmark(row.original.id!)}>삭제</DropdownMenuItem>
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
        <>
            <div className="flex items-center py-4">
                <Input
                    placeholder="설비명으로 검색"
                    value={(table.getColumn("facility")?.getFilterValue() as string) ?? ""}
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
            {/* 테이블 높이 수정 필요 */}
            <div className="rounded-md border h-[414px]">
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
        </>
    )
}

export default BookmarkTable;