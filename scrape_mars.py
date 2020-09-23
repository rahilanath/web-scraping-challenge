# dependencies
from splinter import Browser
from bs4 import BeautifulSoup as bs
import pandas as pd
import time

# def browser
def init_browser():
    executable_path = {"executable_path": "C:/webdrivers/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)

# scrape_mars function
def scrape_mars():
    # init browser
    browser = init_browser()

    try:
        # NASA Mars News Scrape 
        url = 'https://mars.nasa.gov/news.html'
        browser.visit(url)

        # wait for page load
        time.sleep(2)

        # html/soup scrape
        html = browser.html
        soup = bs(html, 'html.parser')

        # get first news article
        news_article = soup.find('div', class_='list_text')

        # get title/paragraph
        news_title = news_article.find('div', class_='content_title')
        news_paragraph = news_article.find('div', class_='article_teaser_body')
        results = {'news_title': news_title.text, 'news_paragraph': news_paragraph.text}
        
        # JPL Mars Space Images - Featured Image
        url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
        browser.visit(url)

        # wait for page load
        time.sleep(2)

        # html/soup scrape
        html = browser.html
        soup = bs(html, 'html.parser')

        # soup find element and slice style string for url
        image = soup.find('article')['style']
        featured_image_url = image[23:-3]
        results['Featured Image'] = featured_image_url

        # Mars Facts
        url = 'https://space-facts.com/mars/'

        # read_html table and preview
        tables = pd.read_html(url)

        # slice into single dataframe and convert to HTML table string
        df = tables[0]
        html_table = df.to_html(header=None, index=False)
        results['html_table'] = html_table 

        # Mars Hemispheres
        url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
        browser.visit(url)

        # wait for page load
        time.sleep(2)

        # html/soup
        html = browser.html
        soup = bs(html, 'html.parser')

        # base_url/url_list
        base_url = 'https://astrogeology.usgs.gov'
        href_list = []

        # fill href_list with distinct individual urls
        links = soup.find_all('a', class_='itemLink product-item')
        for link in links:
            if link['href'] not in href_list:
                href_list.append(link['href'])

        # hemisphere list
        hemispheres = []

        # html/soup/loop through each url
        for href in href_list:
            browser.visit(base_url + href)
            html = browser.html
            soup = bs(html, 'html.parser')
            hemisphere_dict = {}
            hemisphere_dict['title'] = soup.find('h2', class_='title').text[0:-9]
            hemisphere_dict['img_url'] = soup.find('a', text='Sample')['href']
            hemispheres.append(hemisphere_dict)
        
        results['hemispheres'] = hemispheres
    
    except:
        browser.quit()

    # Quit browser because web scraping is done.
    browser.quit()

    # Return results
    return results