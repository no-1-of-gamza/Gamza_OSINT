from urllib import parse
from urllib.request import urlopen
from urllib.request import Request
from urllib.error import HTTPError
import json

class NaverMapApi:
    def __init__(self):
        self.Client_ID = 'Yws8bUSY4DK2vcWBShu7'
        self.Client_Secret = 'ILE_EKhNGw'
        self.api_url = 'https://openapi.naver.com/v1/search/local.json?query='

    def get(self, keyword):
        url = self.api_url + parse.quote(keyword) + "&display=3"
        #print(url)

        request = Request(url)
        request.add_header('X-Naver-Client-Id', self.Client_ID)
        request.add_header('X-Naver-Client-Secret', self.Client_Secret)

        try:
            response = urlopen(request)

        except HTTPError as e:
            print(f'HTTPError: {e}')
        
        else:
            rescode = response.getcode()
            if rescode == 200:
                response = response.read().decode('utf-8')
                response = json.loads(response)

                if not response:
                    print('No result')
                
                elif len(response['items']) == 0:
                    return None, None

                else:
                    #print('Success\n')
                    #print(response)
                    return response['items'][0]['address'], response['items'][0]['roadAddress']
            
            else:
                print(f'Response error, rescode:{rescode}')
    
if __name__ == '__main__':
    keyword = '성북구 에그맛있다'
    api = NaverMapApi()

    print(api.get(keyword))

