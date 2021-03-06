import random
import requests

class Push():

    def _get_push_list(self):
        url = 'https://cobak.co.kr/api/whale/today_push_list/'
        data = requests.get(url).json()
        text ="\n==========오늘의 푸시 정보==========\n"
        push_info = ""
        if data['data'] is None:
            return u"\n 예약된 푸시가 없습니다!"
        for row in data['data']:
            push_info+="*제목*: {0}".format(row['title'])
            push_info+="\n"
            push_info+="*예약시간*: {0}".format(row['reservation_time'])
            push_info+="\n"
        text += push_info
        return text

    def _get_push_result(self):
        url = 'https://cobak.co.kr/api/whale/push_result/'
        data = requests.get(url).json()
        text ="\n==========최근 푸시 결과==========\n"
        push_info = ""
        if data['data'] is None:
            return u"\n 최근에 예약된 푸시가 없습니다!"
        for row in data['data']:
            push_info+="*제목*: {0}".format(row['title'])
            push_info+="\n"
            push_info+="*발송시간*: {0}".format(row['push_time'])
            push_info+="\n"
            push_info+="*ping_count*: {0}".format(row['ping'])
            push_info+="\n"
            push_info+="*pong_count*: {0}".format(row['pong'])
            push_info+="\n"
            push_info+="*오픈비율*: {0}".format(row['rate'])
            push_info+="\n"
            push_info+="====================\n"
        text += push_info
        return text