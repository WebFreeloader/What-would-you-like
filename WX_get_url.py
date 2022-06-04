#导入模板
import requests
import json
import time
import pandas as pd

#利用抓包工具获取所要爬取的公众号的所要文章的title和url
def get_url():
    src_url = 'https://mp.weixin.qq.com/cgi-bin/appmsg'
    fakeid = {
        'MzU4NzI3ODUyNA==': '沙邮餐饮'
    }
    token = {
        '1050138792'
    }

    headers = {
        'Cookie': "appmsglist_action_3901346583=list; ua_id=unqrVz1QTAxFUIvUAAAAAKSTOn7O_IBOTJW1TPBrGzw=; wxuin=48450629280870; xid=baadbf365977cfc0a6c9583989bfbb76; mm_lang=zh_CN; pgv_pvid=9656808516; RK=ZusdQHikcX; ptcz=789e0bd5016e16f9568428c6c8b691a7dfcdc9130b0bc0adb3cf309f4ab68e0b; uuid=4352e25686c2c3b5996e46a04d70b248; rand_info=CAESIEFgMnjZWye+Uud33hMo/ZUK/qLh1xS6DrjLk2DDKWhW; slave_bizuin=3901346583; data_bizuin=3901346583; bizuin=3901346583; data_ticket=DT8CjV16ArZS/suemr1/eiw36mcLi8XLb2vB3xn0WDOVRZwtFFvMmWpVq/tDjQwY; slave_sid=MVZISlBSbDZiZ3QyWE9YckxabGNpR0JiN1BJUGk1YWdHZW5fUFpDckhVMlBSaHlXSHNpR1psVTlyODdfM3VxVmJVNnpvY0tLd3pHZEZlTllTME5QTUhRWjJyTGc0RlVkVEhsN2d5RndDRGh4OHh1RUlnNm9DZnNuRjFQOUthS1dBVjZFczFBYUlMTlo3QlJW; slave_user=gh_f292c2b438f1",
        'User - Agent': 'Mozilla / 5.0(WindowsNT10.0;Win64;x64;rv: 99.0) Gecko / 20100101Firefox / 99.0'
    }
    data = {
        "token": token,
        "lang": "zh_CN",
        "f": "json",
        "ajax": "1",
        "action": "list_ex",
        "begin": '0',
        "count": "5",
        "query": "",
        "fakeid": fakeid,
        "type": "9",
    }
    content_list = []
    for i in range(1):
        data['begin'] = i * 8
        time.sleep(3)
        try:
            content_json = requests.get(url=src_url, headers=headers, params=data).json()
        except requests.exceptions.ConnectionError:
            print('ConnectionError')
        except requests.exceptions.ChunkedEncodingError:
            print('ChunkedEncodingError')
        else:
            print('That is good,no error!')

        #print(content_json)
        for item in content_json["app_msg_list"]:
            items = []
            items.append(item['title'])
            items.append(item["link"])
            content_list.append(items)
    name = ['title', 'link']
    test = pd.DataFrame(columns=name, data=content_list)
    test.to_csv('shayoucanyin.csv', mode='w', encoding='utf-8')