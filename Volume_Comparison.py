#!/usr/bin/env python
# coding: utf-8

# In[13]:


#pip install pytrends


# In[156]:


#pip install twarc


# In[157]:


from time import sleep
from twarc import Twarc2, expansions
import datetime
import re
import json
import sys


# In[ ]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# In[158]:


def volume_default():
    client = Twarc2(bearer_token="AAAAAAAAAAAAAAAAAAAAAPr9ZgEAAAAAIWJPWDKQNTccmIh2VQZKrnsJEzY%3DMOOUbOqWDLusax3Adyvaq8JoWVtVwOx2LuxwEdHGHJXt8i35ML")
    query = "Zelensky -is:retweet -is:quote -is:reply lang:en"
    start_time = datetime.datetime(2022, 2, 23, 0, 0, 0, 0, datetime.timezone.utc)
    end_time = datetime.datetime(2022, 2, 28, 0, 0, 0, 0, datetime.timezone.utc)
    myjson1 = []
    print("Start Crawling...")
    print("It takes 4-5 hours to scrape all the data, you can use static mode to see the analysis quickly")
    print("A file named 'Zelensky_0223_0228_defaultmode.json' is created")
    search_results = client.search_all(query=query, start_time=start_time, end_time=end_time, max_results=100)
    count = 0
    for page in search_results:
        result = expansions.flatten(page)
        for tweet in result:
            count += 1
            myjson1.append(tweet)
        print('[Now get %d tweets]' % len(myjson1))
        with open("Zelensky_0223_0228_defaultmode.json", "w", encoding = 'utf-8') as f1:
            json.dump(myjson1, f1, indent = 4)
    print("Crawled Tweets number: " + str(count) + "\n")
    data_all_original = pd.read_json("Zelensky_0223_0228_defaultmode.json")
    print("Here is a sample of the Twitter data")
    print(data_all_original.head(5))
    data_all_original['time']=pd.DatetimeIndex(data_all_original['created_at']).map(lambda x: x.strftime('%d%H'))
    # Count of tweets every hour
    count=data_all_original.groupby('time').count()['text']
    print("__________________________________________________________________________")
    print("Here is the volume of Original Tweet about Zelensky from Feb 23 to Feb 27")
    print(count)
    #count[:10]
    index =count.index
    plt.figure(figsize=(80,20))
    plt.title('count')
    plt.plot(index,count,linewidth = 10)
    plt.savefig("Twitter_Count.png")
    print("The Twitter volume peaks at" + " " + count.idxmax() + ", which means Feb 26,15:00")
    print("An image called Twiiter_Count has been generated and saved to the HW5_Yi_Yang folder")    
    print("__________________________________________________________________________")
    print("Now lets look at the Google Trends data")
    kw_list = ['Zelensky']
    interest = pytrend.get_historical_interest(kw_list, year_start=2022, month_start=2, day_start=23, year_end=2022, month_end=2, day_end=28, cat=0, geo='', gprop='', sleep=0) 
    print("Here is a sample of the Google Search Data")
    print(interest.head(10))
    plt.figure(figsize=(80, 20))
    plt.plot(interest,linewidth = 10,color = "orange")
    plt.savefig("Google_Search_Volume.png")
    print("The Google Search Volume peaks at" + " " + str(interest["Zelensky"].idxmax()))
    print("An image called Google_Search_Volume has been generated and saved to the HW5_Yi_Yang folder")
    print("From the two images, we can see that after Zelensky posted the video, volume on Google Search and Twitter about Zelensky both rose sharply. Volume on Google Search reached the highest point around 17nhours earlier than Twitter data")
    


# In[124]:


def volume_static(data1, data2):
    print("It may take 2 minutes to read the Twitter data first")  
    data_all_original = pd.read_json(data1)
    #data1 = "Zelensky_original_0223_0228.json"
    print("Here is a sample of the Twitter data")
    print(data_all_original.head(5))
    data_all_original['time']=pd.DatetimeIndex(data_all_original['created_at']).map(lambda x: x.strftime('%d%H'))
    # Count of Tweets every hour
    count=data_all_original.groupby('time').count()['text']
    print("__________________________________________________________________________")
    print("Here is the volume of Original Tweet about Zelensky from Feb 23 to Feb 27")
    print(count)
    #count[:10]
    index =count.index
    plt.figure(figsize=(80,20))
    plt.title('count')
    plt.plot(index,count,linewidth = 10)
    plt.savefig("Twitter_Count.png")
    print("The Twitter volume peaks at" + " " + count.idxmax() + ", which means Feb 26,15:00")
    print("An image called Twiiter_Count has been generated and saved to the HW5_Yi_Yang folder")
    print("__________________________________________________________________________")
    print("Now lets look at the Google Trends data")
    trendsdata = pd.read_csv(data2)
    #data2 = "GoogleSearch.csv"
    print("Here is a sample of the GoogleSearch data")
    print(trendsdata.head(5))
    max_x = trendsdata.loc[trendsdata["Zelensky"].idxmax()]
    maxtime = str((max_x)["date"])
    print("The Google Search Volume peaks at" + " " + maxtime)
    trendsdata.plot(kind='line',x='time',y='Zelensky',figsize = (80,20),linewidth = 10)
    plt.savefig("Google_Search_Volume.png")
    plt.show()
    print("An image called Google_Search_Volume has been generated and saved to the HW5_Yi_Yang folder")
    print("From the two images, we can see that after Zelensky posted the video, volume on Google Search and Twitter about Zelensky both rose sharply. Volume on Google Search reached the highest point around 17hours earlier than Twitter data")


# In[ ]:


if __name__ == '__main__':
    if len(sys.argv) == 1: 
        volume_default()
    elif sys.argv[1] == '--static':
        data1 = sys.argv[2]
        data2 = sys.argv[3]        
        volume_static(data1, data2)

