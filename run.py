import gspread 
from google.oauth2.service_account import Credentials

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
    print("Please enter sales from the last market")
    print("Data should be six numbers, separated by commas")
    print("e.e 10,20,30,40,50\n")

    data_str = input("Enter your data here: ")
    print(f"rhe data provided is {data_str}")

get_sales_data()