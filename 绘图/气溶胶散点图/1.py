from pyhdf.SD import SD, SDC

def print_hdf4_structure(file):
    datasets_dict = file.datasets()
    for idx, sds in enumerate(datasets_dict.keys()):
        print(f"{idx + 1}. {sds}")

# 打开HDF4文件
file = SD('//散点/Merry-2/MERRA2_100.tavgM_2d_aer_Nx.198201.SUB.hdf', SDC.READ)
print_hdf4_structure(file)
file.end()
