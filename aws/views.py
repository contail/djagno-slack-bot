import random
import requests                    

class AWS():

    def _get_web_server_count(self):
        url = 'https://cobak.co.kr/api/whale/get_web_server_count/'
        data = requests.get(url).json()
        current_web_server = data['web_server']
        temp_web_server = data['temp_server']
        text =" 총 {0}대 이고, 임시로 늘린서버는 {1}대 입니다!".format(current_web_server+temp_web_server, temp_web_server)
        return text  
    
    def _get_server_status(self):
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