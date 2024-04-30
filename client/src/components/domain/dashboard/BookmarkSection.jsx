import { useState } from "react";
import { format } from "date-fns"
import {
    flexRender,
    getCoreRowModel,
    getFilteredRowModel,
    getPaginationRowModel,
    getSortedRowModel,
    useReactTable,
} from "@tanstack/react-table"
import { ArrowUpDown, ChevronDown, MoreHorizontal } from "lucide-react"
import { useBookmark } from "@/stores/Bookmark";
import { Button } from "@/components/base/button"
import { Checkbox } from "@/components/base/checkbox"
import {
    Dialog,
    DialogContent,
    DialogDescription,
    DialogHeader,
    DialogTitle,
    DialogTrigger,
} from "@/components/base/dialog"
import {
    DropdownMenu,
    DropdownMenuCheckboxItem,
    DropdownMenuContent,
    DropdownMenuItem,
    DropdownMenuLabel,
    DropdownMenuSeparator,
    DropdownMenuTrigger,
} from "@/components/base/dropdown-menu"
import { Input } from "@/components/base/input"
import {
    Table,
    TableBody,
    TableCell,
    TableHead,
    TableHeader,
    TableRow,
} from "@/components/base/table"
import { p } from "@bokeh/bokehjs/build/js/lib/core/dom";

function BookmarkSection() {

    const { bookmark, deleteBookmark, updateBookmark } = useBookmark();

    const data = bookmark


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
                console.log()


                return <div className="text-center font-medium">
                    {format(data.startDate, 'yy-MM-dd')} {" "}
                    {data.startTime}
                    {" "}~ {" "}
                    {format(data.endDate, 'yy-MM-dd')} {" "}
                    {data.endTime}</div>
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
                            <DropdownMenuLabel>설정</DropdownMenuLabel>
                            <DropdownMenuItem
                                onClick={() => navigator.clipboard.writeText(payment.id)}
                            >
                                세팅값 텍스트로 복사
                            </DropdownMenuItem>
                            <DropdownMenuSeparator />
                            <DropdownMenuItem
                            >세팅값 수정</DropdownMenuItem>
                            <DropdownMenuItem
                                onClick={() => {
                                    deleteBookmark(payment.id);
                                    console.log(bookmark)
                                }}
                            >세팅값 삭제</DropdownMenuItem>
                        </DropdownMenuContent>
                    </DropdownMenu >
                )
            },
        },
    ]






    const [sorting, setSorting] = useState([])
    const [columnFilters, setColumnFilters] = useState(
        []
    )
    const [columnVisibility, setColumnVisibility] =
        useState({})
    const [rowSelection, setRowSelection] = useState({})

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
        state: {
            sorting,
            columnFilters,
            columnVisibility,
            rowSelection,
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
            <div className="flex items-center justify-end space-x-2 py-4">
                <div className="flex-1 text-sm text-muted-foreground">
                    총 {table.getFilteredRowModel().rows.length}개 중{" "}
                    {table.getFilteredSelectedRowModel().rows.length}개 선택됨.
                </div>
                <div className="space-x-2">
                    <Button className="ml-auto">
                        비교하기
                    </Button>
                </div>
            </div>
        </div>
    )
}

export default BookmarkSection;