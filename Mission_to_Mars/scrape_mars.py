
# coding: utf-8

# Dependencies
import pandas as pd
from bs4 import BeautifulSoup
import pymongo
from splinter import Browser
import requests
import time

executable_path = {'executable_path': 'chromedriver.exe'}
browser = Browser('chrome', **executable_path, headless=False)

def scrape():
    final_data = {}
    output = marsNews()
    final_data["mars_news"] = output[0]
    final_data["mars_paragraph"] = output[1]
    final_data["mars_image"] = marsImage()
    final_data["mars_weather"] = marsWeather()
    final_data["facts_table"] = marsFacts()
    final_data["mars_hemisphere"] = marsHemisphere()

    return final_data

def marsNews():
# # Mars News
# url
    url = "https://mars.nasa.gov/news/"
    browser.visit(url)
    html_code = browser.html
    soup = BeautifulSoup(html_code, "html.parser")
    news_title = soup.find('div', class_="bottom_gradient").text
    news_p = soup.find('div', class_="rollover_description_inner").text
    output = [news_title,news_p]
    return output

def marsImage():
# # Mars Featured Image URL
# Featured Image URL
    image_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(image_url)
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")
    image = soup.find("img", class_="thumb")["src"]
    mars_image = "https://www.jpl.nasa.gov" + image
    return mars_image

def marsWeather():
# # Mars Weather
    marsweather_url = "https://twitter.com/marswxreport?lang=en"
    browser.visit(marsweather_url)
    weather_html = browser.html
    soup = BeautifulSoup(weather_html, 'html.parser')
    mars_weather = soup.find('p', class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text").text
    return mars_weather

def marsFacts():
# # Mars Facts
    facts_url = "https://space-facts.com/mars/"
    browser.visit(facts_url)
    mars_data = pd.read_html(facts_url)
    mars_data = pd.DataFrame(mars_data[0])
    mars_facts = mars_data.to_html(header = False, index = False)
    return mars_facts

def marsHemisphere():
# # Mars Hemispheres
    usgs_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(usgs_url)
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")
    mars_hemisphere = []

    results = soup.find("div", class_ = "result-list" )
    hemispheres = results.find_all("div", class_="item")

    for hemisphere in hemispheres:
        title = hemisphere.find("h3").text
        title = title.replace("Enhanced", "")
        end_link = hemisphere.find("a")["href"]
        image_link = "https://astrogeology.usgs.gov/" + end_link    
        browser.visit(image_link)
        html = browser.html
        soup = BeautifulSoup(html, "html.parser")
        downloads = soup.find("div", class_="downloads")
        image_url = downloads.find("a")["href"]
        mars_hemisphere.append({"title": title, "img_url": image_url})
    return mars_hemisphere
