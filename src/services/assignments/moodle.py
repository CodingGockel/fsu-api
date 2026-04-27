#from authentification.ShibbolethSession import ShibbolethSession
import requests

def get_assignemnts():
    cookies = {
        '_shibsession_64656661756c7468747470733a2f2f6d6f6f646c652e756e692d6a656e612e64652f73686962626f6c657468': '_c792457d3fa1a33fa3684971b8253f3b',
        'MoodleSession': 'rvpcq6tuvd9qbe7cebrp9qe2et',
    }

    headers = {
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'accept-language': 'de-DE,de;q=0.9,en-US;q=0.8,en;q=0.7',
        'cache-control': 'no-cache',
        'content-type': 'application/json',
        'origin': 'https://moodle.uni-jena.de',
        'pragma': 'no-cache',
        'priority': 'u=1, i',
        'referer': 'https://moodle.uni-jena.de/my/',
        'sec-ch-ua': '"Google Chrome";v="147", "Not.A/Brand";v="8", "Chromium";v="147"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest',
        # 'cookie': '_shibsession_64656661756c7468747470733a2f2f6d6f6f646c652e756e692d6a656e612e64652f73686962626f6c657468=_c792457d3fa1a33fa3684971b8253f3b; MoodleSession=rvpcq6tuvd9qbe7cebrp9qe2et',
    }

    params = {
        'sesskey': 'PbAYhsfcd1',
        'info': 'core_calendar_get_action_events_by_timesort',
    }

    json_data = [
        {
            'index': 0,
            'methodname': 'core_calendar_get_action_events_by_timesort',
            'args': {
                'limitnum': 6,
                'timesortfrom': 1776031200,
                'limittononsuspendedevents': True,
            },
        },
    ]

    response = requests.post(
        'https://moodle.uni-jena.de/lib/ajax/service.php',
        params=params,
        cookies=cookies,
        headers=headers,
        json=json_data,
    )

    return response
    # Note: json_data will not be serialized by requests
    # exactly as it was in the original request.
    #data = '[{"index":0,"methodname":"core_calendar_get_action_events_by_timesort","args":{"limitnum":6,"timesortfrom":1776031200,"limittononsuspendedevents":true}}]'
    #response = requests.post(
    #    'https://moodle.uni-jena.de/lib/ajax/service.php',
    #    params=params,
    #    cookies=cookies,
    #    headers=headers,
    #    data=data,
    #)
    
if __name__ == "__main__":
    print(get_assignemnts().text)