from bs4 import BeautifulSoup
import requests
import sys
import pyperclip
import emoji


print('\nSitekey Finder - twitter.com/yousefnu - github.com/yousefissa \n\n')

AR_link = ('http://www.adidas.com.ar/zapatillas', 'AR')
AU_link = ('http://www.adidas.com.au/shoes', 'AU')
BR_link = ('http://www.adidas.com.br/calcados', 'BR')
CAE_link = ('http://www.adidas.ca/shoes', 'CA_EN')
CAF_link = ('http://www.adidas.ca/fr/chaussures', 'CA_FR')
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


country_link_list = [AR_link, AU_link, BR_link, CAE_link, CAF_link, DE_link, DK_link, ES_link, FR_link, IE_link, IT_link, MX_link, NOR_link, SE_link, UK_link, US_link]


print('This script supports several countries, type in the regioncode to search: \n\n /// Argentina = AR \t Australia = AU \t Brazil = BR ///\n /// Canada FR = CA_FR \t Canada EN = CA_EN \t Denmark = DK ///\n /// France = FR \t Germany = DE \t\t Ireland = IE /// \n /// Italy = IT \t Spain = ES \t\t Sweden = SE /// \n /// Norway = NO \t United Kingdoms = UK \t United States = US ///\n\n')
def adidas_country():
    country = input('Type the country code you want to work with:')
    country_list = [i[1] for i in country_link_list]
    if country.lower() not in [elem.lower() for elem in country_list]:
        print('Make sure you enter only the country letters, like US, CA, etc. ')
        adidas_country()
    return str(([i[0] for i in country_link_list if i[1] == country])[0])

link = adidas_country()
params = {
   'sz': 120,
   'grid': 'true',
   'start': 0
}

product_selector = '.image a'  # selector on the product page for the individual links
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


# Loops through the list of product categories and store the links in the all_list object
product_links = category_scraper(link, product_selector)

# Checks the individual products for the recaptcha sitekey
print("\nFound {} product links.".format(len(product_links)))
print("Starting site-key scraper. \n")
index = 0
for product in product_links:
    index += 1
    print('{} of {}: Checking for sitekey in: {}'.format(index, len(product_links), product))
    site_key_results = sitekey_scraper(str(product))
    if site_key_results:
        pyperclip.copy(site_key_results)
        print("\nFollowing Recaptcha Sitekey has been copied to clipboard:\n\n{}\n".format(site_key_results))
        break
    else:
        continue
