#!/usr/bin/env python
# coding: utf-8

# In[6]:


#pip install gensim


# In[77]:


#pip install twarc


# In[78]:


import sys
from pathlib import Path
from time import sleep
from twarc import Twarc2, expansions
import datetime
import re


# In[36]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import json
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator


# In[82]:


def wordcloud_default():
    # Crawling
    client = Twarc2(bearer_token="AAAAAAAAAAAAAAAAAAAAAPr9ZgEAAAAAIWJPWDKQNTccmIh2VQZKrnsJEzY%3DMOOUbOqWDLusax3Adyvaq8JoWVtVwOx2LuxwEdHGHJXt8i35ML")
    query = "Zelensky -is:retweet -is:quote -is:reply lang:en"
    start_time1 = datetime.datetime(2022, 2, 23, 0, 0, 0, 0, datetime.timezone.utc)
    end_time1 = datetime.datetime(2022, 2, 26, 0, 0, 0, 0, datetime.timezone.utc)
    myjson1 = []
    print("Start Crawling the first file...")
    print("It takes 2-3 hours to scrape all the data, you can use static mode to see the analysis quickly")
    print("A file named 'Zelensky_before_defaultmode.json' is created")
    search_results = client.search_all(query=query, start_time=start_time1, end_time=end_time1, max_results=100)
    count = 0
    for page in search_results:
        result = expansions.flatten(page)
        for tweet in result:
            count += 1
            myjson1.append(tweet)
        print('[Now get %d tweets]' % len(myjson1))
        with open("Zelensky_before_defaultmode.json", "w", encoding = 'utf-8') as f1:
            json.dump(myjson1, f1, indent = 4)
    print("Crawled Tweets number: " + str(count) + "\n")
    
    #Crawl after file
    client = Twarc2(bearer_token="AAAAAAAAAAAAAAAAAAAAAPr9ZgEAAAAAIWJPWDKQNTccmIh2VQZKrnsJEzY%3DMOOUbOqWDLusax3Adyvaq8JoWVtVwOx2LuxwEdHGHJXt8i35ML")
    query = "Zelensky -is:retweet -is:quote -is:reply lang:en"
    start_time2 = datetime.datetime(2022, 2, 26, 0, 0, 0, 0, datetime.timezone.utc)
    end_time2 = datetime.datetime(2022, 3, 1, 0, 0, 0, 0, datetime.timezone.utc)
    myjson2 = []
    print("Start Crawling the second file...")
    print("A file named 'Zelensky_before_defaultmode.json' is created")
    search_results = client.search_all(query=query, start_time=start_time2, end_time=end_time2, max_results=100)
    count = 0
    for page in search_results:
        result = expansions.flatten(page)
        for tweet in result:
            count += 1
            myjson2.append(tweet)

        print('[Now get %d tweets]' % len(myjson2))
        with open("Zelensky_after_defaultmode.json", "w", encoding = 'utf-8') as f1:
            json.dump(myjson2, f1, indent = 4)
    print("Crawled Tweets number: " + str(count) + "\n")
    
    with open('Zelensky_before_defaultmode.json') as f:
        myjson = json.load(f)
    for i in myjson:
        text = i["text"]
    with open("Zelenskybeforetext.txt","w") as f:
        f.write(text)
    with open("Zelenskybeforetext.txt","w") as f:
        for i in myjson:
            f.write(i["text"])
    print("A file called Zelenskybeforetext.txt has been generated and saved to the HW5_Yi_Yang folder")
    #直接用open导入所有文本
    f = open("Zelenskybeforetext.txt","r")
    text=f.read()

    stopwords = set(STOPWORDS)
    stopwords=stopwords|{"it was"}|{"this is"}|{"able to"}|{"https"}|{"gt"}|{"co"}|{"t"}|{"will"}|{"v"}|{"amp"}|{"U"}|{"s"}
    wc = WordCloud(background_color="white", width=1000,height=600,max_words=200,max_font_size=120,
                   stopwords=stopwords,random_state=42, collocations = False)
    wc.generate(text)
    plt.figure(figsize=(20,15)) 
    plt.imshow(wc, interpolation="bilinear")
    plt.title('Twitter Wordcloud before the video posted')
    plt.savefig("Twitter Wordcloud before the video posted.png")
    print("An image called Twitter Wordcloud before the video posted has been generated and saved to the HW5_Yi_Yang folder")
    print("Here are the top 25 words and their frequency in the tweets before Zelensky posted his selfie video")
    first25before = {k: wc.words_[k] for k in list(wc.words_)[:25]}
    print(first25before)
    print("Most words indicate the description of the war")
    print("______________________________________________________________")
    print("Now let's look at what happened after Zelensky posted the videos")
    with open('Zelensky_after_defaultmode.json') as f2:
        myjson2 = json.load(f2)
    with open("Zelenskyaftertext.txt","w") as f:
        for i in myjson2:
            f.write(i["text"])
    print("A file called Zelenskyaftertext.txt has been generated and saved to the HW5_Yi_Yang folder")
    #直接用open导入所有文本
    f2 = open("Zelenskyaftertext.txt","r")
    text2=f2.read()

    stopwords = set(STOPWORDS)
    stopwords=stopwords|{"it was"}|{"this is"}|{"able to"}|{"https"}|{"amp"}|{"co"}|{"t"}|{"will"}|{"country"}|{"s"}|{"U"}
    wc2 = WordCloud(background_color="white", width=1000,height=600,max_words=200,max_font_size=120,
                   stopwords=stopwords,random_state=42,collocations = False)
    wc2.generate(text2)
    plt.figure(figsize=(20,15)) 
    plt.imshow(wc2, interpolation="bilinear")
    plt.title('Twitter Wordcloud after the video posted')
    plt.savefig("Twitter Wordcloud after the video posted.png")
    print("An image called Twitter Wordcloud beofore the video posted has been generated and saved to the HW5_Yi_Yang folder")
    print("Here are the top 25 words and their frequency in the tweets before Zelensky posted his selfie video")
    first25after = {k: wc2.words_[k] for k in list(wc2.words_)[:25]}
    print(first25after.keys())
    print("Some words as 'hero', 'fight' ,'leader' indicate the positive comment about Zelensky, other words as 'ammunition', 'ride' are from Zelensky's statement in his selfie videos")
    print("From the wordcloud we can also see some words as 'courage','respect',indicating positive comment of Mr.Zelensky")
    print("______________________________________________________________")
    #GoogleNewsBefore
    print("Now let's look at the Google News Data")
    
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
    dfbefore = pd.concat(
        map(pd.read_csv, ['Googlenews_0221.csv', 'Googlenews_0222.csv',"Googlenews_0223.csv","Googlenews_0224.csv"]), ignore_index=True)
    
    textbefore = dfbefore["text"].to_string()
    stopwords = set(STOPWORDS)
    stopwords=stopwords|{"it was"}|{"11"}|{"rev"}|{"nGet"}|{"n"}|{"de"}|{"h"}|{"en"}|{"w"}|{"la"}|{"https"}|{"amp"}|{"co"}|{"s"}|{"ge"}|{"t"}|{"will"}|{"country"}|{"NaN"}|{"Ala"}|{"U"}
    wc3 = WordCloud(background_color="white", width=1000,height=600,max_words=200,max_font_size=120,
                   stopwords=stopwords,random_state=42,collocations = False)
    wc3.generate(textbefore)
    plt.figure(figsize=(20,15)) 
    plt.imshow(wc3, interpolation="bilinear")
    plt.title('wordcloud')

    plt.savefig("GoogleNews_before_wordcloud.png")
    print("An image called 'Google News Wordcloud before Zelensky posted the videos' has been generated and saved to the HW5_Yi_Yang folder")
    newsfirst25before = {k: wc3.words_[k] for k in list(wc3.words_)[:25]}
    print("Here are the top 25 words and their frequency in the news before Zelensky posted his selfie video")
    print(newsfirst25before)
    #GoogleNewsAfter
    print("Now let's look at what happened to the news after Zelensky posted the videos")
    dfafter = pd.concat(
        map(pd.read_csv, ['Googlenews_0226.csv',"Googlenews_0227.csv","Googlenews_0228.csv",'Googlenews_0301.csv','Googlenews_0302.csv']), ignore_index=True)
    textafter = dfafter["text"].to_string()
    stopwords = set(STOPWORDS)
    stopwords=stopwords|{"ad"}|{"n"}|{"U"}|{"https"}|{"amp"}|{"co"}|{"Feb"}|{"t"}|{"will"}|{"country"}|{"P"}|{"NaN"}|{"S"}|{"w"}
    wc4 = WordCloud(background_color="white", width=1000,height=600,max_words=200,max_font_size=120,
                   stopwords=stopwords,random_state=42,collocations = False)
    wc4.generate(textafter)
    plt.figure(figsize=(20,15)) 
    plt.imshow(wc4, interpolation="bilinear")
    plt.title('Google News Wordcloud after Zelensky posted the videos')

    plt.savefig("Google News Wordcloud after Zelensky posted the videos.png")
    print("An image called 'Google News Wordcloud after Zelensky posted the videos' has been generated and saved to the HW5_Yi_Yang folder")
    newsfirst25after = {k: wc4.words_[k] for k in list(wc4.words_)[:25]}
    print("Here are the top 25 words and their frequency in the news after Zelensky posted his selfie video")
    print(newsfirst25after)
    print("Compared with Twitter data, there is no significant difference between the news before and after Zelensky posted the videos.The wording of the reports are more neutral compared with tweets")


# In[75]:


def wordcloud_static(data1, data2, data3, data4):
    with open(data1) as f:
    #data1 = 'Twitter_before.json'
        myjson = json.load(f)
    for i in myjson:
        text = i["text"]
    with open("Zelenskybeforetext.txt","w") as f:
        f.write(text)
    with open("Zelenskybeforetext.txt","w") as f:
        for i in myjson:
            f.write(i["text"])
    print("A file called Zelenskybeforetext.txt has been generated and saved to the HW5_Yi_Yang folder")
    #直接用open导入所有文本
    f = open("Zelenskybeforetext.txt","r")
    text=f.read()

    stopwords = set(STOPWORDS)
    stopwords=stopwords|{"it was"}|{"this is"}|{"able to"}|{"https"}|{"gt"}|{"co"}|{"t"}|{"will"}|{"v"}|{"amp"}|{"U"}|{"s"}
    wc = WordCloud(background_color="white", width=1000,height=600,max_words=200,max_font_size=120,
                   stopwords=stopwords,random_state=42, collocations = False)
    wc.generate(text)
    plt.figure(figsize=(20,15)) 
    plt.imshow(wc, interpolation="bilinear")
    plt.title('Twitter Wordcloud before the video posted')
    plt.savefig("Twitter Wordcloud before the video posted.png")
    print("An image called Twitter Wordcloud before the video posted has been generated and saved to the HW5_Yi_Yang folder")
    print("Here are the top 25 words and their frequency in the tweets before Zelensky posted his selfie video")
    first25before = {k: wc.words_[k] for k in list(wc.words_)[:25]}
    print(first25before)
    print("Most words indicate the description of the war")
    print("______________________________________________________________")
    print("Now let's look at what happened after Zelensky posted the videos")
    with open(data2) as f2:
    #data2 = Twitter_after.json
        myjson2 = json.load(f2)
    with open("Zelenskyaftertext.txt","w") as f:
        for i in myjson2:
            f.write(i["text"])
    print("A file called Zelenskyaftertext.txt has been generated and saved to the HW5_Yi_Yang folder")
    #直接用open导入所有文本
    f2 = open("Zelenskyaftertext.txt","r")
    text2=f2.read()

    stopwords = set(STOPWORDS)
    stopwords=stopwords|{"it was"}|{"this is"}|{"able to"}|{"https"}|{"amp"}|{"co"}|{"t"}|{"will"}|{"country"}|{"s"}|{"U"}
    wc2 = WordCloud(background_color="white", width=1000,height=600,max_words=200,max_font_size=120,
                   stopwords=stopwords,random_state=42,collocations = False)
    wc2.generate(text2)
    plt.figure(figsize=(20,15)) 
    plt.imshow(wc2, interpolation="bilinear")
    plt.title('Twitter Wordcloud after the video posted')

    plt.savefig("Twitter Wordcloud after the video posted.png")
    print("An image called Twitter Wordcloud beofore the video posted has been generated and saved to the HW5_Yi_Yang folder")
    print("Here are the top 25 words and their frequency in the tweets before Zelensky posted his selfie video")
    first25after = {k: wc2.words_[k] for k in list(wc2.words_)[:25]}
    print(first25after)
    print("Some words as 'hero', 'fight' ,'leader' indicate the positive comment about Zelensky, other words as 'ammunition', 'ride' are from Zelensky's statement in his selfie videos")
    print("From the wordcloud we can also see some words as 'courage','respect',indicating positive comment of Mr.Zelensky")
    print("______________________________________________________________")
    #GoogleNewsBefore
    print("Now let's look at the Google News Data")
    dfbefore = pd.read_csv(data3)
    #data3 = GoogleNewsBefore.csv
    textbefore = dfbefore["text"].to_string()
    stopwords = set(STOPWORDS)
    stopwords=stopwords|{"it was"}|{"11"}|{"rev"}|{"nGet"}|{"n"}|{"de"}|{"h"}|{"en"}|{"w"}|{"la"}|{"https"}|{"amp"}|{"co"}|{"s"}|{"ge"}|{"t"}|{"will"}|{"country"}|{"NaN"}|{"Ala"}|{"U"}
    wc3 = WordCloud(background_color="white", width=1000,height=600,max_words=200,max_font_size=120,
                   stopwords=stopwords,random_state=42,collocations = False)
    wc3.generate(textbefore)
    plt.figure(figsize=(20,15)) 
    plt.imshow(wc3, interpolation="bilinear")
    plt.title('wordcloud')

    plt.savefig("GoogleNews_before_wordcloud.png")
    print("An image called 'Google News Wordcloud before Zelensky posted the videos' has been generated and saved to the HW5_Yi_Yang folder")
    newsfirst25before = {k: wc3.words_[k] for k in list(wc3.words_)[:25]}
    print("Here are the top 25 words and their frequency in the news before Zelensky posted his selfie video")
    print(newsfirst25before)
    #GoogleNewsAfter
    print("Now let's look at what happened to the news after Zelensky posted the videos")
    dfafter = pd.read_csv(data4)
    #data4 = GoogleNewsAfter.csv
    textafter = dfafter["text"].to_string()
    stopwords = set(STOPWORDS)
    stopwords=stopwords|{"ad"}|{"n"}|{"U"}|{"https"}|{"amp"}|{"co"}|{"Feb"}|{"t"}|{"will"}|{"country"}|{"P"}|{"NaN"}|{"S"}|{"w"}
    wc4 = WordCloud(background_color="white", width=1000,height=600,max_words=200,max_font_size=120,
                   stopwords=stopwords,random_state=42,collocations = False)
    wc4.generate(textafter)
    plt.figure(figsize=(20,15)) 
    plt.imshow(wc4, interpolation="bilinear")
    plt.title('Google News Wordcloud after Zelensky posted the videos')

    plt.savefig("Google News Wordcloud after Zelensky posted the videos.png")
    print("An image called 'Google News Wordcloud after Zelensky posted the videos' has been generated and saved to the HW5_Yi_Yang folder")
    newsfirst25after = {k: wc4.words_[k] for k in list(wc4.words_)[:25]}
    print("Here are the top 25 words and their frequency in the news after Zelensky posted his selfie video")
    print(newsfirst25after)
    print("Compared with Twitter data, there is no significant difference between the news before and after Zelensky posted the videos.The wording of the reports are more neutral compared with tweets")


# In[ ]:


if __name__ == '__main__': #for your purpose, you can think of this line as the saying "run this chunk of code first"
    if len(sys.argv) == 1: # this is basically if you don't pass any additional arguments to the command line
        wordcloud_default()
    elif sys.argv[1] == '--static': # if you pass '--static' to the command line
        data1 = sys.argv[2]
        data2 = sys.argv[3]
        data3 = sys.argv[4]
        data4 = sys.argv[5]
        
        wordcloud_static(data1, data2, data3, data4)

