import requests
import json

def get_news(api_key):
    url = f'http://newsapi.org/v2/top-headlines?sources=the-times-of-india&apiKey={api_key}'
    news = requests.get(url).text
    news_dict = json.loads(news)
    articles = news_dict['articles']
    try:
        return articles
    except:
        return False
