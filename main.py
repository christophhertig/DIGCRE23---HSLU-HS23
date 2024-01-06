import feedparser
import pandas as pd
import requests
from bs4 import BeautifulSoup
import datetime as dt
from tqdm import tqdm  # Importiere tqdm für den Fortschrittsbalken

rss_url='https://www.srf.ch/news/bnf/rss/1646'
#Read feed xml data
news_feed = feedparser.parse(rss_url)
#Flatten data
df_news_feed=pd.json_normalize(news_feed.entries)

## SRF Content
data_list = []
for number in tqdm(range(len(df_news_feed)), desc="Processing SRF Content"):
    titel = df_news_feed['title'][number]
    link = df_news_feed['link'][number]
    published = df_news_feed['published'][number]
    published_parsed = df_news_feed['published_parsed'][number]
    
    # Only take articles from today
    if published_parsed[2] != dt.date.today().day or published_parsed[1] != dt.date.today().month:
        continue
    
    #Request the article url to get the web page content
    article = requests.get(link)

    # extract all paragraph elements inside the page body
    articles = BeautifulSoup(article.content, 'html.parser')
    article_content = articles.find('section', class_='article-content', itemprop='articleBody')
    p_blocks = article_content.find_all('p')

    long_blocks = []
    for block in p_blocks:
        if len(block.text) > 10:
            long_blocks.append(block.text)
    long_blocks_str = ' '.join(long_blocks)
    long_blocks_str = long_blocks_str.replace('\n', ' ')

    data_list.append({
        'title': titel,
        'link': link,
        'published': published,
        'published_parsed': published_parsed,
        'article_content': long_blocks_str
    })
    
# Convert the list of dictionaries to a DataFrame
df_srf = pd.DataFrame(data_list)


## Blick content
blick_rss_url =['https://www.blick.ch/news/rss.xml', 'https://www.blick.ch/schweiz/rss.xml',
                'https://www.blick.ch/ausland/rss.xml', 'https://www.blick.ch/wirtschaft/rss.xml',
                'https://www.blick.ch/politik/rss.xml']

data_list = []

for rss_url in blick_rss_url:
    news_feed = feedparser.parse(rss_url)
    #Flatten data
    df_news_feed=pd.json_normalize(news_feed.entries)
    
    for number in tqdm(range(len(df_news_feed)), desc="Processing Blick Content"):
        titel = df_news_feed['title'][number]
        link = df_news_feed['link'][number]
        published = df_news_feed['published'][number]
        published_parsed = df_news_feed['published_parsed'][number]
        
        # Only take articles from today
        if published_parsed[2] != dt.date.today().day or published_parsed[1] != dt.date.today().month:
            continue
        
        #Request the article url to get the web page content
        article = requests.get(link)

        # extract all paragraph elements inside the page body
        articles = BeautifulSoup(article.content, 'html.parser')
        article_content = articles.findAll('body')
        p_blocks = article_content[0].findAll('p')

        long_blocks = []
        for block in p_blocks:
            if len(block.text) > 10:
                long_blocks.append(block.text)
        long_blocks_str = ' '.join(long_blocks)
        long_blocks_str = long_blocks_str.replace('\n', ' ')

        data_list.append({
            'title': titel,
            'link': link,
            'published': published,
            'published_parsed': published_parsed,
            'article_content': long_blocks_str
        })
        
    # Convert the list of dictionaries to a DataFrame
df_blick = pd.DataFrame(data_list)

# Get current year_month_day_hour
timestep = dt.datetime.now().strftime('%y_%m_%d_%H')

# path for raspberry pi
# path = '/home/christoph/Desktop/articels/'

# path for win10 laptop
path = './local_test/'


# Save df_srf to csv with filename srf_month_day.csv
# df_srf.to_csv(f'{path}{timestep}_srf.csv', index=False)
# df_blick.to_csv(f'{path}{timestep}_blick.csv', index=False)
df_srf.to_csv(f'{path}{timestep}_srf.csv', index=False, encoding='utf-8')
df_blick.to_csv(f'{path}{timestep}_blick.csv', index=False, encoding='utf-8')

print("Scrip runs successfully!")