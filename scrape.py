from bs4 import BeautifulSoup as bs
import selenium.webdriver as wd
import urllib.request as ureq
import os
import time
from webdriver import ChromeDriver


class Scraper:
    """
    div class="v1Nh3 kIKUG  _bz0w" -> is a post
    post > a > div class="eLaPa" -> image
    post > a > has 2 divs with classes 1. "eLaPa", 2. "u7YqG" -> video/igtv/carousel
      div class="u7YqG" > svg aria-label="Video" -> video
      div class="u7YqG" > svg aria-label="IGTV" -> igtv
      div class="u7YqG" > svg aria-label="Carousel" -> carousel
    """
    ig_url = 'https://www.instagram.com/'
    cd_path = ChromeDriver().get_wd()
    driver = driver2 = None
    soup = soup2 = None
    img_path = ''

    def __init__(self):
        self.driver = wd.Chrome(self.cd_path)
        self.driver2 = wd.Chrome(self.cd_path)

        while True:
            print('username: ')
            user_name = input() + '/'
            if user_name == '/':
                break
            self.img_path = 'post/' + user_name
            self.driver.get(self.ig_url + user_name)
            self.soup = bs(self.driver.page_source, 'html.parser')

            try:
                os.mkdir('post/' + user_name[:-1])
            except FileExistsError:
                print(f'folder {user_name[:-1]} exists')

            try:
                self.get_profile_pic()
                self.iterate_posts()
            except TypeError:
                print('user is private')
            print(f'finished scraping {user_name}')
        self.end_process()

    def get_profile_pic(self):
        profilepic = self.soup.find(class_='_6q-tv')
        ureq.urlretrieve(profilepic['src'], self.img_path + 'profilepic.png')
        print('saved profile pic')

    def save_image(self, a, post):
        img_src = post.find('img')['src']
        img_name = f'{self.img_path}img{a+1}.png'
        ureq.urlretrieve(img_src, img_name)
        print(f'saved image {img_name}')

    def save_video(self, a, post_type):
        video_src = self.soup2.find(class_='_5wCQW').video['src']
        vid_name = '{}{}{}.mp4'.format(self.img_path, post_type.lower(), a+1)
        ureq.urlretrieve(video_src, vid_name)
        print(f'saved video {vid_name}')

    def save_carousel(self, a):
        def get_carousel_steps(a):
            if a % 3 == 0:
                return [1, 3, 3][:a//3]
            else:
                return [0, 3, 3, 3][:a//3+1]

        carousel_folder = f'{self.img_path}post{a+1}'
        try:
            os.mkdir(carousel_folder)
        except FileExistsError:
            print(f'folder {carousel_folder} exists')
        try:
            div = self.soup2.find(class_=['JSZAJ', '_3eoV-', 'IjCL9', 'WXPwG'])
            steps = get_carousel_steps(len(div.find_all('div')))
            btn_next = self.driver2.find_element_by_class_name('_6CZji')
            cnt = 1
            for step in steps:
                for i in range(step):
                    btn_next.click()
                time.sleep(.5)
                self.soup2 = bs(self.driver2.page_source, 'html.parser')
                lsts = self.soup2.find_all(class_='Ckrof')
                for lst in lsts:
                    carousel_src = post_name = ''
                    try:
                        carousel_src = lst.find(class_='FFVAD')['src']
                        post_name = f'{carousel_folder}/img{cnt}.png'
                    except:
                        carousel_src = lst.find(class_='tWeCl')['src']
                        post_name = f'{carousel_folder}/video{cnt}.mp4'
                    ureq.urlretrieve(carousel_src, post_name)
                    cnt += 1
            print(f'saved carousel {carousel_folder} ({cnt-1} img/vid)')
        except:
            print('error processing carousel posts. skipping to next')

    def iterate_posts(self):
        for a, post in enumerate(self.soup.find_all(class_=['v1Nh3', 'kIKUG', '_bz0w'], limit=12)):
            try:
                if post.find(class_='u7YqG'):
                    post_type = post.find(class_='u7YqG').svg['aria-label']
                    self.driver2.get(self.ig_url + post.a['href'])
                    self.soup2 = bs(self.driver2.page_source, 'html.parser')
                    if post_type in ['Video', 'IGTV']:
                        self.save_video(a, post_type)
                    elif post_type == 'Carousel':
                        self.save_carousel(a)
                else:
                    self.save_image(a, post)
            except TypeError:
                print('No more posts')
                break

    def end_process(self):
        self.driver2.close()
        self.driver.close()


if __name__ == '__main__':
    scrape = Scraper()
