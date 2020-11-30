# IG Posts Scraper

Scrape first 12 posts of a public Instagram account; be it images, videos, IGTV or Carousel.

Downloads all posts to a folder named `img` in a file named after the account owner. 
View the sample output in the `img` folder which uses [Ryan Reynolds](https://www.instagram.com/vancityreynolds/)' account.

Start with installing the packages needed as listed in `req.txt` file.
> `pip install -r req.txt`

You will also need a [ChromeDriver](https://chromedriver.chromium.org/) tool, which is included in the folder `./chromedriver/`. 
Just be sure that the driver corresponds to your Google Chrome's version, otherwise it won't work.
> The given ChromeDriver (`chromedriver.exe`) is for Google Chrome version 86. ChromeDriver version 87 is also given.

> Other browsers have their own driver.

If you are scraping a user where you have scraped before (i.e. the folder exists) there might occur an error. Delete the folder first to be able to re-scrape.

Happy scraping!
