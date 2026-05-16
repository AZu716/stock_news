import requests

NEWS_API_KEY = "YOUR_NEWS_API_KEY"

def get_world_news():

    try:

        url = f"https://newsapi.org/v2/top-headlines?category=business&language=en&pageSize=5&apiKey={NEWS_API_KEY}"

        response = requests.get(url)

        data = response.json()

        news_list = []

        for article in data["articles"]:

            news = {
                "title": article["title"],
                "image": article["urlToImage"],
                "description": article["description"]
            }

            news_list.append(news)

        return news_list

    except Exception as e:

        print("Error:", e)

        return []