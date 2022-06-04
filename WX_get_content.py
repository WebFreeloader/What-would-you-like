from bs4 import BeautifulSoup
import csv
import requests
import lxml
import re
import datetime
import WX_get_url
#读取保存的csv文件，并返回要爬取的url
def csv_read():
    csv_src_file='./shayoucanyin.csv'
    csv_file=open(csv_src_file,mode='r',encoding='utf-8')
    csv_reader=csv.reader(csv_file)
    column=[row[2] for row in csv_reader]
    return column
#对每个url进行爬取
def get_data(url_list):

    for i in range(len(url_list)):
        if (i==0):
            continue
        elif i%2==1:
            continue
        else:
            spiders(url_list[i])


def spiders(url):
    headers={
        'User - Agent': 'Mozilla / 5.0(WindowsNT10.0;Win64;x64;rv: 99.0) Gecko / 20100101Firefox / 99.0'
    }
    response=requests.get(url=url,headers=headers)
    with open('./页面源码.html',mode='w',encoding='utf-8') as f:
        f.write(response.text)
        select_tag('./页面源码.html')


def select_tag(file_str):
    with open(file_str,mode='r',encoding='utf-8') as f:
        target_dict={}
        soup=BeautifulSoup(f,'lxml')
        #获取食堂名称
        target_dona=soup.find('h1', {'class':"rich_media_title" ,'id':"activity-name"})
        dona_name=target_dona.text

        dona_name="".join(str(dona_name).split())
        #获取食堂各层名称
        layers=soup.select('section[style="text-align: center;color: rgb(124, 179, 66);letter-spacing: 2px;box-sizing: border-box;"]>p>strong')
        for item in layers:
            target_dict[item.text]={}

        #获取每一层的早、中、晚餐tag
        menu_tag=soup.select('span[style="font-size: 24px;box-sizing: border-box;"]')
        tem_list=[]
        tem_dict = {}
        for item in menu_tag:
            if '日菜品'in item.text:
                continue
            elif '晚餐' in item.text:
                tem_dict[item.text] = ''
                tem_list.append(tem_dict)
                tem_dict = {}
            elif '早餐'in item.text:
                tem_dict[item.text]=''
            elif '午餐' in item.text:
                tem_dict[item.text]=''
            elif '晚餐' in item.text:
                tem_dict[item.text] = ''
                tem_list.append(tem_dict)
                tem_dict = {}

        cout = 0  # 用来记录下标
        for key in target_dict.keys():      #保存每一层的早、中、晚餐tag
            target_dict[key]=tem_list[cout]
            cout+=1
       #获取所有的菜品
        target_mune1=soup.select('section[style="text-align: justify;box-sizing: border-box;"]>p[style="white-space: normal;box-sizing: border-box;"]')
        target_mune2 = soup.select('section[style="text-align: center;box-sizing: border-box;"]>p[style="text-align: left;box-sizing: border-box;"]')
        # target_mune3=soup.select('section[tyle="text-align: justify; box-sizing: border-box; visibility: visible;" powered-by="xiumi.us"]>p[style="white-space: normal;margin: 0px;padding: 0px;box-sizing: border-box;"]')
        # print(target_mune3)
        index1=[]


        for item in target_mune1:
            if ( '。')in item.text:
                index1.append(target_mune1.index(item))
        index1=index1[::-1]
        for i in index1:
            target_mune1.pop(i)

        temp_list1=[]
        target_mune1.extend(target_mune2)
        # target_mune1.extend(target_mune3)
        for item in target_mune1:
            temp_list1.append(item.text)

        index2=[]
        for i in range(1,len(temp_list1)):
            if '\xa0' in temp_list1[i]:
                temp_list1[i-1]=temp_list1[i-1]+'、'+temp_list1[i]
                index2.append(i)
        index2=index2[::-1]
        #逆序删除
        for i in index2:
            temp_list1.pop(i)
        #清除多余的\xa0、\n
        for i in range(len(temp_list1)):
            temp_list1[i]=temp_list1[i].strip(' ')
            temp_list1[i]=temp_list1[i].replace('\xa0','、')
            temp_list1[i]="".join(temp_list1[i].split())

        count = 0
        try:
            for keys ,value in target_dict.items():
                for key in value.keys():
                    target_dict[keys][key]=temp_list1[count]
                    count+=1
        except IndexError:
            pass

        # 供餐时间
        # eat_time_tag=soup.find(attrs={'name':"description"})
        # time_data=eat_time_tag.attrs['content']
        # print(time_data)
        # regex=re.compile(r'\d{1,2}:(\s)*\d\d-\d{1,2}:(\s)*\d\d')
        # regex_data=regex.findall(time_data)
        # print(regex_data)

        # 时间戳
        try:
            target_time = soup.find('span', style="font-size: 24px;box-sizing: border-box;").text
            regex = re.compile(r'^[0-9]\.\d{1,2}')  #用正则表达式来进行字符串的匹配
            regex_qie = regex.findall(target_time)
            # 获得月、日
            mon_day = regex_qie[0]
            menu_day = str(datetime.datetime.now().strftime('%Y')) + '.' + str(mon_day)  #加上年份
            target_dict['时间'] = menu_day
            target_dict['食堂'] = dona_name
            total_datalist.append(target_dict)
            f.close()
        except AttributeError:
            pass
def change(pre_datalist):
    new_datalist=[]
    for day in pre_datalist:
        for key,value in day.items():
            if key=='时间':
                break
            else:
                for key_item,value_item in value.items():
                    temp_value_item=re.split('、|，',value_item)
                    for blank in temp_value_item:
                        if blank=='':
                            temp_value_item.remove(blank)
                    for str_item in temp_value_item:
                        item = []
                        item.append(day['时间'].replace('.','-'))
                        item.append(day['食堂'][:2]+key[:6])
                        item.append(str_item)
                        item.append(key_item)
                        new_datalist.append(item)
    return new_datalist


if __name__=='__main__':
    total_datalist=[]
    # 调用get_url()启动爬虫
    url_obj = WX_get_url.get_url()
    #调用csv_read()读取url
    url_list=csv_read()
    #循环调用get_data()来抓取每一天的菜单
    get_data(url_list)
    #数据整理
    new_total_datalist=change(total_datalist)
    #打印最终的总数据列表
    print(new_total_datalist)


