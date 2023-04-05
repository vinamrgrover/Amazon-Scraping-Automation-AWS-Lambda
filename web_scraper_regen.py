import requests, os
from bs4 import BeautifulSoup
import re, random
import pandas as pd
from requests.exceptions import HTTPError
import boto3

headers = [
  {
    'User-Agent' : '(Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36)'
  }, 
  
  {
    'User-Agent' : '(Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36)'
  }, 

  {
    'User-Agent' : '(Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36)'
  }
]

def get_pages(soup : BeautifulSoup, url : str) -> list:
    span = soup.find('span', {'class' : 's-pagination-strip'})
    last = span.find('span', {'class' : 's-pagination-item s-pagination-disabled'})
    num = int(last.text.strip())

    link = url + '&page={}'
    links = [link.format(str(x)) for x in range(1, num + 1)]
    
    return links

def scrape_data(pages):
    data = {
    'Name' : list(), 
    'Price' : list(), 
    'Ratings' : list(), 
    'Reviews' : list(), 
    'URL' : list() 
    }
    
    print(f'Total Pages {len(pages)}')
    
    for page in range(len(pages)):
        
        print(f'Page {page + 1}')
      
        while True:
            try:
                response = requests.get(pages[page], headers = random.choice(headers))
                response.raise_for_status() # Raises an HTTPError in case of an Error response code

                if response.status_code == 200:
                    break
                    
            except HTTPError:
                pass
              
        soup = BeautifulSoup(response.content, 'html.parser')
        
        grid = soup.find('div', {'class' :  's-main-slot s-result-list s-search-results sg-row'})
        cols = grid.find_all('div', {'data-component-type' : 's-search-result'})

        for col in cols:
            try:
                brand = col.find('h5', {'class' : 's-line-clamp-1'}).text.strip()
            except AttributeError:
                brand = None

            if brand == 'Nike': # Since only Nike Shoes are required 
                
                name = None
                price = None
                link = None
                rating = None
                review = None

                try:
                    a = col.find('a', {'class' : 'a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal'})
                    name = a.text.strip()
                except AttributeError:
                    pass

                try:
                    link = 'https://amazon.in' + a.get('href')
                except AttributeError:
                    pass

                try:   
                    div = col.find('div', {'class' : 'a-row a-size-small'})
                    rating = div.find('span', {'class' : 'a-size-base'}).text.strip()

                    if re.search('[.]', rating):
                        rating = float(rating)
                    else:
                        rating = None
                        
                    span = div.find_all('span')
                    rev = span[len(span) - 1].text.strip()

                    if re.search('\d', rev):
                        review = re.sub('[(),]', '', rev)
                        review = int(review)

                except AttributeError:
                    pass

                try:
                    price = col.find('span', {'class' : 'a-price-whole'}).text.strip()
                    price = re.sub('[,.]', '', price)
                    price = int(price)
                except AttributeError:
                    pass

                data['Name'].append(name)
                data['URL'].append(link)
                data['Ratings'].append(rating)
                data['Reviews'].append(review)
                data['Price'].append(price)

    df = pd.DataFrame(data)

    df.sort_values(by = 'Price', inplace = True)
    df.reset_index(inplace = True, drop = True)
  
    gender_sr = df['Name'].apply(lambda x : 'M' if 'Men' in x else 'F' if 'Women' in x else None)
    df.insert(1, 'Gender', gender_sr)
  
    return df 

def gen_text(df : pd.DataFrame) -> str: # Generating formatted text for Notification
    m_df = df[df['Gender'] == 'M']
    sorted_df = m_df.sort_values(by = 'Price').head(10)
    
    sorted_df.sort_values(by = 'Reviews', ascending = False, inplace = True)
    sorted_df.reset_index(inplace = True, drop = True)
    
    sorted_df.drop(columns = ['Reviews', 'Gender'], inplace = True)
  
    info = [x[1:] for x in sorted_df.itertuples()]
    sorted_df.drop_duplicates(['Name'], inplace = True)
    
    text = ''
    for name, price, rating, link in info:
        name = 'NAME: ' + name
        price = 'PRICE: ' + str(price)
        rating = 'RATING: ' + str(rating)
        link = 'URL: ' + link

        text += name + '\n' + price + '\n' + rating + '\n' + link + '\n\n'
        
    return text


def sns_publish(message : str):
    sns = boto3.client('sns')
    
    topic_arn = 'arn:aws:sns:ap-south-1:358867544823:filtered_shoes'
    response = sns.publish(
        TopicArn = topic_arn, 
        Message = message
    )
    
    return response


def lambda_handler(event = None, context = None): 
    url = 'https://www.amazon.in/s?k=nike+shoes&crid=29X54TW284P32&sprefix=nike+shoe%2Caps%2C278&ref=nb_sb_noss_1'

    while True:
        try:
            response = requests.get(url, headers = random.choice(headers))
            response.raise_for_status()
            if response.status_code == 200:
                break
        except HTTPError:
            pass

    soup = BeautifulSoup(response.content, 'html.parser')

    pages = get_pages(soup, url)
    df = scrape_data(pages)
    text = gen_text(df)

    sns_publish(text)
