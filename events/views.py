from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from slackclient import SlackClient                               
import random
from push.views import *
from aws.views import *
SLACK_VERIFICATION_TOKEN = getattr(settings, 'SLACK_VERIFICATION_TOKEN', None)
SLACK_BOT_USER_TOKEN = getattr(settings, 'SLACK_BOT_USER_TOKEN', None)                                     
Client = SlackClient(SLACK_BOT_USER_TOKEN)                        

class Events(APIView):

    hello_list = ['안녕하세요~', '어서오세요~', '반가워요~']
    goobye_list = ['잘가요 ㅠㅠ', '안녕히가세요 ㅜㅜ']
    luck_list = ['오늘은 운세가 좋아요!!', '오늘은 그럭저럭이네요~~', '오늘은 최악이에요 ㅜㅜ']
    introduce = """
    안녕하세요~ 제이름은 고래입니다 :whale:
    현재 가능한 명령어는
    '운세', '푸시 정보', '푸시 결과', '웹서버 몇대야', '서버 상태' 입니다.
    지속적으로 업데이트 중입니다! 
    감사합니다~ 
    """

    def post(self, request, *args, **kwargs):
         
        slack_message = request.data
        
        if slack_message.get('token') != SLACK_VERIFICATION_TOKEN:
            return Response(status=status.HTTP_403_FORBIDDEN)
        
        if slack_message.get('type') == 'url_verification':
            return Response(data=slack_message, status=status.HTTP_200_OK)

        print(slack_message,"======")
        # greet bot
        if 'event' in slack_message:                               
            event_message = slack_message.get('event')             
            
            # ignore bot's own message
            if event_message.get('subtype') == 'bot_message':     
                return Response(status=status.HTTP_200_OK)        
            
            # process user's message
            user = event_message.get('user')                       
            text = event_message.get('text')   
            channel = event_message.get('channel')      

            if event_message.get('type') == 'member_left_channel':
                Client.api_call(method='chat.postMessage',         
                                    channel=channel,                   
                                    text=random.choice(self.goobye_list))                      
                return Response(status=status.HTTP_200_OK)    

            elif event_message.get('type') == 'member_joined_channel':
                Client.api_call(method='chat.postMessage',         
                                    channel=channel,                   
                                    text=random.choice(self.hello_list))                   
                return Response(status=status.HTTP_200_OK) 
            else:
                print(text,)
                if '안녕' in text.lower():
                    bot_text = '<@{}> 반가워요! :wave:'.format(user)  
                elif '자기소개' in text.lower():
                    bot_text = '<@{}> \n'.format(user) + self.introduce                              
                elif '운세' in text.lower():
                    bot_text = '<@{0}> {1} '.format(user, random.choice(self.luck_list))   

                elif '웹서버 몇대야' in text.lower():
                    aws = AWS()
                    aws_count = aws._get_web_server_count()
                    bot_text = '<@{0}> {1} '.format(user, aws_count)                                
                
                elif '푸시 정보' in text.lower():
                    push_info =Push()
                    result = push_info._get_push_list()
                    bot_text = '<@{0}> {1} '.format(user, result)   
                
                elif '푸시 결과' in text.lower():
                    push_info =Push()
                    result = push_info._get_push_result()
                    bot_text = '<@{0}> {1} '.format(user, result)
                elif '서버 상태' in text.lower():
                    aws = AWS()
                    payload = aws._get_server_status()
                    print(payload)
                
                    Client.api_call(method='chat.postMessage',         
                                    channel=channel,                   
                                    text="서버상태",
                                    attachments=payload['attachments'])  
                    return Response(status=status.HTTP_200_OK)   
                Client.api_call(method='chat.postMessage',         
                                channel=channel,                   
                                text=bot_text)                 
                return Response(status=status.HTTP_200_OK)   
        if 'payload' in slack_message:
            if slack_message['payload'].get('attachments'):
                print(slack_message['payload'])
                Client.api_call(method='chat.postMessage',         
                                    channel=slack_message['channel'],                   
                                    text=slack_message['text'],
                                    attachments = slack_message['payload']['attachments'])
            else:
                Client.api_call(method='chat.postMessage',         
                                    channel=slack_message['channel'],                   
                                    text=slack_message['text'])


        return Response(status=status.HTTP_200_OK)