# Parsing title, alt, typ with indexing

## Parsing 
Parsing is done with PySpark and regex
You can check regexes at this links:\
[Parse type.object.type tripplet]()\
[Parse common.topic.alias tripplet]()\
[Parse type.object.name tripplet]()\

Parsing logic is in file `parse.py`
Dataset for parsing is downloaded from [this page](https://developers.google.com/freebase)\
To extract part of the file use this:
```
gzip -cd freebase_triples.gz | dd ibs=1024 skip=0 count=1000000 > foo.txt
```
This extracts 1GB file with offset of 0.\
### Running parsing script 
**Prerequisities are:**
- PySpark (I have used spark-3.3.1-bin-hadoop2)
- JAVA 8 
- Python3 (I have used Python 3.10.7)
- Correctly setup enviroment variables (`JAVA_HOME`, `HADOOP_HOME`, `SPARK_HOME`, `SPARK_PYTHON`)
- If using windows add `winutils.exe` to `SPARKHJOME/bin`

Add extracted .txt file dataset to folder `./datasets` and change file `conf.py` corresponding to name of the extracted file e

To run parsing script use: 
```
spark-submit parse.py
```
Output of parsing script is saved in parquet files located in predefined output directory.


## Indexing


## Searching

