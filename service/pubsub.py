import requests

URL = "https://pubsubhubbub.appspot.com/subscribe"
TOPIC_BASE_URL = "https://www.youtube.com/xml/feeds/videos.xml?channel_id="
CALLBACK_URL = "https://yttextsearch-production.up.railway.app/api/yt_sub"

# hub.callback: https://ergsd.com/hook
# hub.topic: https://www.youtube.com/xml/feeds/videos.xml?channel_id=thehistorysquad
# hub.verify: async
# hub.mode: subscribe
# hub.verify_token:
# hub.secret:
# hub.lease_numbers:


def subscribe(channel_id: str):
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
    }
    data = {
        'hub.callback': CALLBACK_URL,
        'hub.topic': f"{TOPIC_BASE_URL}{channel_id}",
        'hub.verify': 'async',
        'hub.mode': 'subscribe',
        'hub.verify_token': '',
        'hub.secret': '',
        'hub.lease_numbers': '',
    }
    response = requests.post(URL, data=data, headers=headers)
    print(response.status_code)
    print(response.text)


if __name__ == '__main__':
    subscribe("@proguide66")
