import { useEffect, useState } from "react";
import {
    flexRender,
    getCoreRowModel,
    getFilteredRowModel,
    getPaginationRowModel,
    getSortedRowModel,
    useReactTable,
} from "@tanstack/react-table"
import { MoreHorizontal, ChevronsUpDown, Check } from "lucide-react"
import { useBookmarkStore, useSelectedBookmarkStore } from "@/stores/Bookmark";
import { Checkbox } from "@/components/base/checkbox";
import {
    Select,
    SelectContent,
    SelectGroup,
    SelectItem,
    SelectTrigger,
    SelectValue,
} from "@/components/base/select";
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
import { useFacilityStore } from "@/stores/Facility";

function BookmarkTable() {

    const { bookmark, deleteBookmark } = useBookmarkStore();
    const { setSelectedBookmark } = useSelectedBookmarkStore();
    const { batchList } = useFacilityStore();

    // 테이블 관련 hook
    // ==============================
    const data = bookmark
    const [sorting, setSorting] = useState([])
    const [columnFilters, setColumnFilters] = useState([])
    const [columnVisibility, setColumnVisibility] = useState({})
    const [rowSelection, setRowSelection] = useState({})
    const [pagination, setPagination] = useState({
        pageIndex: 0,
        pageSize: 5,
    });
    // ==============================

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
            header: () => <div className="text-center">배치</div>,
            cell: ({ row }) => {
                return <div className="text-center font-medium">
                    <Select>
                        <SelectTrigger className="w-[180px]">
                            <SelectValue placeholder="배치 선택" />
                        </SelectTrigger>
                        <SelectContent>
                            <SelectGroup>
                                {batchList[row.original.facility]?.map((batch) =>
                                    <SelectItem
                                        key={batch.batchName}
                                        value={batch.batchName}
                                    >
                                        {batch.batchName}
                                    </SelectItem>
                                )}
                            </SelectGroup>
                        </SelectContent>
                    </Select>
                </div>
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
                            <DropdownMenuItem onClick={() => deleteBookmark(row.original.id)}>세팅값 삭제</DropdownMenuItem>
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
        onRowSelectionChange: async (row) => {
            await setRowSelection(row)
            setSelectedBookmark(table.getSelectedRowModel().rows.map((row) => row.original))
        },
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