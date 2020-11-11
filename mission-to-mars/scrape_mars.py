from splinter import Browser
from bs4 import BeautifulSoup as bs
import pandas as pd

def init_browser():
    executable_path = {"executable_path": r"C:/Users/willi/.wdm/drivers/chromedriver/win32/86.0.4240.22/chromedriver.exe"}
    return Browser("chrome", **executable_path, headless=False)

def scrape():
    browser = init_browser()
    mars_dict ={}

    mars_url = 'https://mars.nasa.gov/news/'
    browser.visit(mars_url)
    html = browser.html
    soup = bs(html, 'html.parser')
    article = soup.find('li', class_='slide')
    news_title = article.find('div', class_='content_title').text
    news_p = article.find('div', class_='article_teaser_body').text

    jpl_url = 'https://www.jpl.nasa.gov'
    ft_image_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(ft_image_url)
    html2 = browser.html
    soup2 = bs(html2, 'html.parser')
    ftimage_url  = soup2.find('article')['style'].replace('background-image: url(','').replace(');', '')[1:-1]
    ftimage_url = jpl_url + ftimage_url

    mars_facts_url = 'https://space-facts.com/mars/'
    tables = pd.read_html(mars_facts_url)
    mars_df = tables[2]
    mars_df.columns = ["Description", "Value"]
    mars_facts_html = mars_df.to_html()
    mars_facts_html=mars_facts_html.replace('\n', '')
    
    
    main_url = 'https://astrogeology.usgs.gov'
    hemi_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(hemi_url)
    hemi_html = browser.html
    soup3 = bs(hemi_html, 'html.parser')

    mars_hemi = soup3.find('div', class_='collapsible results')
    mars_hemi = mars_hemi.find_all('div', class_='item')
    hemi_img_urls = []
    
    for hemi in mars_hemi:
        hemisphere = hemi.find('div', class_="description")
        title = hemisphere.h3.text
        hemi_link = hemisphere.a["href"]    
        browser.visit(main_url + hemi_link)
        image_html = browser.html
        image_soup = bs(image_html, 'html.parser')
        image_link = image_soup.find('div', class_='downloads')
        image_url = image_link.find('li').a['href']
        image_dict = {}
        image_dict['title'] = title
        image_dict['img_url'] = image_url
    
        hemi_img_urls.append(image_dict)

    mars_dict = {
        "news_title": news_title,
        "news_p": news_p,
        "featured_image_url": ftimage_url,
        "fact_table": str(mars_facts_html),
        "hemisphere_images": hemi_img_urls
    }

    browser.quit()
    return mars_dict