import os
# import requests
from bs4 import BeautifulSoup as bs

class ChromeDriver:
    dl_url = 'https://chromedriver.chromium.org/downloads'
    wd_path = 'chromedriver/'

    # def download_driver(self):
    #     wd_r = requests.get(self.dl_url)
    #     wd_soup = bs(wd_r.content, 'html.parser')
    #     dl_list = wd_soup.find(class_='n8H08c UVNKR')
    #     dl_list = [i.a['href'] for i in dl_list if i.a]
    #     # halted here, cant scrape the download page TODO

    def get_wd(self):
        drivers = [i for i in os.listdir(self.wd_path)]
        drivers.sort()
        latest_driver = drivers[-1]
        return self.wd_path + latest_driver
