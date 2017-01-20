# author github.com/yousefissa
import tweepy
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
from time import sleep
from config import *
from datetime import datetime


US_link = ('http://www.adidas.com/us/ultra-boost-uncaged-shoes/BA9797.html', 'US')
UK_link = ('http://www.adidas.co.uk/white-mountaineering-nmd-trail-shoes/BA7518.html', 'UK')

# sitekey retrieval
def get_sitekey(country_link):
	captcha_page = Request(country_link[0], headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_2) AppleWebKit/537.36'
	                '(KHTML, like Gecko) Chrome/56.0.2924.28 Safari/537.36'})
	product_page = urlopen(captcha_page)
	soup = BeautifulSoup(product_page, 'html.parser')
	sitekey = soup.find('div', attrs={'class': 'g-recaptcha'})['data-sitekey']
	return sitekey

# twitter portion
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
api = tweepy.API(auth)

def send_tweet(country_link):
	print('Tweeted sitekey.')

def main():
	current_sitekey_US, current_sitekey_Uk = get_sitekey(US_link), get_sitekey(UK_link)
	send_tweet(US_link), send_tweet(UK_link)
	while (current_sitekey_US == get_sitekey(US_link)) & (current_sitekey_Uk == get_sitekey(UK_link)):
		sleep(10*60)
		print('Sleeping 10 minutes.')
	print('Sitekey has changed!')
	main()

if __name__ == '__main__':
	main()

