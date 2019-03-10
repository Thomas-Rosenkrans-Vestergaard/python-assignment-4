import requests
import pandas as pd
from zipfile import ZipFile
from io import StringIO
import os

def download_file(url, to='.'):
    """ Downloads and writes to disc a file from the provided url. 
        The name of the file is taken from the Content-Disposition header.
        The to parameter can be used to change the directory the file is saved in.
        If the directory does not exist, one will be created.
    """ 
    response = requests.get(url, allow_redirects=True)
    base = to.rstrip('/').rstrip('\\')
    filename = base + '/' + response.headers['Content-Disposition'].split('=')[1]
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    open(filename, 'wb').write(response.content)
    return filename

def extract_csv_from_zip(zip_filename, in_dir = '.', to_dir = None):
    """ Extracts a csv file from the provided zip file. 
        The csv file must have the same name as the zip file (Ignoring extension).
    """

    if to_dir is None:
        to_dir = in_dir

    in_dir = in_dir.rstrip('/').rstrip('\\')
    with ZipFile(zip_filename, 'r') as zipObj:
        zipObj.extractall(to_dir)
        csv_filename = to_dir + '/' + zip_filename.replace('.zip', '.csv').lstrip(in_dir).lstrip('/').lstrip('\\')
        return csv_filename

def read_csv_pandas(csv_filename, ignore_lines = 0, delimiter = ','):
    """ Reads the contents of a csv file into a pandas DataFrame. """
    with open(csv_filename) as f:
        lines = f.readlines()
        return pd.read_csv(StringIO(''.join(lines[ignore_lines:])), delimiter)

def filter_column(data, column, values):
    if len(values) < 1:
        return data.iloc[0:0]

    series = data[column]
    mask = (series == values[0])
    for value in values[1:]:
        mask = mask | (series == value)
    
    return data.loc[mask]

def filter_country_code(data, *country_codes):
    return filter_column(data, 'Country Code', country_codes)

def get_years(data):
    return data.columns[4:-1]

def get_years_data(data):
    return data[data.columns[4:-1]]

def get_country_codes(data, indicies=None):
    """ Returns the country codes from a data set.
        When indicies = None all country codes are returned.
        When indecies != None, the country codes, in the provided indicies, are returned.
    """
    
    if indicies is None:
        return data['Country Code']

    return data.loc[indicies]['Country Code']

def normalize(data):
    codes = get_country_codes(data)
    data = get_years_data(data)
    data = data.transpose()
    data = data.interpolate()
    data = data.dropna()
    data.columns = codes
    return data

def plot(data):
    return data.plot(marker='o', linestyle='-', ms=3)