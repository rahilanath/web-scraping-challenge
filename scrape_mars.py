# Dependencies
import os
import pandas as pd

# Dependencies for Beautiful Soup
import requests
from bs4 import BeautifulSoup as bs

# Dependencies for Splinter
from splinter import Browser

# NASA Mars News Scrape 
# URL/get/soup
url = "https://mars.nasa.gov/news.html"
html = requests.get(url).text
soup = bs(html, 'lxml')

# print title
news_title = soup.title.text[8::]
print(news_title)

# print paragraph
news_paragraphs = soup.find_all('p')
for paragraph in news_paragraphs:
    print(paragraph.text)

# JPL Mars Space Images - Featured Image
# executable/URL/browser
executable_path = {'executable_path': 'chromedriver.exe'}
browser = Browser('chrome', **executable_path, headless=False)
url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'

# open browser
browser.visit(url)

# html/soup
html = browser.html
soup = bs(html, 'html.parser')

# soup find element and slice style string for url
image = soup.find('article')['style']
featured_image_url = image[23:-3]

# print image url
print(featured_image_url)

# Mars Facts
# url
url = 'https://space-facts.com/mars/'

# read_html table and preview
tables = pd.read_html(url)

# slice into single dataframe and convert to HTML table string
df = tables[0]
html_table = df.to_html(header=None, index=False)

# Mars Hemispheres
# url/visit
url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
browser.visit(url)

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

# Quit browser because web scraping is done.
browser.quit()

