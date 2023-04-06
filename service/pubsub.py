import requests
import xml.etree.ElementTree as ET

URL = "https://pubsubhubbub.appspot.com/subscribe"
TOPIC_BASE_URL = "https://www.youtube.com/xml/feeds/videos.xml?channel_id="
CALLBACK_URL = "https://yttextsearch-production.up.railway.app/api/yt_sub"


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


def parse_notification(data: str):
    root = ET.fromstring(data)
    entry = root.find('{http://www.w3.org/2005/Atom}entry')
    video_id = entry.find(
        '{http://www.youtube.com/xml/schemas/2015}videoId').text
    return {
        "video_id": video_id
    }


if __name__ == '__main__':
    subscribe("UCALaO58yDzt0djpHNGZqCDA")
