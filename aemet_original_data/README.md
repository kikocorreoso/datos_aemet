**[Sorry, most of this document is available only in spanish. If you 
want it in other language, please, consider sending a pull request.]**

Data available in the present folder
====================================

All data in the present folder (except this *README.md* file) has been
downloaded from 
[https://foro.tiempo.com/las-series-climatologicas-de-aemet-en-un-click-hasta-septiembre-de-2012-t139231.0.html](https://foro.tiempo.com/las-series-climatologicas-de-aemet-en-un-click-hasta-septiembre-de-2012-t139231.0.html).

The *series.zip* downloadable from the link above contains:

* *daily* folder. It is the same than the *diarios* folder in the *series.zip* file. Inside there are two folders:
  * *by_station* folder. It is the same than *estaciones* folder in the *series.zip* file.
  * *by_year* folder. It is the same than *año* folder in the *series.zip* file.
* *monthly* folder. It is the same than the *mensuales* folder in the *series.zip* file. Inside there are two folders:
  * *by_station* folder. It is the same than *estaciones* folder in the *series.zip* file.
  * *by_year* folder. It is the same than *año* folder in the *series.zip* file.

Inside these folders there are the original *.csv* files available in the *series.zip* file.

* *maestro.csv*. File containing metadata of the stations: name, location, altitude,...

* *LEEME.txt*. Its content is similar to this *README.md* file. General description of the data files. **In spanish**.
* *NOTA_LEGAL.txt*. Information about legal issues regarding the collection and the use of the data. **In spanish**. A more or less summary of the usage can be found below:

> People can use freely this data. You should mention AEMET as the 
> collector of the original data in every situation except if you are
> using this data privately and individually.
> AEMET makes no warranty as to the accuracy or completeness of the Archive 
> Products. All Archive Products are provided on an "as is" basis. 
> AEMET is not responsible for any damage or loss derived from the 
> interpretation or use of this data.


RESUMEN DIARIO Y MENSUAL DE DATOS                     
=================================                      

En este apartado están accesibles los datos diarios y mensuales 
de una amplia selección de estaciones.
 
En algunas estaciones se incluyen datos desde 1920.

Para algunas localidades existe más de una estación, que no se solapan en el tiempo, 
o lo hacen durante un breve período y, normalmente, es debido a cambios de emplazamiento 
del observatorio, por lo que la serie más actual puede considerarse como continuación 
de la más antigua.

La lista de estaciones está en el fichero maestro.csv

ORIGEN DE LOS DATOS
===================

Los datos provienen de la red de estaciones de AEMET.

FORMATO DE LOS FICHEROS:
========================

Todos los ficheros se ofrecen comprimidos. Las indicaciones
que siguen se refieren a los ficheros descomprimidos.

Los ficheros estan en formato *.csv*.

Los ficheros de datos constan de los siguientes campos,
separados por punto y coma:

* Indicativo climatológico de la estación
* Nombre de la estación
* Provincia
* Altitud de la estación en metros
* Campos de fecha
* Variables meteorológicas

(Las variables meteorológicas se describen en los fichero LEEME_DATOS.txt de cada directorio)
(Las horas de las observaciones son UTC)

El fichero maestro, consta de los siguientes campos,
separados por punto y coma:

* Indicativo climatológico de la estación
* Nombre de la estación
* Provincia
* Altitud de la estación en metros
* Latitud en formato ggmmss
* Longitud en formato ggmmss, con indicación de la orientación:
                                E: Este, W: Oeste
* Indicativo sinóptico (si lo hay)                               

Para algunas localidades existe más de una estación, que no se solapan en el tiempo,
o lo hacen durante un breve periodo, y normalmente es debido a cambios de emplazamiento
del observatorio, por lo que la serie más actual puede considerarse como continuación
de la más antigua.
    
TIPOS DE FICHERO:
=================

Hay dos tipos de ficheros de datos:

* Ficheros con datos diarios
* Ficheros con datos mensuales

A su vez, para cada uno de estos tipos, los datos se presentan agrupados
de dos maneras distintas:

* Por estación (todos los datos de una estación)
* Por año (todos los datos de todas las estaciones para un año dado)
     
DIRECTORIOS DE ALMACENAMIENTO:
==============================

Partiendo del directorio raiz hay dos directorios:

* *daily* (para los datos diarios)
* monthly (para los datos mensuales)
     
En cada uno de estos directorios hay otros dos directorios:

* *by_year* (para los datos agrupados por años)
* *by_station* (para los datos agrupados por estaciones)


NOMBRES DE LOS FICHEROS:
========================
     
Para los ficheros con los datos agrupados por estación:

* *CCCCC.csv*, siendo *CCCCC* el indicativo climatológico de la estación.

Para los ficheros con los datos agrupados por año:
    
* *AAAA.csv*, siendo *AAAA* el año al que corresponden los datos.
