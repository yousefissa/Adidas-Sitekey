# author github.com/yousefissa
import tweepy
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
from time import sleep
from config import *
from datetime import datetime

# sitekey retrieval
def get_sitekey():
	captcha_page = Request('http://www.adidas.com/us/ultra-boost-uncaged-shoes/BA9797.html', headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_2) AppleWebKit/537.36'
	                '(KHTML, like Gecko) Chrome/56.0.2924.28 Safari/537.36'})
	product_page = urlopen(captcha_page)
	soup = BeautifulSoup(product_page, 'html.parser')
	sitekey = soup.find('div', attrs={'class': 'g-recaptcha'})['data-sitekey']
	return sitekey

# twitter portion
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
api = tweepy.API(auth)

def send_tweet():
	api.update_status('Current Adidas Sitekey as of: {} is {}'.format(datetime.now(), get_sitekey()))
	print('Tweeted sitkey - {}'.format(sitekey))

def main():
	current_sitekey = get_sitekey()
	send_tweet()
	while current_sitekey == get_sitekey():
		sleep(10*60)
		print('Sleeping 10 minutes.')
	print('Sitekey has changed!')
	main()

if __name__ == '__main__':
	main()








