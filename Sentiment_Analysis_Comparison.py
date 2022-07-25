#!/usr/bin/env python
# coding: utf-8

# In[88]:


#pip install twarc


# In[102]:


#pip install goose3


# In[106]:


import bs4
import sys
import csv
import requests
from bs4 import BeautifulSoup
import random
import pandas as pd
import numpy as np
import re
from urllib.parse import urljoin
from bs4.dammit import EncodingDetector
from goose3 import Goose
import matplotlib.pyplot as plt
from pathlib import Path
from time import sleep
from twarc import Twarc2, expansions
import datetime
import re
import json


# In[86]:


def sentiment_default():
    # Crawling
    client = Twarc2(bearer_token="AAAAAAAAAAAAAAAAAAAAAPr9ZgEAAAAAIWJPWDKQNTccmIh2VQZKrnsJEzY%3DMOOUbOqWDLusax3Adyvaq8JoWVtVwOx2LuxwEdHGHJXt8i35ML")
    query = "Zelensky -is:retweet -is:quote -is:reply lang:en"
    start_time = datetime.datetime(2022, 2, 23, 0, 0, 0, 0, datetime.timezone.utc)
    end_time = datetime.datetime(2022, 2, 28, 0, 0, 0, 0, datetime.timezone.utc)
    myjson1 = []
    print("Start Crawling the file...")
    print("It takes 4-5 hours to scrape all the data, you can use static mode to see the analysis quickly")
    print("A file named 'Twitter_0223_0228_defaultmode.json' is created")
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
    data_all_original = pd.read_json("Twitter_0223_0228_defaultmode.json")
    print("Here is a sample of the Twitter data")
    print(data_all_original.head(5))
    import nltk
    from nltk.sentiment.vader import SentimentIntensityAnalyzer
    nltk.download('vader_lexicon')
    # 取出评论列
    target=data_all_original["text"]
    sia = SentimentIntensityAnalyzer()
    score_array=[]
    for sen in target:
        score = sia.polarity_scores(sen)
        for k in score:
            score_array.append(score[k])
    #得到分数矩阵
    score_df=pd.DataFrame(np.array(score_array).reshape(-1,4)).rename(columns={0:'neg',1:'neu',2:'pos',3:'compound'})
    #各分数均值
    score_df.mean()
    #合并矩阵
    data_all_original=data_all_original.join(score_df)
    # 细分评论时间
    data_all_original['time']=pd.DatetimeIndex(data_all_original['created_at']).map(lambda x: x.strftime('%d%H')) 
    data_all_original[2000:2005]
    # 每小时的推特条数
    count=data_all_original.groupby('time').count()['text']
    # 每小时的分数均值
    neg=data_all_original.groupby('time')['neg'].mean()
    pos=data_all_original.groupby('time')['pos'].mean()
    neu=data_all_original.groupby('time')['neu'].mean()
    print("Here is positive scores for Tweets every hour from Feb 23 to Feb 27")
    print(pos)
    print("______________________________________________________________________")
    print("Here is negative scores for Tweets every hour from Feb 23 to Feb 27")
    print(neg)
    print("______________________________________________________________________")
    print("Here is neutral scores for Tweets every hour from Feb 23 to Feb 27")
    print(neu)
    print("______________________________________________________________________")
    index=pos.index
    plt.figure(figsize=(80,20))
    plt.title('positive score')
    plt.plot(index,pos,color = "orange", linewidth = 10)
    plt.savefig("Positive_Score_Twitter.png")
    print("An image called Positive_Score_Twitter has been generated and saved to the HW5_Yi_Yang folder")
    print("Positive Score shows an upward trend after Feb 25 when Zelensky posted the videos")
    index=neg.index
    plt.figure(figsize=(80,20))
    plt.title('negative score')
    plt.plot(index,neg,color = "blue", linewidth = 10)
    plt.savefig("Negative_Score_Twitter.png")
    print("An image called Negative_Score_Twitter has been generated and saved to the HW5_Yi_Yang folder")
    print("Negative Score shows an downward trend after Feb 25 when Zelensky posted the videos despite some fluctuations")
    index=neu.index
    plt.figure(figsize=(80,20))
    plt.title('neutral score')
    plt.plot(index,neu,color = "grey", linewidth = 10)
    plt.savefig("Neutral_Score_Twitter.png")
    print("An image called Neutral_Score_Twitter has been generated and saved to the HW5_Yi_Yang folder")
    print("_____________________________________________________________________________________________")
    
    
    
    print("Now let's look at the Google_News Data")
    url1= 'https://www.google.com'
    text = 'zelensky&tbm=nws&tbs=cdr:1,cd_min:2/21/2022,cd_max:2/21/2022&lr=lang_en&num=100' 
    url = 'https://google.com/search?q=' + text

    headers =    {
      "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Safari/537.36",
    }
    #Use beautifulsoup to request 
    print("Now using beautifulsoup to request title and link for Google news on 0221")
    s = requests.session()
    s.cookies.clear()
    r = s.get(url, headers=headers)
    soup = BeautifulSoup(r.text, 'lxml')
    #Get the list of news hyperlink on the page
    final_urls = []
    for link in soup.find_all('a'):
        if link.attrs.get('class') and ('WlydOe' in link.attrs['class']):
            href = link.attrs.get("href")
            href = urljoin(url1, href)
            final_urls.append(href)
    #Remove duplicate URL's  
    unique_urls = set(final_urls)
    #Convert it back to lists
    unique_urls_list = list(unique_urls)
    print('Get %s unique links' %len(unique_urls_list))
    print("Now using goose3 to scrape the article......")
    print("It may take 10 minutes to scrape the article")
    #Scrape content from the lists
    final_title_list = []
    final_text_list = []
    final_source_list = []
    final_date_list = []
    for data in unique_urls_list:
            request = requests.get(data)
            g = Goose()
            article = g.extract(url=request.url)
            title = article.title
            text = article.cleaned_text
            domain = article.domain
            date = article.publish_date
            #source=re.findall(r'(?<=\.)([^.]+)(?:\.(?:co\.uk|ac\.us|[^.]+(?:$|\n)))',domain)
            final_title_list.append(title)
            final_text_list.append(text)
            final_date_list.append(date)
    #final_source_list.extend(source)
    dict_1 = {'title': final_title_list, 'text': final_text_list, 'author':final_source_list,"date":final_date_list}
    df0221 = pd.DataFrame({key: pd.Series(value) for key, value in dict_1.items()})
    #to csv
    df0221["time"] = "0221"
    df0221.to_csv('Googlenews_0221.csv', encoding='utf-8', index=False)
    print("A file named 'Googlenews_0221.csv'has been created and saved to the HW5_Yi_Yang folder")
    url1= 'https://www.google.com'
    text = 'zelensky&tbm=nws&tbs=cdr:1,cd_min:2/22/2022,cd_max:2/22/2022&lr=lang_en&num=100' 
    url = 'https://google.com/search?q=' + text

    headers =    {
      "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Safari/537.36",
    }
    #Use beautifulsoup to request 
    print("Now using beautifulsoup to request title and link for Google news on 0222")
    s = requests.session()
    s.cookies.clear()
    r = s.get(url, headers=headers)
    soup = BeautifulSoup(r.text, 'lxml')
    #Get the list of news hyperlink on the page
    final_urls = []
    for link in soup.find_all('a'):
        if link.attrs.get('class') and ('WlydOe' in link.attrs['class']):
            href = link.attrs.get("href")
            href = urljoin(url1, href)
            final_urls.append(href)
    #Remove duplicate URL's  
    unique_urls = set(final_urls)
    #Convert it back to lists
    unique_urls_list = list(unique_urls)
    print('Get %s unique links' %len(unique_urls_list))
    print("Now using goose3 to scrape the article......")
    print("It may take 10 minutes to scrape the article")
    #Scrape content from the lists
    final_title_list = []
    final_text_list = []
    final_source_list = []
    final_date_list = []
    for data in unique_urls_list:
            request = requests.get(data)
            g = Goose()
            article = g.extract(url=request.url)
            title = article.title
            text = article.cleaned_text
            domain = article.domain
            date = article.publish_date
            #source=re.findall(r'(?<=\.)([^.]+)(?:\.(?:co\.uk|ac\.us|[^.]+(?:$|\n)))',domain)
            final_title_list.append(title)
            final_text_list.append(text)
            final_date_list.append(date)
    #final_source_list.extend(source)
    dict_1 = {'title': final_title_list, 'text': final_text_list, 'author':final_source_list,"date":final_date_list}
    df0222 = pd.DataFrame({key: pd.Series(value) for key, value in dict_1.items()})
    #to csv
    df0222.to_csv('Googlenews_0222.csv', encoding='utf-8', index=False)
    df0222["time"] = "0222"
    print("A file named 'Googlenews_0222.csv'has been created and saved to the HW5_Yi_Yang folder")
    url1= 'https://www.google.com'
    text = 'zelensky&tbm=nws&tbs=cdr:1,cd_min:2/23/2022,cd_max:2/23/2022&lr=lang_en&num=100' 
    url = 'https://google.com/search?q=' + text

    headers =    {
      "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Safari/537.36",
    }
    #Use beautifulsoup to request 
    print("Now using beautifulsoup to request title and link for Google news on 0223")
    s = requests.session()
    s.cookies.clear()
    r = s.get(url, headers=headers)
    soup = BeautifulSoup(r.text, 'lxml')
    #Get the list of news hyperlink on the page
    final_urls = []
    for link in soup.find_all('a'):
        if link.attrs.get('class') and ('WlydOe' in link.attrs['class']):
            href = link.attrs.get("href")
            href = urljoin(url1, href)
            final_urls.append(href)
    #Remove duplicate URL's  
    unique_urls = set(final_urls)
    #Convert it back to lists
    unique_urls_list = list(unique_urls)
    print('Get %s unique links' %len(unique_urls_list))
    print("Now using goose3 to scrape the article......")
    print("It may take 10 minutes to scrape the article")
    #Scrape content from the lists
    final_title_list = []
    final_text_list = []
    final_source_list = []
    final_date_list = []
    for data in unique_urls_list:
            request = requests.get(data)
            g = Goose()
            article = g.extract(url=request.url)
            title = article.title
            text = article.cleaned_text
            domain = article.domain
            date = article.publish_date
            #source=re.findall(r'(?<=\.)([^.]+)(?:\.(?:co\.uk|ac\.us|[^.]+(?:$|\n)))',domain)
            final_title_list.append(title)
            final_text_list.append(text)
            final_date_list.append(date)
    #final_source_list.extend(source)
    dict_1 = {'title': final_title_list, 'text': final_text_list, 'author':final_source_list,"date":final_date_list}
    df0223 = pd.DataFrame({key: pd.Series(value) for key, value in dict_1.items()})
    #to csv
    df0223.to_csv('Googlenews_0223.csv', encoding='utf-8', index=False)
    df0223["time"] = "0223"
    print("A file named 'Googlenews_0223.csv'has been created and saved to the HW5_Yi_Yang folder")

    url1= 'https://www.google.com'
    text = 'zelensky&tbm=nws&tbs=cdr:1,cd_min:2/24/2022,cd_max:2/24/2022&lr=lang_en&num=100' 
    url = 'https://google.com/search?q=' + text

    headers =    {
      "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Safari/537.36",
    }
    #Use beautifulsoup to request 
    print("Now using beautifulsoup to request title and link for Google news on 0224")
    s = requests.session()
    s.cookies.clear()
    r = s.get(url, headers=headers)
    soup = BeautifulSoup(r.text, 'lxml')
    #Get the list of news hyperlink on the page
    final_urls = []
    for link in soup.find_all('a'):
        if link.attrs.get('class') and ('WlydOe' in link.attrs['class']):
            href = link.attrs.get("href")
            href = urljoin(url1, href)
            final_urls.append(href)
    #Remove duplicate URL's  
    unique_urls = set(final_urls)
    #Convert it back to lists
    unique_urls_list = list(unique_urls)
    print('Get %s unique links' %len(unique_urls_list))
    print("Now using goose3 to scrape the article......")
    print("It may take 10 minutes to scrape the article")
    #Scrape content from the lists
    final_title_list = []
    final_text_list = []
    final_source_list = []
    final_date_list = []
    for data in unique_urls_list:
            request = requests.get(data)
            g = Goose()
            article = g.extract(url=request.url)
            title = article.title
            text = article.cleaned_text
            domain = article.domain
            date = article.publish_date
            #source=re.findall(r'(?<=\.)([^.]+)(?:\.(?:co\.uk|ac\.us|[^.]+(?:$|\n)))',domain)
            final_title_list.append(title)
            final_text_list.append(text)
            final_date_list.append(date)
    #final_source_list.extend(source)
    dict_1 = {'title': final_title_list, 'text': final_text_list, 'author':final_source_list,"date":final_date_list}
    df0224 = pd.DataFrame({key: pd.Series(value) for key, value in dict_1.items()})
    #to csv
    df0224["time"] = "0224"
    df0224.to_csv('Googlenews_0224.csv', encoding='utf-8', index=False)
    print("A file named 'Googlenews_0224.csv'has been created and saved to the HW5_Yi_Yang folder")

    url1= 'https://www.google.com'
    text = 'zelensky&tbm=nws&tbs=cdr:1,cd_min:2/25/2022,cd_max:2/25/2022&lr=lang_en&num=100' 
    url = 'https://google.com/search?q=' + text

    headers =    {
      "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Safari/537.36",
    }
    #Use beautifulsoup to request 
    print("Now using beautifulsoup to request title and link for Google news on 0225")
    s = requests.session()
    s.cookies.clear()
    r = s.get(url, headers=headers)
    soup = BeautifulSoup(r.text, 'lxml')
    #Get the list of news hyperlink on the page
    final_urls = []
    for link in soup.find_all('a'):
        if link.attrs.get('class') and ('WlydOe' in link.attrs['class']):
            href = link.attrs.get("href")
            href = urljoin(url1, href)
            final_urls.append(href)
    #Remove duplicate URL's  
    unique_urls = set(final_urls)
    #Convert it back to lists
    unique_urls_list = list(unique_urls)
    print('Get %s unique links' %len(unique_urls_list))
    print("Now using goose3 to scrape the article......")
    print("It may take 10 minutes to scrape the article")
    #Scrape content from the lists
    final_title_list = []
    final_text_list = []
    final_source_list = []
    final_date_list = []
    for data in unique_urls_list:
            request = requests.get(data)
            g = Goose()
            article = g.extract(url=request.url)
            title = article.title
            text = article.cleaned_text
            domain = article.domain
            date = article.publish_date
            #source=re.findall(r'(?<=\.)([^.]+)(?:\.(?:co\.uk|ac\.us|[^.]+(?:$|\n)))',domain)
            final_title_list.append(title)
            final_text_list.append(text)
            final_date_list.append(date)
    #final_source_list.extend(source)
    dict_1 = {'title': final_title_list, 'text': final_text_list, 'author':final_source_list,"date":final_date_list}
    df0225 = pd.DataFrame({key: pd.Series(value) for key, value in dict_1.items()})
    #to csv
    df0225["time"] = "0225"
    display(df0225)
    df0225.to_csv('Googlenews_0225.csv', encoding='utf-8', index=False)
    print("A file named 'Googlenews_0225.csv'has been created and saved to the HW5_Yi_Yang folder")
    url1= 'https://www.google.com'
    text = 'zelensky&tbm=nws&tbs=cdr:1,cd_min:2/26/2022,cd_max:2/26/2022&lr=lang_en&num=100' 
    url = 'https://google.com/search?q=' + text

    headers =    {
      "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Safari/537.36",
    }
    #Use beautifulsoup to request 
    print("Now using beautifulsoup to request title and link for Google news on 0226")
    s = requests.session()
    s.cookies.clear()
    r = s.get(url, headers=headers)
    soup = BeautifulSoup(r.text, 'lxml')
    #Get the list of news hyperlink on the page
    final_urls = []
    for link in soup.find_all('a'):
        if link.attrs.get('class') and ('WlydOe' in link.attrs['class']):
            href = link.attrs.get("href")
            href = urljoin(url1, href)
            final_urls.append(href)
    #Remove duplicate URL's  
    unique_urls = set(final_urls)
    #Convert it back to lists
    unique_urls_list = list(unique_urls)
    print('Get %s unique links' %len(unique_urls_list))
    print("Now using goose3 to scrape the article......")
    print("It may take 10 minutes to scrape the article")
    #Scrape content from the lists
    final_title_list = []
    final_text_list = []
    final_source_list = []
    final_date_list = []
    for data in unique_urls_list:
            request = requests.get(data)
            g = Goose()
            article = g.extract(url=request.url)
            title = article.title
            text = article.cleaned_text
            domain = article.domain
            date = article.publish_date
            #source=re.findall(r'(?<=\.)([^.]+)(?:\.(?:co\.uk|ac\.us|[^.]+(?:$|\n)))',domain)
            final_title_list.append(title)
            final_text_list.append(text)
            final_date_list.append(date)
    #final_source_list.extend(source)
    dict_1 = {'title': final_title_list, 'text': final_text_list, 'author':final_source_list,"date":final_date_list}
    df0226 = pd.DataFrame({key: pd.Series(value) for key, value in dict_1.items()})
    #to csv
    df0226["time"] = "0226"
    df0226.to_csv('Googlenews_0226.csv', encoding='utf-8', index=False)
    print("A file named 'Googlenews_0226.csv'has been created and saved to the HW5_Yi_Yang folder")

    url1= 'https://www.google.com'
    text = 'zelensky&tbm=nws&tbs=cdr:1,cd_min:2/27/2022,cd_max:2/27/2022&lr=lang_en&num=100' 
    url = 'https://google.com/search?q=' + text

    headers =    {
      "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Safari/537.36",
    }
    #Use beautifulsoup to request 
    print("Now using beautifulsoup to request title and link for Google news on 0227")
    s = requests.session()
    s.cookies.clear()
    r = s.get(url, headers=headers)
    soup = BeautifulSoup(r.text, 'lxml')
    #Get the list of news hyperlink on the page
    final_urls = []
    for link in soup.find_all('a'):
        if link.attrs.get('class') and ('WlydOe' in link.attrs['class']):
            href = link.attrs.get("href")
            href = urljoin(url1, href)
            final_urls.append(href)
    #Remove duplicate URL's  
    unique_urls = set(final_urls)
    #Convert it back to lists
    unique_urls_list = list(unique_urls)
    print('Get %s unique links' %len(unique_urls_list))
    print("Now using goose3 to scrape the article......")
    print("It may take 10 minutes to scrape the article")
    #Scrape content from the lists
    final_title_list = []
    final_text_list = []
    final_source_list = []
    final_date_list = []
    for data in unique_urls_list:
            request = requests.get(data)
            g = Goose()
            article = g.extract(url=request.url)
            title = article.title
            text = article.cleaned_text
            domain = article.domain
            date = article.publish_date
            #source=re.findall(r'(?<=\.)([^.]+)(?:\.(?:co\.uk|ac\.us|[^.]+(?:$|\n)))',domain)
            final_title_list.append(title)
            final_text_list.append(text)
            final_date_list.append(date)
    #final_source_list.extend(source)
    dict_1 = {'title': final_title_list, 'text': final_text_list, 'author':final_source_list,"date":final_date_list}
    df0227 = pd.DataFrame({key: pd.Series(value) for key, value in dict_1.items()})
    #to csv
    df0227["time"] = "0227"
    display(df0227)
    df0227.to_csv('Googlenews_0227.csv', encoding='utf-8', index=False)
    print("A file named 'Googlenews_0227.csv'has been created and saved to the HW5_Yi_Yang folder")

    url1= 'https://www.google.com'
    text = 'zelensky&tbm=nws&tbs=cdr:1,cd_min:2/28/2022,cd_max:2/28/2022&lr=lang_en&num=100' 
    url = 'https://google.com/search?q=' + text

    headers =    {
      "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Safari/537.36",
    }
    #Use beautifulsoup to request 
    print("Now using beautifulsoup to request title and link for Google news on 0228")
    s = requests.session()
    s.cookies.clear()
    r = s.get(url, headers=headers)
    soup = BeautifulSoup(r.text, 'lxml')
    #Get the list of news hyperlink on the page
    final_urls = []
    for link in soup.find_all('a'):
        if link.attrs.get('class') and ('WlydOe' in link.attrs['class']):
            href = link.attrs.get("href")
            href = urljoin(url1, href)
            final_urls.append(href)
    #Remove duplicate URL's  
    unique_urls = set(final_urls)
    #Convert it back to lists
    unique_urls_list = list(unique_urls)
    print('Get %s unique links' %len(unique_urls_list))
    print("Now using goose3 to scrape the article......")
    print("It may take 10 minutes to scrape the article")
    #Scrape content from the lists
    final_title_list = []
    final_text_list = []
    final_source_list = []
    final_date_list = []
    for data in unique_urls_list:
            request = requests.get(data)
            g = Goose()
            article = g.extract(url=request.url)
            title = article.title
            text = article.cleaned_text
            domain = article.domain
            date = article.publish_date
            #source=re.findall(r'(?<=\.)([^.]+)(?:\.(?:co\.uk|ac\.us|[^.]+(?:$|\n)))',domain)
            final_title_list.append(title)
            final_text_list.append(text)
            final_date_list.append(date)
    #final_source_list.extend(source)
    dict_1 = {'title': final_title_list, 'text': final_text_list, 'author':final_source_list,"date":final_date_list}
    df0228 = pd.DataFrame({key: pd.Series(value) for key, value in dict_1.items()})
    #to csv
    df0228["time"] = "0228"
    df0228.to_csv('Googlenews_0228.csv', encoding='utf-8', index=False)
    print("A file named 'Googlenews_0228.csv'has been created and saved to the HW5_Yi_Yang folder")
    url1= 'https://www.google.com'
    text = 'zelensky&tbm=nws&tbs=cdr:1,cd_min:3/1/2022,cd_max:3/1/2022&lr=lang_en&num=100' 
    url = 'https://google.com/search?q=' + text

    headers =    {
      "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Safari/537.36",
    }
    #Use beautifulsoup to request 
    print("Now using beautifulsoup to request title and link for Google news on 0301")
    s = requests.session()
    s.cookies.clear()
    r = s.get(url, headers=headers)
    soup = BeautifulSoup(r.text, 'lxml')
    #Get the list of news hyperlink on the page
    final_urls = []
    for link in soup.find_all('a'):
        if link.attrs.get('class') and ('WlydOe' in link.attrs['class']):
            href = link.attrs.get("href")
            href = urljoin(url1, href)
            final_urls.append(href)
    #Remove duplicate URL's  
    unique_urls = set(final_urls)
    #Convert it back to lists
    unique_urls_list = list(unique_urls)
    print('Get %s unique links' %len(unique_urls_list))
    print("Now using goose3 to scrape the article......")
    print("It may take 10 minutes to scrape the article")
    #Scrape content from the lists
    final_title_list = []
    final_text_list = []
    final_source_list = []
    final_date_list = []
    for data in unique_urls_list:
            request = requests.get(data)
            g = Goose()
            article = g.extract(url=request.url)
            title = article.title
            text = article.cleaned_text
            domain = article.domain
            date = article.publish_date
            #source=re.findall(r'(?<=\.)([^.]+)(?:\.(?:co\.uk|ac\.us|[^.]+(?:$|\n)))',domain)
            final_title_list.append(title)
            final_text_list.append(text)
            final_date_list.append(date)
    #final_source_list.extend(source)
    dict_1 = {'title': final_title_list, 'text': final_text_list, 'author':final_source_list,"date":final_date_list}
    df0301 = pd.DataFrame({key: pd.Series(value) for key, value in dict_1.items()})
    #to csv
    df0301["time"] = "0301"
    df0301.to_csv('Googlenews_0301.csv', encoding='utf-8', index=False)
    print("A file named 'Googlenews_0301.csv'has been created and saved to the HW5_Yi_Yang folder")
    url1= 'https://www.google.com'
    text = 'zelensky&tbm=nws&tbs=cdr:1,cd_min:3/2/2022,cd_max:3/2/2022&lr=lang_en&num=100' 
    url = 'https://google.com/search?q=' + text

    headers =    {
      "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Safari/537.36",
    }
    #Use beautifulsoup to request 
    print("Now using beautifulsoup to request title and link for Google news on 0301")
    s = requests.session()
    s.cookies.clear()
    r = s.get(url, headers=headers)
    soup = BeautifulSoup(r.text, 'lxml')
    #Get the list of news hyperlink on the page
    final_urls = []
    for link in soup.find_all('a'):
        if link.attrs.get('class') and ('WlydOe' in link.attrs['class']):
            href = link.attrs.get("href")
            href = urljoin(url1, href)
            final_urls.append(href)
    #Remove duplicate URL's  
    unique_urls = set(final_urls)
    #Convert it back to lists
    unique_urls_list = list(unique_urls)
    print('Get %s unique links' %len(unique_urls_list))
    print("Now using goose3 to scrape the article......")
    print("It may take 10 minutes to scrape the article")
    #Scrape content from the lists
    final_title_list = []
    final_text_list = []
    final_source_list = []
    final_date_list = []
    for data in unique_urls_list:
            request = requests.get(data)
            g = Goose()
            article = g.extract(url=request.url)
            title = article.title
            text = article.cleaned_text
            domain = article.domain
            date = article.publish_date
            #source=re.findall(r'(?<=\.)([^.]+)(?:\.(?:co\.uk|ac\.us|[^.]+(?:$|\n)))',domain)
            final_title_list.append(title)
            final_text_list.append(text)
            final_date_list.append(date)
    #final_source_list.extend(source)
    dict_1 = {'title': final_title_list, 'text': final_text_list, 'author':final_source_list,"date":final_date_list}
    df0302 = pd.DataFrame({key: pd.Series(value) for key, value in dict_1.items()})
    #to csv
    df0302["time"] = "0302"
    df0302.to_csv('Googlenews_0302.csv', encoding='utf-8', index=False)
    print("A file named 'Googlenews_0302.csv'has been created and saved to the HW5_Yi_Yang folder")

    # merging csv files
    googledata = pd.concat(
        map(pd.read_csv, ['Googlenews_0221.csv', 'Googlenews_0222.csv',"Googlenews_0223.csv","Googlenews_0224.csv","Googlenews_0225.csv","Googlenews_0226.csv","Googlenews_0227.csv","Googlenews_0228.csv","Googlenews_0301.csv","Googlenews_0302.csv"]), ignore_index=True)
    googledata['time'] = googledata['time'].replace([221],'0221')
    googledata['time'] = googledata['time'].replace([222],'0222')
    googledata['time'] = googledata['time'].replace([223],'0223')
    googledata['time'] = googledata['time'].replace([224],'0224')
    googledata['time'] = googledata['time'].replace([225],'0225')
    googledata['time'] = googledata['time'].replace([226],'0226')
    googledata['time'] = googledata['time'].replace([227],'0227')
    googledata['time'] = googledata['time'].replace([301],'0301')
    googledata['time'] = googledata['time'].replace([302],'0302')
    googledata['time'] = googledata['time'].replace([229],'0228')
    googledata['time'] = googledata['time'].replace([228.0],'0228')
    print(googledata.head(5))
    # 取出评论列
    target=googledata["text"].to_list()
    sia = SentimentIntensityAnalyzer()
    score_array=[]
    for sen in target:
        try:
            score = sia.polarity_scores(sen)
        except:
            pass
        for k in score:
            score_array.append(score[k])
    #得到分数矩阵
    score_df=pd.DataFrame(np.array(score_array).reshape(-1,4)).rename(columns={0:'neg',1:'neu',2:'pos',3:'compound'})
    #各分数均值
    score_df.mean()
    googledata=googledata.join(score_df)
    neg2=googledata.groupby('time')['neg'].mean()
    pos2=googledata.groupby('time')['pos'].mean()
    neu2=googledata.groupby('time')['neu'].mean()
    print("Here is the positive score of news every day")
    print(pos2)
    print("_____________________________________________")
    print("Here is the negtive score of news every day")
    print(neg2)
    print("_____________________________________________")
    print("Here is the neutral score of news every day")
    print(neu2)
    print("_____________________________________________")
    index=pos2.index
    plt.figure(figsize=(16,5))
    plt.title('positive score')
    plt.plot(index,pos2,linewidth = 5, color = "orange")
    plt.savefig("Positive_Score_Google_News.png")
    print("An image called Positive_Score_Google_News has been generated and saved to the HW5_Yi_Yang folder")
    index=neg2.index
    plt.figure(figsize=(16,5))
    plt.title('negative score')
    plt.plot(index,neg2,linewidth = 5, color = "blue")
    plt.savefig("Negative_Score_Google_News.png")
    print("An image called Negative_Score_Google_News has been generated and saved to the HW5_Yi_Yang folder")
    index=neu2.index
    plt.figure(figsize=(16,5))
    plt.title('neutral score')
    plt.plot(index,neu2,linewidth = 5, color = "grey")
    plt.savefig("Neutral_Score_Google_News.png")
    print("An image called Neutral_Score_Google_News has been generated and saved to the HW5_Yi_Yang folder")


# In[82]:


def sentiment_static(data1,data2):
    print("Now reading data, may take 30 seconds to generate a preview")
    data_all_original = pd.read_json(data1)
    #data1 = "Zelensky_original_0223_0228.json"
    print("Here is a sample of the Twitter data")
    print(data_all_original.head(5))
    print("Now calculating the sentiment score using SentimentIntensityAnalyser")
    import nltk
    from nltk.sentiment.vader import SentimentIntensityAnalyzer
    nltk.download('vader_lexicon')
    # 取出评论列
    target=data_all_original["text"]
    sia = SentimentIntensityAnalyzer()
    score_array=[]
    for sen in target:
        score = sia.polarity_scores(sen)
        for k in score:
            score_array.append(score[k])
    #get score
    score_df=pd.DataFrame(np.array(score_array).reshape(-1,4)).rename(columns={0:'neg',1:'neu',2:'pos',3:'compound'})
    #mean score
    score_df.mean()
    #合并矩阵
    data_all_original=data_all_original.join(score_df)
    # 细分评论时间
    data_all_original['time']=pd.DatetimeIndex(data_all_original['created_at']).map(lambda x: x.strftime('%d%H')) 
    data_all_original[2000:2005]
    # 每小时的推特条数
    count=data_all_original.groupby('time').count()['text']
    # 每小时的分数均值
    neg=data_all_original.groupby('time')['neg'].mean()
    pos=data_all_original.groupby('time')['pos'].mean()
    neu=data_all_original.groupby('time')['neu'].mean()
    print("Here is positive scores for Tweets every hour from Feb 23 to Feb 27")
    print(pos)
    print("______________________________________________________________________")
    print("Here is negative scores for Tweets every hour from Feb 23 to Feb 27")
    print(neg)
    print("______________________________________________________________________")
    print("Here is neutral scores for Tweets every hour from Feb 23 to Feb 27")
    print(neu)
    print("______________________________________________________________________")
    index=pos.index
    plt.figure(figsize=(80,20))
    plt.title('positive score')
    plt.plot(index,pos,color = "orange", linewidth = 10)
    plt.savefig("Positive_Score_Twitter.png")
    print("An image called Positive_Score_Twitter has been generated and saved to the HW5_Yi_Yang folder")
    print("Positive Score shows an upward trend after Feb 25 when Zelensky posted the videos")
    index=neg.index
    plt.figure(figsize=(80,20))
    plt.title('negative score')
    plt.plot(index,neg,color = "blue", linewidth = 10)
    plt.savefig("Negative_Score_Twitter.png")
    print("An image called Negative_Score_Twitter has been generated and saved to the HW5_Yi_Yang folder")
    print("Negative Score shows an downward trend after Feb 25 when Zelensky posted the videos despite some fluctuations")
    index=neu.index
    plt.figure(figsize=(80,20))
    plt.title('neutral score')
    plt.plot(index,neu,color = "grey", linewidth = 10)
    plt.savefig("Neutral_Score_Twitter.png")
    print("An image called Neutral_Score_Twitter has been generated and saved to the HW5_Yi_Yang folder")
    print("Now let's look at the Google_News Data")
    googledata = pd.read_csv(data2)  
    #data2 =  'GoogleNews_0221_0302.csv'
    print("Here is a sample of the Google News Data")
    print(googledata.head(5))
    target=googledata["text"].to_list()
    sia = SentimentIntensityAnalyzer()
    score_array=[]
    for sen in target:
        try:
            score = sia.polarity_scores(sen)
        except:
            pass
        for k in score:
            score_array.append(score[k])
    #get scores
    score_df=pd.DataFrame(np.array(score_array).reshape(-1,4)).rename(columns={0:'neg',1:'neu',2:'pos',3:'compound'})
    #mean score
    score_df.mean()
    googledata=googledata.join(score_df)
    googledata['date'] = googledata['date'].replace([221],'0221')
    googledata['date'] = googledata['date'].replace([222],'0222')
    googledata['date'] = googledata['date'].replace([223],'0223')
    googledata['date'] = googledata['date'].replace([224],'0224')
    googledata['date'] = googledata['date'].replace([225],'0225')
    googledata['date'] = googledata['date'].replace([226],'0226')
    googledata['date'] = googledata['date'].replace([227],'0227')
    googledata['date'] = googledata['date'].replace([301],'0301')
    googledata['date'] = googledata['date'].replace([302],'0302')
    googledata['date'] = googledata['date'].replace([229],'0228')
    neg2=googledata.groupby('date')['neg'].mean()
    pos2=googledata.groupby('date')['pos'].mean()
    neu2=googledata.groupby('date')['neu'].mean()
    print("Here is the positive score of news every day")
    print(pos2)
    print("_____________________________________________")
    print("Here is the negtive score of news every day")
    print(neg2)
    print("_____________________________________________")
    print("Here is the neutral score of news every day")
    print(neu2)
    print("_____________________________________________")
    index=pos2.index
    plt.figure(figsize=(16,5))
    plt.title('positive score')
    plt.plot(index,pos2,linewidth = 5, color = "orange")
    plt.savefig("Positive_Score_Google_News.png")
    print("An image called Positive_Score_Google_News has been generated and saved to the HW5_Yi_Yang folder")
    index=neg2.index
    plt.figure(figsize=(16,5))
    plt.title('negative score')
    plt.plot(index,neg2,linewidth = 5, color = "blue")
    plt.savefig("Negative_Score_Google_News.png")
    print("An image called Negative_Score_Google_News has been generated and saved to the HW5_Yi_Yang folder")
    index=neu2.index
    plt.figure(figsize=(16,5))
    plt.title('neutral score')
    plt.plot(index,neu2,linewidth = 5, color = "grey")
    plt.savefig("Neutral_Score_Google_News.png")
    print("An image called Neutral_Score_Google_News has been generated and saved to the HW5_Yi_Yang folder")


# In[ ]:


if __name__ == '__main__': #for your purpose, you can think of this line as the saying "run this chunk of code first"
    if len(sys.argv) == 1: # this is basically if you don't pass any additional arguments to the command line
        sentiment_default()
    elif sys.argv[1] == '--static': # if you pass '--static' to the command line
        data1 = sys.argv[2]
        data2 = sys.argv[3]
        sentiment_static(data1, data2)

