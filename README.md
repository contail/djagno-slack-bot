# djagno-slack-bot

## [Django] 슬랙 봇 만들기

## 프로젝트 설명
- 반복되는 업무를 간소화 하고, 간단한 정보를 슬랙에서 볼 수 있도록 하기위해 제작했습니다.
- [**해당 사이트**](https://medium.com/freehunch/how-to-build-a-slack-bot-with-python-using-slack-events-api-django-under-20-minute-code-included-269c3a9bf64e) 를 사이트를 참고하여 제작했습니다.


### 주요파일 설명
* key.jsons는 본 프로젝트의 AWS 정보를 담고 있는 key:value 입니다.
* secret_manager.py는 AWS의 Secret_manager를 이용하여 보안에 민감한 key:value들을 호출합니다.
* events는 슬랙에서 봇을 호출 할 경우 호출에 따른 이벤트를 처리 할 수 있도록 분기시켜놓은 class 입니다.


### Git으로 설치하기

```
git init
git clone https://github.com/contail/djagno-slack-bot.git
pip install -r requirements.txt
```

### 주요 명령어

* AWS 서버 상태 확인 (CPU) / 웹서버 갯수 확인하기
* 미세먼지 측정 (Open Api 이용 https://www.data.go.kr/dataset/15000581/openapi.do )
* RestFul Api를 이용하여 사용하고 싶은 데이터 셋이나 결과를 Slack으로 전송 


### slack으로 Post 할 경우 Response 설정
* [**참고자료**] (https://api.slack.com/docs/message-attachments#when_to_use_attachments)

#### Payload가 없을 경우

```
Client.api_call(method='chat.postMessage',        
                                channel=channel,                  
                                text=bot_text)
                               
```

#### PayLoad가 있을 경우

* attachments 추가

```
Client.api_call(method='chat.postMessage',
                                            channel=channel,
                                            text=bot_text,
                                            attachments=payload['attachments'])
```

### slack app 설정하기

#### Event를 받을 URL 설정하기
<img width="701" alt="스크린샷 2019-03-16 오후 4 04 43" src="https://user-images.githubusercontent.com/15063135/54472034-64853a80-4805-11e9-8acd-2379ba102613.png">

#### Evnet를 받을 봇 스크립트 설정하기
<img width="678" alt="스크린샷 2019-03-16 오후 4 07 12" src="https://user-images.githubusercontent.com/15063135/54472081-fd1bba80-4805-11e9-8fa3-087fcc6e807d.png">
