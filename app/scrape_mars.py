# Import Splinter, BeautifulSoup, and Pandas
from splinter import Browser, browser
#from bs4 import BeautifulSoup as soup
import pandas as pd
import datetime as dt
from webdriver_manager.chrome import ChromeDriverManager
import time
from bs4 import BeautifulSoup as bs

executable_path = {'executable_path': ChromeDriverManager().install()}


def scrape_all():
    # Initiate headless driver for deployment
    browser = Browser('chrome', **executable_path, headless=False)


    news_title, news_paragraph = mars_news(browser)

    # Run all scraping functions and store results in a dictionary
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "hemispheres": hemispheres_bg(),
        "last_modified": dt.datetime.now()
    }

    # Stop webdriver and return data
    browser.quit()
    return data

def mars_news(browser):
    # Visit the Mars news site
    url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    browser.visit(url)

    # Convert the browser html to a soup object
    html = browser.html
    soup = bs(html, 'html.parser')

    #Use the parent element to find the first a tag and save it as `news_title`
    element = soup.select_one('div.list_text')
    element.find('div', class_='content_title')
    news_title = element.find('div', class_='content_title').get_text()
    #news_title
    # Use the parent element to find the paragraph text
    news_p = element.find('div', class_='article_teaser_body').get_text()
    #news_p

    return news_title, news_p

def featured_image(browser):
    # Visit URL
    jpl_url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'
    browser.visit(jpl_url)

    # Find and click the full image button use .click
    variable_button = browser.find_by_tag('button')[1]
    variable_button.click()

    # Parse the resulting html with soup
    html_page = browser.html
    html_soup = bs(html_page, 'html.parser')
    #print(html_soup)

    # find the relative image url
    featured_image_url = html_soup.find('img', class_ = 'fancybox-image').get('src')
    #featured_image_url

    # Use the base url (prefix webpage) to create an absolute url
    jpeg_html = ('https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/' + featured_image_url)
    #print(jpeg_html)
    
    return jpeg_html

def mars_facts():
    mars_df = pd.read_html('https://space-facts.com/mars/')[0]
    mars_df.columns = ['Description', 'Mars']
    mars_df.set_index('Description', inplace=True)
    #mars_df.style.set_caption('Mars Facts')
    
    return mars_df.to_html(classes="table table-striped")
  
def hemispheres_bg(): 
    browser = Browser('chrome', **executable_path, headless=False)
    browser.visit('https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars')

    hemisphere_image_urls = []

    for i in range (4):
        #looks like an active person is using the webpage and not look like scraping
        #time.sleep(15)
        images=browser.find_by_tag('h3')
        images[i].click()
        html=browser.html
        soup=bs(html, 'html.parser')
        #<img class="wide-image" src="/cache/images/f5e372a36edfa389625da6d0cc25d905_cerberus_enhanced.tif_full.jpg">
        ending_url = soup.find('img', class_ = 'wide-image')['src']
        #<h2 class="title">Cerberus Hemisphere Enhanced</h2>
        image_title = soup.find('h2', class_='title').text
        image_url = f'https://astrogeology.usgs.gov{ending_url}'
        image_dict = {'title': image_title, 'image_url': image_url}
        hemisphere_image_urls.append(image_dict)
        browser.back()

    browser.quit()
    
    return hemisphere_image_urls

if __name__ == "__main__":

    # If running as script, print scraped data
    print(scrape_all())
    #print(hemispheres_bg())