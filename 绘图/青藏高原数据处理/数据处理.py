import os
import re
import pandas as pd
import datetime
import numpy as np
import xarray as xr


def extract_coordinates(filename):
    pattern = r"data_(\d+\.\d+)_(\d+\.\d+)"
    match = re.match(pattern, filename)
    if match:
        lat, lon = float(match.group(1)), float(match.group(2))
        return lat, lon
    else:
        return None


def read_first_column(file_path):
    with open(file_path, 'r') as f:
        raw_data = f.readlines()

    data = []
    for row in raw_data:
        fields = row.split()
        data.append(fields)

    df = pd.DataFrame(data)
    column_names = ['tp', 'tem', 'win', 'win1']
    df.columns = column_names
    return df['tp'].values


def create_time_dimension(start_year, end_year):
    start_date = datetime.date(start_year, 1, 1)
    end_date = datetime.date(end_year, 12, 31)
    delta = datetime.timedelta(days=1)
    time_dimension = []
    while start_date <= end_date:
        time_dimension.append(start_date)
        start_date += delta
    return time_dimension


folder_path = "/home/wangxianghao/dyl/yyuchen/青藏高原数据处理/raw_data"
time_dimension = create_time_dimension(1957, 2020)

data_dict = {}

for file in os.listdir(folder_path):
    coordinates = extract_coordinates(file)
    if coordinates:
        lat, lon = coordinates
        print(f"文件名：{file}，纬度：{lat}，经度：{lon}")
        file_path = os.path.join(folder_path, file)
        first_column = read_first_column(file_path)

        if len(first_column) != len(time_dimension):
            missing_days = len(time_dimension) - len(first_column)
            first_column = np.concatenate((first_column, [np.nan] * missing_days))

        time_series = pd.Series(first_column, index=time_dimension)
        data_dict[(lat, lon)] = time_series


# Create xarray Dataset
lats, lons = zip(*data_dict.keys())
lats_grid = np.unique(sorted(lats)) - 2.5
lons_grid = np.unique(sorted(lons)) - 2.5
data_vars = {'tp': (('lon', 'lat', 'time'), np.zeros((len(lons_grid), len(lats_grid), len(time_dimension))), {'units': 'mm'})}

coords = {'time': np.array(time_dimension, dtype='datetime64'), 'lat': lats_grid, 'lon': lons_grid}
dataset = xr.Dataset(data_vars=data_vars, coords=coords)

# Fill in the data
for idx_lat, lat in enumerate(lats_grid):
    for idx_lon, lon in enumerate(lons_grid):
        center_lat = lat + 2.5
        center_lon = lon + 2.5
        if (center_lat, center_lon) in data_dict:
            dataset['tp'].loc[lon, lat, :] = data_dict[(center_lat, center_lon)].values

# Save the dataset to a NetCDF file
dataset.to_netcdf('output.nc')

