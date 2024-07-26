import requests
from bs4 import BeautifulSoup
import time

def get_data(url):
    r = requests.get(url)
    print(f'URL: {url}')
    print(f'response: {r}')
    return r.text


##Special characters for URL:
    #&: %26
    #+: %2B
##URL include:
    #limit=100
    #type=link
    #before=fullname => newer posts
    #after=fullname => older posts
url = 'https://old.reddit.com/search?q=oranges&type=link'

def scrape(search_terms, limit=100, reddit_id=None, before_after=None):
    posts = []
    url = 'https://old.reddit.com/search?q='
    img_extensions = ('jpg', 'jpeg', 'png')
    
    #Construct URL
    url += search_terms
    if before_after:
        url += f'&{before_after}='
    if reddit_id:
        url += f'&{reddit_id}'
    url += f'&limit={limit}'
    url += f'&type=link'
    
    before_after = None
    htmldata = get_data(url)
    soup = BeautifulSoup(htmldata, 'html.parser')

    for result in soup.select('.search-result-link'):
        post_obj = {}
        
        post_obj['full_name'] = result.get('data-fullname')
        post_obj['date_time'] = result.time.get('datetime')
        post_obj['post_title'] = result.select('.search-title')[0].text
        post_obj['post_link'] = result.select('.search-title')[0].get('href')
        
        if result.select('.search-link') and (
        result.select('.search-link')[0].get('href').endswith(img_extensions)            
        ):
            post_obj['post_img'] = result.select('.search-link')[0].get('href')
        else:
            post_obj['post_img'] = None
        
        if result.select('.search-result-body'):
            post_obj['post_body'] = result.select('.search-result-body')[0].select('p')[0].text
        else:
            post_obj['post_body'] = None
        
        posts.append(post_obj)

    if posts:
        return posts
    else:
        return False

if __name__ == '__main__':
    scrape('orange')





    