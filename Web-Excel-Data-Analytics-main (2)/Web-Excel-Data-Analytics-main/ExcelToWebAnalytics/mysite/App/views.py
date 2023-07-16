# views.py file

from django.shortcuts import render
from django.core.paginator import Paginator
import pandas as pd
import numpy as np
import warnings
from .models import ExcelFile


# default home view
def home(request):
    # Fetching Excel file from home.html file
    if request.method == 'POST' and request.FILES['excel']:
        excel_file = request.FILES['excel']
        file_name = excel_file.name

        # Using pandas dataframe method read_excel to read excel file
        df = pd.read_excel(excel_file, sheet_name=None)

        # Accessing all sheet names from the file
        sheets = list(df.keys())

        # Creating a local object of the Excel file
        obj = ExcelFile.objects.create(file=excel_file)

        # Redirecting to the same page with the sheet names
        return render(request, 'App/home.html', {'sheets': sheets, 'file_name': file_name, 'file_id': obj.id})

    # Else returning nothing
    return render(request, 'App/home.html')


# sheet_columns view function:
def sheet_columns(request, file_id, file_name, sheet_name, col_name):

    # Accessing the local file object using file ID
    obj = ExcelFile.objects.get(id=file_id)

    # Accessing the Sub sheet in the Excel file using sheet_name attribute
    df1 = pd.read_excel(obj.file, sheet_name=sheet_name)

    # Data cleaning and transformation
    columns = [col for col in df1.columns if not 'Unnamed' in col]

    # Another data frame to access records
    df = pd.read_excel(obj.file, sheet_name=sheet_name, header=2)

    # Adding Exception Handling
    try:
        # Data cleaning and transformation
        warnings.filterwarnings("ignore")
        df.columns = df.columns.str.replace(r'[#,@,&,.,\d+,' ']', '')
        df.fillna(value="N/A", inplace=True)

        # Creating a table header for dataframe
        if col_name == 'BasicInfo':
            t_header = []
            t_header_cols = df[col_name].head(1).values.tolist()
            for temp in t_header_cols:
                for rar in temp:
                    t_header.append(rar)

            data = df[col_name].tail(-1).values.tolist()

            # Adding pagination to the dataframe by 10 rows per page
            paginator = Paginator(data, 10)
            page = request.GET.get('page')
            data = paginator.get_page(page)
        else:
            try:
                # Creating a table header for dataframe
                t_header = []
                data1 = df['BasicInfo']
                data1_cols = data1.head(1).values.tolist()
                for temp in data1_cols:
                    for rar in temp:
                        t_header.append(rar)

                data1 = data1.tail(-1).values
                data2 = df[col_name]
                data2_cols = data2.head(1).values.tolist()
                for temp in data2_cols:
                    for rar in temp:
                        t_header.append(rar)

                data2 = data2.tail(-1).values

                # Merging teh existing column with the BasicInfo Column
                arr = np.column_stack((data1, data2))
                data = arr.tolist()

                # Adding pagination to the dataframe by 10 rows per page
                paginator = Paginator(data, 10)
                page = request.GET.get('page')
                data = paginator.get_page(page)

            except Exception as e:
                # Checking for any exception
                print('Check for: ', e)

                # Code incase BasicInfo column is not present in the dataframe

                # Creating a table header for dataframe
                t_header = []
                t_header_cols = df[col_name].head(1).values.tolist()
                for temp in t_header_cols:
                    for rar in temp:
                        t_header.append(rar)

                data = df[col_name].tail(-1).values.tolist()

                # Adding pagination to the dataframe by 10 rows per page
                paginator = Paginator(data, 10)
                page = request.GET.get('page')
                data = paginator.get_page(page)

                print('BasicInfo Column NOT present the Excel Sheet!')

        # Redirecting to display_sheet.html page with following attributes.
        return render(request, 'App/display_sheet.html',
                      {'columns': columns,
                       'file_name': file_name,
                       'sheet_name': sheet_name,
                       'data': data,
                       't_header': t_header})
    except Exception as e:
        print('************ Check: ', e, ' *********************')


# sheet view function
def sheet(request, file_id, file_name, sheet_name):

    # Accessing the local file object using file ID
    obj = ExcelFile.objects.get(id=file_id)

    # Accessing the Sub sheet in the Excel file using sheet_name attribute
    df1 = pd.read_excel(obj.file, sheet_name=sheet_name)

    # Data cleaning and transformation
    columns = [col for col in df1.columns if not 'Unnamed' in col]

    # Another data frame to access records
    df = pd.read_excel(obj.file, sheet_name=sheet_name, header=2)

    # Exception Handling for grouping columns
    try:
        # Data cleaning and transformation
        warnings.filterwarnings("ignore")
        df.columns = df.columns.str.replace(r'[#,@,&,.,\d+,' ']', '')

        # Grouping the columns using groupby
        grouped_df = df.groupby(df.columns, axis=1).sum()

        data = df.values.tolist()

        # Redirecting to sheet_columns.html page with following information.
        return render(request, 'App/sheet_columns.html',
                      {'columns': columns, 'file_name': file_name, 'sheet_name': sheet_name, 'data': data,
                       'grouped_df': grouped_df, 'df': df,
                       'file_id': obj.id})
    except Exception as e:
        print('************ Check: ', e, ' *********************')
