# -*- coding: utf-8 -*-
"""
@author: Shuowen Wei  -- weisw9@gmail.com 

Question 2
 - Plot a histogram of the number of the trip distance ("Trip Distance").
 - Report any structure you find and any hypotheses you have about that structure.
"""
import pandas as pd, numpy as np, matplotlib.pyplot as plt


"""
Note: 
1. use must define the path and file name to load  
"""

# add label on the top of bars in histogram graph 
def autolabel(rects):
    for rect in rects:
        height = rect.get_height()
        plt.text(rect.get_x()+rect.get_width()/2., 0.05+height, '%d'%int(height),
                ha='center', va='bottom')  
                
def plotHistgram(tripDistance):
    width = 0.5
    bins = [0,1,2,3,4,5,10,20,50,max(tripDistance)]
    counts, _ = np.histogram(tripDistance, bins)
    location = np.arange( len(counts) )*2 + width
    p = plt.bar(location, counts, width*2, align='edge',color='green')
    plt.title('Trip Distinace Histogram - Green Taxi - 09/2015')
    plt.ylim(0, 480000)
    plt.xlabel('Trip Distance Range(miles)')
    plt.ylabel('Number of Trips')
    plt.xticks(location+width, ('0~1', '1~2', '2~3', '3~4', '4~5','5~10', '10~20', '20~50', '>50'))
    autolabel(p)
    plt.savefig("TripDistinaceHistogram_Q2.png")
    plt.show()

if __name__ == "__main__":
    # define the path and file name to load
    save_file_name = r'green_tripdata_201509.csv'
    df = pd.read_csv(save_file_name, sep=',') 
    
    plotHistgram( df['Trip_distance'] )
    
    # Some analysis: 
    lessthan5  = len(df['Trip_distance'][df['Trip_distance'] < 5 ])
    lessthan10  = len(df['Trip_distance'][df['Trip_distance'] < 10 ])
    morethan50  = len(df['Trip_distance'][df['Trip_distance'] >= 100 ])
    print('Number of trips with distances < 5 miles: {0:d}, or {1:5.2f}%.'.format(lessthan5,100*lessthan5/df.shape[0])) 
    print('Number of trips with distances < 10 miles: {0:d}, or {1:5.2f}%.'.format(lessthan10,100*lessthan10/df.shape[0])) 
    print('Number of trips with distances >= 100 miles: {0:d}, or {1:5.4f}%.'.format(morethan50,100*morethan50/df.shape[0])) 
    

