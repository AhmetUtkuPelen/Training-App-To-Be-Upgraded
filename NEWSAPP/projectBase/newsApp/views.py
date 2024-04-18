from django.shortcuts import render
from .models import*
import requests

# Create your views here.

# !training dummy function ! #
# def index(request):
#     return render(request,'newsApp/index.html')


# ! beautiful soup ajax function ! #
def get_html_content(request):
    import requests
    city = request.GET.get('city')
    city = city.replace(" ", "+")
    USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36"
    LANGUAGE = "en-US,en;q=0.5"
    session = requests.Session()
    session.headers['User-Agent'] = USER_AGENT
    session.headers['Accept-Language'] = LANGUAGE
    session.headers['Content-Language'] = LANGUAGE
    html_content = session.get(f'https://www.google.com/search?q=weather+{city}').text
    return html_content


# ! landing page function ! #
def index(request):
    context = {}
    
    context["result"] = None
    
    if 'city' in request.GET:
    # fetch the weather from Google.
            html_content = get_html_content(request)
            from bs4 import BeautifulSoup
            soup = BeautifulSoup(html_content, 'html.parser')
            result = dict()
    # extract region
            result['region'] = soup.find("span", attrs={"class": "BNeawe tAd8D AP7Wnd"}).text
    # extract temperature now
            result['temp_now'] = soup.find("div", attrs={"class": "BNeawe iBp4i AP7Wnd"}).text
    # get the day, hour and actual weather
            result['dayhour'], result['weather_now'] = soup.find("div", attrs={"class": "BNeawe tAd8D AP7Wnd"}).text.split(
            '\n')
    context["readadminnews"] = CreateNews.objects.all()
    
    return render(request, 'newsApp/index.html', context)


API_KEY = '9018c98f43cc4f5f8a7a42207ae84947'

# ! global news function ! #
def globalNews(request):
    category = request.GET.get('category')
    url = f'https://newsapi.org/v2/top-headlines?category={category}&apiKey={API_KEY}'
    response = requests.get(url)
    data = response.json()
        
    articles = data['articles']
    
    context = {
        'articles':articles
    }
    return render(request,'newsApp/globalnews.html',context)



def readadminnews(request,nid):
    read_news = CreateNews.objects.filter(id=nid)
    return render(request,'newsApp/readadminnews.html',{"readnews":read_news})