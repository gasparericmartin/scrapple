import requests
from bs4 import BeautifulSoup
import time

def getData(url):
    r = requests.get(url)
    print(f'URL: {url}')
    print(f'response: {r}')
    return r.text

if __name__ == '__main__':
    test_list = []

    keep_going = True

    url = 'https://old.reddit.com/search?q=oranges&type=link'

    for x in range(3):


        htmldata = getData(url)
        soup = BeautifulSoup(htmldata, 'html.parser')
        
        ##Scrape link for next page of results, assign to url variable
        next_page = None

        if len(soup.select('.nextprev')[0].select('a')) < 2:
            url = soup.select('.nextprev')[0].select('a')[0].get('href')
        elif len(soup.select('.nextprev')[0].select('a')) == 2:
            url = soup.select('.nextprev')[0].select('a')[1].get('href')


        for result in soup.select('.search-result-link'):
            post_obj = {}
            
            post_obj['full_name'] = result.get('data-fullname')
            post_obj['date_time'] = result.time.get('datetime')
            post_obj['post_title'] = result.select('.search-title')[0].text
            post_obj['post_link'] = result.select('.search-title')[0].get('href')
            
            if result.select('.search-link'):
                post_obj['post_img'] = result.select('.search-link')[0].get('href')
            else:
                post_obj['post_img'] = None
            
            if result.select('.search-result-body'):
                post_obj['post_body'] = result.select('.search-result-body')[0].select('p')[0].text
            else:
                post_obj['post_body'] = None

            ##Test to see if post has already been processed
            # if post_obj['full_name'] in [object['full_name'] for object in test_list]:
            #     keep_going = False
            
            test_list.append(post_obj)

            time.sleep(2)

    breakpoint()

    print(test_list)