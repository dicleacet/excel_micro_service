import pandas as pd
from datetime import datetime
import uuid
from app.settings import BASE_DIR
import os, json

dir_path = BASE_DIR / 'media/json_files'


class AutoVariable:
    def __init__(self, file):
        self.df = pd.read_excel(file)
        self.value_mean = {
            "columns": [],
            "rows": []
        }
        self.category = []

    def info_file(self):
        numerics = ['int16', 'int32', 'int64', 'float16', 'float32', 'float64']
        numeric = dict(self.df.select_dtypes(include=numerics))
        self.df = self.df.drop(numeric, axis=1)
        category = dict(self.df.nunique() <= 8)
        return category, numeric

    # def categorical_fill(self, category):
    #     for col in category:
    #         shape = dict(self.df.pivot_table(columns=[col], aggfunc='size'))
    #         try:
    #             print(self.df[col])
    #             self.df[col] = self.df[col].fillna(min(shape))
    #         except TypeError:
    #             self.df[col] = self.df[col].fillna(0)

    def convert_json(self, datas):
        dict_data = [
                    {
                        "numeric": datas['numeric'],
                        "alias":[],
                    },
                    {
                        "categorical": datas['categorical'],
                        "alias": [],
                    },
                    {
                        "open_ended": datas['open_ended'],
                        "alias": [],
                    }
                ]
        if not os.path.exists(dir_path):
            os.mkdir(dir_path)
        for data in datas['numeric']:
            dict_data[0]['alias'].append(list(self.df[data]))
        for data in datas['categorical']:
            dict_data[1]['alias'].append(list(self.df[data]))
        for data in datas['open_ended']:
            dict_data[2]['alias'].append(list(self.df[data]))
        file_name = str(uuid.uuid4()) + '.json'
        json.dump(dict_data, open(dir_path / file_name, 'w'))
        return f'media/json_files/{file_name}'

    def convert_categorical_data(self, category):
        for col in category:
            self.value_mean['columns'].append(col)
            dataframe = self.df[col].astype('category')
            self.value_mean['rows'].append(dict(enumerate(dataframe.cat.categories)))
            self.df[col] = dataframe.cat.codes
        return self.value_mean

    def split_data(self, datas):
        numeric = []
        categorical = []
        open_ended = []
        self.df.fillna(0, inplace=True)
        for data in datas:
            if data['categorical']:
                categorical.append(data['name'])
            if data['open_ended']:
                open_ended.append(data['name'])
            if data['numeric']:
                numeric.append(data['name'])
        value_mean = self.convert_categorical_data(categorical)
        data = {
            'numeric': numeric,
            'categorical': categorical,
            'open_ended': open_ended,
        }
        file_path = self.convert_json(data)
        return value_mean, file_path
