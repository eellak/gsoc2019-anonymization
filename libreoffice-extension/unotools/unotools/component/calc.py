# -*- coding: utf-8 -*-
from operator import methodcaller

import uno  # pragma: no flakes
from com.sun.star.awt import Rectangle
from com.sun.star.table import CellRangeAddress

from unotools.unohelper import ComponentBase
from unotools.unohelper import LoadingComponentBase
from unotools.datatypes import Sequence


class ChartDocument(ComponentBase):
    pass


class TableChart(ComponentBase):

    def get_embedded_object(self) -> ChartDocument:
        return ChartDocument(self.context, self.raw.getEmbeddedObject())


class TableCharts(ComponentBase):
    pass


class CellRange(ComponentBase):
    pass


class Cell(ComponentBase):
    pass


class Spreadsheet(ComponentBase):

    def set_rows_cell_data(self, x: int, y: int, data: list, method_name: str):
        for datum in data:
            methodcaller(method_name, datum)(self.raw.getCellByPosition(x, y))
            y += 1

    def set_columns_cell_data(self, x: int, y: int, data: list,
                              method_name: str):
        for datum in data:
            methodcaller(method_name, datum)(self.raw.getCellByPosition(x, y))
            x += 1

    def set_rows(self, x: int, y: int, data: list, method_names: str):
        for i, datum in enumerate(data):
            self.set_rows_cell_data(x, y, [datum], method_names[i])
            x += 1

    def set_columns(self, x: int, y: int, data: list, method_names: str):
        for i, datum in enumerate(data):
            self.set_rows_cell_data(x, y, [datum], method_names[i])
            y += 1

    def set_rows_str(self, x: int, y: int, data: list):
        self.set_rows_cell_data(x, y, data, 'setString')

    def set_columns_str(self, x: int, y: int, data: list):
        self.set_columns_cell_data(x, y, data, 'setString')

    def set_rows_value(self, x: int, y: int, data: list):
        self.set_rows_cell_data(x, y, data, 'setValue')

    def set_columns_value(self, x: int, y: int, data: list):
        self.set_columns_cell_data(x, y, data, 'setValue')

    def set_rows_formula(self, x: int, y: int, data: list):
        self.set_rows_cell_data(x, y, data, 'setFormula')

    def set_columns_formula(self, x: int, y: int, data: list):
        self.set_columns_cell_data(x, y, data, 'setFormula')

    def get_cell_by_position(self, x: int, y: int) -> Cell:
        return Cell(self.context, self.raw.getCellByPosition(x, y))

    def get_cell_range_by_name(self, range_: str) -> CellRange:
        return CellRange(self.context, self.raw.getCellRangeByName(range_))

    def get_cell_range_by_position(self, left: int, top: int, right: int,
                                   bottom: int) -> CellRange:
        raw = self.raw.getCellRangeByPosition(left, top, right, bottom)
        return CellRange(self.context, raw)

    @property
    def charts(self) -> TableCharts:
        return TableCharts(self.context, self.raw.getCharts())

    def get_charts_count(self) -> int:
        return self.charts.getCount()

    def add_charts_new_by_name(self, name: str,
                               rect: Rectangle, ranges: CellRangeAddress,
                               column_headers: bool, row_headers: bool):
        self.charts.addNewByName(name, rect, Sequence(ranges),
                                 column_headers, row_headers)

    def get_chart_by_index(self, index: int) -> TableChart:
        return TableChart(self.context, self.charts.getByIndex(index))

    def get_chart_by_name(self, name: str) -> TableChart:
        return TableChart(self.context, self.charts.getByName(name))


class Spreadsheets(ComponentBase):
    pass


class Calc(LoadingComponentBase):

    URL = 'private:factory/scalc'

    @property
    def sheets(self) -> Spreadsheets:
        return Spreadsheets(self.context, self.raw.getSheets())

    def get_sheets_count(self) -> int:
        return self.sheets.getCount()

    def get_sheet_by_index(self, index: int) -> Spreadsheet:
        return Spreadsheet(self.context, self.sheets.getByIndex(index))

    def get_sheet_by_name(self, name: str) -> Spreadsheet:
        return Spreadsheet(self.context, self.sheets.getByName(name))

    def insert_sheets_new_by_name(self, name: str, position: int):
        self.sheets.insertNewByName(name, position)

    def insert_multisheets_new_by_name(self, data: list, position: int):
        for i, datum in enumerate(data):
            self.insert_sheets_new_by_name(datum, position + i)

    def remove_sheets_by_name(self, name: str):
        self.sheets.removeByName(name)
