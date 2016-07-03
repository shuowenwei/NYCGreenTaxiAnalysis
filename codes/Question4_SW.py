# -*- coding: utf-8 -*-
"""
@author: Shuowen Wei  -- weisw9@gmail.com 

Question 4
 - Build a derived variable for tip as a percentage of the total fare.
 - Does the tip percentage follow the same distribution for trips originating 
     in upper Manhattan as those originating in the outer boroughs?
 - Build a predictive model for tip as a percentage of the total fare. Use as
     much of the data as you like (or all of it). We will validate a sample
"""

import pandas as pd, numpy as np, matplotlib.pyplot as plt
from geopandas import GeoDataFrame
from shapely.geometry import Point
import numpy
from matplotlib import pyplot
"""
Note:
1. use must define the path and file name to load 
2. need downlaod 4 libaraies to use geopandas before running this program, please follow instructions here: 
    http://geoffboeing.com/2014/09/using-geopandas-windows/
3. need to downlaod the "Pediacities NYC Neighborhoods" dataset here: 
    http://catalog.opendata.city/dataset/pediacities-nyc-neighborhoods
4. Indentify all the neighborhoods in the "upper Manhattan" area:
   Wiki reference: https://en.wikipedia.org/wiki/List_of_Manhattan_neighborhoods.
    Midtown
    Harlem
    Marble Hill
    Morningside Heights
    Inwood
    East Harlem
    Upper East Side
    Washington Heights
    Upper West Side
    Randall's Island
5. Outer boroughs of NYC area includes: 
    Bronx 
    Brooklyn
    Queens 
    Staten Island
"""


"""
# Question 4.1
"""
# define the path and file name to load
save_file_name = r'green_tripdata_201509.csv'
df = pd.read_csv(save_file_name, sep=',') 
df['lpep_pickup_datetime'] = pd.to_datetime(df['lpep_pickup_datetime'])
df['Lpep_dropoff_datetime'] = pd.to_datetime(df['Lpep_dropoff_datetime'])
df['hourofDay'] = df['lpep_pickup_datetime'].map(lambda x: x.hour)

#Build a derived variable for tip as a percentage of the total fare.
df['tip_pct'] = round( df['Tip_amount'] / df['Fare_amount'],4) * 100 


"""
# Question 4.2 
Identify upper Manhattan area and outer boroughs of NYC area first, see the notes above: 
"""
NYC_geofile = 'NYCNeighborhoods.geojson' 
NYCneighborhoods = GeoDataFrame.from_file(NYC_geofile) 
upper_Manhattan = GeoDataFrame(NYCneighborhoods['geometry'][(NYCneighborhoods.neighborhood == 'Midtown') | 
                                                            (NYCneighborhoods.neighborhood == 'Harlem') | 
                                                            (NYCneighborhoods.neighborhood == 'Marble Hill') | 
                                                            (NYCneighborhoods.neighborhood == 'Morningside Heights') | 
                                                            (NYCneighborhoods.neighborhood == 'East Harlem') | 
                                                            (NYCneighborhoods.neighborhood == 'Upper East Side') | 
                                                            (NYCneighborhoods.neighborhood == 'Washington Heights') | 
                                                            (NYCneighborhoods.neighborhood == 'Upper West Side') | 
                                                            (NYCneighborhoods.neighborhood == 'Randall\'s Island')                                                          
                                                            ])
outer_boroughs = GeoDataFrame(NYCneighborhoods['geometry'][(NYCneighborhoods.borough != 'Manhattan')])

# trips from the upper Manhattan area and outer boroughs
df = GeoDataFrame(df)
df['geometry'] = df.apply(lambda row: Point(row['Pickup_longitude'], row['Pickup_latitude']), axis=1)

upper_ManhattanTrips = df[ df['geometry'].intersects(upper_Manhattan['geometry'].unary_union) ] 
outer_boroughsTrips = df[ df['geometry'].intersects(outer_boroughs['geometry'].unary_union) ] 
print('There’re {0:d} trips originating in upper Manhattan. '.format(len(upper_ManhattanTrips)))
print('There’re {0:d} trips originating in outer boroughs. '.format(len(outer_boroughsTrips)))


# tip percentage distribution of upper Manhattan v.s. outer boroughs
bins = numpy.linspace(0, 100, 10)
pyplot.hist(upper_ManhattanTrips['tip_pct'], bins, alpha=0.5, label='upper_Manhattan')
pyplot.hist(outer_boroughsTrips['tip_pct'], bins, alpha=0.5, label='outer_boroughs')
pyplot.xlabel('Tip precentage(0~100%)')
pyplot.ylabel('Number of Trips')
pyplot.title('tip percentage')
pyplot.legend(loc='upper right')
pyplot.savefig("TipPercentageDistribution_Q4.png")
pyplot.show()

pyplot.hist(upper_ManhattanTrips['tip_pct'], bins, alpha=0.5, label='upper_Manhattan',normed=True)
pyplot.hist(outer_boroughsTrips['tip_pct'], bins, alpha=0.5, label='outer_boroughs',normed=True)
pyplot.xlabel('Tip precentage(0~100%)')
pyplot.ylabel('Percentage of Trips')
pyplot.title('tip percentage - normed')
pyplot.legend(loc='upper right')
pyplot.savefig("TipPercentageDistribution_normed_Q4.png")
pyplot.show()



"""
# Question 4.3  
Build a predictive model for tip as a percentage of the total fare
 - clean the data first, 99.87% data were kept for modeling 
 - apply RandomForestRegressor model and measure the performance by mse 
"""
df['tip_pct'] = 100 * df['Tip_amount']/df['Fare_amount']
df_cleandata = df[[
                'lpep_pickup_datetime',
                'Lpep_dropoff_datetime',
                'RateCodeID',
                'Passenger_count',
                'Trip_distance',
                'Fare_amount',
                'Extra',
                'MTA_tax',
                'Tip_amount',
                'Tolls_amount',
                'improvement_surcharge',
                'Total_amount',
                'Payment_type',
                'tip_pct'
                 ]][ (df.Fare_amount > 0 ) & 
                     (df.Tip_amount >= 0 ) &
                     (df.Trip_distance >= 0) &
                     (df.tip_pct <= 100)]
                     
df_cleandata['lpep_pickup_datetime'] = pd.to_datetime(df_cleandata['lpep_pickup_datetime'])
df_cleandata['lpep_pickup_datetime'] = pd.to_datetime(df_cleandata['lpep_pickup_datetime'])

# add a two derived variables 
df_cleandata['hourofDay'] = df_cleandata['lpep_pickup_datetime'].map(lambda x: x.hour)
df_cleandata['dayofWeek'] = df_cleandata['lpep_pickup_datetime'].map(lambda x: x.dayofweek)

# drop puckup and dropoff datetime 
df_cleandata = df_cleandata.drop('lpep_pickup_datetime', 1)
df_cleandata = df_cleandata.drop('Lpep_dropoff_datetime', 1)

X_features = df_cleandata[['RateCodeID',
                'Passenger_count',
                'Trip_distance',
                'Fare_amount',
                'Extra',
                'MTA_tax',
                'Tip_amount',
                'Tolls_amount',
                'improvement_surcharge',
                'Total_amount',
                'Payment_type',
                'hourofDay',
                'dayofWeek'
                ]]
Y_labels = df_cleandata['tip_pct']

from sklearn.cross_validation import train_test_split
from sklearn import linear_model
from sklearn.metrics import mean_squared_error 
from sklearn.svm import SVR
from sklearn.ensemble import RandomForestRegressor

X_train, X_test, y_train, y_test = train_test_split(X_features, Y_labels, test_size=0.33, random_state=42)

# tried some other models
#clf = linear_model.LinearRegression()
#clf = linear_model.Ridge(alpha = 100)
#clf = linear_model.RidgeCV(alphas=[0.01, 10.0, 100.0])
#clf = linear_model.Lasso(alpha = 0.1)
#clf = linear_model.LassoCV(alphas=[0.1, 1.0, 10.0])
#clf = linear_model.LassoLarsCV()
#clf = linear_model.LassoLars(alpha = 0.0001)
#clf = linear_model.BayesianRidge()
#clf = linear_model.SGDRegressor()
#svr_rbf = SVR(kernel='rbf', C=1e3, gamma=0.1)
#svr_lin = SVR(kernel='linear', C=1e3)
#svr_poly = SVR(kernel='poly', C=1e3, degree=2)

estimator = RandomForestRegressor(random_state=0, n_estimators=100)
modelSettings = estimator.fit (X_train, y_train)
pred_train = estimator.predict (X_test) 
mse = mean_squared_error(y_test, pred_train)
print(mse)
