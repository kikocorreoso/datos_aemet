#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep  3 12:37:14 2017

@author: tornado
"""

import os
from glob import glob
import datetime as dt
from functools import reduce

import numpy as np
import matplotlib.pyplot as plt
plt.style.use("bmh")
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq

def convert_dt(x):
    """Function to convert times with format 'HH:MM' or 'HH' to an UTC 
    timestamp"""
    try:
        if isinstance(x[1], float):
            return np.nan
        elif x[1] != 'Varias' and ':' in x[1]:
            hh = int(x[1][:2])
            if hh == 24: hh = 0
            mm = int(x[1][-2:])
            if hh > 23 or mm > 60:
                return np.nan
            return dt.datetime(x[0].year, x[0].month, x[0].day, hh, mm)
        elif x[1] != 'Varias' and ':' not in x[1]:
            hh = int(x[1])
            if hh == 24: hh = 0
            mm = int(x[1][-2:])
            return dt.datetime(x[0].year, x[0].month, x[0].day, hh, 0)
        else:
            return np.nan
    except:
        print(x)
        return np.nan

def convert_d(x):
    """Function to convert dates to an UTC timestamp"""
    try:
        if isinstance(x[1], float):
            if np.isnan(x[1]):
                return np.nan
            else:
                return dt.datetime(x[0].year, x[0].month, int(x[1]), 0, 0)
        elif x[1] != 'Varias':
            return dt.datetime(x[0].year, x[0].month, int(x[1]), 0, 0)
        else:
            return np.nan
    except:
        print(x)
        return np.nan

def parse_rainfall(rf):
    """'Ip' value is when rainfall is below 0.1 mm.
    These values are returned as 0.05. Indicating that rainfall was very low
    but there was rainfall."""
    if rf == 'Ip':
        return 0.05
    elif isinstance(rf, float):
        return np.nan
    elif rf == 'Acum':
        return np.nan
    else:
        return float(rf.replace(',', '.'))

def parse_coords(coord):
    dd = float(coord[:2])
    mm = float(coord[2:4]) / 60
    ss = float(coord[4:6]) / 3600
    di = coord[-1]
    if di == 'N':
        return dd + mm + ss
    if di == 'S':
        return -(dd + mm + ss)
    if di == 'E':
        return dd + mm + ss
    if di == 'W':
        return -(dd + mm + ss)

path_aemet = os.path.join(os.path.pardir, 'aemet_original_data')
# Read of master metadata of stations
master = pd.read_csv(
    os.path.join(path_aemet, 'maestro.csv'), 
    delimiter=';',
    encoding='latin1',
    converters={'INDSINOP': str}
)
master['LONGITUD'] = [parse_coords(ll) for ll in master['LONGITUD']]
master['LATITUD'] = [parse_coords(ll) for ll in master['LATITUD']]
master.rename(
    columns={
        'INDICATIVO': 'station_code',
        'NOMBRE': 'station_name', 
        'PROVINCIA': 'province', 
        'ALTITUD': 'altitude', 
        'LATITUD': 'latitude', 
        'LONGITUD': 'longitude', 
        'INDSINOP': 'synop_code'
    },
    inplace=True
)

# HDFStore object to be filled below.
store = pd.HDFStore(
    os.path.join(os.path.pardir, 'hdf5', 'aemet.h5'), 
    mode = 'w'
)

# Processing of daily by station and by year data.
path_daily_sta = os.path.join(path_aemet, 'daily', 'by_station')
path_daily_year = os.path.join(path_aemet, 'daily', 'by_year')
paths = (path_daily_sta, path_daily_year)
for path in paths:
    files = glob(os.path.join(path, '*.CSV.gz'))
    for f in files:
        print(f)
        df = pd.read_csv(
            f, 
            delimiter=';', 
            header=0, 
            encoding='latin1',
            parse_dates=[[4, 5, 6]],
            decimal=',',
            converters={'Indicativo': str}
        )
        # Rename columns
        df.rename(columns={
                'Indicativo': 'station_code',
                'Nombre': 'station_name',
                'Provincia': 'province',
                'Altitud': 'altitude',
                'Año_Mes_Dia': 'date',
                'T.Max': 'temperature_max[C]',
                'Hora': 'temperature_max_timestamp',
                'T.Min': 'temperature_min[C]',
                'Hora.1': 'temperature_min_timestamp',
                'T.Med': 'temperature_avg[C]',
                'Racha': 'windspeed_gust[m/s]',
                'Dir': 'winddirection_gust[degrees]',
                'Hora.2': 'wind_gust_timestamp',
                'Vel.media': 'windspeed_avg[m/s]',
                'Prec.': 'rainfall[mm]',
                'Sol': 'sun[h]',
                'Pres.máx': 'pressure_max[hPa]',
                'Hora.3': 'pressure_max_timestamp',
                'Pres.min': 'pressure_min[hPa]',
                'Hora.4': 'pressure_min_timestamp'
            },
            inplace=True
        )
        # Correct some time columns...
        cols = ['date', 'temperature_max_timestamp']
        temperature_max_timestamp = [convert_dt(t) for t in df[cols].values]
        df['temperature_max_timestamp'] = temperature_max_timestamp
        cols = ['date', 'temperature_min_timestamp']
        temperature_min_timestamp = [convert_dt(t) for t in df[cols].values]
        df['temperature_min_timestamp'] = temperature_min_timestamp
        cols = ['date', 'wind_gust_timestamp']
        wind_gust_timestamp = [convert_dt(t) for t in df[cols].values]
        df['wind_gust_timestamp'] = wind_gust_timestamp
        cols = ['date', 'pressure_max_timestamp']
        pressure_max_timestamp = [convert_dt(t) for t in df[cols].values]
        df['pressure_max_timestamp'] = pressure_max_timestamp
        cols = ['date', 'pressure_min_timestamp']
        pressure_min_timestamp = [convert_dt(t) for t in df[cols].values]
        df['pressure_min_timestamp'] = pressure_min_timestamp
        # correct rainfall column
        rainfall = [parse_rainfall(rf) for rf in df['rainfall[mm]'].values]
        df['rainfall[mm]'] = rainfall
        # Reindex again
        # Check if metadata in master and in file are the same
        station_code = df.iloc[0]['station_code']
        metadata = master[master['station_code'] == station_code]
        if len(metadata) != 1:
            print(station_code, metadata)
        if df.iloc[0]['station_name'] != metadata.iloc[0]['station_name']:
            print(station_code, 'wrong_station_name')
        if df.iloc[0]['province'] != metadata.iloc[0]['province']:
            print(station_code, 'wrong_province_name')
        if df.iloc[0]['altitude'] != metadata.iloc[0]['altitude']:
            print(station_code, 'wrong_station_altitude')
        # if metadata correct, add lat and lon columns
        df['latitude'] = metadata.iloc[0]['latitude']
        df['longitude'] = metadata.iloc[0]['longitude']
        df['synop_code'] = metadata.iloc[0]['synop_code']
        # reorder columns for the output
        cols = [
            'date', 'station_code', 'synop_code', 'station_name', 'province', 
            'altitude', 'latitude', 'longitude',
            'temperature_max[C]', 'temperature_max_timestamp',
            'temperature_min[C]', 'temperature_min_timestamp',
            'temperature_avg[C]', 'windspeed_gust[m/s]',
            'winddirection_gust[degrees]', 'wind_gust_timestamp',
            'windspeed_avg[m/s]', 'rainfall[mm]', 'sun[h]', 'pressure_max[hPa]',
            'pressure_max_timestamp', 'pressure_min[hPa]',
            'pressure_min_timestamp'
        ]
        # save csv file
        out_file = f.replace('aemet_original_data', 'csv')
        df[cols].to_csv(out_file, compression='gzip', index=False)
        # save parquet file
        out_file = f.replace('aemet_original_data', 'parquet')
        out_file = out_file.replace('CSV.gz', 'parquet')
        table = pa.Table.from_pandas(df[cols])
        pq.write_table(table, out_file, compression='gzip')
#        # Save HDF5 file
        if "by_station" in path:
            path_parts = f.split(os.path.sep)
            route = "/".join([
                path_parts[2], 
                path_parts[3], 
                'station' + path_parts[4].split('.')[0]
            ])
            reduced_cols = cols = [
                'date',
                'temperature_max[C]', 'temperature_max_timestamp',
                'temperature_min[C]', 'temperature_min_timestamp',
                'temperature_avg[C]', 'windspeed_gust[m/s]',
                'winddirection_gust[degrees]', 'wind_gust_timestamp',
                'windspeed_avg[m/s]', 'rainfall[mm]', 'sun[h]', 'pressure_max[hPa]',
                'pressure_max_timestamp', 'pressure_min[hPa]',
                'pressure_min_timestamp'
            ]
            store.put(route, df[cols])
            route = [
                'root', 
                path_parts[2], 
                path_parts[3], 
                'station' + path_parts[4].split('.')[0]
            ]
            grp = reduce(getattr, route, store)
            # We add metadata to the df group saving space of unuseful
            # repeated data columns
            meta = {
                'code': metadata.iloc[0]['station_code'],
                'synop_code': metadata.iloc[0]['synop_code'],
                'name': metadata.iloc[0]['station_name'],
                'province': metadata.iloc[0]['province'],
                'altitude': metadata.iloc[0]['altitude'],
                'latitude': metadata.iloc[0]['latitude'],
                'longitude': metadata.iloc[0]['longitude']
            }
            grp._v_attrs['aemet_station_metadata'] = meta
            # We also add metadata about each column meaning and units
            meta = {
                'date': "Day when the records were measured",
                'temperature_max[C]': (
                    "Maximum temperature recorded during the day in Celsius "
                    "degrees."
                ),
                'temperature_max_timestamp': (
                    "Timestamp (UTC) when the maximum temperature was "
                     "recorded."
                ),
                'temperature_min[C]': (
                    "Minimum temperature recorded during the day in Celsius "
                    "degrees."
                ),
                'temperature_min_timestamp': (
                    "Timestamp (UTC) when the minimum temperature was "
                     "recorded."
                ),
                'temperature_avg[C]': (
                    "Average temperature recorded during the day in Celsius "
                    "degrees."
                ), 
                'windspeed_gust[m/s]': (
                    "Wind speed gust recorded during the day in meters per "
                    "second."
                ),
                'winddirection_gust[degrees]': (
                    "Direction of the wind gust recorded during the day in "
                    "degrees clockwise from the North."
                ),
                'wind_gust_timestamp': (
                    "Timestamp (UTC) when the wind gust was recorded."
                ),
                'windspeed_avg[m/s]': (
                    "Average wind speed recorded during the day in meters per "
                    "second."
                ), 
                'rainfall[mm]': (
                    "Accumulated rainfall during the day in mm."
                ), 
                'sun[h]': (
                    "Accumulated hours of sun during the day."
                ),
                'pressure_max[hPa]': (
                    "Maximum air pressure recorded during the day in "
                    "hectopascals."
                ),
                'pressure_max_timestamp': (
                    "Timestamp (UTC) when the maximum air pressure was "
                    "recorded."
                ),
                'pressure_min[hPa]': (
                    "Minimum air pressure recorded during the day in "
                    "hectopascals."
                ),
                'pressure_min_timestamp': (
                    "Timestamp (UTC) when the maximum air pressure was "
                    "recorded."
                ),
            }
            grp._v_attrs['aemet_variables_metadata'] = meta

# Processing of monthly by station and by year data.
path_monthly_sta = os.path.join(path_aemet, 'monthly', 'by_station')
path_monthly_year = os.path.join(path_aemet, 'monthly', 'by_year')
paths = (path_monthly_sta, path_monthly_year)
for path in paths:
    files = glob(os.path.join(path, '*.CSV.gz'))
    for f in files:
        print(f)
        df = pd.read_csv(
            f, 
            delimiter=';', 
            header=0, 
            encoding='latin1',
            parse_dates=[[4, 5]],
            decimal=',',
            converters={'Indicativo': str}
        )
        # Rename columns
        df.rename(columns={
                'Año_Mes': 'date',
                'Indicativo': 'station_code',
                'Nombre': 'station_name',
                'Provincia': 'province',
                'Altitud': 'altitude',
                'T.Med.': 'temperature_avg[C]',
                'T.Max.Med': 'temperature_max_avg[C]',
                'T.Min.Med': 'temperature_min_avg[C]',
                'T.Max.Abs': 'temperature_max[C]',
                'Día': 'temperature_max_timestamp',
                'T.Min.Abs': 'temperature_min[C]',
                'Día.1': 'temperature_min_timestamp',
                'Min.Sup': 'temperature_min_max[C]',
                'Max.Inf': 'temperature_max_min[C]',
                'DíasHelada': 'frost_days_count',
                'Prec.total': 'rainfall[mm]',
                'Prec.max': 'rainfall_max[mm]',
                'Día.2': 'rainfall_max_timestamp',
                'DiasPrec.Apre': 'rainfall_days_001_count',
                'DiasPrecSup10': 'rainfall days_100_count',
                'DíasLluvia':  'rainfall_days_000_count',
                'DíasNieve': 'snow_days_count',
                'DíasGranizo': 'hail_days_count', ############################
                'VelRacha': 'windspeed_gust[m/s]',
                'DirRacha': 'winddirection_gust[degrees]',
                'Dia': 'wind_gust_day',
                'Hora': 'wind_gust_time',
                'DíasRachaSup55': 'windgust_days_55km/h_count',
                'DíasRachaSup91': 'windgust_days_91km/h_count',
                'Vel.media': 'windspeed_avg[m/s]',
                'Insol.media': 'sun_avg[h]', #######################################
                '%Insol': 'sun_avg[%]', ##########################################
                'Pres.media': 'pressure_avg[hPa]',
                'Pres.Max.Abs': 'pressure_max[hPa]',
                'Día.3': 'pressure_max_timestamp',
                'Pres.Min.Abs': 'pressure_min[hPa]',
                'Día.4': 'pressure_min_timestamp',
                'Pres.MediaNivelMar': 'pressure_msl[hPa]'
            },
            inplace=True
        )
        # Correct some time columns...
        cols = ['date', 'temperature_max_timestamp']
        temperature_max_timestamp = [convert_d(t) for t in df[cols].values]
        df['temperature_max_timestamp'] = pd.to_datetime(
            temperature_max_timestamp
        )
        cols = ['date', 'temperature_min_timestamp']
        temperature_min_timestamp = [convert_d(t) for t in df[cols].values]
        df['temperature_min_timestamp'] = pd.to_datetime(
            temperature_min_timestamp
        )
        cols = ['date', 'rainfall_max_timestamp']
        rainfall_max_timestamp = [convert_d(t) for t in df[cols].values]
        df['rainfall_max_timestamp'] = pd.to_datetime(
            rainfall_max_timestamp
        )
        cols = ['date', 'wind_gust_day', 'wind_gust_time']
        wind_gust_timestamp = [
            convert_dt((convert_d(t[:2]), t[2])) for t in df[cols].values
        ]
        df['wind_gust_timestamp'] = pd.to_datetime(wind_gust_timestamp)
        cols = ['date', 'pressure_max_timestamp']
        pressure_max_timestamp = [convert_d(t) for t in df[cols].values]
        df['pressure_max_timestamp'] = pd.to_datetime(pressure_max_timestamp)
        cols = ['date', 'pressure_min_timestamp']
        pressure_min_timestamp = [convert_d(t) for t in df[cols].values]
        df['pressure_min_timestamp'] = pd.to_datetime(pressure_min_timestamp)
        # correct rainfall columns
        rainfall = [parse_rainfall(rf) for rf in df['rainfall[mm]'].values]
        df['rainfall[mm]'] = rainfall
        rainfall = [parse_rainfall(rf) for rf in df['rainfall_max[mm]'].values]
        df['rainfall_max[mm]'] = rainfall
        # Check if metadata in master and in file are the same
        station_code = df.iloc[0]['station_code']
        metadata = master[master['station_code'] == station_code]
        if len(metadata) != 1:
            print(station_code, metadata)
        if df.iloc[0]['station_name'] != metadata.iloc[0]['station_name']:
            print(station_code, 'wrong_station_name')
        if df.iloc[0]['province'] != metadata.iloc[0]['province']:
            print(station_code, 'wrong_province_name')
        if df.iloc[0]['altitude'] != metadata.iloc[0]['altitude']:
            print(station_code, 'wrong_station_altitude')
        # if metadata correct, add lat and lon columns
        df['latitude'] = metadata.iloc[0]['latitude']
        df['longitude'] = metadata.iloc[0]['longitude']
        df['synop_code'] = metadata.iloc[0]['synop_code']
        # reorder columns for the output
        cols = [
            'date', 'station_code', 'synop_code', 'station_name', 'province', 
            'altitude', 'latitude', 'longitude',
            'temperature_avg[C]', 'temperature_max_avg[C]',
            'temperature_min_avg[C]', 'temperature_max[C]',
            'temperature_max_timestamp', 'temperature_min[C]',
            'temperature_min_timestamp', 'temperature_min_max[C]',
            'temperature_max_min[C]', 'frost_days_count', 'rainfall[mm]',
            'rainfall_max[mm]', 'rainfall_max_timestamp', 
            'rainfall_days_001_count', 'rainfall days_100_count', 
            'rainfall_days_000_count', 'snow_days_count',
            'hail_days_count', 'winddirection_gust[degrees]', 
            'windspeed_gust[m/s]', 'wind_gust_timestamp',
            'windgust_days_55km/h_count',  'windgust_days_91km/h_count', 
            'windspeed_avg[m/s]', 'sun_avg[h]', 'sun_avg[%]',
            'pressure_avg[hPa]', 'pressure_max[hPa]', 'pressure_max_timestamp',
            'pressure_min[hPa]', 'pressure_min_timestamp', 'pressure_msl[hPa]',
        ]
#        # save csv file
        out_file = f.replace('aemet_original_data', 'csv')
        df[cols].to_csv(out_file, compression='gzip')
#        # save parquet file
        out_file = f.replace('aemet_original_data', 'parquet')
        out_file = out_file.replace('CSV.gz', 'parquet')
        table = pa.Table.from_pandas(df[cols])
        pq.write_table(table, out_file, compression='gzip')
        # Save HDF5 file
        if "by_station" in path:
            path_parts = f.split(os.path.sep)
            route = "/".join([
                path_parts[2], 
                path_parts[3], 
                'station' + path_parts[4].split('.')[0]
            ])
            reduced_cols = cols = [
                'date',
                'temperature_avg[C]', 'temperature_max_avg[C]',
                'temperature_min_avg[C]', 'temperature_max[C]',
                'temperature_max_timestamp', 'temperature_min[C]',
                'temperature_min_timestamp', 'temperature_min_max[C]',
                'temperature_max_min[C]', 'frost_days_count', 'rainfall[mm]',
                'rainfall_max[mm]', 'rainfall_max_timestamp', 
                'rainfall_days_001_count', 'rainfall days_100_count', 
                'rainfall_days_000_count', 'snow_days_count',
                'hail_days_count', 'winddirection_gust[degrees]', 
                'windspeed_gust[m/s]', 'wind_gust_timestamp',
                'windgust_days_55km/h_count',  'windgust_days_91km/h_count', 
                'windspeed_avg[m/s]', 'sun_avg[h]', 'sun_avg[%]',
                'pressure_avg[hPa]', 'pressure_max[hPa]', 
                'pressure_max_timestamp', 'pressure_min[hPa]', 
                'pressure_min_timestamp', 'pressure_msl[hPa]',
            ]
            store.put(route, df[cols])
            route = [
                'root', 
                path_parts[2], 
                path_parts[3], 
                'station' + path_parts[4].split('.')[0]
            ]
            grp = reduce(getattr, route, store)
            # We add metadata to the df group saving space of unuseful
            # repeated data columns
            meta = {
                'code': metadata.iloc[0]['station_code'],
                'synop_code': metadata.iloc[0]['synop_code'],
                'name': metadata.iloc[0]['station_name'],
                'province': metadata.iloc[0]['province'],
                'altitude': metadata.iloc[0]['altitude'],
                'latitude': metadata.iloc[0]['latitude'],
                'longitude': metadata.iloc[0]['longitude']
            }
            grp._v_attrs['aemet_station_metadata'] = meta
            # We also add metadata about each column meaning and units
            meta = {
                'date': "Month when the records were measured",
                'temperature_avg[C]': (
                    "Average temperature recorded during the month in Celsius "
                    "degrees."
                ), 
                'temperature_max_avg[C]': (
                    "Average of the maximum daily temperatures recorded "
                    "during the month in Celsius degrees."
                ),
                'temperature_min_avg[C]': (
                    "Average of the minimum daily temperatures recorded "
                    "during the month in Celsius degrees."
                ),
                'temperature_max[C]': (
                    "Maximum temperature recorded during the month in Celsius "
                    "degrees."
                ),
                'temperature_max_timestamp': (
                    "Timestamp (UTC) when the maximum temperature was "
                     "recorded."
                ),
                'temperature_min[C]': (
                    "Minimum temperature recorded during the day in Celsius "
                    "degrees."
                ),
                'temperature_min_timestamp': (
                    "Timestamp (UTC) when the minimum temperature was "
                    "recorded."
                ),
                'temperature_min_max[C]':(
                    "Maximum of the minimum daily temperatures recorded "
                    "during the month in Celsius degrees."
                ),
                'temperature_max_min[C]': (
                    "Minimum of the maximum daily temperatures recorded "
                    "during the month in Celsius degrees."
                ),
                'frost_days_count': (
                    "Number of days with temperature below or equal to 0 "
                    "Celsius degrees recorded during the month."
                ), 
                'rainfall[mm]': (
                    "Accumulated rainfall during the month in mm."
                ), 
                'rainfall_max[mm]': (
                    "Maximum daily accumulated rainfall recorded during the "
                    "month in mm."
                ), 
                'rainfall_max_timestamp': (
                    "Timestamp (UTC) when the maximum daily accumulated "
                    "rainfall was recorded."
                ), 
                'rainfall_days_001_count': (
                    "Number of days with accumulated rainfall above 0.1 mm."
                ), 
                'rainfall days_100_count': (
                    "Number of days with accumulated rainfall above 10.0 mm."
                ), 
                'rainfall_days_000_count': (
                    "Number of rainfall days recorded during the month."
                ), 
                'snow_days_count': (
                    "Number of snow days recorded during the month."
                ),
                'hail_days_count': (
                    "Number of hail days recorded during the month."
                ),
                'winddirection_gust[degrees]': (
                    "Direction of the wind gust recorded during the month in "
                    "degrees clockwise from the North."
                ),
                'windspeed_gust[m/s]': (
                    "Wind speed gust recorded during the month in meters per "
                    "second."
                ),
                'wind_gust_timestamp': (
                    "Timestamp (UTC) when the wind gust was recorded."
                ),
                'windgust_days_55km/h_count': (
                    "Number of days with wind gust above 55 km/h."
                ),  
                'windgust_days_91km/h_count': (
                    "Number of days with wind gust above 91 km/h."
                ), 
                'windspeed_avg[m/s]': (
                    "Average wind speed recorded during the month in meters "
                    "second."
                ), 
                'sun_avg[h]': (
                    "Average daily sun isolation recorded during the month "
                    "in hours."
                ),
                'sun_avg[%]': (
                    "Average daily sun isolation recorded during the month "
                    "in percentage."
                ),
                'pressure_avg[hPa]': (
                    "Average air pressure recorded during the month in "
                    "hectopascals."
                ), 
                'pressure_max[hPa]': (
                    "Maximum air pressure recorded during the month in "
                    "hectopascals."
                ),
                'pressure_max_timestamp': (
                    "Timestamp (UTC) when the maximum air pressure was "
                    "recorded."
                ),
                'pressure_min[hPa]': (
                    "Minimum air pressure recorded during the month in "
                    "hectopascals."
                ),
                'pressure_min_timestamp': (
                    "Timestamp (UTC) when the maximum air pressure was "
                    "recorded."
                ),
                'pressure_msl[hPa]': (
                    "Average mean sea level air pressure recorded during the "
                    "the month in hectopascals."
                )
            }
            grp._v_attrs['aemet_variables_metadata'] = meta

store.close()