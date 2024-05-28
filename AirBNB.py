#https://app.datacamp.com/workspace/w/7cd2cddc-ecd0-424c-b72f-2b0f6219bb6a/edit
import pandas as pd
import matplotlib.pyplot as pit
import numpy as np
import geopandas as gpd
import re
df = pd.read_csv('listings_austin.csv')
df.dropna(how='any')
df.drop_duplicates(inplace=True) 

#explore
gnp=df.groupby(["neighbourhood", "room_type"])["price"].median() 
gnp.plot.bar(xlabel="Zip Code by room type", ylabel="Median Rent", title="Median Rent by Zipcode and room type", figsize=(10,30))

#visualize
df_geo=gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df.longitude, df.latitude)) 
world_data=gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
axis=world_data[world_data.continent=="North America"].plot(color='lightblue', edgecolor="black")
geomapAustin=df_geo.plot(ax=axis, column=df['price'], cmap='gist_rainbow', legend=True, legend_kwds={"label": "Rent Price", "orientation": "horizontal"})
geomapAustin.set_xlabel("latitude")
geomapAustin.set_ylabel("longitude")
geomapAustin.set_title("Colormap of Austin Texas based on rent price")

#analyze
#plots min nights by median rent price for that group
minNightRent=df.groupby(["minimum_nights"])["price"].median()  
print(minNightRent)
minNightRent.plot.bar(xlabel="Min Nights", ylabel="Median Rent", title="Min nights on median rent",figsize=(10,30))

#plots the location of rent of min night >=7 and has the size based on the rent price 
More7=df.query('minimum_nights>=7')
print(df['minimum_nights'])
df_geoNumNights=gpd.GeoDataFrame(More7, geometry=gpd.points_from_xy(More7.longitude, More7.latitude))
world_dataNumNights=gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
axis=world_dataNumNights[world_dataNumNights.continent=="North America"].plot(color='lightblue', edgecolor="black")
geomapAustinNumNights=df_geoNumNights.plot(ax=axis, column='minimum_nights', cmap='gist_rainbow', legend=True, markersize=More7['price']/100, legend_kwds={"label": "Minimum Nights", "orientation": "horizontal"})
geomapAustinNumNights.set_xlabel("latitude")
geomapAustinNumNights.set_ylabel("longitude")
geomapAustinNumNights.set_title("Colormap of Austin Texas based on minimum nights more than 7 and radius based on price")


#plots the location of rent of min night >=7 and has the size based on the rent price 
Less7=df.query('minimum_nights<7')
print(df['minimum_nights'])
df_geoNumNights=gpd.GeoDataFrame(Less7, geometry=gpd.points_from_xy(Less7.longitude, Less7.latitude))
world_dataNumNights=gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
axis=world_dataNumNights[world_dataNumNights.continent=="North America"].plot(color='lightblue', edgecolor="black")
geomapAustinNumNights=df_geoNumNights.plot(ax=axis, column='minimum_nights', cmap='gist_rainbow', legend=True, markersize=Less7['price']/100, legend_kwds={"label": "Minimum Nights", "orientation": "horizontal"})
geomapAustinNumNights.set_xlabel("latitude")
geomapAustinNumNights.set_ylabel("longitude")
geomapAustinNumNights.set_title("Colormap of Austin Texas based on minimum nights less than 7 and radius based on price")

#plots the location of rent of min night >=7 and <7 as 2 groups and has the size based on the rent price
df['color']=np.where(df["minimum_nights"]<7, 'blue', 'red')
df_geoNumNights=gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df.longitude, df.latitude))
world_dataNumNights=gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
axis=world_dataNumNights[world_dataNumNights.continent=="North America"].plot(color='lightblue', edgecolor="black")
geomapAustinNumNights=df_geoNumNights.plot(ax=axis, c=df['color'], legend=True, markersize=df['price']/100)
geomapAustinNumNights.set_xlabel("latitude")
geomapAustinNumNights.set_ylabel("longitude")
geomapAustinNumNights.set_title("Colormap of Austin Texas based on minimum nights less than 7(blue) and >= than 7(red) and radius based on price")
geomapAustinNumNights.legend()

#a boxplot
df['numNightGroup']=pd.cut(df['minimum_nights'], bins=[-float('inf'), 7, float('inf')], labels=['Less than 7', '7 or more'])
df.boxplot(column='price',by='numNightGroup')
pit.ylabel("price")
pit.title("Comparison of price between apartments with a minimum night stay less than 7 and more or equal to 7")

pit.show()