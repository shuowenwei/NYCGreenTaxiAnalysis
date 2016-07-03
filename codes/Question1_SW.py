# -*- coding: utf-8 -*-
"""
@author: Shuowen Wei  -- weisw9@gmail.com 

Question 1
 - Programmatically download and load into your favorite analytical tool the trip data for September 2015.
 - Report how many rows and columns of data you have loaded.
"""

from urllib import request
import ssl
import pandas as pd

""" 
Note: 
1. use must define the url of the targer csv file
2. use must define the csv file name to save locally 
"""
target_csv_url = r'https://storage.googleapis.com/tlc-trip-data/2015/green_tripdata_2015-09.csv'
save_file_name = r'green_tripdata_201509.csv'

# Programmatically download csv file and save locally 
def download_Trip_data(csv_url, save_file):
    gcontext = ssl.SSLContext(ssl.PROTOCOL_SSLv23) 
    response = request.urlopen(csv_url, context=gcontext).read()
    csv_str = str(response)
    lines = csv_str.strip("b'").split(r'\r\n')
    print('Number of rows downloaded: {0:d}'.format(len(lines)) ) 
    print('Number of columns downloaded: {0:d}'.format(len(lines[0].split(","))) )    
    writeFile = open(save_file,"w")
    for line in lines:
        writeFile.write(line + '\n')
    writeFile.close()

# main function 
if __name__ == "__main__": 
    download_Trip_data(target_csv_url,save_file_name) 
    # load data 
    df = pd.read_csv(save_file_name, sep=',') 
    print('Number of rows loaded: {0:d}.'.format(df.shape[0]) ) 
    print('Number of columns loaded: {0:d}.'.format(df.shape[1]))   