#import modules
import pandas as pd
from splinter import Browser
from bs4 import BeautifulSoup
import requests
import time

#this function scrapes various mars websites for useful data to be used for a website
def scrape():
    #initialize dictionary that we will store all useful data into
    mars_final_data = {}

    # URL of page to be scraped
    url = 'https://mars.nasa.gov/news/'

    # Retrieve page with the requests module
    response = requests.get(url)

    # Create BeautifulSoup object; parse with 'html.parser'
    soup = BeautifulSoup(response.text, 'html.parser')

    #STEP 1: SCRAPING

    #Scrape the NASA Mars News Site and collect the latest News Title and Paragraph Text.
    #Assign the text to variables that you can reference later.

    #title of first article
    title = soup.find('div', class_="content_title").a.text
    #clean indents
    title = title.replace('\n','')
    #store to dictionary
    mars_final_data['title'] = title

    #paragraph explanation
    paragraph_text = soup.find('div', class_="image_and_description_container").find('div',class_='rollover_description_inner').text
    #clean indents
    paragraph_text = paragraph_text.replace('\n', '')
    #store to dictionary
    mars_final_data['paragraph_text'] = paragraph_text


    #JPL Mars Space Images - Featured Image

    #execute chromedriver
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)

    browser.visit('https://www.jpl.nasa.gov/spaceimages/')
    browser.click_link_by_partial_text('FULL IMAGE')
    time.sleep(2)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    featured_image_url = f"https://www.jpl.nasa.gov/{soup.find('a', class_='ready').img['src']}"
    #store to dictionary
    mars_final_data['featured_image_url'] = featured_image_url

    #MARS WEATHER
    #Visit the Mars Weather twitter account and scrape the latest Mars weather tweet from the page
    #Save the tweet text for the weather report as a variable called mars_weather

    #go to web page in same browser
    browser.visit('https://twitter.com/marswxreport')

    #get html code via beautifulsoup
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    #get the latest tweet text
    mars_weather = soup.find('p', class_='tweet-text').text
    #store data to dictionary
    mars_final_data['mars_weather'] = mars_weather

    #MARS FACTS
    #visit the Mars Facts webpage here and use Pandas to scrape the table containing facts about the planet
    tables = pd.read_html('https://space-facts.com/mars/')

    #save as dataframe and create columns
    df = tables[0]
    df.columns = ['Mars Fact','Value']

    #convert to html string
    html_table = df.to_html()
    #clean up table by stripping unwanted new lines
    html_table = html_table.replace('\n', '')
    #store table to dictionary
    mars_final_data['mars_facts_table'] = html_table

    #MARS HEMISPHERE
    #go to web page in same browser
    browser.visit('https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars')

    #get html code via beautifulsoup
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    #get names of all the links
    #retrieve the parent divs for all links
    links = soup.find_all('div', class_='item')

    hemisphere_image_urls = []

    #for loop to click on each planet link on home page and grab image url
    #must have browser open to astrogeology science center page
    for link in links:
        #get names of links (which are our titles)
        title = link.find('div', class_='description').a.text
        
        #click on link for each planet
        browser.click_link_by_partial_text(f"{title}")
        #get html code via beautifulsoup
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')
        #save image url (jpg)
        image_url = soup.find('div', class_='downloads').li.a['href']
        
        #back to home page
        browser.back()
        
        #save values to dictionary
        post = {'title': title, 'image_url': image_url}
        #append to list
        hemisphere_image_urls.append(post)
    
    #quit out of browser
    browser.quit()

    mars_final_data['image_urls'] = hemisphere_image_urls
    
    #return dictionary
    return(mars_final_data)