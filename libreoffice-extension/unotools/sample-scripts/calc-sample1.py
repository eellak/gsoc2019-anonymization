# -*- coding: utf-8 -*-
import sys
from os.path import join as pathjoin

from unotools import Socket, connect
from unotools.component.calc import Calc
from unotools.data.csv import CsvFile
from unotools.unohelper import constant, convert_path_to_url
from unotools.utils import search_file


def calc_sample(args, context):
    calc = Calc(context)
    sheet = calc.get_sheet_by_index(0)
    sheet.set_columns_str(0, 0, ['Month', 'Sales', 'End Date'])

    path = next(search_file(args.datadirs[0], 'data1.csv'))
    csv_file = CsvFile(path, has_header=True)
    for i, data in enumerate(csv_file.read(), 1):
        sheet.set_rows(0, i, data, csv_file.header)

    format_date = constant('com.sun.star.util.NumberFormat.DATE')
    formats = calc.get_number_formats()
    locale = context.create_struct('com.sun.star.lang.Locale')
    cell_range = sheet.get_cell_range_by_name('C2:C13')
    cell_range.NumberFormat = formats.getStandardFormat(format_date, locale)

    chart_cell_range = sheet.get_cell_range_by_name('A1:B13')
    sheet.add_charts_new_by_name('Sales',
                context.make_rectangle(8000, 1000, 16000, 10000),
                chart_cell_range.get_range_address(), True, True)
    chart = sheet.get_chart_by_name('Sales')
    chart_doc = chart.get_embedded_object()

    title_text_shape = chart_doc.get_title()
    title_text_shape.String = 'Sales Chart'

    diagram = chart_doc.create_instance('com.sun.star.chart.BarDiagram')
    diagram.Vertical = True
    diagram.DataCaption = constant('com.sun.star.chart.ChartDataCaption.VALUE')
    chart_doc.set_diagram(diagram)

    sheets_count = calc.get_sheets_count()
    new_sheets_data = ['sales', 'benefit', 'budget']
    calc.insert_multisheets_new_by_name(new_sheets_data, sheets_count)
    calc.get_sheet_by_name('budget').set_name('cost')

    base_path = convert_path_to_url(pathjoin(args.outputdir, 'sample'))
    calc.store_to_url(base_path + '.ods', 'FilterName', 'calc8')
    calc.store_to_url(base_path + '.xls', 'FilterName', 'MS Excel 97')
    calc.store_to_url(base_path + '.csv',
                      'FilterName', 'Text - txt - csv (StarCalc)')
    calc.store_to_url(base_path + '-calc.pdf', 'FilterName', 'calc_pdf_Export')
    calc.store_to_url(base_path + '-calc.html',
                      'FilterName', 'HTML (StarCalc)')

    calc.close(True)


if __name__ == '__main__':
    from unotools import parse_argument
    args = parse_argument(sys.argv[1:])
    context = connect(Socket(args.host, args.port), option=args.option)
    calc_sample(args, context)
