import giphy_client
from whale.settings import GIPHY
class Giphy():

    __BASE_URL = "http://api.jjalkey.com/v1/search"
    __api_key = GIPHY
    def __init__(self, base_url=__BASE_URL, api_key=__api_key):
        self.base_url = base_url
        self.api_key = api_key
        self.api_instance = giphy_client.DefaultApi()
        self.fmt = 'json'
        self.lang = 'en'
        self.limit = 10
        self.offset = 0
        self.rating = 'g'
        self.result_list = []

    def get_keyword_giphy(self, keyword):

        try:
            data = self.api_instance.gifs_search_get(self.api_key, keyword, limit=self.limit, offset=self.offset, rating=self.rating, lang=self.lang, fmt=self.fmt)
            content = data.to_dict()
            for row in content['data']:
                self.result_list.append(row['images']['fixed_height']['url'])
        except:
            pass
        self.set_payload(keyword)
    def set_payload(self, keyword):
        if len(self.result_list) > 0 :
            payload = {}
            import random
            r = lambda: random.randint(0, 255)
            payload["attachments"] = [
                {
                    "title": "{} 짤".format(keyword),
                    "color": '#%02X%02X%02X' % (r(), r(), r()),
                    "image_url" : random.choice(self.result_list)
                }
            ]
            return payload
        else:
            payload = {}
            import random
            r = lambda: random.randint(0, 255)
            payload["attachments"] = [
                {
                    "title": "{}의 짤 이 없네요ㅠㅠ".format(keyword),
                    "color": '#%02X%02X%02X' % (r(), r(), r()),
                    "image_url" : "https://media3.giphy.com/media/xT77Y9OPycJV5r6RmU/giphy-preview.gif"
                }
            ]

            return payload