import json
import os
import uuid
import pandas as pd
from app.settings import BASE_DIR

dir_path = BASE_DIR / 'media/json_files'


class AutoVariable:
    def __init__(self, file):
        self.df = pd.read_excel(file)
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
        print(datas)
        if not os.path.exists(dir_path):
            os.mkdir(dir_path)
        for data in datas['numeric']['columns']:
            datas['numeric']['rows'].append(list(self.df[data]))
        for data in datas['open_ended']['columns']:
            datas['open_ended']['rows'].append(list(self.df[data]))
        file_name = str(uuid.uuid4()) + '.json'
        json.dump(datas, open(dir_path / file_name, 'w'))
        return f'media/json_files/{file_name}'

    def convert_categorical_data(self, category):
        all_rows = []
        for col in category:
            rows = []
            dataframe = self.df[col].astype('category')
            alias = dict(enumerate(dataframe.cat.categories))
            self.df[col] = dataframe.cat.codes
            for key in self.df[col]:
                value = alias.get(key)
                row = {
                    'value': value,
                    'alias': key
                }
                rows.append(row)
            all_rows.append(rows)
        return all_rows

    def split_data(self, datas):
        numeric = {
            'columns': [],
            'rows': []
        }
        categorical = {
            'columns': [],
            'rows': []
        }
        open_ended = {
            'columns': [],
            'rows': []
        }
        for data in datas:
            if data['categorical']:
                categorical['columns'].append(data['name'])
            if data['open_ended']:
                open_ended['columns'].append(data['name'])
            if data['numeric']:
                numeric['columns'].append(data['name'])
        categorical_rows = self.convert_categorical_data(categorical['columns'])
        categorical['rows'] = categorical_rows
        data = {
            'numeric': numeric,
            'categorical': categorical,
            'open_ended': open_ended,
        }
        file_path = self.convert_json(data)
        return file_path
