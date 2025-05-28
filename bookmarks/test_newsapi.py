import requests

# Replace with your actual NewsAPI key
API_KEY = '67c1f11c5a014e87910655670ea6961e'

# Define the endpoint and parameters
url = 'https://newsapi.org/v2/top-headlines'
params = {
    'country': 'us',          # Change to your preferred country code
    'pageSize': 5,            # Limit number of articles
    'apiKey': API_KEY
}

# Send GET request
response = requests.get(url, params=params)

# Check for success
if response.status_code == 200:
    data = response.json()
    articles = data.get('articles', [])
    
    print("Top Headlines:\n")
    for i, article in enumerate(articles, start=1):
        title = article.get('title')
        source = article.get('source', {}).get('name')
        print(f"{i}. {title} (Source: {source})")
else:
    print(f"Failed to fetch news. Status code: {response.status_code}")
    print(response.json())
