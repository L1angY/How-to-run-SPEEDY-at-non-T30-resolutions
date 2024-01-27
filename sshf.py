import myfunction as myfun
import numpy as np
from scipy.stats import t
from sklearn.preprocessing import StandardScaler
from cartopy.util import add_cyclic_point
import cartopy.io.shapereader as shpreader
import cartopy.crs as ccrs
import proplot as plot


lat_run, lon_run, sshf_run = myfun.read_Exp_data(
    r'C:\Users\59799\Desktop\attm101.nc', 'sshf', slice(-90, 90), slice(0, 360),
    slice('1979-01-01', '2008-12-31'), yrs_num=30, first_mon_index=5,
    mon_num=1, level=None)

sshf_run = sshf_run.mean(axis=0)
sshf_run[sshf_run==0] = np.nan


lat_ori, lon_ori, sshf_ori = myfun.read_Exp_data(
    r'C:\Users\59799\Desktop\hflux_speedy_ver41.5_1979_2008_clim.nc', 'sshf',
    slice(-90, 90), slice(0, 360),
    slice('1979-01-01', '1979-12-31'), yrs_num=1, first_mon_index=5,
    mon_num=1, level=None)

sshf_ori = sshf_ori.mean(axis=0)
sshf_ori[sshf_ori==0] = np.nan


# %% 绘图
subplot_array = [[1, 2]]

plot.rc.reso = 'lo'  # 海岸线使用分辨率 'hi' 'med' 'lo'
proj = plot.Proj('cyl', lon_0=200)
fig = plot.figure(axwidth=3, wspace=0.7, hspace=0.7)
axs = fig.subplots(subplot_array, proj=proj)

axs.format(
    abc='(a)', abcloc='ul', abcsize=9, titlepad=3, gridlabelsize=7.5,
    land=True, landcolor='gray2',
    gridlabelweight='heavy', gridlabelpad=2, labels=True,
    latlim=(-80, 80), lonlines=60, latlines=20,
    gridminor=True, coast=True, coastlinewidth=0.9, coastcolor='gray',
    coastzorder=1, toplabelsize=8.7, toplabelpad=0.8,
    toplabels=('Ori (SSHF, June)', 'Run (SSHF, June)'))

axs[:, 1:].format(latlabels=False)

cmap = plot.Colormap('bam')

cycle_corrmap, cycle_lon = add_cyclic_point(
    sshf_ori, coord=lon_ori)  # 避免出现白线
m = axs[0].contourf(
    cycle_lon, lat_ori, cycle_corrmap, cmap=cmap, cmap_kw={'cut': -0.11},
    extend='both', levels=np.arange(-200, 200.1, 40), zorder=1)

cycle_corrmap, cycle_lon = add_cyclic_point(
    sshf_run, coord=lon_run)  # 避免出现白线
m = axs[1].contourf(
    cycle_lon, lat_run, cycle_corrmap, cmap=cmap, cmap_kw={'cut': -0.11},
    extend='both', levels=np.arange(-200, 200.1, 40), zorder=1)

fig.colorbar(
    m, loc='b', width=0.06, ticklabelsize=6, length=0.6,
    extendsize='1.7em', tickdir='in', pad=0.5, ticklen=2.5)

fig.save(
    r'C:\Users\59799\Desktop\test.png',
    dpi=600)
plot.close()  # figure的GUI界面经常卡死(图片像素太高),所以直接保存后直接关了