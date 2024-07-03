import pandas as pd

from selenium import webdriver
from selenium.webdriver.common.by import By


def write_csv(data):
    df = pd.DataFrame(data)
    df.to_csv('news_selenium.csv', index=False, header=False)


def parcer_selenium():
    driver = webdriver.Chrome()
    driver.get('https://rbc.ru/')
    page = driver.find_elements(By.CLASS_NAME, "main__inner l-col-center")

    driver.quit()


def main():
    ...


if __name__ == '__main__':
    parcer_selenium()
