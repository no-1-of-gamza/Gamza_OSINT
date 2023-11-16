'''
dictionary_list = [
    {'title': '주소지', 'url': 'https:~', 'preview': '미리보기', 'content': '전체 내용'},
    {'title': '주소지', 'url': 'https:~', 'preview': '미리보기', 'content': '전체 내용'},
    {'title': '주소지', 'url': 'https:~', 'preview': '미리보기', 'content': '전체 내용'}
]
'''
from util import crawler
from util import address
from util import NaverMapApi

class Data_PreProcessing:
    def __init__(self):
        self.crawler = crawler.Crawler()
        self.check = address.Address()
        self.api = NaverMapApi.NaverMapApi()
        self.api_word = []
    
    # 주소 인근 단어 추출
    def for_api(self, data_list):
        result = []
        temp = ''
        separate = 'on'
        # 주소 값이 아닐 경우, on(주소 이후 단어일 경우): 추가 / off(처음으로 오는 단어일 경우): 버림
        # 주소 값일 경우, on/off 둘다 추가, 하지만 off일 때 주소 값이 왔다면 on으로 변경(시작임을 알림)
        # '경기도 광주 삼겹살 식당' -> '경기도 광주 삼겹살'까지 저장

        for item_list in data_list:
            for item in item_list:
                if self.check.get(item) == -1:
                    if separate == 'on':
                        temp += item
                        result.append(temp)
                        temp = ''
                        separate = 'off'
                    else:
                        pass
                else:
                    if separate == 'on':
                        temp += item
                    else: 
                        temp += item
                        separate = 'on'
        return result
        
    def Pre_Processing(self, crawling_list):
        # 특수 문자 제거
        special_charavters = '!@#$%^&*()_+<>?:"{}|[];\',.'

        for item in crawling_list:
            for key, value in item.items():
                for char in special_charavters:
                    value = value.replace(char, ' ')
                item[key] = value

        # 사용할 데이터 추출
        title = []
        preview = []
        content = []
        for item in crawling_list:
            if 'title' in item:
                title.append(item['title'].split())
            elif 'preview' in item:
                preview.append(item['preview'].split())
            elif 'content' in item:
                content.append(item['content'].split())
            else:
                pass
        
        # 주소 관련 단어인지 확인 및 인근 단어 추출
        self.api_word.extend(self.for_api(title))
        self.api_word.extend(self.for_api(preview))
        self.api_word.extend(self.for_api(content))

        # naver api
        address_dic = {}
        roadAddress_dic = {}
        for item in self.api_word:
                    address, roadAddress = self.api.get(item)
                    if address is None or roadAddress is None:
                        pass
                    else: 
                        address_dic[item] = address
                        roadAddress_dic[item] = roadAddress
        
        return address_dic, roadAddress_dic

    def start(self, image_text):
        
        crawling_list = self.crawler.start(image_text)
        result_add, result_road = self.Pre_Processing(crawling_list)
        return result_add, result_road

if __name__ == "__main__":
    data = Data_PreProcessing()
    image_text = "성북구 동선동 2가 에그맛있다"
    result_add, result_road = data.start()
    print("address: \n", result_add)
    print("\n")
    print("road address: \n", result_road)
