from bs4 import BeautifulSoup as soup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import urllib.parse
import json
import time

BASE_URL = "https://www.bbc.com"
TARGET_URL = urllib.parse.urljoin(BASE_URL, "/news")

# The maximum number of blog posts to crawl
MAX_BLOG_LIMIT = 10

class Crawler_BBC():
    def __init__(self, driver: webdriver) -> None:
        self.driver = driver
        self.selected_blogs = {
            "titles": [],
            "urls": []
        }


    def  __search_topic(self, topic: str):
        self.driver.get(BASE_URL)
        WebDriverWait(self.driver, 10).until(EC.title_contains("BBC"))

        # open up side bar to show search bar
        self.driver.find_element(By.CLASS_NAME, "sc-8a068d35-3.kvafkS").click()

        # input topic to be searched in search bar
        search_bar = self.driver.find_element(By.CLASS_NAME, "sc-e1a87ea7-1.iARAvt")
        search_bar.send_keys(topic)

        # click search button
        search_submit_button = self.driver.find_element(By.CLASS_NAME, "sc-f6c53a81-2.sc-f6c53a81-3.dyeOnJ.dQfGZm")
        search_submit_button.click()

        # wait for the page to load
        WebDriverWait(self.driver, 10).until(EC.title_contains("BBC"))


    def __select_blog_in_search_page(self):
        raw_blogs = self.driver.find_element(By.ID, "main-content").get_attribute("innerHTML")
        # to prevent dynamic class value of different articles generated by backend, use bs4 to trace tag
        raw_blogs = soup(raw_blogs, features="html.parser")
        raw_blogs = raw_blogs.findAll("div", attrs={"data-testid": "liverpool-card"}, recursive=True)

        if not raw_blogs:
            return

        for raw_blog in raw_blogs:
            title = raw_blog.find('h2', attrs={"data-testid": "card-headline"}, recursive=True).text.replace('\n', '').lower()
            # prevent crawl duplicate blog from different source
            if not title in self.selected_blogs.get('titles'):
                # skip blogs that are not news
                try:
                    url = raw_blog.find('a', attrs={"data-testid": "internal-link"}, recursive=True)["href"]
                except Exception:
                    continue
                # skip blogs that are not news
                if not "news" in url:
                    continue
                self.selected_blogs["titles"].append(title)
                # bbc's href links only contains path 
                if not urllib.parse.urlparse(url).netloc:
                    url = urllib.parse.urljoin(BASE_URL, url)
                self.selected_blogs["urls"].append(url)

        if len(self.selected_blogs["urls"]) < MAX_BLOG_LIMIT:
            # go to next page
            next_page_btn = self.driver.find_element(By.CSS_SELECTOR, "button[data-testid=\"pagination-next-button\"]")
            try:
                next_page_btn.click()
                time.sleep(2)
                self.__select_blog_in_search_page()
            except:
                import traceback
                print(traceback.format_exc())
        else:
            self.selected_blogs["titles"] = self.selected_blogs["titles"][:MAX_BLOG_LIMIT]
            self.selected_blogs["urls"] = self.selected_blogs["urls"][:MAX_BLOG_LIMIT]


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
        file = open(f"./saved_articles/BBC_{blog_title}.json", 'w')
        json.dump(blog, file)
        file.close()
        time.sleep(2)


    def search_and_save(self, topic: str):
        self.__search_topic(topic)
        self.__select_blog_in_search_page()
        url_list = self.selected_blogs.get("urls", [])
        for url in url_list:
            self.__get_and_save_blog(url)


    def direct_save(self, url: str):
        self.__get_and_save_blog(url)


    def test(self):
        try:
            self.search_and_save("test")
            # self.direct_save("https://www.bbc.com/news/articles/c2edewgv2kpo")
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
    crawler = Crawler_BBC(driver)
    crawler.test()