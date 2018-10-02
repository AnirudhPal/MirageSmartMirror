from newsapi import NewsApiClient
import requests
import json


# Init
newsapi = NewsApiClient(api_key='33ff7834a7ee40928e7bb90746c8b6e5')

# /v2/top-headlines
top_headlines = newsapi.get_top_headlines(
                                        language='en',
                                          country='us')

# /v2/everything
#all_articles = newsapi.get_everything(language='en',
                                      # sort_by='relevancy')

# /v2/sources
sources = newsapi.get_sources()
# print(all_articles)
# print(top_headlines)

url = ('https://newsapi.org/v2/top-headlines?'
       'country=us&'
       'apiKey=33ff7834a7ee40928e7bb90746c8b6e5')
response = requests.get(url)
data = response.json()
print(data['articles'])
