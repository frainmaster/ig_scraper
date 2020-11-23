from bs4 import BeautifulSoup as bs
import selenium.webdriver as wd
import urllib.request as ureq
import os

ig_url = 'https://www.instagram.com/'
print('username: ')
user_name = input() + '/'
cd_path = 'chromedriver.exe'

driver = wd.Chrome(cd_path)
driver2 = wd.Chrome(cd_path)
driver.get(ig_url + user_name)

soup = bs(driver.page_source, 'html.parser')

try:
	os.mkdir('img/' + user_name[:-1])
except:
	print('folder "{}" exists'.format(user_name[:-1]))

imgpath = 'img/' + user_name

for a, post in enumerate(soup.find_all(class_=['v1Nh3', 'kIKUG', '_bz0w'], limit=12)):
	try:
		if post.find(class_='u7YqG'):
			posttype = post.find(class_='u7YqG').span['aria-label']
			driver2.get(ig_url + post.a['href'])
			soup = bs(driver2.page_source, 'html.parser')
			if posttype in ['Video', 'IGTV']:
				video_src = soup.find(class_='_5wCQW').video['src']
				vid_name = '{}{}{}.mp4'.format(imgpath, posttype.lower(), a)
				ureq.urlretrieve(video_src, vid_name)
				print('saved video {}'.format(vid_name))
			elif posttype == 'Carousel':
				carousel_folder = '{}post{}'.format(imgpath, a)
				os.mkdir(carousel_folder)
				try:
					div = soup.find(class_=['JSZAJ', '_3eoV-', 'IjCL9', 'WXPwG'])
					# print(div.find_all('div'))
					for i in range(len(div.find_all('div'))):
						# print(div.find_all('div')[i])
						print(i)
						content_src = soup.find(class_='KL4Bh').img['src']
						content_name = '{}/{}{}.png'.format(carousel_folder, posttype.lower(), i)
						if not content_src:
							content_src = soup.find(class_='_5wCQW').video['src']
							content_name = '{}/{}{}.mp4'.format(carousel_folder, posttype.lower(), i)
						# try:
						# 	content_src = soup.find(class_='KL4Bh').img['src']
						# 	content_name = '{}/{}{}.png'.format(carousel_folder, posttype.lower(), i)
						# except:
						# 	content_src = soup.find(class_='_5wCQW').video['src']
						# 	content_name = '{}/{}{}.mp4'.format(carousel_folder, posttype.lower(), i)
						ureq.urlretrieve(content_src, content_name)
						# go to next content of carousel
						if i != len(div.find_all('div'))-1:
							btn_next = driver2.find_element_by_id('_6CZji')
							btn_next.click()
					print('saved carousel {}'.format(carousel_folder))
				except:
					print('error processing carousel posts. skipping to next')
		else:
			img_src = post.find('img')['src']
			imgname = '{}img{}.png'.format(imgpath, a)
			ureq.urlretrieve(img_src, imgname)
			print('saved image {}'.format(imgname))
	except:
		print('no more posts')
		break

driver2.close()
driver.close()


# ig
# div class="v1Nh3 kIKUG  _bz0w" -> is a post
# post > a > div class="eLaPa" -> image
# post > a > has 2 divs with classes 1. "eLaPa", 2. "u7YqG" -> video/igtv/carousel
#   div class="u7YqG" > span aria-label="Video" -> video
#   div class="u7YqG" > span aria-label="IGTV" -> igtv
#   div class="u7YqG" > span aria-label="Carousel" -> carousel
