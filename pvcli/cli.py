from pvcli.config import Config
import os
from argparse import ArgumentParser

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
DEFAULT_CONFIG_PATH = os.path.join(CURRENT_DIR,'config/config.yaml')


def _get_args():
    parser = ArgumentParser()
    #配置文件, array数, array中的串行模块数, 并行模块数, 天气csv文件
    parser.add_argument("-c", "--config-path", type=str, default=DEFAULT_CONFIG_PATH,
                        help="config yaml file path, default to %(default)r")
    parser.add_argument( "--arrays", type=int, default=1,
                        help="Number of arrays.")
    parser.add_argument( "--modules-per-string", type=int, default=1,
                        help="Number of modules per string in the array.")
    parser.add_argument( "--strings", type=int, default=1,
                        help="Number of parallel strings in the array.")
    #csv格式 utc_time temp_air  relative_humidity    ghi     dni    dhi   IR(h)  wind_speed  wind_direction  pressure
    parser.add_argument("-w","--weather-csv-file", type=str, default=None,
                        help="The weather csv file path.")
    
    # 纬度、经度、地点名称、海拔高度和时区
    parser.add_argument( "--Latitude", type=float, default=None,
                        help="Latitude,such as 32.2")
    parser.add_argument( "--longitude", type=float, default=None,
                        help="longitude,such as -111.0")
    parser.add_argument( "--place", type=str, default=None,
                        help="place name,such as Tucson")
    parser.add_argument( "--altitude", type=int, default=None,
                        help="altitude,such as 700")
    parser.add_argument( "--time-zone", type=str, default="Etc/GMT+8",
                        help="time zone,such as Etc/GMT+8")

    args = parser.parse_args()
    return args


def main():
    args = _get_args() # set launch arguments
    Config(DEFAULT_CONFIG_PATH) # load config yaml

    print("Hello, this is your command line program!")
    print(Config().cli["cec_mod_db"])
    print(Config().cli["mod_name"])

if __name__ == "__main__":
    main()