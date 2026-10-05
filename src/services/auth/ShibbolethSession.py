import requests
from bs4 import BeautifulSoup
import re

class ShibbolethSession:
    """
    example:
        session = ShibbolethSession(
            service_url='moodle.uni-jena.de',
            idp_base_url='idp.uni-jena.de'
        ).login()
    """
    DEFAULT_HEADERS: dict = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
        'accept-language': 'de-DE,de;q=0.9',
    }
    
    def __init__(
        self,
        service_base_url: str,
        idp_base_url: str,
        username: str,
        password: str,
        headers: dict | None = None,
    ):
        self.service_url: str = service_base_url
        self.idp_base_url: str = f'https://{idp_base_url}'
        self.entry_url: str = f'https://{service_base_url}/auth/shibboleth/index.php'
        self.post_url: str = f'https://{service_base_url}/Shibboleth.sso/SAML2/POST'
        self.username: str = username
        self.password: str = password
        self.headers: dict = headers or self.DEFAULT_HEADERS
        self.session: requests.Session = requests.Session()
        self.sess_key: str = ''

    def _get_soup(self, response: requests.Response) -> BeautifulSoup:
        return BeautifulSoup(response.text, 'html.parser')
    
    def _get_sess_key(self) -> str:
        res = self.session.get(f'https://{self.service_url}/my/', headers=self.headers)
        sesskey = re.search(r'"sesskey":"([^"]+)"', res.text).group(1) # type: ignore 
        return sesskey         
    
    def _fetch_login_page(self) -> requests.Response:
        res: requests.Response = self.session.get(self.entry_url, headers=self.headers)
        return res
        
    def _local_storage_check(self, soup: BeautifulSoup) -> requests.Response:
        csrf_token: str = soup.find('input', {'name': 'csrf_token'})['value'] # type: ignore 
        form_action: str = soup.find('form', {'name': 'form1'})['action'] # type: ignore 
        idp_post_url: str = self.idp_base_url + form_action
        res: requests.Response = self.session.post(
            idp_post_url,
            headers={**self.headers, 'content-type': 'application/x-www-form-urlencoded'},
            data={
                'csrf_token': csrf_token,
                'shib_idp_ls_exception.shib_idp_session_ss': '',
                'shib_idp_ls_success.shib_idp_session_ss': 'true',
                'shib_idp_ls_value.shib_idp_session_ss': '',
                'shib_idp_ls_exception.shib_idp_persistent_ss': '',
                'shib_idp_ls_success.shib_idp_persistent_ss': 'true',
                'shib_idp_ls_value.shib_idp_persistent_ss': '',
                'shib_idp_ls_supported': 'true',
                '_eventId_proceed': '',
            }
        )
        return res
    
    def _post_login(self, soup: BeautifulSoup) -> requests.Response:
        csrf_token: str = soup.find('input', {'name': 'csrf_token'})['value'] # type: ignore 
        form_action: str = soup.find('form')['action'] # type: ignore 
        idp_login_url: str = self.idp_base_url + form_action
        res:requests.Response = self.session.post(
            idp_login_url,
            headers={**self.headers, 'content-type': 'application/x-www-form-urlencoded'},
            data={
                'csrf_token': csrf_token,
                'j_username': self.username,
                'j_password': self.password,
                '_eventId_proceed': '',
            }
        )
        return res
    
    def _post_SAML2(self, soup: BeautifulSoup) -> requests.Response:
        saml_response: str = soup.find('input', {'name': 'SAMLResponse'}) # type: ignore 
        relay_state: str = soup.find('input', {'name': 'RelayState'}) # type: ignore 
        if saml_response and relay_state:
            res = self.session.post(
                self.post_url,
                headers={**self.headers, 'content-type': 'application/x-www-form-urlencoded'},
                data={
                    'SAMLResponse': saml_response['value'], # type: ignore 
                    'RelayState': relay_state['value'], # type: ignore 
                }
            )
        else:
            print("Login failed")
        return res
    
    def login(self):
        current_response = self._fetch_login_page()
        current_response = self._local_storage_check(self._get_soup(current_response))
        current_response = self._post_login(self._get_soup(current_response))
        current_response = self._post_SAML2(self._get_soup(current_response))
        self.sess_key = self._get_sess_key()
    
    def get_session(self) -> requests.Session:
        return self.session
    
    def get_sess_key(self) -> str:
        return self.sess_key
    
    def validate_session(self) -> bool:
        res: requests.Response = self.session.get(f'https://{self.service_url}/my/')
        if(res.status_code == 200):
            return True
        return False
    
    def get_service_url(self) -> str:
        return self.service_url

