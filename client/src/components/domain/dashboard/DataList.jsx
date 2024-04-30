import { useState } from "react";
import {
    flexRender,
    getCoreRowModel,
    getFilteredRowModel,
    getPaginationRowModel,
    getSortedRowModel,
    useReactTable,
} from "@tanstack/react-table"
import { ArrowUpDown, ChevronDown, MoreHorizontal } from "lucide-react"

import { Button } from "@/components/base/button"
import { Checkbox } from "@/components/base/checkbox"
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

const data = [
    {
        id: "m5gr84i9",
        times: "24-02-01 11:03 ~ 24-02-01 13:03",
        parameter: "No_1_P",
        facility: "F1490",
    },
    {
        id: "3u1reuv4",
        times: "24-02-02 14:03 ~ 24-02-02 15:03",
        parameter: "No_2_P",
        facility: "F1491",
    },
    {
        id: "derv1ws0",
        times: "24-02-02 14:03 ~ 24-02-02 15:03",
        parameter: "No_3_P",
        facility: "F1422",
    },
    {
        id: "5kma53ae",
        times: "24-02-02 14:03 ~ 24-02-02 15:03",
        parameter: "No_4_P",
        facility: "F1221",
    },
    {
        id: "bhqecj4p",
        times: "24-02-02 14:03 ~ 24-02-02 15:03",
        parameter: "No_5_A",
        facility: "F1111",
    },
]


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
            const times = row.getValue("times")

            return <div className="text-center font-medium">{times}</div>
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
                        <DropdownMenuItem>세팅값 수정</DropdownMenuItem>
                        <DropdownMenuItem>세팅값 삭제</DropdownMenuItem>
                    </DropdownMenuContent>
                </DropdownMenu>
            )
        },
    },
]



function DataList() {

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
                <DropdownMenu>
                    <DropdownMenuTrigger asChild>
                        <Button variant="outline" className="ml-auto">
                            칼럼 필터링 <ChevronDown className="ml-2 h-4 w-4" />
                        </Button>
                    </DropdownMenuTrigger>
                    <DropdownMenuContent align="end">
                        {table
                            .getAllColumns()
                            .filter((column) => column.getCanHide())
                            .map((column) => {
                                return (
                                    <DropdownMenuCheckboxItem
                                        key={column.id}
                                        className="capitalize"
                                        checked={column.getIsVisible()}
                                        onCheckedChange={(value) =>
                                            column.toggleVisibility(!!value)
                                        }
                                    >
                                        {column.id}
                                    </DropdownMenuCheckboxItem>
                                )
                            })}
                    </DropdownMenuContent>
                </DropdownMenu>
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
                                    No results.
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
        </div>
    )
}

export default DataList;