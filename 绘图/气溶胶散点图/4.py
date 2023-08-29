import geopandas as gpd

# 读取SHP文件
china_gdf = gpd.read_file('/Users/yanyuchen/气溶胶散点图/ne_50m_admin_1_states_provinces/ne_50m_admin_1_states_provinces.shp', encoding='utf-8')
print(china_gdf.columns)
print(china_gdf['name'].unique())
# 通过行政区划名称筛选塔里木地区
tarim_region = china_gdf[china_gdf['name'] == 'Xinjiang']
tarim_region.to_file('tarim_region.shp', encoding='utf-8')