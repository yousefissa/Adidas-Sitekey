# author github.com/yousefissa
import tweepy
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
from time import sleep
from config import *
from datetime import datetime

US_link = ('http://www.adidas.com/us/white-mountaineering-campus-80s-shoes/BA7517.html', 'US')
UK_link = ('http://www.adidas.co.uk/eqt-support-adv-shoes/BB2324.html', 'UK')
AU_link = ('http://www.adidas.com.au/ultra-boost/BB0819.html', 'AU')
CA_link = ('http://www.adidas.ca/en/womens-ultra-boost-shoes/BA8928.html', 'CA')
country_link_list = [US_link, UK_link, AU_link, CA_link]

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
	api.update_status('Current Adidas {} Sitekey as of: {} is {}'.format(country_link[1], datetime.now(), get_sitekey(country_link)))
	print('Tweeted {} sitekey.'.format(country_link[1]))

def main():
	try:
		sitekey_list = [get_sitekey(i) for i in country_link_list]
	except TypeError:
		print('One of the links does not have a captcha. Check your links.')
		exit()
	for link in country_link_list:
		send_tweet(link)
	while (sitekey_list[0] == get_sitekey(US_link)) & (sitekey_list[1] == get_sitekey(UK_link)) & (sitekey_list[2] == get_sitekey(AU_link)) & (sitekey_list[3] == get_sitekey(CA_link)):
		print('Sleeping 10 minutes.')
		sleep(10*60)
	print('Sitekey has changed!')
	main()

if __name__ == '__main__':
	main()