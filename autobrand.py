import requests
from bs4 import BeautifulSoup
import re
from decouple import config

client = requests.Session()


class Scrapper():
    def __init__(self) -> None:
        '''
        Initialize the scrapper with the username, password and usefull links
        '''
        self.user = config('AUTOBRAND_USER')
        self.password = config('AUTOBRAND_PASS')
        self.main_url = 'https://online.autobrand.ro'
        self.login_url = 'https://online.autobrand.ro/csp/berta/portal/index.csp?SPR=RO'

    def credentials_setup(self, username, password):
        '''Optionally you can change the username and password here'''
        self.user = username
        self.password = password

    def login(self):
        '''
        Login on the site and navigate to the page that contains the search box
        '''
        self.html = client.get(self.login_url).content
        self.soup = BeautifulSoup(self.html, "html.parser")
        self.csp_token = self.soup.find(
            'input', {'name': 'CSPToken'}).get('value')
        self.csp_chd = self.soup.find('input', {'name': 'CSPCHD'}).get('value')

        self.login_information = {
            'NAME': self.user,
            'WEBPASSC': self.password,
            'CSPToken': self.csp_token,
            'CSPCHD': self.csp_chd}

        # Log in
        response = client.post(self.login_url, data=self.login_information)
        response = client.get(
            self.main_url + '/csp/berta/portal/UtilLogin.csp', data=self.login_information)

        # Print the response status code
        if response.status_code != 200:
            print("Authentication failed.")
            exit()

        self.soup = BeautifulSoup(response.text, 'html.parser')
        # Find the "Home" button link
        self.home_button = self.soup.find('li', class_='nav-item item-top')

        if self.home_button:
            # Extract URL with the new token that we need to use
            onclick_value = self.home_button.get('onclick')
            home_url = re.search(r"'(.*?)'", onclick_value).group(1)
            home_url = home_url.replace('\\u0024', '$')
        else:
            print("Home button not found.")
            exit()

        response = client.post(
            self.main_url + home_url, data=self.login_information)
        self.soup = BeautifulSoup(response.text, 'html.parser')

    def search_item(self, item) -> dict:
        '''
        Search for the item on the site
        '''

        # Find the new search token and search for the item
        search_token = self.soup.find(
            'input', {'name': 'CSPToken'}).get('value')

        search_url = self.main_url + '/csp/berta/portal/ArtSuche.csp?CSPToken='

        search_data = {
            'CSPToken': self.csp_token,
            'suche': item,
        }

        search_url += search_token
        # Send a POST request to perform the search
        search_response = client.post(search_url, data=search_data)

        # Check if the search request was successful
        if search_response.status_code == 200:
            print("Search request successful!")
        else:
            print("Search request failed with status code:",
                  search_response.status_code)
            exit()

        # Populate the data with the results from the search
        soup = BeautifulSoup(search_response.text, 'html.parser')
        item_code = soup.find(
            'span', class_='current-cat current-art').get_text()
        item_name = soup.find('td', class_='itemlist-col-BEZ').get_text()
        item_price = soup.find('span', class_='price-value').get_text()
        item_producer = soup.find(
            'td', class_='itemlist-col-HERSTELLBEZ').get_text()
        item_availability = soup.find(
            'td', class_='itemlist-col-BESTANDVGST').find('img')['alt']

        self.item_info = {
            'Code': item_code.strip(),
            'Name': item_name.strip(),
            'Price': item_price.strip(),
            'Producer': item_producer.strip(),
            'Availability': item_availability.strip()
        }

        return self.item_info
