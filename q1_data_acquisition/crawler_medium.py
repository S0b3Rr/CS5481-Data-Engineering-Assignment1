from bs4 import BeautifulSoup as soup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import urllib.parse
import json
import time

BASE_URL = "https://www.medium.com"

# The maximum number of blog posts to crawl
MAX_BLOG_LIMIT = 10

class Crawler_Medium():
    def __init__(self, driver: webdriver) -> None:
        self.driver = driver
        self.selected_blogs = {
            "titles": [],
            "urls": []
        }


    def  __search_topic(self, topic: str):
        # Not implemented because some of the articles in Medium can only be viewed after logging in.
        # If you want to implement the login function, 
        # you need to crack oauth (Use selenium to simulate the user login process) 
        # or access the email api, 
        # which is beyond the scope of this assignment, I believe.
        raise NotImplementedError()


    def __select_blog_in_search_page(self):
        # Not implemented because some of the articles in Medium can only be viewed after logging in.
        raise NotImplementedError()


    def __retrieve_blog(self) -> dict:
        blog_container = self.driver.find_element(By.ID, "main-content")
        raw_blog = soup(blog_container.get_attribute("innerHTML"), features="html.parser")

        blog_title = raw_blog.find('div', attrs={"data-component": "headline-block"}, recursive=True).text
        blog_time = raw_blog.find('time', recursive=True).text
        blog_contributor = raw_blog.find('div', attrs={"data-testid": "byline-new-contributors"}, recursive=True).text
        blog_meta = {"time": blog_time, "author": blog_contributor}
        blog_content_blocks = raw_blog.find_all('div', attrs={"data-component": "text-block"}, recursive=True)

        blog_content = ""

        for block in blog_content_blocks:
            blog_content += block.text
        
        return {
            "title": blog_title,
            "meta": blog_meta,
            "content": blog_content
        }


    def __get_and_save_blog(self, url: str):
        self.driver.get(url)
        time.sleep(3)
        
        blog = self.__retrieve_blog()

        blog_title = blog.get("title", "")
        print(blog_title)
        file = open(f"./saved_articles/Medium_{blog_title}.json", 'w')
        json.dump(blog, file)
        file.close()
        time.sleep(2)


    def search_and_save(self, topic: str):
        # Not implemented because some of the articles in Medium can only be viewed after logging in.
        raise NotImplementedError()


    def direct_save(self, url: str):
        self.__get_and_save_blog(url)


    def test(self):
        articles = []
        try:
            self.direct_save("")
        except Exception as e:
            import traceback
            print(traceback.format_exc())
        finally:
            self.driver.quit()



if __name__ == "__main__":
    from selenium.webdriver.chrome.options import Options
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(options=chrome_options)
    crawler = Crawler_Medium(driver)
    crawler.test()