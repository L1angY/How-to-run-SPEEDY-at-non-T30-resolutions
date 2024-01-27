import myfunction as myfun
import numpy as np
import xarray as xr


mon_index = np.arange(0, 12, 1, dtype=np.int32)

sshf_monthly = []
lshf_monthly = []

for i in range(len(mon_index)):
    lat, lon, sshf = myfun.read_Exp_data(
    r'C:\Users\59799\Desktop\attm104.nc', 'sshf', slice(-90, 90), slice(0, 360),
    slice('1979-01-01', '2008-12-31'), yrs_num=30, first_mon_index=mon_index[i],
    mon_num=1, level=None)

    _, _, lshf = myfun.read_Exp_data(
    r'C:\Users\59799\Desktop\attm104.nc', 'lshf', slice(-90, 90), slice(0, 360),
    slice('1979-01-01', '2008-12-31'), yrs_num=30, first_mon_index=mon_index[i],
    mon_num=1, level=None)

    sshf_monthly.append(sshf)
    lshf_monthly.append(lshf)


sshf_cli = np.array(sshf_monthly, dtype=np.float32).mean(axis=1)  # 必须要单精度(float32)
lshf_cli = np.array(lshf_monthly, dtype=np.float32).mean(axis=1)  # 不然NCL处理成grd文件并用cdo重新转换成
                                                                  # nc文件检查的时候会出问题


data_vars = {'lshf': (('time', 'lat', 'lon'), lshf_cli),
             'sshf': (('time', 'lat', 'lon'), sshf_cli)}

coords = {'time': np.arange('1979-01-01', '1980-01-01', dtype='datetime64[M]'),
          'lat': lat,
          'lon': lon}

ds = xr.Dataset(data_vars=data_vars, coords=coords)
ds.to_netcdf(r'C:\Users\59799\Desktop\hflux_speedy_ver41.5_1979_2008_clim.t47.nc')

