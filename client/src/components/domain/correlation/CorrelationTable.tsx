import { useMemo, useState, useEffect } from "react";
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
import {
    Table,
    TableBody,
    TableCell,
    TableHead,
    TableHeader,
    TableRow,
} from "@/components/base/table"
import { Input } from '@/components/base/input'
import { Checkbox } from '@/components/base/checkbox';
import { useCorrelationStore } from '@/stores/Correlation';
import { useFacilityStore } from '@/stores/Facility';
import { Button } from "@/components/base/button";


type Parameter = {
    id: number;
    parameter: string;
}

function CorrelationTable() {
    const { selectedFacility, setSelectedParameters } = useCorrelationStore();
    const { facilityList } = useFacilityStore();

    const data = useMemo(
        () => {
            if (facilityList[selectedFacility]) {
                const result = facilityList[selectedFacility].parameters.map((parameter, id) => {
                    const parameterObj = {
                        id: id,
                        parameter: parameter
                    }
                    return parameterObj
                })
                return result
            }
            else return []
        },
        [selectedFacility]
    )
    const columns: ColumnDef<Parameter>[] = [
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
            accessorKey: "parameter",
            header: () => <div className="text-center">파라미터</div>,
            cell: ({ row }) => {
                const parameter: string = row.getValue("parameter")
                return <div className="text-center">{parameter}</div>
            }
        },


    ]

    const [sorting, setSorting] = useState<SortingState>([])
    const [columnFilters, setColumnFilters] = useState<ColumnFiltersState>([])
    const [columnVisibility, setColumnVisibility] = useState({})
    const [rowSelection, setRowSelection] = useState({})
    const [pagination, setPagination] = useState({
        pageIndex: 0,
        pageSize: 8,
    });



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


    useEffect(() => {
        console.log(rowSelection)
        const parameters = table.getSelectedRowModel().rows.map((row) => row.original.parameter);
        setSelectedParameters(parameters)
    }, [rowSelection])


    table.getTotalSize

    return (
        <div className="gap-0">
            <div className="flex items-center py-4">
                <Input
                    placeholder="파라미터명으로 검색"
                    value={(table.getColumn("parameter")?.getFilterValue() as string) ?? ""}
                    onChange={(event) =>
                        table.getColumn("parameter")?.setFilterValue(event.target.value)
                    }
                    className="w-auto"
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
            <div className='rounded-md border h-[480px]'>
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
                                    파라미터가 없습니다.
                                </TableCell>
                            </TableRow>
                        )}
                    </TableBody>
                </Table>
            </div>
            <div className="flex items-center justify-end space-x-2 py-4">
                <div className="flex-1 text-sm text-muted-foreground">
                    {table.getFilteredSelectedRowModel().rows.length} / {table.getFilteredRowModel().rows.length} 개 선택됨.
                </div>
                {Object.keys(rowSelection).length > 8 ?
                    <p className="ml-auto text-sm text-red-500">8개를 초과하여 선택할 수 없습니다.</p>
                    :
                    <p className="ml-auto text-sm text-white">null</p>
                }
            </div>
        </div>
    )

}

export default CorrelationTable;