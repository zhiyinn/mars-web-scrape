#import dependencies
from bs4 import BeautifulSoup as bs
from splinter import Browser
import os
import pandas as pd
import time
import pymongo

#NASA News 
#access directory
executable_path = {'executable_path': 'chromedriver.exe'}
browser = Browser('chrome', **executable_path, headless=False)

#access webpage
url = "https://mars.nasa.gov/news/"
browser.visit(url)

#find title and associated text
news_title = soup.find("div",class_="content_title").text
news_p = soup.find("div", class_="article_teaser_body").text
print(f"{news_title}")
print(f"{news_p}")

#access Mars image webpage
url_image = "https://www.jpl.nasa.gov/spaceimages/?search=&category=featured#submit"
browser.visit(url_image)

#write webpage to html
html = browser.html
soup = bs(html,"html.parser")
print(soup.body.prettify())

# get background image url from style tag 
featured_image_url = soup.find('article')['style'].replace('background-image: url(','').replace(');', '')[1:-1]
featured_image_url

# website Url 
main_url = 'https://www.jpl.nasa.gov'

# concatenated website url with scraped route
featured_image_url = main_url + featured_image_url

# featured image URL
featured_image_url

# access Mars Weather Twitter URL
weather_url = 'https://twitter.com/marswxreport?lang=en'
browser.visit(weather_url)

#write webpage to html
html = browser.html
soup = bs(html,"html.parser")
print(soup.body.prettify())

tweet = soup.find('p', class_='TweetTextSize TweetTextSize--normal js-tweet-text tweet-text').text

#scrape Mars facts using Pandas
#convert pandas table to html table string.
request_mars_space_facts = requests.get("https://space-facts.com/mars/")

#use pandas to scrape html table data
mars_space_table_read = pd.read_html(request_mars_space_facts.text)
df = mars_space_table_read[0]

#set the index to the titles of each statistic/value
df.set_index(0, inplace=True)
mars_data_df = df

#convert new pandas df to html, replace "\n" to get html code
mars_data_html = mars_data_df.to_html()
mars_data_html.replace('\n', '')
mars_data_df.to_html('facts.html')

mars_hemisphere = []

products = soup.find("div", class_ = "result-list" )
hemispheres = products.find_all("div", class_="item")

for hemisphere in hemispheres:
    title = hemisphere.find("h3").text
    title = title.replace("Enhanced", "")
    end_link = hemisphere.find("a")["href"]
    image_link = "https://astrogeology.usgs.gov/" + end_link    
    browser.visit(image_link)
    html = browser.html
    soup=bs(html, "html.parser")
    downloads = soup.find("div", class_="downloads")
    image_url = downloads.find("a")["href"]
    mars_hemisphere.append({"title": title, "img_url": image_url})

# initialize PyMongo
conn = 'mongodb://localhost:27017'
client = pymongo.MongoClient(conn)

# set database and collection
db = client.mars_db
collection = db.mars_info

# dictionary to push
post = {
    'news_title': news_title,
    'news_p': news_p,
    'featured_image': featured_image_url,
    'mars_weather': tweet,
    'hemispheres': image_url
}

# insert dictionary of updated data into MongoDB as a document 
collection.delete_many({})
collection.insert_one(post)
