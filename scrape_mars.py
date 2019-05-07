#!/usr/bin/env python
# coding: utf-8

import requests
from bs4 import BeautifulSoup
import pandas as pd
from splinter import Browser
from selenium import webdriver

# def init_browser():
    # executable_path = {"executable_path": "chromedriver.exe"}
    # return Browser("chrome", **executable_path, headless=False)
dict = {}
def scrape():
    url = 'https://mars.nasa.gov/news/'
    response = requests.get(url)
    soup = BeautifulSoup(response.text,'html.parser')
    news_title = soup.find('div', class_='content_title').text.strip()
    news_p = soup.find('div',class_='rollover_description_inner').text.strip()
    dict.update({'news_title':news_title})
    dict.update({'news_p':news_p})


    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    browser= Browser("chrome", **executable_path, headless=False)
    galaxy_images = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(galaxy_images)
    html = browser.html
    soup2 = BeautifulSoup(html,'html.parser')
    featured  = soup2.find('article',class_='carousel_item')['style'][23:-3]
    jpl = 'https://www.jpl.nasa.gov'
    furl = jpl + featured
    dict.update({'featured_image':furl})

    twitterurl = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(twitterurl)
    response2 = requests.get(twitterurl)
    soup = BeautifulSoup(response2.text,'html.parser')
    mars_weather = soup.find('div',class_='js-tweet-text-container').text.strip()
    dict.update({'mars_weather':mars_weather})

    mars_facts_url = 'https://space-facts.com/mars/'
    facts = pd.read_html(mars_facts_url)
    mars_df = facts[0]
    mars_df.columns=['Description', 'Value']
    mars_df['Description'] = mars_df['Description'].str[0:-1]
    mars_df = mars_df.set_index('Description')
    dict.update({'mars_df':mars_df})

    hemi_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(hemi_url)
    html=browser.html
    soup3 = BeautifulSoup(html,'html.parser')
    hemi_items = soup3.find_all('div', class_='item')
    hemi_urls_list = []
    hemispheres_url = 'https://astrogeology.usgs.gov'

    for i in hemi_items:
        title = i.find('h3').text
        partial_img_url = i.find('a', class_='itemLink product-item')['href']
        executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
        browser= Browser("chrome", **executable_path, headless=False)
        browser.visit(hemispheres_url + partial_img_url)
        partial_img_html = browser.html
        soup = BeautifulSoup(partial_img_html, 'html.parser')
        img_url = hemispheres_url + soup.find('img', class_='wide-image')['src']
        hemi_urls_list.append({"title" : title, "img_url" : img_url})
        dict.update({'hemi_urls':hemi_urls_list})
        browser.quit()

    print(dict['mars_df'])
