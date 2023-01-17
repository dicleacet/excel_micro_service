import pandas as pd
from datetime import datetime
import uuid
from app.settings import BASE_DIR
import os

dir_path = BASE_DIR / 'media/documents'


class AutoVariable:
    def __init__(self, file):
        dir_date = datetime.now().strftime("%Y-%m-%d")
        self.custom_path = f"{dir_date}/{uuid.uuid4()}"
        self.base_path = f"{dir_path}/{self.custom_path}"
        self.file_name = file.name.split(".")[-2]
        self.df = pd.read_excel(file)
        self.value_mean = {}
        self.category = []

    def info_file(self):
        category = dict(self.df.nunique() <= 8)
        return category

    # def categorical_fillna(self):
    #     for col in self.df.columns:
    #         if len(self.df[col].unique()) <= 8:
    #             shape = dict(self.df.pivot_table(columns=[col], aggfunc='size'))
    #             try:
    #                 self.df[col] = self.df[col].fillna(min(shape))
    #             except:
    #                 continue

    # def convert_csv(self):
    #     if not os.path.isdir(self.base_path):
    #         os.makedirs(self.base_path)
    #     self.df.to_csv(f"{self.base_path}/{self.file_name}.csv")
    #
    # def convert_categorical_data(self):
    #     self.categorical_fillna()
    #     for col in self.df.columns:
    #         if len(self.df[col].unique()) <= 8:
    #             dataframe = self.df[col].astype('category')
    #             self.value_mean[col] = dict(enumerate(dataframe.cat.categories))
    #             self.df[col] = dataframe.cat.codes
    #     self.convert_csv()
    #     return f"documents/{self.custom_path}/{self.file_name}.csv", self.value_mean
    #
    #

