# -*- coding: utf-8 -*-
"""
@author: Shuowen Wei  -- weisw9@gmail.com 

Question 5
 - Build a derived variable representing the average speed over the course of a trip.
 - Can you perform a test to determine if the average trip speeds are materially 
     the same in all weeks of September? If you decide they are not the same, 
     can you form a hypothesis regarding why they differ?
 - Can you build up a hypothesis of average trip speed as a function of time of day?
"""

import pandas as pd, numpy as np, matplotlib.pyplot as plt
import numpy
from matplotlib import pyplot
"""
Note:
1. use must define the path and file name to load 
"""

"""
# Question 5.1
"""
# define the path and file name to load
# define the path and file name to load
save_file_name = r'green_tripdata_201509.csv'
df = pd.read_csv(save_file_name, sep=',') 

df['lpep_pickup_datetime'] = pd.to_datetime(df['lpep_pickup_datetime'])
df['Lpep_dropoff_datetime'] = pd.to_datetime(df['Lpep_dropoff_datetime'])

df['timeDiff'] = (df['Lpep_dropoff_datetime'] - df['lpep_pickup_datetime']).map(lambda diff: diff.seconds/3600)
df['aveSpeed'] = df['Trip_distance']/df['timeDiff']
df['hourofDay'] = df['lpep_pickup_datetime'].map(lambda x: x.hour)
df['weekofyear'] = df['lpep_pickup_datetime'].map(lambda x: x.weekofyear)

min(df['aveSpeed'])
max(df['aveSpeed'])

df_cleandata = df[  (df.Trip_distance > 0) & 
                    (df.timeDiff > 0) &
                    (df.aveSpeed < 80)]
# spot check anormly         
#anormly =  df_cleandata[(df_cleandata.aveSpeed > 80 )  ]
print('Teh average speed over the course of trips is {0:5.2f}. '.format(df_cleandata['aveSpeed'].mean()))

"""
# Question 5.2
 - weeks in Sep. 2015 is from week 36 to week 40 of the year 2015 
""" 
bins = numpy.linspace(0, 80, 10)
pyplot.hist((df_cleandata['aveSpeed'][df_cleandata.weekofyear==36],
             df_cleandata['aveSpeed'][df_cleandata.weekofyear==37],
             df_cleandata['aveSpeed'][df_cleandata.weekofyear==38],
             df_cleandata['aveSpeed'][df_cleandata.weekofyear==39],
             df_cleandata['aveSpeed'][df_cleandata.weekofyear==40],
             ), 
            bins, label=['week1','week2','week3','week4','week5'],normed=True)
pyplot.xlabel('Average Spped (miles/hour)')
pyplot.ylabel('Number of Trips')
pyplot.title('Average Speed by week in Sep. 2015')
pyplot.legend(loc='upper right')
pyplot.savefig("TripAverageSppedbyweek_Q5.png")
pyplot.show()


"""
# Question 5.3 
  Average speed by hour of day 
"""
speed_by_hour= []
for i in range(24): 
    speed_mean = df_cleandata['aveSpeed'][df.hourofDay == i].mean()
    speed_by_hour.append(speed_mean) 
    print('The mean average speed at hour {0:1d} of the day is: {1:0.2f}.'.format(i,speed_mean)) 

plt.xlim(0,24)
plt.scatter(np.arange(0,24,1),speed_by_hour)
pyplot.title('Average Speed by hour in Sep. 2015')
pyplot.xlabel('Hour of day (0 ~ 23)')
pyplot.ylabel('Average Spped (miles/hour)')
pyplot.savefig("TripAverageSppedbyhour_Q5.png")
pyplot.show()


                     



