from bs4 import BeautifulSoup as soup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import urllib.parse
import json
import time
import re

BASE_URL = "https://english.news.cn"
XINHUA_OVERSEAS_REGIONS = ["asiapacific", "europe", "africa", "northamerica"]

# The maximum number of blog posts to crawl
MAX_BLOG_LIMIT = 15

class Crawler_NewsCN():
    def __init__(self, driver: webdriver) -> None:
        self.driver = driver
        self.selected_blogs = {
            "titles": [],
            "urls": []
        }


    def  __search_topic(self, topic: str):
        self.driver.get(BASE_URL)
        WebDriverWait(self.driver, 10).until(EC.title_contains("Xinhua"))

        # input topic to be searched in search bar
        search_bar = self.driver.find_element(By.CLASS_NAME, "search-input")
        search_bar.send_keys(topic)

        # click search button
        search_submit_button = self.driver.find_element(By.ID, "searchSubmit")
        search_submit_button.click()

        # close home window and switch to new window
        self.driver.close()
        self.driver.switch_to.window(self.driver.window_handles[0])
        WebDriverWait(self.driver, 10).until(EC.title_contains("Xinhua research"))


    def __select_blog_in_search_page(self):
        raw_blogs = self.driver.find_element(By.CLASS_NAME, "content").get_attribute("innerHTML")
        raw_blogs = soup(raw_blogs, features="html.parser")
        raw_blogs = raw_blogs.findAll("div", attrs={"class": "item"}, recursive=True)

        if not raw_blogs:
            return

        for raw_blog in raw_blogs:
            title = raw_blog.find('div', class_="title").text.replace('\n', '').replace(' ', '').lower()
            # prevent crawl duplicate blog from different source
            if not title in self.selected_blogs.get('titles'):
                self.selected_blogs["titles"].append(title)
                self.selected_blogs["urls"].append(raw_blog.find('a')["href"])

        if len(self.selected_blogs["urls"]) < MAX_BLOG_LIMIT:
            # go to next page
            next_page_btn = self.driver.find_element(By.CLASS_NAME, "ant-pagination-next")
            if next_page_btn.get_attribute("aria-disabled") != "true":
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

        # print(self.selected_blogs["urls"])


    def __retrieve_overseas_blog(self) -> dict:
        blog_container = self.driver.find_element(By.CLASS_NAME, "main.clearfix")
        blog_title = blog_container.find_element(By.CLASS_NAME, "Btitle").text
        blog_meta = blog_container.find_element(By.CLASS_NAME, "wzzy").text
        blog_content = blog_container.find_element(By.ID, "detailContent").text
        
        return {
            "title": blog_title,
            "meta": blog_meta,
            "content": blog_content
        }


    def __retrieve_china_blog(self) -> dict:
        blog_container = self.driver.find_element(By.CLASS_NAME, "conBox")
        blog_title_meta_container = blog_container.find_element(By.CLASS_NAME, "conTop")
        blog_title = blog_title_meta_container.find_element(By.TAG_NAME, "h1").text
        blog_meta = blog_title_meta_container.find_element(By.CLASS_NAME, "infoBox.clearfix").text
        blog_content_container = blog_container.find_element(By.CLASS_NAME, "conLeft")
        blog_content = blog_content_container.find_element(By.ID, "detailContent").text

        return {
            "title": blog_title,
            "meta": blog_meta,
            "content": blog_content
        }


    def __get_and_save_blog(self, url: str):
        self.driver.get(url)
        WebDriverWait(self.driver, 10).until(EC.title_contains("Xinhua"))
        region_code = urllib.parse.urlparse(url).path.split('/')[1]
        if region_code in XINHUA_OVERSEAS_REGIONS:
            blog = self.__retrieve_overseas_blog()
        else:
            blog = self.__retrieve_china_blog()
        blog_title = blog.get("title", "")
        print(blog_title)

        # Remove invalid char in file_path_name on Windows
        invalid_chars_pattern = r'[\\/:*?"<>|]'
        blog_title = re.sub(invalid_chars_pattern, '', blog_title)

        file = open(f"./saved_articles/Xinhua_{blog_title}.json", 'w')
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
            self.search_and_save("china")
            # self.direct_save("<an url>")
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
    crawler = Crawler_NewsCN(driver)
    crawler.test()
