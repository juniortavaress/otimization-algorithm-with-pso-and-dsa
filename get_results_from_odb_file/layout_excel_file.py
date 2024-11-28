# Creates and returns formats for Excel cells.
def create_formats(workbook):
    """
    Args:
        workbook (xlsxwriter.workbook.Workbook): The workbook where formats will be applied.

    Returns:
        tuple: A tuple containing gray-filled and centered formats.
    """
    gray_fill_format = workbook.add_format({'bold': True, 'align': 'center', 'valign': 'vcenter', 'bg_color': '#D9D9D9', 'border': 1})
    centered_format = workbook.add_format({'align': 'center', 'valign': 'vcenter'})  # Zentrale Formatierung
    return gray_fill_format, centered_format


# Formats the statistics sheet in an Excel workbook.
def format_statistics_sheet_xlsxwriter(worksheet, workbook, temperature_threshold, start_percent, end_percent):
    """
    Args:
        worksheet (xlsxwriter.worksheet.Worksheet): The worksheet to be formatted.
        workbook (xlsxwriter.workbook.Workbook): The workbook containing the worksheet.
        temperature_threshold (float): The temperature threshold for penetration depth evaluation.
        start_percent (float): The starting percentage for the cutting force range.
        end_percent (float): The ending percentage for the cutting force range.
    """
    gray_fill_format, centered_format = create_formats(workbook)

    # Merging cells for descriptive headers
    worksheet.merge_range('B1:E1', f"Normal Cutting Force FcN in the range of {start_percent*100:.0f}-{end_percent*100:.0f} % [N]", gray_fill_format)
    worksheet.merge_range('F1:I1', f"Cutting Force Fc in the range of {start_percent*100:.0f}-{end_percent*100:.0f} % [N]", gray_fill_format)
    worksheet.merge_range('J1:K1', 'Temperature Evaluation at the Last Frame', gray_fill_format)
    worksheet.merge_range('L1:M1', 'Temperature Evaluation at Frame with Tmax at 1st Node', gray_fill_format)

    # Define statistics headers (minimum, maximum, mean, standard deviation, etc.)
    statistics_headers = [
        "Filename", "Minimum", "Maximum", "Mean", "Standard Deviation",
        "Minimum", "Maximum", "Mean", "Standard Deviation",
        "Maximum Temperature [°C]", f"Penetration Depth for Temperature < {temperature_threshold}°C [µm]",
        "Maximum Temperature [°C]", f"Penetration Depth for Temperature < {temperature_threshold}°C [µm]"
    ]

    # Write the headers to the worksheet
    for col_num, header in enumerate(statistics_headers):
        worksheet.write(1, col_num, header, gray_fill_format)

    # Set column widths and apply centered formatting
    column_widths = [42, 15, 15, 15, 20, 15, 15, 15, 20, 27, 45, 27, 45]
    for col_num, width in enumerate(column_widths):
        worksheet.set_column(col_num, col_num, width, centered_format)
    worksheet.set_zoom(80)


# Formats the Excel worksheet, including headers and column widths.
def format_excel_sheet(worksheet, workbook):
    """    
    Args:
        worksheet (xlsxwriter.worksheet.Worksheet): The worksheet to be formatted.
        workbook (xlsxwriter.workbook.Workbook): The workbook containing the worksheet.
    """
    gray_fill_format, centered_format = create_formats(workbook)

    # Writing the headers for the main sheet
    headers = [
        ('A1', 'Time [ms]'),
        ('B1', 'Cutting Force Fc [N]'),
        ('C1', 'Normal Cutting Force FcN [N]'),
        ('E1', 'Penetration Depth [µm]'),
        ('F1', 'Temperature at Last Frame [°C]'),
        ('G1', 'Maximum Temperature [°C]'),
        ('I1', 'Time [ms]'),
        ('J1', 'Temperature at 1st Node [°C]')
    ]
    
    for cell, header in headers:
        worksheet.write(cell, header, gray_fill_format)

    # Setting column widths 
    column_widths = [10, 20, 30, 20, 30, 33, 25, 20, 10, 27]
    for col_num, width in enumerate(column_widths):
        worksheet.set_column(col_num, col_num, width, centered_format)
    worksheet.set_zoom(90)


# Adds charts to an Excel worksheet.
def add_graps_to_excel(writer, sheet_name, combined_df_with_results):
    """
        Args:
        writer (pandas.ExcelWriter): Excel writer object.
        sheet_name (str): Name of the worksheet to add charts.
        combined_df_with_results (pd.DataFrame): DataFrame with results to generate the charts.
    """
    workbook = writer.book
    worksheet = writer.sheets[sheet_name]

    # Apply basic formatting to the worksheet
    format_excel_sheet(worksheet, workbook)

    # Add chart 1: Force components over time
    chart1 = workbook.add_chart({'type': 'scatter', 'subtype': 'straight_with_markers'})

    # Series for Cutting Force Fc [N]
    categories1 = [sheet_name, 1, 0, len(combined_df_with_results), 0]  # Time
    values1 = [sheet_name, 1, 1, len(combined_df_with_results), 1]      # Cutting Force Fc [N]
    chart1.add_series({'name': 'Cutting Force Fc', 'categories': categories1, 'values': values1, 'marker': {'type': 'none'}, 'line': {'width': 1.5}})

    # Series for Normal Cutting Force FcN [N]
    values2 = [sheet_name, 1, 2, len(combined_df_with_results), 2]  # Normal Cutting Force FcN [N]
    chart1.add_series({'name': 'Normal Cutting Force FcN', 'categories': categories1, 'values': values2, 'marker': {'type': 'none'}, 'line': {'width': 1.5}})

    # Configure chart title and axes
    chart1.set_title({'name': sheet_name, 'name_font': {'size': 14}})
    chart1.set_x_axis({'name': 'Time t [ms]', 'name_font': {'size': 11}, 'num_font': {'size': 11}})
    chart1.set_y_axis({'name': 'Force Component Fi [N]', 'name_font': {'size': 11}, 'num_font': {'size': 11}})
    chart1.set_legend({'position': 'bottom', 'font': {'size': 11}})
    worksheet.insert_chart('L2', chart1)