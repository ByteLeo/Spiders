import requests
from bs4 import BeautifulSoup
from pyecharts import Bar

All_DATA = []

def parse_page(url):
    headers = {
        'User-Agent':"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36"
            }#检查网页获得headers伪装自己，防止网页反爬虫机制
    response = requests.get(url,headers = headers)#获取网页
    #print(response.content.decode('utf-8'))
    text = response.content.decode('utf-8')#网页内容解码
    # soup = BeautifulSoup(text,'lxml')#BS包装（方便操作网页标签内容）
    soup = BeautifulSoup(text, 'html5lib')#html5lib能够自动补齐不规范的缺失标签
    conMidtab = soup.find('div',class_ = 'conMidtab')#查找第一个div标签，且class属性为conMidtab，表格数据标签在此标签下
    # print(conMidtab)
    tables = conMidtab.find_all('table')#找出conMidtab标签下所有的table标签

    for table in tables:
        # print(table)
        # print('==='*20)
        trs = table.find_all('tr')[2:]#过滤table下前两个不含城市信息tr标签
        for index,tr in enumerate(trs):
            # print(tr)
            # print('=='*30)
            tds = tr.find_all('td')#找出tr标签下所有td标签
            city_td = tds[0]#城市名称在第0个td中
            if index == 0:
                city_td = tds[1]#特殊：第0个tr标签中城市名称在第1个td标签中
            city = list(city_td.stripped_strings)[0]#取列表元素
            # print(list(city_td.stripped_strings)[0])
            # 或 print(city_td.text.split()[0])
            # print(city)
            #stripped_strings：用来获取目标路径下所有的子孙非标签字符串，会自动去掉空白字符串，返回的是一个生成器
            #stripped_strings一下子能取出对应目录下的所有文本，并且自动把空白去掉

            temp_td = tds[-2]#最低温度信息在倒数第二个td标签中
            min_temp = list(temp_td.stripped_strings)[0]
            All_DATA.append({'city':city,'min_temp':min_temp})
            #print({'city':city,'min_temp':min_temp})
        #break
def main():
    #url = 'http://www.weathner.com.cn/textFC/hb.shtml'
    #url = 'http://www.weather.com.cn/textFC/gat.shtml'
    basic = 'http://www.weather.com.cn/textFC/'
    rgs = ['hb','db','hz','hn','hd','xb','xn','gat']#地区
    for index,rg in enumerate(rgs):
        url = basic + rgs[index] + '.shtml'#拼接
        parse_page(url)

    #分析数据
    #最低气温排序
    # def sorr_key(data):
    #     min_temp = int(data['min_temp'])
    #     return min_temp
    #
    # All_DATA.sort(key = sorr_key)

    All_DATA.sort(key = lambda data:int(data['min_temp']))
    #lambda函数： ：前为传入参数，：后为返回值

    data = All_DATA[:10]
    cities = []

    # for city_temp in data:
    #     city = city_temp['city']
    #     cities.append(city)

    # map()会根据提供的函数对指定序列做映射。第一个参数 function 以参数序列中的每一个元素调用 function 函数，返回包含每次 function 函数返回值的新列表。
    cities = list(map(lambda x : x['city'], data)) #提取列表data中的城市名称
    temps = list(map(lambda x: x['min_temp'], data))#提取列表data中的最低温度

    chart = Bar("中国最低气温排行榜")
    chart.add('',cities,temps)
    chart.render('temperature.html')
    print(data)

if __name__=='__main__':
    main()

#补充知识点：
#若去温度中'℃'，用replace函数 x.replace('℃','')，若类型为列表，用map函数对单个元素操作
