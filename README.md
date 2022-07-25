# Tweets-about-Zelensky-Selfie-Video
Description: I used three codes to conduct analysis for the datasets I have scraped from Twitter, Google News, and Google Trends.
Package to be installed
	1	pandas
	2	pytrends
	3	numpy
	4	twarc
	5	beautifulsoup4
	6	requests
	7	gensim
	8	matplotlib
	9	goose3
	10	wordcloud
	11	nltk

To install the above packages use the following command: 

pip3 install --user -r requirement.txt 

'requirement.txt' file has a list of all the necessary packages required to run ALL THREE CODES. 



The first file is Volume_Comparison.py

Running the Code:

This code can be run in two modes: default and static
***Note: Default mode may take 4-5 HOURS to scrape all the data from Twitter, using static mode is HIGHLY RECOMMENDED.

To run the code in default mode, please type the following command:

python3 Volume_Comparison.py 

In this mode, A file named Zelensky_0223_0228_defaultmode.json and a file named "GoogleSearchdefaultmode" will be created in the scraping stage.
For analysis, the code will print the date and time when Volume of Mr.Zelensky peaked on Twitter and Google Search. It will also generate and save two images to show the change of the volumes.

To run the code in static mode, please type the following command:

python3 Volume_Comparison.py --static ./Datasets/Zelensky_original_0223_0228.json ./Datasets/GoogleSearch.csv

For analysis, the code will print the date and time when Volume of Mr.Zelensky peaked on Twitter and Google Search. It will also generate and save two images to show the change of the volumes.


The second file is Sentiment_Analysis_Comparison.py

Running the Code:
The code can be run in two modes: default and static
***Note: Default mode may take 4-5 HOURS to scrape all the data from Twitter, using static mode is HIGHLY RECOMMENDED.

Default mode: To run the code in default mode, type command 

python3 Sentiment_Analysis_Comparison.py

In this mode, a file named "Twitter_0223_0228_defaultmode.json" will be created first
Then it will scrape the Google News data using bs4 and goose3. As I have stated in HW4, it can only scrape up to 100 news per query. That's why I run the scrape process for multiple times to get more data. It will generate and save 10 csv files (each file stands for news on one single day)and then the code will merge the files together to dataframe and do analysis.

Static mode: To run the code in static mode, type command  

python3 Sentiment_Analysis_Comparison.py --static ./Datasets/Zelensky_original_0223_0228.json ./Datasets/GoogleNews_0221_0302.csv

In this mode, I printed the sample of mean sentiment scores of Tweets each hour and mean sentiment scores of Google News each day. Then I generated and saved six images in the HW5_Yi_Yang folder to show the change of positive, negative, and neutral scores for the two datasets in the given period.



The third file is WordCloud_Comparison.py


Running the Code:
The code can be run in two modes: default and static

***Note: Default mode may take 4-5 HOURS to scrape all the data from Twitter, using static mode is HIGHLY RECOMMENDED.

Default mode: To run the code in default mode, type command 

python3 WordCloud_Comparison.py

For scraping, I created "Zelensky_before_defaultmode.json" and "Zelensky_after_defaultmode.json" to compare the Twitter data before and after Zelensky posted the videos.
As I did in the second file, I generated 10 files from GoogleNews data and merge them together to do data analysis. I used the data from 0221-0225 to make the Google News WordCloud before Zelensky posted the video, and then I used the data from 0226 to 0302 to make the Google News WordCloud after Zelensky posted the video.
For analysis, I created and compared WordCloud for Tweets and Google News before and after Zelensky posted the videos to see if there is any differences. I also generated two files named "Zelenskybeforetext.txt" and "Zelenskyaftertext.txt" from my datasets as a medium to do the analysis.



Static mode: To run the code in static mode, type command  

python3 WordCloud_Comparison.py --static ./Datasets/Twitter_before.json ./Datasets/Twitter_after.json ./Datasets/GoogleNewsBefore.csv ./Datasets/GoogleNewsAfter.csv


For analysis, I created and compared WordCloud for Tweets and Google News before and after Zelensky posted the videos to see if there is any differences. I also generated two files named "Zelenskybeforetext.txt" and "Zelenskyaftertext.txt" from my datasets as a medium to do the analysis.

 
