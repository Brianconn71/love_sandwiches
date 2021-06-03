import gspread 
from google.oauth2.service_account import Credentials
from pprint import pprint

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('love_sandwiches')

def get_sales_data():
    """
        Get sales input figures from users
    """
    while True:
        print("Please enter sales from the last market")
        print("Data should be six numbers, separated by commas")
        print("e.e 10,20,30,40,50\n")

        data_str = input("Enter your data here: ")

        sales_data = data_str.split(",")
        if validate_data(sales_data):
            print("Data is valid")
            break
    
    return sales_data


def validate_data(values):
    """
        inside the try, converts all string values injto integers.
        Raises ValueError if string cammot be converted into ints
        or if there aren't six values.
    """
    try:
        [int(value) for value in values]
        if len(values) != 6:
            raise ValueError(
            f"exactly 6 values required, you provided {len(values)}"
        )
    except ValueError as e:
        print(f"Invalid data: {e}, please try again.\n")
        return False

    return True


# def update_sales_worksheet(data):
#     """
#         update sales worksheet, add new row with the list data provided.
#     """
#     print("Updating sales worksheet...\n")
#     sales_worksheet = SHEET.worksheet("sales")
#     sales_worksheet.append_row(data)
#     print("Sales Worksheets updated successfully\n")

def calculate_surplus_data(sales_row):
    """
        Compare sales with stock and calculate the surplus for each item.
        Surplus id defined as sales figures subtracted from the stock.
    """
    print("Calculating surplus data...\n")
    stock = SHEET.worksheet('stock').get_all_values()
    stock_row = stock[-1]

    surplus_data = []
    for stock, sales in zip(stock_row, sales_row):
        surplus = int(stock) - int(sales)
        surplus_data.append(int(surplus))
    return surplus_data

# def update_surplus_worksheet(data):
#     """
#         update surplus worksheet, add new row with the list data provided.
#     """
#     print("Updating surplus worksheet...\n")
#     surplus_worksheet = SHEET.worksheet("surplus")
#     surplus_worksheet.append_row(data)
#     print("surplus Worksheets updated successfully\n")

def update_worksheet(data, worksheet):
    """
        receive a list of integers to be inserted into a worksheet
        update the relevant worksheet with the data provided
    """
    print(f"Updating {worksheet} worksheet...\n")
    worksheet_to_update = SHEET.worksheet(worksheet)
    worksheet_to_update.append_row(data)
    print(f"{worksheet} worksheet updated successfullt \n")


def get_last_5_entries_sales():
    """
        collects columns of data from sales worksheet, collecting the last 5 entries for each sandwich and returns the data as a list of lists
    """
    sales = SHEET.worksheet('sales')
    # column = sales.col_values(3)
    # print(column)

    columns = []
    for x in range(1,7):
        column = sales.col_values(x)
        columns.append(column[-5:])
    return columns

def main():
    """
        Run all program functions
    """
    data = get_sales_data()
    sales_data = [int(num) for num in data]
    update_worksheet(sales_data, "sales")
    new_surplus_data = calculate_surplus_data(sales_data)
    update_worksheet(new_surplus_data, "surplus")

print("Welcome to Love Sandwiches Data Automation")
# main()
sales_columns = get_last_5_entries_sales()