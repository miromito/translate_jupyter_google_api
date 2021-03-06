import pandas as pd
pd.set_option('display.max_columns', 100)

import os
from collections import OrderedDict
from IPython.core.display import display, HTML
from datetime import datetime, timedelta

import nltk
nltk.download('punkt')

#INPUT PATH TO YOUR FILE BELOW:
input_path = r"C:\Users\MyUser\MyFolder\MyCsvFile.csv"

def translate_FR_to_EN(text, from_lang, to_lang, capitalize=True):
    import json
    import requests
    import html
    from nltk import sent_tokenize
    
    if capitalize:
        text = ' '.join([sent.capitalize() for sent in sent_tokenize(text)])
        
    url_pattern = "https://www.googleapis.com/language/translate/v2?key={}&source={}&target={}&q={}"
    
#INPUT YOUR API KEY BELOW:    
    API_key = 'MyApiKey'
    
    response = requests.get(url_pattern.format(API_key, from_lang, to_lang, text))
    
    return html.unescape(json.loads(response.text,)['data']['translations'][0]['translatedText'])

translate_sufix = 'INITIAL_to_EN'

input_dir = os.path.dirname(input_path)
input_filename, file_ext = os.path.splitext(os.path.basename(input_path))
output_file = os.path.join(input_dir, input_filename + translate_sufix + file_ext)

output_path = os.path.join(input_dir, output_file)

input_data = pd.read_csv(input_path, encoding='utf-8')
imput_column_list = list(input_data.columns)
imput_column_list


columns_to_translate = OrderedDict(
    [
#INPUT YOUR COLUMNS HEADERS BELOW    
('TEXT',
 'TEXT TRANSLATED'),
( '('TEXT_1',
 'TEXT_1 TRANSLATED')')
    ]
)


columns_to_check = []

for key, val in columns_to_translate.items():
    columns_to_check.append(key)
    columns_to_check.append(val)

# fill all empty cells in columns to tramslate with '' instead fo NaN
for col_name in columns_to_translate:
    input_data[col_name] = input_data[col_name].fillna('')
    input_data[columns_to_translate[col_name]] = input_data[columns_to_translate[col_name]].fillna('')

# output_column_list -  with additional columns for traslation
# output_column_list = []

output_data = input_data

# for col_name in imput_column_list:
#     output_column_list.append(col_name)
#     if col_name in columns_to_translate:
#         output_column_list.append(col_name + translate_sufix)
#         output_data[col_name + translate_sufix] = ''
        
# # rearanging columns, so columns with translation goes right after columns to translate
# output_data = output_data[output_column_list]


pattern = '{:>6}   {:>7}   {:_<30} {:_<40}  {}'

row = '<tr><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td></tr>'

header = ['Column Letter',
          'col_num',
          'field name',
          'actual field name',
          'char num',
          'line num']

header_row = row.format(*header)

table = '<table>{}{}</table>'

table_body = ''

for field_name in columns_to_translate:
    info = [
        '-',
        list(input_data.columns).index(field_name)+1,
        '-',
        field_name,
        input_data[field_name].fillna('').map(lambda x: len(str(x))).sum(),
        len(input_data[field_name].fillna(''))
    ]
    
    table_body += (row.format(*info) + '\n')
    

display(HTML(table.format(header_row, table_body)))

started_time = datetime.now()


for index, row in output_data.iterrows():
    # writing data row by row to not lose translation if something happened
    output_data.to_csv(output_path, encoding='utf-8', index=False)
    
    for col_name, data in row.iteritems():
        if (col_name in columns_to_translate) and (index >= 0
                                                ):
                                                #INPUT SOURCE AND DESTINATION LANGUAGE BELOW. IN THIS EXAMPLE - FROM FRENCH TO ENGLISH ('fr', 'en')
            translated_text = translate_FR_to_EN(data, 'fr', 'en')
            
            print('{} {}\n\n{}\n\n{}\n\n'.format(index, col_name, data, translated_text))
            
            output_data.set_value(index, columns_to_translate[col_name], translated_text)
            
            print(datetime.now() - started_time)
            
    
        

    #break

output_data.loc[:, columns_to_check]
