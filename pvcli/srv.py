import sys
import pvlib
import pandas as pd

from pvlib.pvsystem import PVSystem, Array, FixedMount

class pv_manage:
    def __init__(self, mod_db_name, mod_name, inverter_db_name, inverter_name, temp_mod_param='sapm', temp_mod_param_second='open_rack_glass_glass'):
        self.mod_db_name = mod_db_name
        self.mod_name = mod_name
        self.inverter_db_name = inverter_db_name
        self.inverter_name = inverter_name
        self.temp_mod_param = temp_mod_param
        self.temp_mod_param_second = temp_mod_param_second
        self.weather = None # 存储典型气象年数据
    
    
    def get_weathers_by_csv(self, csv_file_path, latitude, longitude):            
        # # 获取指定纬度和经度的典型气象年数据
        # weather = pvlib.iotools.get_pvgis_tmy(latitude, longitude)[0]
        # weather.index.name = "utc_time"
        # self.weather = weather
        # print(self.weather)
        self.weather = pd.read_csv(csv_file_path, parse_dates=['time(UTC)'], index_col='time(UTC)')
        self.weather.index.name = "utc_time"
        print("The following is the weather information provided:")
        print(self.weather)

    def calculate(self, latitude, longitude, city, altitude, array_count,surface_tilt, surface_azimuth=180,strings = 1 ,modules_per_string = 1,csv_file_path=None,timezone="Etc/GMT+8"):
        cec_mod_db = pvlib.pvsystem.retrieve_sam(self.mod_db_name)
        inverter_db = pvlib.pvsystem.retrieve_sam(self.inverter_db_name)#检索了 cecinverter 数据库中的逆变器信息
        # 获取模块和逆变器
        module = cec_mod_db[self.mod_name]
        inverter = inverter_db[self.inverter_name]

        temperature_model_parameters = pvlib.temperature.TEMPERATURE_MODEL_PARAMETERS[self.temp_mod_param][self.temp_mod_param_second]#温度模型参数，这里默认选择了 'sapm' 模型和 'open_rack_glass_glass' 环境

        # 获取天气数据
        self.get_weathers_by_csv(csv_file_path,latitude, longitude)
        if self.weather.empty:
            print("天气数据不能为空")
            sys.exit(0)

        # 创建 Location 对象
        location = pvlib.location.Location(latitude, longitude, name=city, altitude=altitude,tz=timezone)

        #太阳能板的倾斜角度为当前地点的纬度，朝向南方（surface_azimuth=180）
        #surface_tilt:表面倾斜角。倾斜角定义为与水平面的角度。
        #surface_azimuth：模块表面的方位角。 北=0，东=90，南=180，西=270。 [度]
        mount = FixedMount(surface_tilt=surface_tilt, surface_azimuth=surface_azimuth)

        # 创建多个个太阳能板阵列
        arrays = []
        for _ in range(array_count):
            modules = []  # 创建空列表用于存放模块
            array = Array(
                mount=mount,
                module_parameters=module,
                temperature_model_parameters=temperature_model_parameters,
                strings=strings, #并联的串数，默认为1。
                modules_per_string = modules_per_string, #每个串中的模块数量，默认为1。
            )
            arrays.append(array)

        # 创建 PVSystem 对象
        system = pvlib.pvsystem.PVSystem(arrays=arrays, inverter_parameters=inverter)

        # 创建 ModelChain 对你喜欢的原因  可能
        mc = pvlib.modelchain.ModelChain(system, location, aoi_model="physical")


        self.weather["precipitable_water"] = pvlib.atmosphere.gueymard94_pw(self.weather["temp_air"], self.weather["relative_humidity"])  # needed for aoi_model="physical" if using CECModueles
        # 运行模型
        mc.run_model(self.weather)
        
        # 获取模拟结果中每个时间步长的交流功率
        ac_power = mc.results.ac
        
        yearly_energy = ac_power.sum()
        daily_energy = ac_power.resample('D').sum()
        hourly_energy = ac_power.resample('H').sum()

        return yearly_energy, daily_energy, hourly_energy

