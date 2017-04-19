from bs4 import BeautifulSoup
import requests
import sys
import pyperclip
import emoji


print('\nSitekey Finder - twitter.com/yousefnu - github.com/yousefissa \n\n')

AR_link = ('http://www.adidas.com.ar/zapatillas', 'AR')
AU_link = ('http://www.adidas.com.au/shoes', 'AU')
BR_link = ('http://www.adidas.com.br/calcados', 'BR')
CA_link = ('http://www.adidas.ca/shoes', 'CA')
DE_link = ('http://www.adidas.de/schuhe', 'DE')
DK_link = ('http://www.adidas.dk/sko', 'DK')
ES_link = ('http://www.adidas.es/calzado', 'ES')
FR_link = ('http://www.adidas.fr/chaussures', 'FR')
IE_link = ('http://www.adidas.ie/shoes', 'IE')
IT_link = ('http://www.adidas.it/scarpe', 'IT')
MX_link = ('http://www.adidas.mx/calzado', 'MX')
NOR_link = ('http://www.adidas.no/shoes', 'NO')
SE_link = ('http://www.adidas.se/skor', 'SE')
UK_link = ('http://www.adidas.co.uk/shoes', 'UK')
US_link = ('http://www.adidas.com/us/shoes', 'US')
RU_link = ('http://www.adidas.ru/muzhchiny-obuv', 'RU')



country_link_list = [AR_link, AU_link, BR_link, CA_link, DE_link, DK_link,
                     ES_link, FR_link, IE_link, IT_link, MX_link, NOR_link, RU_link, SE_link, UK_link, US_link]
print('This script supports several countries, type in the regioncode to search: \n\n {}'.format(
    list(country[1] for country in country_link_list)))

# gets the adidas country you want.
def adidas_country():
    country = input('\nType the country code you want to work with: ')
    country_list = [i[1] for i in country_link_list]
    if country.lower() not in [elem.lower() for elem in country_list]:
        print(
            'Make sure you enter only the country letters, like US, CA, etc. ')
        adidas_country()
    return str(([i[0] for i in country_link_list if i[1] == country])[0])

link = adidas_country()
params = {
    'sz': 120,
    'grid': 'true',
    'start': 0
}

# selector on the product page for the individual links
product_selector = '.image a'
product_links = []  # placeholder for the individual product links

captcha_class = '.g-recaptcha'  # selector for the site-key placeholder
site_key = 'data-sitekey'  # element attribute to get the site-key


# Gets a new html session
def new_session(url):
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/52.0.2743.116 Safari/537.36',
        'Accept': 'text/html, application/xhtml+xml, application/xml',
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language': 'en-US,en;q=0.8,da;q=0.6',
        'DNT': '1'
    })
    response = session.get(url, params=params)
    soup = BeautifulSoup(response.content, 'html.parser')
    return soup


# Scrapes category pages for product links with the selector for the anchor tag
def category_scraper(url, selector):
    category = new_session(url)
    for link_src in category.select(selector):
        product_links.append(link_src['href'])
    return product_links


# Scrapes individual product pages for a captcha token
def sitekey_scraper(url):
    product = new_session(url)
    selector_captcha = product.find_all(attrs={"class": "g-recaptcha"})
    if selector_captcha:
        captcha_attribute = selector_captcha[0]['data-sitekey']
        if captcha_attribute:
            print('\n\nSitekey Found on {}'.format(url))
            return captcha_attribute
    else:
        return


# Loops through the list of product categories and store the links in the
# all_list object
product_links = category_scraper(link, product_selector)

# keeps track if sitekey is found or not.
sitekey_found = False

def product_search():
    # Checks the individual products for the recaptcha sitekey
    print("\nFound {} product links on page {}.\n".format(len(product_links), params['start']))
    index = 0
    for product in product_links:
        index += 1
        print('{} of {}: Checking for sitekey in: {}'.format(index + len(product_links)*(params['start']-1), len(product_links) * params['start'], product))
        site_key_results = sitekey_scraper(str(product))
        if site_key_results:
            pyperclip.copy(site_key_results)
            print("\nFollowing Recaptcha Sitekey has been copied to clipboard:\n\n{}\n".format(
                site_key_results))
            sitekey_found = True
            break
        else:
            continue

# # where the magic happens, u feel?
if __name__ == "__main__":
    print("Starting site-key scraper. \n")
    while sitekey_found == False:
        # loop pages lol
        params['start'] += 1
        # finally start
        product_search()
