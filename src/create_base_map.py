#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from functools import reduce

import folium
import pandas as pd
import branca

tpl = open("template.html", 'r').read()

# create README.html page
html = """
        <div id="readme" class="center-block">
          <h1>Readme</h1>
          <p>
            Please, go  <a href="https://github.com/kikocorreoso/datos_aemet">here</a>
            to learn more about the data.
          </p>
          <p>
            All the original data has been provided by 
            <a href="http://www.aemet.es/es/portada">Aemet</a>, 
            the Spanish meteorological agency.
          </p>
          <h2>How to use this site</h2>
          <p>
            In the <a href="./index.html">front page</a> you have a map 
            with markers. Each markers represents the location of a met mast.
            When you click on a marker a popup window will appear with information
            about the met mast and with links to access the available data in 
            several formats.
          </p>
          <p>
            If you use the data in some way, please, read the 
            <a href="https://github.com/kikocorreoso/datos_aemet#license-for-the-data-original-data">license</a>
            and, if you want, tell us how you are using the data (
            <a href="https://twitter.com/Pybonacci">twitter</a>, 
            <a href="https://github.com/kikocorreoso/datos_aemet/issues">filling an issue on github</a>,..).
          </p>
          <p>
            If you find an error in the data, please, open an 
            <a href="https://github.com/kikocorreoso/datos_aemet/issues">issue</a>
            and tell us all the details. If it was our fault sorry about it.
          <p>
          <p>
            Enjoy data.
          </p>
        </div>
"""
readme = tpl.replace('##replace##', html)
with open(os.path.join(os.path.pardir, "readme.html"), 'w') as f:
    f.write(readme)

# Create front page (INDEX.html)
store = pd.HDFStore('aemet.h5', 'r')
keys = store.keys()

map_osm = folium.Map(location=[36.2, -6], zoom_start=5)
feat_lt5 = folium.FeatureGroup(name='less than 5 years of data')
feat_5_to_10 = folium.FeatureGroup(name='between 5 and 10 years of data.')
feat_10_to_20 = folium.FeatureGroup(name='between 10 and 20 years of data.')
feat_20_to_30 = folium.FeatureGroup(name='between 20 and 30 years of data.')
feat_30_to_50 = folium.FeatureGroup(name='between 30 and 50 years of data.')
feat_gt50 = folium.FeatureGroup(name='more than 50 years of data.')

for key in keys:
    if 'daily' in key:
        obj = reduce(getattr, ['root'] + key.split('/')[1:], store)
        metadata = obj._v_attrs['aemet_station_metadata']
        df = store[key]
        start = df['date'].min()
        end = df['date'].max()
        if end.month > start.month:
            period = end.year - start.year
        else:
            period = end.year - start.year - 1
        if period < 5: 
            feat = feat_lt5
            color = "blue"
        if 5 < period < 10: 
            feat = feat_5_to_10
            color = "yellow"
        if 10 < period < 20: 
            feat = feat_10_to_20
            color = "green"
        if 20 < period < 30: 
            feat = feat_20_to_30
            color = "red"
        if 30 < period < 50: 
            feat = feat_30_to_50
            color = "black"
        if period > 50: 
            feat = feat_gt50
            color = "gray"
        html = f"""
        <h1> Station metadata:</h1>
        <p><b>Aemet station code:</b>{metadata['code']}</p>
        <p><b>SYNOP station code:</b>{metadata['synop_code']}</p>
        <p><b>Aemet station name:</b>{metadata['name']}</p>
        <p><b>Province:</b>{metadata['province']}</p>
        <p><b>Altitude (amsl):</b>{metadata['altitude']} m</p>
        <p><b>Longitude:</b>{metadata['longitude']:7.4f}</p>
        <p><b>Latitude:</b>{metadata['latitude']: 7.4f}</p>
        <p><b>Measurements start:</b>{start.strftime('%Y/%m/%d')}</p>
        <p><b>Measurements end:</b>{end.strftime('%Y/%m/%d')}</p>
        <br>
        <h1>Download links:</h1>
        <h2>Daily</h2>
        <p>Modified file (csv): <a href="https://github.com/kikocorreoso/datos_aemet/raw/master/csv/daily/by_station/{metadata['code']}.CSV.gz">link</a><p>
        <p>Modified file (parquet): <a href="https://github.com/kikocorreoso/datos_aemet/raw/master/parquet/daily/by_station/{metadata['code']}.parquet">link</a><p>
        <p>Original file (csv): <a href="https://github.com/kikocorreoso/datos_aemet/raw/master/aemet_original_data/daily/by_station/{metadata['code']}.CSV.gz">link</a><p>
        <h2>Monthly</h2>
        <p>Modified file (csv): <a href="https://github.com/kikocorreoso/datos_aemet/raw/master/csv/monthly/by_station/{metadata['code']}.CSV.gz">link</a><p>
        <p>Modified file (parquet): <a href="https://github.com/kikocorreoso/datos_aemet/raw/master/parquet/monthly/by_station/{metadata['code']}.parquet">link</a><p>
        <p>Original file (csv): <a href="https://github.com/kikocorreoso/datos_aemet/raw/master/aemet_original_data/monthly/by_station/{metadata['code']}.CSV.gz">link</a><p>
        <h2>Complete stations dataset in HDF5</h2>
        <p>HDF5: <a href="https://github.com/kikocorreoso/datos_aemet/raw/master/hdf5/aemet.h5.gz">link</a><p>
        <h2>Read about the datasets</h2>
        <p><a href="https://github.com/kikocorreoso/datos_aemet/blob/master/README.md">link</a><p>
        """
        iframe = branca.element.IFrame(html=html, width=500, height=300)
        popup = folium.Popup(iframe, max_width=500)
        folium.Marker(
            location=[metadata['latitude'], metadata['longitude']],
            popup=popup,
            icon=folium.Icon(color=color)
        ).add_to(feat)

feat_lt5.add_to(map_osm)
feat_5_to_10.add_to(map_osm)
feat_10_to_20.add_to(map_osm)
feat_20_to_30.add_to(map_osm)
feat_30_to_50.add_to(map_osm)
feat_gt50.add_to(map_osm)
folium.LayerControl().add_to(map_osm)

map_osm.save(os.path.join(os.path.pardir, 'map.html'))

index = tpl.replace(
    "##replace##", 
    """
        <iframe src="./map.html" id="myiframe" scrolling="no" frameborder="0" >
        </iframe>
    """
)

with open(os.path.join(os.path.pardir, "index.html"), 'w') as f:
    f.write(index)