from bs4 import BeautifulSoup as bs
import selenium.webdriver as wd
import urllib.request as ureq
import os
import time


# fancy way of getting the number of steps to traverse the carousel posts
def get_carousel_steps(a):
    if a % 3 == 0:
        return [1, 3, 3][:a//3]
    else:
        return [0, 3, 3, 3][:a//3+1]


ig_url = 'https://www.instagram.com/'
print('username: ')
user_name = input() + '/'
cd_path = 'chromedriver/chromedriver.exe'

driver = wd.Chrome(cd_path)
driver2 = wd.Chrome(cd_path)
driver.get(ig_url + user_name)

soup = bs(driver.page_source, 'html.parser')

try:
    os.mkdir('img/' + user_name[:-1])
except FileExistsError:
    print('folder "{}" exists'.format(user_name[:-1]))

imgpath = 'img/' + user_name

profilepic = soup.find(class_='_6q-tv')
ureq.urlretrieve(profilepic['src'], imgpath + 'profilepic.png')
print('saved profile pic')

for a, post in enumerate(soup.find_all(class_=['v1Nh3', 'kIKUG', '_bz0w'], limit=12)):
    try:
        if post.find(class_='u7YqG'):
            posttype = post.find(class_='u7YqG').span['aria-label']
            driver2.get(ig_url + post.a['href'])
            soup = bs(driver2.page_source, 'html.parser')
            if posttype in ['Video', 'IGTV']:
                video_src = soup.find(class_='_5wCQW').video['src']
                vid_name = '{}{}{}.mp4'.format(imgpath, posttype.lower(), a+1)
                ureq.urlretrieve(video_src, vid_name)
                print('saved video {}'.format(vid_name))
            # if post type is Carousel, create a folder and save all image/video in the folder
            elif posttype == 'Carousel':
                carousel_folder = '{}post{}'.format(imgpath, a+1)
                os.mkdir(carousel_folder)
                try:
                    div = soup.find(class_=['JSZAJ', '_3eoV-', 'IjCL9', 'WXPwG'])
                    steps = get_carousel_steps(len(div.find_all('div')))
                    btn_next = driver2.find_element_by_class_name('_6CZji')
                    cnt = 1
                    for step in steps:
                        for i in range(step):
                            btn_next.click()
                        time.sleep(.5)
                        soup2 = bs(driver2.page_source, 'html.parser')
                        lsts = soup2.find_all(class_='Ckrof')
                        for lst in lsts:
                            carousel_src = post_name = ''
                            try:
                                carousel_src = lst.find(class_='FFVAD')['src']
                                post_name = '{}/img{}.png'.format(carousel_folder, cnt)
                            except:
                                carousel_src = lst.find(class_='tWeCl')['src']
                                post_name = '{}/video{}.mp4'.format(carousel_folder, cnt)
                            ureq.urlretrieve(carousel_src, post_name)
                            cnt += 1
                    print('saved carousel {} ({} img/vid)'.format(carousel_folder, cnt-1))
                except:
                    print('error processing carousel posts. skipping to next')
        else:
            img_src = post.find('img')['src']
            imgname = '{}img{}.png'.format(imgpath, a+1)
            ureq.urlretrieve(img_src, imgname)
            print('saved image {}'.format(imgname))
    except:
        print('no more posts')
        break

driver2.close()
driver.close()

# div class="v1Nh3 kIKUG  _bz0w" -> is a post
# post > a > div class="eLaPa" -> image
# post > a > has 2 divs with classes 1. "eLaPa", 2. "u7YqG" -> video/igtv/carousel
#   div class="u7YqG" > span aria-label="Video" -> video
#   div class="u7YqG" > span aria-label="IGTV" -> igtv
#   div class="u7YqG" > span aria-label="Carousel" -> carousel
