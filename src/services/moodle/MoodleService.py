from services.auth.ShibbolethSession import ShibbolethSession
import requests
import json
from bs4 import BeautifulSoup
from typing import Any, Dict

class MoodleService():

    DEFAULT_HEADERS: dict = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
            'accept-language': 'de-DE,de;q=0.9',
        }
    
    def __init__(
        self,
        shibboleth_session: ShibbolethSession
    ):
        self.shibboleth_session: ShibbolethSession = shibboleth_session
        self.moodle_service_url: str = f'https://{shibboleth_session.get_service_url()}/lib/ajax/service.php'

    def get_all_courses(self, limit: int) -> dict:
        self.shibboleth_session.login()
        session: requests.Session = self.shibboleth_session.get_session()
        
        params: dict = {
            'sesskey': self.shibboleth_session.get_sess_key(),
            'info': 'core_course_get_enrolled_courses_by_timeline_classification',
        }

        json_data: list[dict[str, Any]] = [
            {
                'index': 0,
                'methodname': 'core_course_get_enrolled_courses_by_timeline_classification',
                'args': {
                    'offset': 0,
                    'limit': limit,
                    'classification': 'all',
                    'sort': 'fullname',
                    'customfieldname': '',
                    'customfieldvalue': '',
                    'requiredfields': [
                        'id',
                        'fullname',
                        'shortname',
                        'showcoursecategory',
                        'showshortname',
                        'visible',
                        'enddate',
                    ],
                },
            },
        ]
        print(self.shibboleth_session.get_sess_key())
        response: requests.Response = session.post(
            self.moodle_service_url,
            params=params,
            json=json_data,
        )
        data: dict = response.json()

        return data

    
        