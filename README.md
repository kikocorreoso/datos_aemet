Datos aemet
===========

Data from Aemet (the Spanish meteorological agency) meteorological masts.

There are daily summaries and monthly summaries since the installation 
of the masts until 2012, when AEMET decided to close the access to the data.

# Content

There are several folders in the present repo:

	.
	├── aemet_original_data
	│   ├── daily
	│   │   ├── by_station
	│   │   └── by_year
	│   └── monthly
	│       ├── by_station
	│       └── by_year
	├── csv
	│   ├── daily
	│   │   ├── by_station
	│   │   └── by_year
	│   └── monthly
	│       ├── by_station
	│       └── by_year
	├── hdf5
	├── parquet
	│   ├── daily
	│   │   ├── by_station
	│   │   └── by_year
	│   └── monthly
	│       ├── by_station
	│       └── by_year
	└── src

## *aemet_original_data* folder

It is a collection of the data made by the community. It is downloaded 
from [the forums on tiempo.com](https://foro.tiempo.com/las-series-climatologicas-de-aemet-en-un-click-hasta-septiembre-de-2012-t139231.0.html).

The data in the present repo is the same data that could be obtained from the link above 
but changing the folder names and including some more information in a 
[README.md file](https://github.com/kikocorreoso/datos_aemet/blob/master/aemet_original_data/README.md). 
Please, read that README file to know more about 
[the original data](https://github.com/kikocorreoso/datos_aemet/blob/master/aemet_original_data/README.md#resumen-diario-y-mensual-de-datos) 
(in spanish), the license,...

## *csv* folder

It is a derived dataset with some modifications:

* Column names have changed to a more detailed description including units:

Daily files:

| Original column name       | New column name in derived datasets  | Description |
|:--------------------------:|:------------------------------------:|:-----------:|
| 'Año' + 'Mes' + 'Dia' (\*) | 'date'                               | Day when the records were measured |
| 'Indicativo'               | 'station_code'                       | Aemet station code |
| (**)                       | 'synop_code'                         | International synop code |
| 'Nombre'                   | 'station_name'                       | Aemet station name |
| 'Provincia'                | 'province'                           | Spanish province where the station is located |
| 'Altitud'                  | 'altitude'                           | Altitude above mean sea level |
| (**)                       | 'latitude'                           | Latitude of the station (positive values are North and negative values are South) |
| (**)                       | 'longitude'                          | Longitude of the station (positive values are East and negative values are West) |
| 'T.Max'                    | 'temperature_max[C]'                 | Maximum temperature recorded during the day in Celsius degrees |
| 'Hora'                     | 'temperature_max_timestamp'          | Timestamp (UTC) when the maximum temperature was recorded (time resolution: minutes) |
| 'T.Min'                    | 'temperature_min[C]'                 | Minimum temperature recorded during the day in Celsius degrees |
| 'Hora'                     | 'temperature_min_timestamp'          | Timestamp (UTC) when the minimum temperature was recorded (time resolution: minutes) |
| 'T.Med'                    | 'temperature_avg[C]'                 | Average temperature recorded during the day in Celsius degrees |
| 'Racha'                    | 'windspeed_gust[m/s]'                | Wind speed gust recorded during the day in meters per second |
| 'Dir'                      | 'winddirection_gust[degrees]'        | Direction of the wind gust recorded during the day in degrees clockwise from the North |
| 'Hora'                     | 'wind_gust_timestamp'                | Timestamp (UTC) when the wind gust was recorded (time resolution: minutes) |
| 'Vel.media'                | 'windspeed_avg[m/s]'                 | Average wind speed recorded during the day in meters per second |
| 'Prec.'                    | 'rainfall[mm]'                       | Accumulated rainfall during the day in mm |
| 'Sol'                      | 'sun[h]                              | Accumulated hours of sun during the day |
| 'Pres.máx'                 | 'pressure_max[hPa]'                  | Maximum air pressure recorded during the day in hectopascals |
| 'Hora'                     | 'pressure_max_timestamp'             | Timestamp (UTC) when the maximum air pressure was recorded (time resolution: hours) |
| 'Pres.min'                 | 'pressure_min[hPa]'                  | Minimum air pressure recorded during the day in hectopascals |
| 'Hora'                     | 'pressure_min_timestamp'             | Timestamp (UTC) when the maximum air pressure was recorded (time resolution: hours) |

(*) Columns 'Año', 'Mes' and 'Día' indicating the day of the row records 
have been merged in column 'date'.

(**) These columns don't exist in the original files but in the 
postprocessed files have been included for convenience. It is more space 
but you don't have to open the *maestro.csv* file with the metadata of 
the stations.

Monthly files

| Original column name    | New column name in derived datasets  | Description |
|:-----------------------:|:------------------------------------:|:-----------:|
| 'Año' + 'Mes' (\*)      | 'date'                               | Day when the records were measured |
| 'Indicativo'            | 'station_code'                       | Aemet station code |
| (**)                    | 'synop_code'                         | International synop code |
| 'Nombre'                | 'station_name'                       | Aemet station name |
| 'Provincia'             | 'province'                           | Spanish province where the station is located |
| 'Altitud'               | 'altitude'                           | Altitude above mean sea level |
| (\*\*)                  | 'latitude'                           | Latitude of the station (positive values are North and negative values are South) |
| (\*º*)                  | 'longitude'                          | Longitude of the station (positive values are East and negative values are West) |
| 'T.Med'                 | 'temperature_avg[C]'                 | Average temperature recorded during the month in Celsius degrees |
| 'T.Max.Med              | 'temperature_max_avg[C]'             | Average of the maximum daily temperatures recorded during the month in Celsius degrees |
| 'T.Min.Med              | 'temperature_min_avg[C]'             | Average of the minimum daily temperatures recorded during the month in Celsius degrees |
| 'T.Max.Abs              | 'temperature_max[C]'                 | Maximum temperature recorded during the month in Celsius degrees |
| 'Día'                   | 'temperature_max_timestamp'          | Timestamp (UTC) when the maximum temperature was recorded (time resolution: days) |
| 'T.Min.Abs'             | 'temperature_min[C]'                 | Minimum temperature recorded during the month in Celsius degrees |
| 'Día'                   | 'temperature_min_timestamp'          | Timestamp (UTC) when the minimum temperature was recorded (time resolution: days) |
| 'Min.Sup'               | 'temperature_min_max[C]'             | Maximum of the minimum daily temperatures recorded during the month in Celsius degrees |
| 'Max.Inf'               | 'temperature_max_min[C]'             | Minimum of the maximum daily temperatures recorded during the month in Celsius degrees |
| 'DíasHelada'            | 'frost_days_count'                   | Number of days with temperature below or equal to 0 Celsius degrees recorded during the month |
| 'Prec.total'            | 'rainfall[mm]'                       | Accumulated rainfall during the month in mm |
| 'Prec.max'              | 'rainfall_max[mm]'                   | Maximum daily accumulated rainfall recorded during the month in mm |
| 'Día'                   | 'rainfall_max_timestamp'             | Timestamp (UTC) when the maximum daily accumulated rainfall was recorded (time resolution: days) |
| 'DiasPrec.Apre'         | 'rainfall_days_001_count'            | Number of days with accumulated rainfall above 0.1 mm |
| 'DiasPrecSup10'         | 'rainfall_days_100_count'            | Number of days with accumulated rainfall above 10.0 mm |
| 'DíasLluvia'            | 'rainfall_days_000_count'            | Number of rainfall days recorded during the month |
| 'DíasNieve'             | 'snow_days_count'                    | Number of snow days recorded during the month |
| 'DíasGranizo'           | 'hail_days_count'                    | Number of hail days recorded during the month |
| 'VelRacha'              | 'windspeed_gust[m/s]'                | Wind speed gust recorded during the month in meters per second |
| 'DirRacha'              | 'windirection gust[degrees]'         | Direction of the wind gust recorded during the month in degrees clockwise from the North |
| 'Dia' + 'Hora' (\*\*\*) | 'wind_gust_timestamp'                | Timestamp (UTC) when the wind gust was recorded  (time resolution: minutes)|
| 'DíasRachaSup55'        | 'windgust_days_55km/h_count'         | Number of days with wind gust above 55 km/h |
| 'DíasRachaSup91'        | 'windgust_days_91km/h_count'         | Number of days with wind gust above 91 km/h |
| 'Vel.media'             | 'windspeed_avg[m/s]'                 | Average wind speed recorded during the month in meters second |
| 'Insol.media'           | 'sun_avg[h]'                         | Average daily sun isolation recorded during the month in hours |
| '%Insol'                | 'sun_avg[%]'                         | Average daily sun isolation recorded during the month in percentage |
| 'Pres.media'            | 'pressure_avg[hPa]'                  | Average air pressure recorded during the month in hectopascals |
| 'Pres.Max.Abs'          | 'pressure_max[hPa]'                  | Maximum air pressure recorded during the month in hectopascals |
| 'Día'                   | 'pressure_max_timestamp'             | Timestamp (UTC) when the maximum air pressure was recorded (time resolution: days) |
| 'Pres.Min.Abs'          | 'pressure_min[hPa]'                  | Minimum air pressure recorded during the month in hectopascals |
| 'Día'                   | 'pressure_min_timestamp'             | Timestamp (UTC) when the maximum air pressure was recorded (time resolution: days) |
| 'Pres.MediaNivelMar     | 'pressure_msl[hPa]'                  | Average mean sea level air pressure recorded during the the month in hectopascals |

(\*) Columns 'Año' and 'Mes' indicating the month of the row records 
have been merged in column 'date'.

(\*\*) These columns don't exist in the original files but in the 
postprocessed files have been included for convenience. It is more space 
but you don't have to open the *maestro.csv* file with the metadata of 
the stations.

(\*\*\*) Columns 'Día' and 'Hora' indicating the day and hour of the maximum
monthly wind gust have been merged in the column 'wind_gust_timestamp'.

* Rainfall values modifications
  * In the original files the values of the rainfall colums are numeric, 'Ip' or 'Acum'. Numeric values have been maintained. 'Ip' means that there was rain but it was lower than 0.1 mm. 'Ip' values have been changed to `0.05` in order to have numeric columns and do not mix types on the same colum but take into account that this value is invented and should be used only to filter the 'Ip' records. I Don't know what 'Acum' values are so these values are `nan`s in the derived datasets.

## *parquet* folder

All the files are similar to that on the *csv* folder but in *parquet* format (same column names, same issues with rainfall values,...). Read more about Apache Arrow [here](https://github.com/apache/arrow).

The only difference is that apache files maintain the index column. I didn't know how to remove it during the conversion :-( The parquet/arrow format is evolving.

Files are compressed using `gzip`.

To open the files in python read [here](https://arrow.apache.org/docs/python/parquet.html).

## *hdf5* folder

There is a file called *aemet.h5*. It is included the daily and monthly files only *by_station*. Store also the *by_year* files is redundant. 
If you need the files *by_year* just file an issue explaining your motivation.

In this case, the columns with repeated values ('date', 'station_code', 
'synop_code', 'station_name' , 'province', 'altitude', 'latitude', 
'longitude') are not included in the file and this data is included as
metadata. Also, the description of the columns is available as metadata.

To access the information with Python you can use Pandas (you will need 
also PyTables installed to work with HDF5):

```python
import pandas as pd

store = pd.HDFStore('path/to/aemet.h5', mode='r')

# this will show all the dataframes included in the file
print(store)
```

The output from the previous code should be something like:

```
<class 'pandas.io.pytables.HDFStore'>
File path: ../hdf5/aemet.h5
/daily/by_station/station0016A              frame        (shape->[24017,16])
/daily/by_station/station0076               frame        (shape->[30378,16])
/daily/by_station/station0200E              frame        (shape->[33847,16])
/daily/by_station/station0367               frame        (shape->[14374,16])
/daily/by_station/station0370B              frame        (shape->[18274,16])
/daily/by_station/station1014               frame        (shape->[20864,16])
/daily/by_station/station1024E              frame        (shape->[30925,16])
/daily/by_station/station1082               frame        (shape->[23884,16])
/daily/by_station/station1109               frame        (shape->[20748,16])
/daily/by_station/station1110               frame        (shape->[26761,16])
/daily/by_station/station1111               frame        (shape->[11608,16])
/daily/by_station/station1208               frame        (shape->[9044,16]) 
/daily/by_station/station1208A              frame        (shape->[13758,16])
/daily/by_station/station1208H              frame        (shape->[4227,16]) 
/daily/by_station/station1212E              frame        (shape->[16015,16])
/daily/by_station/station1249I              frame        (shape->[14549,16])
/daily/by_station/station1387               frame        (shape->[29951,16])
/daily/by_station/station1387E              frame        (shape->[14915,16])
/daily/by_station/station1428               frame        (shape->[25110,16])
/daily/by_station/station1484               frame        (shape->[8036,16]) 
/daily/by_station/station1484C              frame        (shape->[9862,16]) 
/daily/by_station/station1495               frame        (shape->[20607,16])
/daily/by_station/station1505               frame        (shape->[12315,16])
/daily/by_station/station1549               frame        (shape->[22554,16])
/daily/by_station/station1690A              frame        (shape->[16234,16])
/daily/by_station/station1690B              frame        (shape->[6360,16]) 
/daily/by_station/station2030               frame        (shape->[25121,16])
/daily/by_station/station2331               frame        (shape->[25264,16])
/daily/by_station/station2401               frame        (shape->[12998,16])
/daily/by_station/station2422               frame        (shape->[14245,16])
/daily/by_station/station2444               frame        (shape->[10865,16])
/daily/by_station/station2444C              frame        (shape->[10665,16])
/daily/by_station/station2462               frame        (shape->[24380,16])
/daily/by_station/station2465               frame        (shape->[8766,16]) 
/daily/by_station/station2465A              frame        (shape->[17999,16])
/daily/by_station/station2539               frame        (shape->[27666,16])
/daily/by_station/station2614               frame        (shape->[33049,16])
/daily/by_station/station2661               frame        (shape->[27302,16])
/daily/by_station/station2867               frame        (shape->[24745,16])
/daily/by_station/station2870               frame        (shape->[13504,16])
/daily/by_station/station3013               frame        (shape->[22642,16])
/daily/by_station/station3129               frame        (shape->[22554,16])
/daily/by_station/station3168A              frame        (shape->[12592,16])
/daily/by_station/station3168C              frame        (shape->[8556,16]) 
/daily/by_station/station3175               frame        (shape->[18871,16])
/daily/by_station/station3191E              frame        (shape->[12025,16])
/daily/by_station/station3195               frame        (shape->[33844,16])
/daily/by_station/station3196               frame        (shape->[24625,16])
/daily/by_station/station3200               frame        (shape->[22554,16])
/daily/by_station/station3259               frame        (shape->[22186,16])
/daily/by_station/station3260B              frame        (shape->[11200,16])
/daily/by_station/station3469               frame        (shape->[24472,16])
/daily/by_station/station3469A              frame        (shape->[10897,16])
/daily/by_station/station4121               frame        (shape->[15310,16])
/daily/by_station/station4121C              frame        (shape->[17775,16])
/daily/by_station/station4452               frame        (shape->[21093,16])
/daily/by_station/station4605               frame        (shape->[23498,16])
/daily/by_station/station4642E              frame        (shape->[10349,16])
/daily/by_station/station5000A              frame        (shape->[17690,16])
/daily/by_station/station5000C              frame        (shape->[3349,16]) 
/daily/by_station/station5270               frame        (shape->[21125,16])
/daily/by_station/station5270B              frame        (shape->[9930,16]) 
/daily/by_station/station5402               frame        (shape->[18031,16])
/daily/by_station/station5514               frame        (shape->[27238,16])
/daily/by_station/station5530E              frame        (shape->[14702,16])
/daily/by_station/station5783               frame        (shape->[22554,16])
/daily/by_station/station5796               frame        (shape->[22434,16])
/daily/by_station/station5910               frame        (shape->[8796,16]) 
/daily/by_station/station5960               frame        (shape->[23146,16])
/daily/by_station/station5973               frame        (shape->[20010,16])
/daily/by_station/station6000A              frame        (shape->[17289,16])
/daily/by_station/station6001               frame        (shape->[24077,16])
/daily/by_station/station6155A              frame        (shape->[25721,16])
/daily/by_station/station6297               frame        (shape->[16505,16])
/daily/by_station/station6325O              frame        (shape->[16345,16])
/daily/by_station/station7031               frame        (shape->[24898,16])
/daily/by_station/station7178I              frame        (shape->[10410,16])
/daily/by_station/station7228               frame        (shape->[26329,16])
/daily/by_station/station8019               frame        (shape->[16700,16])
/daily/by_station/station8025               frame        (shape->[27047,16])
/daily/by_station/station8096               frame        (shape->[22522,16])
/daily/by_station/station8175               frame        (shape->[26603,16])
/daily/by_station/station8178D              frame        (shape->[10862,16])
/daily/by_station/station8368U              frame        (shape->[9680,16]) 
/daily/by_station/station8414A              frame        (shape->[17437,16])
/daily/by_station/station8416               frame        (shape->[27363,16])
/daily/by_station/station8500A              frame        (shape->[13423,16])
/daily/by_station/station8501               frame        (shape->[13115,16])
/daily/by_station/station9087               frame        (shape->[14211,16])
/daily/by_station/station9091O              frame        (shape->[13135,16])
/daily/by_station/station9170               frame        (shape->[23345,16])
/daily/by_station/station9262               frame        (shape->[21427,16])
/daily/by_station/station9263D              frame        (shape->[13788,16])
/daily/by_station/station9381               frame        (shape->[15796,16])
/daily/by_station/station9381I              frame        (shape->[6538,16]) 
/daily/by_station/station9390               frame        (shape->[33754,16])
/daily/by_station/station9434               frame        (shape->[26206,16])
/daily/by_station/station9771               frame        (shape->[8646,16]) 
/daily/by_station/station9771C              frame        (shape->[10835,16])
/daily/by_station/station9898               frame        (shape->[24899,16])
/daily/by_station/station9981A              frame        (shape->[33482,16])
/daily/by_station/stationB228               frame        (shape->[12692,16])
/daily/by_station/stationB278               frame        (shape->[14671,16])
/daily/by_station/stationB893               frame        (shape->[16619,16])
/daily/by_station/stationB954               frame        (shape->[22484,16])
/daily/by_station/stationC029O              frame        (shape->[14579,16])
/daily/by_station/stationC139E              frame        (shape->[15509,16])
/daily/by_station/stationC249I              frame        (shape->[15826,16])
/daily/by_station/stationC429I              frame        (shape->[11780,16])
/daily/by_station/stationC430E              frame        (shape->[32881,16])
/daily/by_station/stationC447A              frame        (shape->[22920,16])
/daily/by_station/stationC449C              frame        (shape->[29839,16])
/daily/by_station/stationC649I              frame        (shape->[22554,16])
/daily/by_station/stationC929I              frame        (shape->[14184,16])
/monthly/by_station/station0016A            frame        (shape->[789,33])  
/monthly/by_station/station0076             frame        (shape->[998,33])  
/monthly/by_station/station0200E            frame        (shape->[1112,33]) 
/monthly/by_station/station0367             frame        (shape->[472,33])  
/monthly/by_station/station0370B            frame        (shape->[601,33])  
/monthly/by_station/station1014             frame        (shape->[685,33])  
/monthly/by_station/station1024E            frame        (shape->[1017,33]) 
/monthly/by_station/station1082             frame        (shape->[785,33])  
/monthly/by_station/station1109             frame        (shape->[681,33])  
/monthly/by_station/station1110             frame        (shape->[887,33])  
/monthly/by_station/station1111             frame        (shape->[383,33])  
/monthly/by_station/station1208             frame        (shape->[297,33])  
/monthly/by_station/station1208A            frame        (shape->[452,33])  
/monthly/by_station/station1208H            frame        (shape->[139,33])  
/monthly/by_station/station1212E            frame        (shape->[526,33])  
/monthly/by_station/station1249I            frame        (shape->[489,33])  
/monthly/by_station/station1387             frame        (shape->[984,33])  
/monthly/by_station/station1387E            frame        (shape->[490,33])  
/monthly/by_station/station1428             frame        (shape->[825,33])  
/monthly/by_station/station1484             frame        (shape->[618,33])  
/monthly/by_station/station1484C            frame        (shape->[324,33])  
/monthly/by_station/station1495             frame        (shape->[741,33])  
/monthly/by_station/station1505             frame        (shape->[404,33])  
/monthly/by_station/station1549             frame        (shape->[741,33])  
/monthly/by_station/station1690A            frame        (shape->[601,33])  
/monthly/by_station/station1690B            frame        (shape->[381,33])  
/monthly/by_station/station2030             frame        (shape->[826,33])  
/monthly/by_station/station2331             frame        (shape->[830,33])  
/monthly/by_station/station2401             frame        (shape->[801,33])  
/monthly/by_station/station2422             frame        (shape->[468,33])  
/monthly/by_station/station2444             frame        (shape->[357,33])  
/monthly/by_station/station2444C            frame        (shape->[350,33])  
/monthly/by_station/station2462             frame        (shape->[801,33])  
/monthly/by_station/station2465             frame        (shape->[288,33])  
/monthly/by_station/station2465A            frame        (shape->[772,33])  
/monthly/by_station/station2539             frame        (shape->[909,33])  
/monthly/by_station/station2614             frame        (shape->[1112,33]) 
/monthly/by_station/station2661             frame        (shape->[897,33])  
/monthly/by_station/station2867             frame        (shape->[813,33])  
/monthly/by_station/station2870             frame        (shape->[444,33])  
/monthly/by_station/station3013             frame        (shape->[745,33])  
/monthly/by_station/station3129             frame        (shape->[741,33])  
/monthly/by_station/station3168A            frame        (shape->[652,33])  
/monthly/by_station/station3168C            frame        (shape->[279,33])  
/monthly/by_station/station3175             frame        (shape->[736,33])  
/monthly/by_station/station3191E            frame        (shape->[396,33])  
/monthly/by_station/station3195             frame        (shape->[1112,33]) 
/monthly/by_station/station3196             frame        (shape->[809,33])  
/monthly/by_station/station3200             frame        (shape->[741,33])  
/monthly/by_station/station3259             frame        (shape->[743,33])  
/monthly/by_station/station3260B            frame        (shape->[368,33])  
/monthly/by_station/station3469             frame        (shape->[804,33])  
/monthly/by_station/station3469A            frame        (shape->[358,33])  
/monthly/by_station/station4121             frame        (shape->[503,33])  
/monthly/by_station/station4121C            frame        (shape->[597,33])  
/monthly/by_station/station4452             frame        (shape->[694,33])  
/monthly/by_station/station4605             frame        (shape->[772,33])  
/monthly/by_station/station4642E            frame        (shape->[340,33])  
/monthly/by_station/station5000A            frame        (shape->[625,33])  
/monthly/by_station/station5000C            frame        (shape->[112,33])  
/monthly/by_station/station5270             frame        (shape->[767,33])  
/monthly/by_station/station5270B            frame        (shape->[325,33])  
/monthly/by_station/station5402             frame        (shape->[594,33])  
/monthly/by_station/station5514             frame        (shape->[917,33])  
/monthly/by_station/station5530E            frame        (shape->[483,33])  
/monthly/by_station/station5783             frame        (shape->[741,33])  
/monthly/by_station/station5796             frame        (shape->[747,33])  
/monthly/by_station/station5910             frame        (shape->[395,33])  
/monthly/by_station/station5960             frame        (shape->[800,33])  
/monthly/by_station/station5973             frame        (shape->[657,33])  
/monthly/by_station/station6000A            frame        (shape->[723,33])  
/monthly/by_station/station6001             frame        (shape->[1104,33]) 
/monthly/by_station/station6155A            frame        (shape->[845,33])  
/monthly/by_station/station6297             frame        (shape->[579,33])  
/monthly/by_station/station6325O            frame        (shape->[537,33])  
/monthly/by_station/station7031             frame        (shape->[818,33])  
/monthly/by_station/station7178I            frame        (shape->[342,33])  
/monthly/by_station/station7228             frame        (shape->[865,33])  
/monthly/by_station/station8019             frame        (shape->[549,33])  
/monthly/by_station/station8025             frame        (shape->[888,33])  
/monthly/by_station/station8096             frame        (shape->[740,33])  
/monthly/by_station/station8175             frame        (shape->[874,33])  
/monthly/by_station/station8178D            frame        (shape->[357,33])  
/monthly/by_station/station8368U            frame        (shape->[318,33])  
/monthly/by_station/station8414A            frame        (shape->[573,33])  
/monthly/by_station/station8416             frame        (shape->[899,33])  
/monthly/by_station/station8500A            frame        (shape->[441,33])  
/monthly/by_station/station8501             frame        (shape->[655,33])  
/monthly/by_station/station9087             frame        (shape->[466,33])  
/monthly/by_station/station9091O            frame        (shape->[471,33])  
/monthly/by_station/station9170             frame        (shape->[777,33])  
/monthly/by_station/station9262             frame        (shape->[704,33])  
/monthly/by_station/station9263D            frame        (shape->[453,33])  
/monthly/by_station/station9381             frame        (shape->[519,33])  
/monthly/by_station/station9381I            frame        (shape->[215,33])  
/monthly/by_station/station9390             frame        (shape->[1109,33]) 
/monthly/by_station/station9434             frame        (shape->[861,33])  
/monthly/by_station/station9771             frame        (shape->[284,33])  
/monthly/by_station/station9771C            frame        (shape->[356,33])  
/monthly/by_station/station9898             frame        (shape->[821,33])  
/monthly/by_station/station9981A            frame        (shape->[1113,33]) 
/monthly/by_station/stationB228             frame        (shape->[417,33])  
/monthly/by_station/stationB278             frame        (shape->[649,33])  
/monthly/by_station/stationB893             frame        (shape->[546,33])  
/monthly/by_station/stationB954             frame        (shape->[741,33])  
/monthly/by_station/stationC029O            frame        (shape->[479,33])  
/monthly/by_station/stationC139E            frame        (shape->[510,33])  
/monthly/by_station/stationC249I            frame        (shape->[520,33])  
/monthly/by_station/stationC429I            frame        (shape->[387,33])  
/monthly/by_station/stationC430E            frame        (shape->[1105,33]) 
/monthly/by_station/stationC447A            frame        (shape->[824,33])  
/monthly/by_station/stationC449C            frame        (shape->[1089,33]) 
/monthly/by_station/stationC649I            frame        (shape->[741,33])  
/monthly/by_station/stationC929I            frame        (shape->[466,33]) 
```

To access the values of the daily data of a station:

```python
from pprint import pprint

import pandas as pd

store = pd.HDFStore('path/to/aemet.h5', mode='r')

# To access, e.g., the daily values of station 0076:
df = store['/daily/by_station/station0076']

The metadata for that dataset could be accessed using:
key = 'aemet_station_metadata'
st_meta = store.root.daily.by_station.station0076._v_attrs[key]
key = 'aemet_variables_metadata'
cols_desc = store.root.daily.by_station.station0076._v_attrs[key]
pprint(st_meta) # station metadata
pprint(cols_desc) # Long description of columns
```

The result of the previous code will print:

```
{'altitude': 4,
 'code': '0076',
 'latitude': 41.292777777777779,
 'longitude': 2.0700000000000003,
 'name': 'BARCELONA AEROPUERTO',
 'province': 'BARCELONA',
 'synop_code': '08181'}
{'date': 'Day when the records were measured',
 'pressure_max[hPa]': 'Maximum air pressure recorded during the day in '
                      'hectopascals.',
 'pressure_max_timestamp': 'Timestamp (UTC) when the maximum air pressure was '
                           'recorded.',
 'pressure_min[hPa]': 'Minimum air pressure recorded during the day in '
                      'hectopascals.',
 'pressure_min_timestamp': 'Timestamp (UTC) when the maximum air pressure was '
                           'recorded.',
 'rainfall[mm]': 'Accumulated rainfall during the day in mm.',
 'sun[h]': 'Accumulated hours of sun during the day.',
 'temperature_avg[C]': 'Average temperature recorded during the day in Celsius '
                       'degrees.',
 'temperature_max[C]': 'Maximum temperature recorded during the day in Celsius '
                       'degrees.',
 'temperature_max_timestamp': 'Timestamp (UTC) when the maximum temperature '
                              'was recorded.',
 'temperature_min[C]': 'Minimum temperature recorded during the day in Celsius '
                       'degrees.',
 'temperature_min_timestamp': 'Timestamp (UTC) when the minimum temperature '
                              'was recorded.',
 'wind_gust_timestamp': 'Timestamp (UTC) when the wind gust was recorded.',
 'winddirection_gust[degrees]': 'Direction of the wind gust recorded during '
                                'the day in degrees clockwise from the North.',
 'windspeed_avg[m/s]': 'Average wind speed recorded during the day in meters '
                       'per second.',
 'windspeed_gust[m/s]': 'Wind speed gust recorded during the day in meters per '
                        'second.'}
```

This file is not compressed to keep things simple.

## *src* folder

It contains the python script used to create *csv*, *parquet* and *hdf5*
folders from data contained in *aemet_original_data* folder.

# License for the data original data

You can read about it [here](https://github.com/kikocorreoso/datos_aemet/blob/master/aemet_original_data/NOTA_LEGAL.txt) (in spanish).

A summary for the usage of the data could be interpreted as:

> People can use freely this data. You should mention AEMET as the 
> collector of the original data in every situation except if you are 
> using this data privately and individually. AEMET makes no warranty 
> as to the accuracy or completeness of the data. All 
> data are provided on an "as is" basis. AEMET is not 
> responsible for any damage or loss derived from the interpretation or 
> use of this data.

# License

The license for the derived work from the original data is MIT.

# Issues

If you work with the data and 
[find an issue, please, tell me to correct it](https://github.com/kikocorreoso/datos_aemet/issues).

# Enhancements

If you think the data could be improved, please, 
[tell me](https://github.com/kikocorreoso/datos_aemet/issues) with a detailed
explanation to think about it and apply new changes if necessary or, even better,
send a [pull request with your ideas](https://github.com/kikocorreoso/datos_aemet/pulls).

# TO-DO

* A sqlite version but I have to think about the best scheme to keep things simple.
* ~~A front-end showing the location of the stations with links to each file.~~ See https://kikocorreoso.github.io/datos_aemet/

# Tell me about how you use the data

It is very interesting to know what you are doing with the data, how
useful are the provided formats, if you have any need regarding these datasets,...

# Alternatives to these datasets

I have found the excellent work done by [@chucheria](https://github.com/chucheria)
available on on [data.world](https://data.world/chucheria/spain-weather-data-from-1920).
