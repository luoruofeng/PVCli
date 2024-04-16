import sys
import threading
from pvcli.config import Config
from pvcli.srv import pv_manage
import os
from argparse import ArgumentParser
import signal

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
    parser.add_argument( "--latitude", type=float, default=None,
                        help="Latitude,such as 32.2")
    parser.add_argument( "--longitude", type=float, default=None,
                        help="longitude,such as -111.0")
    parser.add_argument( "--place", type=str, default="",
                        help="place name,such as Tucson")
    parser.add_argument( "--altitude", type=int, default=0,
                        help="altitude,such as 700")
    parser.add_argument( "--time-zone", type=str, default="Etc/GMT+8",
                        help="time zone,such as Etc/GMT+8")
    parser.add_argument( "--surface-azimuth", type=int, default=180,
                        help="Azimuth angle of the module surface. North=0, East=90, South=180,West=270")
    parser.add_argument( "--surface-tilt", type=float, default=0,
                        help="Surface tilt angle. The tilt angle is defined as angle from horizontal")
    args = parser.parse_args()
    return args


SHUT_DOWN_EVENT = threading.Event()
SHUTDOWN_SIGNAL_RECEIVED = False # 设置一个标志，初始时为 False

def signal_handler(sig, frame):
    global SHUTDOWN_SIGNAL_RECEIVED
    # 检查标志是否已经被设置
    if SHUTDOWN_SIGNAL_RECEIVED:
        # 如果已经接收到信号，直接返回
        return
    # 设置标志，表示信号已经接收
    SHUTDOWN_SIGNAL_RECEIVED = True
    print("good bye!")
    sys.exit(0)

def main():
    args = _get_args() # set launch arguments
    Config(DEFAULT_CONFIG_PATH) # load config yaml
    signal.signal(signal.SIGINT, signal_handler)  # 注册Ctrl+C信号处理程序

    # 初始化 pv_manage 对象
    manager = pv_manage(mod_db_name=Config().cli["mod_db_name"],
                mod_name=Config().cli["mod_name"],
                inverter_db_name=Config().cli["inverter_db_name"],
                inverter_name=Config().cli["inverter_name"],
                temp_mod_param=Config().cli["temp_mod_param"], 
                temp_mod_param_second=Config().cli['temp_mod_param_second']
                )

    # 计算发电量
    yearly_energy, daily_energy, hourly_energy = manager.calculate(latitude=args.latitude,
                                                 longitude=args.longitude,
                                                 city=args.place,
                                                 altitude=args.altitude, 
                                                 array_count=args.arrays, 
                                                 surface_tilt=args.surface_tilt,
                                                 surface_azimuth=args.surface_azimuth,
                                                 strings = args.strings ,
                                                 modules_per_string = args.modules_per_string,
                                                 csv_file_path=args.weather_csv_file,
                                                 timezone=args.time_zone)

    print(yearly_energy, daily_energy, hourly_energy)


if __name__ == "__main__":
    main()