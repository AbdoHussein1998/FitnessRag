from ProjectAssetes import get_logger
import gspread
from gspread_dataframe import get_as_dataframe
import os 
import pandas as pd

filename_path = os.path.join(os.getcwd(), "DataBase","GoogleSheet","GoogleSheetAssets", "GoogleSheetAPi.json")


logger=get_logger("Connection To Google Sheet")

# def df_connection(url: str, sheet_name: str, cell_range: str = None,header:str =None):


#     logger.info("Authentication...")
#     gc = gspread.service_account(filename=filename_path)
#     logger.info("Authentication done successfully")
#     logger.info(f"try to connect to {sheet_name} .....")

#     sheet = gc.open_by_url(url).worksheet(sheet_name)
#     logger.info(f"You're connected to the sheet: {sheet_name}")

#     # If a cell range is provided, use it; otherwise, fetch all data
#     if cell_range :
#             logger.info("cell range ",cell_range)
#             data = sheet.get_all_values(cell_range)  # Fetch the data from the specified range
#             # Convert the data into a dataframe (assuming data has headers in the first row)
#             if header :
#                 header=sheet.get_all_values(header)[0]
#                 logger.info(header)
#             else:
#                 df=pd.DataFrame(data)
#                 df.columns = ['Column_' + str(col) for col in df.columns]

#     else:
#             # Fetch all data and get actual values (no formula evaluation)
#             df = get_as_dataframe(sheet, evaluate_formula=False)


#     logger.info(f"Your Data from the sheet ( {sheet_name} ) is downloaded successfully")
#     return df




from typing import Optional
import pandas as pd
import gspread
from gspread_dataframe import get_as_dataframe

def df_connection(
    url: str,
    sheet_name: str,
    cell_range: Optional[str] = None,
    header_range: Optional[str] = None
) -> pd.DataFrame:
    logger.info("Authenticating with Google Sheets...")
    gc = gspread.service_account(filename=filename_path)
    logger.info("Authentication successful.")

    logger.info(f"Connecting to sheet: {sheet_name}")
    sheet = gc.open_by_url(url).worksheet(sheet_name)
    logger.info(f"Connected to sheet: {sheet_name}")

    if cell_range:
        logger.info(f"Fetching data from range: {cell_range}")
        data = sheet.get(cell_range)

        if header_range:
            logger.info(f"Fetching header from range: {header_range}")
            header = sheet.get(header_range)[0]
            df = pd.DataFrame(data, columns=header)
        else:
            df = pd.DataFrame(data)
            df.columns = [f"Column_{i}" for i in range(len(df.columns))]
            logger.warning("No header specified. Using default column names.")
    else:
        logger.info("No cell range provided. Fetching entire sheet.")
        df = get_as_dataframe(sheet, evaluate_formula=False)
        logger.info("Dataframe created from full sheet.")

    logger.info(f"Data from sheet '{sheet_name}' downloaded successfully.")
    return df
