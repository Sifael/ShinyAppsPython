from multiprocessing.sharedctypes import Value
import pandas as pd
from janitor import clean_names
from typing import List, Optional 

class DataSet:

    def __init__( self, data_path: Optional[str] = None, date_column: Optional[str] = None):
        self.data_path = data_path
        self.date_column = date_column
        self.data: Optional[pd.DataFrame] = None

    
    def read_csv(self):
        if not self.data_path:
            raise ValueError("data_path must be provided")

        try:
            self.data = pd.read_csv(self.data_path)
            self.data = clean_names(self.data)
        except Exception as e:
            raise RuntimeError(f"Failed to read csv file {e}") from e

    def _ensure_data_loaded(self):
        if self.data is None:
            raise ValueError("Data has not been loaded. Call read_csv() first")


    def get_column_names(self):
        self._ensure_data_loaded()
        return list(self.data.columns)


    def get_numeric_columns(self):
        self._ensure_data_loaded()
        return self.data.select_dtypes(include="number")


    def get_numeric_column_names(self) -> List[str]:
        """Return capitalized names of numeric columns."""
        numeric_cols = self.get_numeric_columns().columns
        return [col.capitalize() for col in numeric_cols]


    def process_data(self):
        self.read_csv()

        if not self.date_column:
            raise Value("date_column must be specified")

        if self.date_column not in self.data.columns:
            raise KeyError(f"{self.date_column} not found in the data")

        self.data[self.date_column] = pd.to_datetime(self.data[self.date_column])
        self.data.rename(
            columns = lambda col: col.split("_worldwide")[0].capitalize(),
            inplace=True
        )

        