# PVCli
PV system terminal tool.Base on python 3.12 version.


## create virtual python env
```
conda create -n pvcli python=3.12
conda activate pvcli
pip install -r requirements.txt
```

## install client
```
pip install .
```

## uninstall client
```
pip uninstall pvcli
```



## 举例说明
1. config配置文件中mod_db_name和mod_db_path选项不能同时出现。
2. mod_db_name代表从数据库查询光伏板信息
3. mod_db_path代表从本地csv文件查询光伏板信息
```
 pvcli --arrays 1  --modules-per-string 1  --strings 2 -w ~/miniconda3/lib/python3.11/site-packages/pvcli/source/weather_demo.csv --latitude 26.683213 --longitude 101.855071 --place yanbian --altitude 400 --time-zone Etc/GMT+8 --surface-azimuth 180 --surface-tilt 30 -c ~/miniconda3/lib/python3.11/site-packages/pvcli/config/test/config.yaml
 ```