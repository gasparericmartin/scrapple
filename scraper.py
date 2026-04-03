import requests
from bs4 import BeautifulSoup
import time

session = requests.Session()
session.headers.update({'User-Agent': 'scrapple/1.0'})

def confirm_over18(dest_url):
    over18_url = f'https://old.reddit.com/over18?dest={dest_url}'
    response = session.get(over18_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    data = {'over18': 'yes'}
    
    for hidden_input in soup.find_all('input', {'type': 'hidden'}):
        data[hidden_input['name']] = hidden_input['value']
    
    session.post('https://old.reddit.com/over18', data=data)

def get_data(url, params=None):
    r = session.get(url, params=params)
    print(f'URL: {r.url}')
    print(f'response: {r}')
    return r.text


def scrape(
        search_terms, 
        subreddit=None,
        limit=100, 
        reddit_id=None, 
        before_after=None, 
        include_over_18=False,
        sort='new',
        time_filter='all',
        restrict_to_subreddit=False,
        pages=1):
    posts = []
    img_extensions = ('jpg', 'jpeg', 'png')
    count = 0
    
    if subreddit:
        base_url = f'https://old.reddit.com/r/{subreddit}/search/'
    else:
        base_url = 'https://old.reddit.com/search/'

    params = {
        'q': ' '.join(search_terms),
        'limit': limit,
        'type': 'link',
        'sort': sort,
        't': time_filter
    }

    if include_over_18:
        params['include_over_18'] = 'on'
        confirm_over18(base_url)
    
    if subreddit and restrict_to_subreddit:
        params['restrict_sr'] = 'on'

    if before_after and reddit_id:
        params[before_after] = reddit_id

    for page in range(pages):
        if count > 0:
            params['count'] = count
            params['after'] = posts[-1]['full_name']

        htmldata = get_data(base_url, params)
        soup = BeautifulSoup(htmldata, 'html.parser')
        page_posts = []

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
            
            page_posts.append(post_obj)

        if not page_posts:
            print(f'No results on page {page + 1}, stopping.')
            break

        posts.extend(page_posts)
        count += len(page_posts)
        print(f'Page {page + 1} scraped, total posts so far: {count}')
        time.sleep(2)

    if posts:
        print(f'Posts: {posts}')
        return posts
    else:
        return False
    
if __name__ == '__main__':
    scrape(
        search_terms=['f4m'],
        limit=5,
        include_over_18=True,
        subreddit='nyr4r',
        restrict_to_subreddit=True,
    )