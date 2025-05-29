# import numpy as np
# import pandas as pd
# import os
# import re

# def to_snake_case(s):
#     s = re.sub(r'([A-Z])', r'_\1', s)
#     s = s.replace(' ', '_')
#     s = s.replace('__', '_')
#     return s.lower()

# def process_file(input_file):
#     with open(input_file) as f:
#         data = f.read()
#         headers = re.findall(r'"([a-zA-Z0-9 .]+)"', data)
#         headers = [to_snake_case(header) for header in headers]
#         data = data.split('Data {')[1].split('}')[0].split()
#         data = np.array(data, dtype=float)

#         data_dict = {header: [] for header in headers}
#         for i, value in enumerate(data):
#             header = headers[i % len(headers)]
#             data_dict[header].append(value)

#         dataframe = pd.DataFrame(data_dict)
#         output_file = os.path.splitext(input_file)[0] + '.csv'
#         print(output_file)
#         return dataframe.to_csv(output_file, index=False)
        

# # process_file('/Users/sonnyding/Documents/code/tcad-plt2csv/nmos_idvg_01.plt')

import numpy as np
import pandas as pd
import re
import os

def to_snake_case(s):
    s = re.sub(r'[()\s,.-]+', '_', s)
    s = re.sub(r'([A-Z])', r'_\1', s)
    s = s.replace(' ', '_')
    s = s.replace('__', '_')
    s = s.strip('_')
    return s.lower()

def process_file(file_obj, output_dir):
    data = file_obj.read().decode('utf-8')
    headers = re.findall(r'"([a-zA-Z0-9 .(),-]+)"', data)
    headers = [to_snake_case(header) for header in headers]
    data = data.split('Data {')[1].split('}')[0].split()
    data = np.array(data, dtype=float)

    data_dict = {header: [] for header in headers}
    for i, value in enumerate(data):
        header = headers[i % len(headers)]
        data_dict[header].append(value)

    dataframe = pd.DataFrame(data_dict)
    
    output_file = os.path.join(output_dir, os.path.splitext(file_obj.name)[0] + '.csv')
    
    dataframe.to_csv(output_file, index=False)
    return output_file