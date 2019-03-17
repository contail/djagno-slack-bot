import random
from whale.settings import OPEN_DATA_API_KEY      
from requests.adapters import HTTPAdapter
from urllib3 import Retry           
import requests
class Weather():
    __API_BASE_URL = 'http://openapi.airkorea.or.kr/openapi/services/' \
                     'rest/ArpltnInforInqireSvc/{}?' \
                     'serviceKey={}' \
                     '&{}&ver=1.3'

    def __init__(self, api_base_url=__API_BASE_URL):            
        self.fields = []
        self.api_base_url = api_base_url
        self.request_timeout = 120
        self.session = requests.Session()
        retries = Retry(total=5, backoff_factor=0.5, status_forcelist=[502, 503, 504])
        self.session.mount('http://', HTTPAdapter(max_retries=retries))
        self.unit = '㎍/㎥'

    def __request(self, url):
        import json
        try:
            response = self.session.get(url, timeout=self.request_timeout)
            if response.status_code == 429:
                import time
                time.sleep(2)
                return
            response.raise_for_status()

            content = json.loads(response.content.decode('utf-8'))
            # print(content)
            return content
        except Exception as e:
            raise

    def get_station_name_value(self, station_name):
        station_name = str(station_name)
        condition = "getMsrstnAcctoRltmMesureDnsty"
        api_url = "{}&stationName={}&_returnType=json".format(self.__API_BASE_URL.format
                                                              (condition,OPEN_DATA_API_KEY,'dataTerm=DAILY'),station_name)
        print(api_url)
        import requests
        # print(requests.get(api_url).json())
        data = self.__request(api_url)
        print(data['list'])
        try:
            if len(data['list']) != 0:
                current_time = data['list'][0]['dataTime']
                pm10_value = data['list'][0]['pm10Value']
                pm25_value = data['list'][0]['pm25Value']

                if pm10_value != "-":
                    pm10_grade = self.convert_grade_to_emotion(self.convert_pm10_value_to_grade(int(pm10_value)))
                    pm10_set_value = pm10_grade + " " + str(pm10_value) + self.unit
                else:
                    pm10_set_value = " 정보없음!"
                if pm25_value !="-":
                    pm25_grade = self.convert_grade_to_emotion(self.convert_pm25_value_to_grade(int(pm25_value)))
                    pm25_set_value = pm25_grade + " " + str(pm25_value) + self.unit
                else:
                    pm25_set_value = " 정보없음!"
                self.set_fields("미세먼지", pm10_set_value)
                self.set_fields("초미세먼지", pm25_set_value)
                return True, self.set_payload(station_name + " {0} 기준".format(current_time), self.fields)
            else:
                return False, 0
        except:
            return False, 0
    def get_sido_name_value(self, sido_name):

        condition = "getCtprvnMesureSidoLIst"
        api_url = "{}&sidoName={}&numOfRows=20&_returnType=json".format(self.__API_BASE_URL.format
                                                              (condition, OPEN_DATA_API_KEY,'searchCondition=HOUR'),
                                                              sido_name)
        data = self.__request(api_url)
        print(data)
        date_time = None
        # try:
        for row in data['list']:
            print(row)
            city_name = row['cityName']
            pm10_value = row['pm10Value']
            pm25_value = row['pm25Value']
            date_time = row['dataTime']
            print(city_name, pm10_value)
            pm10_grade = self.convert_grade_to_emotion(self.convert_pm10_value_to_grade(int(pm10_value)))
            pm10_set_value = pm10_grade + " " + str(pm10_value) + self.unit
            pm25_grade = self.convert_grade_to_emotion(self.convert_pm25_value_to_grade(int(pm25_value)))
            pm25_set_value = pm25_grade + " " + str(pm25_value) + self.unit

            value = "미세먼지 "+pm10_set_value + "\n 초미세먼지 " + pm25_set_value
            self.set_sido_fields(city_name, value)
        return True, self.set_payload(sido_name + " {0} 기준".format(date_time), self.fields)
        # except:
        #     return False, 0

    def convert_pm10_value_to_grade(self, pm10_value):
        if pm10_value <= 30:
            return 0
        elif pm10_value <= 80:
            return 1
        elif pm10_value <= 150:
            return 2
        else:
            return 3

    def convert_pm25_value_to_grade(self, pm25_value):
        if pm25_value <= 15:
            return 0
        elif pm25_value <= 35:
            return 1
        elif pm25_value <= 75:
            return 2
        else:
            return 3

    def convert_grade_to_emotion(self, grade):

        if grade == 0:
            return "좋아요 :heart_eyes:"
        elif grade == 1:
            return "보통 :thinking_face:"
        elif grade == 2:
            return "나쁨 :sob:"
        else:
            return "매우나쁨 :scream:"

    def all_area_list(self, area):
        area_list = ['서울', '부산', '대구', '인천', '광주', '대전', '울산', '경기', '강원', '충북', '충남', '전북', '전남', '경북', '경남', '제주', '세종']
        if area in area_list:
            return True
        else:
            return False

    #TODO: 나중에 디테일 작업 해주기
    def detail_area_list(self):
        seoul_list = ['중구', '한강대로', '종로구', '청계천로', '종로', '용산구', '광진구', '성동구', '강변북로', '중랑구', '동대문구', '홍릉로', '성북구', '정릉로', '도봉구', '은평구', '서대문구', '마포구', '신촌로', '강서구', '공항대로', '구로구', '영등포구', '영등포로', '동작구', '동작대로 중앙차로', '관악구', '강남구', '서초구', '도산대로', '강남대로', '송파구', '강동구', '천호대로', '금천구', '시흥대로', '강북구', '양천구', '노원구', '화랑로']
        busan_list = ['광복동', '초량동', '태종대', '전포동', '온천동', '명장동', '대연동', '학장동', '덕천동', '청룡동', '좌동', '장림동', '대저동', '녹산동', '연산동', '기장읍', '용수리', '수정동', '부곡동', '광안동', '대신동', '덕포동', '부산북항', '부산신항']


    def set_fields(self, title, value):

        self.fields.append({
            "title": title,
            "value": value,
        })

    def set_sido_fields(self, title, value):
        self.fields.append({
            "title": title,
            "value": value,
            "short": True,
        })

    def set_payload(self, title, fields=[]):
        payload = {}
        import random
        r = lambda: random.randint(0, 255)
        payload["attachments"] = [
            {
                "title" : title,
                "color": '#%02X%02X%02X' % (r(), r(), r()),
                "fields": fields
            }
        ]
        return payload