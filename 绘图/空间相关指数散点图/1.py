import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
import cmocean

# Define constants
yrs = 1991
yre = 2020
nmon = 12
nlag = 6
lagmonth = ["12", "11", "10", "09", "08", "07"]

# Read Obs data
fdir = "/GFPS8p/hjwang/zhouf/Data/CMAP_Precipitation/"
inFile1 = "precip.mon.mean.nc"
ds = xr.open_dataset(fdir + inFile1)
precip = ds['precip'].sel(time=slice(str(yrs), str(yre)))

# Calculate anomalies
precip_anom = precip.groupby("time.month") - precip.groupby("time.month").mean("time")

# Calculate DJF averages
precip_anom_DJF = precip_anom.rolling(time=3, center=True).mean().sel(time=precip_anom['time.season'] == 'DJF')

# Read BCC data
YY = np.empty((yre - yrs, nlag, 181, 360))

for ilg in range(nlag):
    for iyr in range(yrs, yre):
        fname = f"/GFPS8p/hjwang/zhouf/Data/MODESdatasetV2/NCC_CSM11/MODESv2_ncc_csm11_{iyr}{lagmonth[ilg]}_monthly_em.nc"
        ds_bcc = xr.open_dataset(fname)
        YY[iyr - yrs, ilg, :, :] = ds_bcc['precsfc'][ilg:ilg+3, :, :].sum("time")

# Calculate correlation coefficient
TCC = np.empty((nlag, 72, 144))

# Function to calculate the correlation coefficient
def corr_coeff(a, b):
    return np.corrcoef(a, b)[0, 1]

# Calculate TCC
for ilg in range(nlag):
    for lat in range(72):
        for lon in range(144):
            TCC[ilg, lat, lon] = corr_coeff(YY[:, ilg, lat * 2:lat * 2 + 2, lon * 2:lon * 2 + 2], precip_anom_DJF)

# Plotting
fig, axes = plt.subplots(nrows=3, ncols=2, figsize=(15, 15), subplot_kw={'projection': ccrs.PlateCarree()})
cmap = cmocean.cm.balance

for i, ax in enumerate(axes.flat):
    cont = ax.contourf(np.linspace(-20, 160, 144), np.linspace(-40, 45, 72), TCC[i, :, :], levels=np.linspace(-1, 1, 21), cmap=cmap, extend='both')
    ax.coastlines()
    ax.set_xlim([-20, 160])
    ax.set_ylim([-40, 45])
    gl = ax.gridlines(crs=ccrs.PlateCarree(), draw_labels=True, linewidth=1, color='gray', alpha=0.5, linestyle='--')
    gl.xlabels_top = False
    gl.ylabels_right = False
    gl.xformatter = LONGITUDE_FORMATTER
    gl.yformatter = LATITUDE_FORMATTER
    gl.xlabel_style = {'size': 12}
    gl.ylabel_style = {'size': 12}
    ax.set_title(lagmonth[i], fontsize=14)



fig.subplots_adjust(bottom=0.15)
cbar_ax = fig.add_axes([0.15, 0.1, 0.7, 0.03])
cbar = fig.colorbar(cont, cax=cbar_ax, orientation='horizontal', ticks=np.linspace(-1, 1, 21), extendrect=True)
cbar.ax.tick_params(labelsize=12)

plt.suptitle("DJF Precipitation TCC", fontsize=16, y=0.95)
plt.show()
