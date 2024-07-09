import random

import pandas as pd
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By

COUNT_CATEGORIES_FOR_PARSING = 5
COUNT_NEWS_FOR_PARSING = 2
NEWS_URL = 'https://ria.ru/'


def write_csv(data):
    df = pd.DataFrame(data)
    df.to_csv('news_selenium.csv', index=False, header=False, encoding='CP1251')


def parser_selenium():
    news_selenium = []
    driver = webdriver.Chrome()
    driver.get(NEWS_URL)
    lenta = driver.find_element(By.CSS_SELECTOR, "div.the-in-carousel__stage")
    categories = lenta.find_elements(By.CLASS_NAME, "the-in-carousel__item")
    categories_links = [c.find_element(By.CLASS_NAME, 'cell-extension__item-link').get_attribute('href')
                        for c in categories]
    for cat_link in categories_links[:COUNT_CATEGORIES_FOR_PARSING]:
        driver.execute_script(f"window.open('{cat_link}');")
        driver.switch_to.window(driver.window_handles[1])
        category = driver.find_element(By.CLASS_NAME, 'tag-input__tag-text').text

        post_links = [n.find_element(By.CSS_SELECTOR, 'a').get_attribute('href')
                      for n in driver.find_elements(By.CLASS_NAME, 'list-item')]

        for post_link in post_links[:COUNT_NEWS_FOR_PARSING]:
            driver.execute_script(f"window.open('{post_link}');")
            driver.switch_to.window(driver.window_handles[2])

            short_description = driver.find_elements(By.CLASS_NAME, 'article__second-title')
            short_description = short_description[0].text if short_description else ''

            headline = driver.find_element(By.CLASS_NAME, 'article__title').text
            news_selenium.append([
                category,
                headline,
                post_link,
                short_description
            ])
            driver.close()
            driver.switch_to.window(driver.window_handles[1])

        driver.close()
        driver.switch_to.window(driver.window_handles[0])

    driver.quit()

    write_csv(news_selenium)


def parser_requests():
    news_selenium = []
    features = 'html.parser'
    response = requests.get(NEWS_URL)
    soup = BeautifulSoup(response.content, features)
    lenta = soup.find_all(class_='cell-extension__item-link color-font-hover-only')
    for l in lenta[:COUNT_CATEGORIES_FOR_PARSING]:
        cat_link = f"https://ria.ru{l.get('href')}"
        category = l.find('span', class_='cell-extension__item-title').text
        response = requests.get(cat_link)
        soup = BeautifulSoup(response.content, features)
        post_links = soup.find_all('span', class_='schema_org')
        post_links = [ps.find('a').get('href') for ps in post_links]
        for post_link in post_links[:COUNT_NEWS_FOR_PARSING]:
            response = requests.get(post_link)
            soup = BeautifulSoup(response.content, features)
            headline = soup.find(class_='article__title').text
            short_description = soup.find(class_='article__second-title')
            short_description = short_description.text if short_description else ''

            news_selenium.append([
                category,
                headline,
                post_link,
                short_description
            ])

    write_csv(news_selenium)


def run_parser():
    if random.random() > 0.5:
        parser_selenium()
    else:
        parser_requests()


if __name__ == '__main__':
    ...
