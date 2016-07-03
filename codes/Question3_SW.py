# -*- coding: utf-8 -*-
"""
@author: Shuowen Wei  -- weisw9@gmail.com 

Question 3
 - Report mean and median trip distance grouped by hour of day.
 - We'd like to get a rough sense of identifying trips that originate or terminate at one 
   of the NYC area airports. Can you provide a count of how many transactions fit this 
   criteria, the average fair, and any other interesting characteristics of these trips.
"""

import pandas as pd
from geopandas import GeoDataFrame
from shapely.geometry import Point

"""
Note:
1. use must define the path and file name to load 
2. need downlaod 4 libaraies to use geopandas before running this program, please follow instructions here: 
    http://geoffboeing.com/2014/09/using-geopandas-windows/
3. need to downlaod the "Pediacities NYC Neighborhoods" dataset here: 
    http://catalog.opendata.city/dataset/pediacities-nyc-neighborhoods
"""

"""
# Question 3.1
"""
# define the path and file name to load
save_file_name = r'green_tripdata_201509.csv'
df = pd.read_csv(save_file_name, sep=',') 
df['lpep_pickup_datetime'] = pd.to_datetime(df['lpep_pickup_datetime'])
df['hourofDay'] = df['lpep_pickup_datetime'].map(lambda x: x.hour)

# record and print mean and median trip distance by hour of the day 
tripsPerHour = {}
for i in range(24): 
    trip_mean = df['Trip_distance'][df.hourofDay == i].mean()
    trip_median = df['Trip_distance'][df.hourofDay == i].median()
    tripsPerHour[i] = [round(trip_mean,2), trip_median]
    print('The mean and median trip distance at hour {0:1d} of the day are: {1:0.2f} and {2:0.2f}.'.format(i,trip_mean,trip_median)) 


"""
# Question 3.2 
# need to downlaod the "Pediacities NYC Neighborhoods" dataset first
    dataset line: http://catalog.opendata.city/dataset/pediacities-nyc-neighborhoods
Airports to consider: 
    'John F. Kennedy International Airport'
    'LaGuardia Airport'
"""
NYC_geofile = 'NYCNeighborhoods.geojson' 
NYCneighborhoods = GeoDataFrame.from_file(NYC_geofile)
airport = GeoDataFrame(NYCneighborhoods['geometry'][(NYCneighborhoods.neighborhood == 'John F. Kennedy International Airport') | 
                                                (NYCneighborhoods.neighborhood == 'LaGuardia Airport')])
df = GeoDataFrame(df)

# Trips originate/pick up at NYC area airports
df['geometry'] = df.apply(lambda row: Point(row['Pickup_longitude'], row['Pickup_latitude']), axis=1)
pickup = df['geometry'].intersects(airport['geometry'].unary_union)
df_pickup_at_airport = df[pickup]
print('Number of trips originate at NYC area airports is {0:d}'.format(len(df_pickup_at_airport)))
print('Average fair of trips originate at NYC area airports is {0:5.2f}'.format(df_pickup_at_airport['Fare_amount'].mean())) 

# Trips terminate/drop off at NYC area airports
df['geometry'] = df.apply(lambda row: Point(row['Dropoff_longitude'], row['Dropoff_latitude']), axis=1)
dropoff = df['geometry'].intersects(airport['geometry'].unary_union) 
df_dropoff_at_airport = df[dropoff]
print('Number of trips terminate at NYC area airports is {0:d}'.format(len(df_dropoff_at_airport)))
print('Average fair of trips terminate at NYC area airports is {0:5.2f}'.format(df_dropoff_at_airport['Fare_amount'].mean())) 


# Some other interesting characteristics: 
print('Average tip of trips originate at NYC area airports is {0:5.2f}'.format(df_pickup_at_airport['Tip_amount'].mean())) 
print('Average tip of trips terminate at NYC area airports is {0:5.2f}'.format(df_dropoff_at_airport['Tip_amount'].mean())) 

print('Average tolls of trips originate at NYC area airports is {0:5.2f}'.format(df_pickup_at_airport['Tolls_amount'].mean())) 
print('Average tolls of trips terminate at NYC area airports is {0:5.2f}'.format(df_dropoff_at_airport['Tolls_amount'].mean())) 

print('Average tolls of trips originate at NYC area airports is {0:5.2f}'.format(df_pickup_at_airport['Trip_distance'].mean())) 
print('Average tolls of trips terminate at NYC area airports is {0:5.2f}'.format(df_dropoff_at_airport['Trip_distance'].mean())) 
