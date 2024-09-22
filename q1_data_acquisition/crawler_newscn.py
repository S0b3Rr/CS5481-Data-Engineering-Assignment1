from bs4 import BeautifulSoup as soup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import urllib.parse
import json

BASE_URL = "https://english.news.cn"
XINHUA_OVERSEAS_REGIONS = ["asiapacific", "europe", "africa", "northamerica"]

# The maximum number of blog posts to crawl
MAX_BLOG_LIMIT = 10

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
            # if next_page_btn.get_attribute("aria-disabled") != "true":
            if next_page_btn.is_enabled():
                next_page_btn.click()
                self.__select_blog_in_search_page()
        else:
            self.selected_blogs["titles"] = self.selected_blogs["titles"][:MAX_BLOG_LIMIT]
            self.selected_blogs["urls"] = self.selected_blogs["urls"][:MAX_BLOG_LIMIT]


    def __retrieve_overseas_blog(self) -> dict:
        blog_container = driver.find_element(By.CLASS_NAME, "main.clearfix")
        blog_title = blog_container.find_element(By.CLASS_NAME, "Btitle").text
        blog_meta = blog_container.find_element(By.CLASS_NAME, "wzzy").text
        blog_content = blog_container.find_element(By.ID, "detailContent").text
        
        return {
            "title": blog_title,
            "meta": blog_meta,
            "content": blog_content
        }


    def __retrieve_china_blog(self) -> dict:
        blog_container = driver.find_element(By.CLASS_NAME, "conBox")
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

        file = open(f"./saved_articals/Xinhua_{blog_title}.json", 'w')
        json.dump(blog, file)
        file.close()
        self.driver.close()


    def test(self):
        try:
            # self.__search_topic("food safety")
            # self.__select_blog_in_search_page()
            # self.__get_and_save_blog()
            self.__get_and_save_blog("https://english.news.cn/20240921/0c4426d134e94fb18d4045d53479ca78/c.html")
        except Exception as e:
            import traceback
            print(traceback.format_exc())
            print(e)
        # print(self.selected_blogs)
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


    markup = '''
<div class="item">
 <div class="title">
  <a href="https://english.news.cn/asiapacific/20240423/516d81af8f0f47e086876ad6e369d66b/c.html" rel="noreferrer" target="_blank">
   Indian
   <font color="red">
    food
   </font>
   <font color="red">
    safety
   </font>
   regulator to check spice quality after Hong Kong, Singapore raise concern
  </a>
 </div>
 <div class="brief">
  <div class="text">
   <div class="abs">
   </div>
   <div class="info">
    <div class="source">
     亚太分网英文版
    </div>
    <div class="pub-tim">
     2024-04-23 18:45:15
    </div>
   </div>
  </div>
 </div>
</div>'''

    # raw_blog = soup(markup, features="html.parser")
    # title = raw_blog.find('div', class_="title").text.replace('\n', '').replace(' ', '').lower()
    # print(title)
    
    