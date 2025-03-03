from selenium import webdriver
from bs4 import BeautifulSoup

def scrape_example(url):
    driver = webdriver.Chrome()
    driver.get(url)
    soup = BeautifulSoup(driver.page_source, "html.parser")
    driver.quit()
    return soup.title.text

if __name__ == "__main__":
    print(scrape_example("https://www.wikipedia.org/"))
