"""
由于本文件夹内的代码文件为定图所用代码,考虑到精简代码,将所有需要重复使用的函数统一打包进myfunction.py中
然后在分析代码中直接调用(包括:读取数据,计算区域平均指数,计算相关图以及合成分析等)
函数来自code11以前的代码,针对之前的使用体验进行了一定的优化
"""


import numpy as np
import xarray as xr
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
import scipy.special
from scipy.stats.mstats import ttest_ind
from scipy.stats import t


# %% 读取模式试验的数据函数(这里不需要什么扣除线性趋势,也没有办法进行标准化,滤波也取消了)
def read_Exp_data(
        path, var, lat_range, lon_range, time_range, yrs_num,
        first_mon_index, mon_num=3, level=None):
    """
    :param path: 文件路径
    :param var: nc文件中的变量名(例如'sst')
    :param lat_range: 纬度范围(例如:np.arange(60, -62, -2))
    :param lon_range: 经度范围(例如:np.arange(0, 360, 2))
    :param time_range: 时间范围(例如:slice('1979-01-01', '2022-12-31'))
    :param yrs_num: 年份数(例如:需要1979-2022年逐年的D(-1)JF均值时,yrs_num=44)
    :param first_mon_index: 第一个月份的索引,例如需要NDJ平均的数据,则first_mon_index=10
                            (当time_range=slice('1978-01-01', '2022-12-31')时)
    :param mon_num: 需要几个月份平均在一起,例如mon_num=3表示3月平均
    :param level: 需选择的层级
    :return:
    lat: 纬度
    lon: 经度
    array_res: 变量的数组(year, lat, lon)  # 模式实验取出的原始值,需要扣除控制试验来获取异常
    """
    data = xr.open_dataset(path)
    if level is None:
        data = data.sel(lat=lat_range, lon=lon_range, time=time_range)
    else:
        try:
            data = data.sel(lat=lat_range, lon=lon_range, time=time_range,
                            level=level)
        except:
            data = data.sel(lat=lat_range, lon=lon_range, time=time_range,
                            lev=level)

    lat = data.lat.data
    lon = data.lon.data
    array = data[var].data

    # 构建空数组存数据
    array_res = np.empty((yrs_num, len(lat), len(lon)))

    for i in range(yrs_num):
        index = first_mon_index + 12 * i
        array_res[i] = array[index:index + mon_num].mean(axis=0)

    return lat, lon, array_res


# %% 提示本代码均为函数,直接运行无用
if __name__=='__main__':

    print ('本代码均为函数,为了精简后续分析的代码而构建,直接运行无用'
           '在本文件夹其他代码中是使用import语句来调用')