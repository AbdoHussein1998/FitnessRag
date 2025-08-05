from .GoogleSheetAssets import df_connection
from ProjectAssetes import get_logger
from gspread.exceptions import APIError  # still useful for other API issues

class Questions:
    def __init__(self):
        self.WORKSHEETURL = "https://docs.google.com/spreadsheets/d/1xoeMltpJO8P7bINy7gSKZVRkJ7QfvGqq2T2dArkiz70/edit?gid=884513156#gid=884513156"
        self.SHEETNAME = "Form Responses 1"
        self.logger = get_logger("Questions")
        self.sheet = None
        self.clean_sheet=None
    def download_sheet(self):
        try:
            df = df_connection(
                url=self.WORKSHEETURL,
                sheet_name=self.SHEETNAME,
                cell_range="A:ZZZ"
            )

            df.columns = df.iloc[0]
            df = df.drop(index=0).reset_index(drop=True)
            self.sheet = df

        except PermissionError as ex:
            self.logger.error(f"Permission denied while accessing the sheet: {ex}")
        except APIError as ex:
            self.logger.error(f"Google Sheets API error: {ex}")
        except Exception as ex:
            self.logger.exception("Unexpected error occurred while downloading the sheet")

    def cleaning_the_sheet(self):
        self.sheet.rename(columns={ 'سؤال العميل ':"Question",
                   'الإجابة ':"Answer"},inplace=True)
        self.clean_sheet=self.sheet[~self.sheet[["Timestamp","Question","Answer"]].eq("").all(axis=1)] 
    
    def get_questions(self):
        self.download_sheet()
        self.cleaning_the_sheet()
        return self
