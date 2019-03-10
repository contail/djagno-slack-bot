from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from slackclient import SlackClient                               
import random

SLACK_VERIFICATION_TOKEN = getattr(settings, 'SLACK_VERIFICATION_TOKEN', None)
SLACK_BOT_USER_TOKEN = getattr(settings, 'SLACK_BOT_USER_TOKEN', None)                                     
Client = SlackClient(SLACK_BOT_USER_TOKEN)                        

class AWS(APIView):

    def post(self, request, *args, **kwargs):

        print(request.data)
        pass

    def _get_web_server_count(self):
        import requests
        url = 'https://cobak.co.kr/api/whale/get_web_server_count/'
        data = requests.get(url).json()
        current_web_server = data['web_server']
        temp_web_server = data['temp_server']
        text =" 총 {0}대 이고, 임시로 늘린서버는 {1}대 입니다!".format(current_web_server+temp_web_server, temp_web_server)
        return text  
    def _get_server_status(self):
        import requests
        url = 'https://cobak.co.kr/api/whale/get_server_status/'
        data = requests.get(url).json()
      
        web_server = data['web_server']
        rds_server = data['rds_server']
        fields = []
        for row in web_server:
            fields.append({
                "title": row['name'],
                "value": "CPU :{0}".format(str(row['cpu'])),
            })
        fields.append({
            'title': "RDS",
            'value' : "CPU :{0}".format(str(rds_server))
        });
        payload = {}
        import random
        r = lambda: random.randint(0,255)
        payload["attachments"] = [
                    {
                        "color": '#%02X%02X%02X' % (r(),r(),r()),
                        "fields": fields
                    }
                ]
  
        return payload 