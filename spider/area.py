# coding: utf8

import json
import os
import sys
import datetime
from SpiderBase import SpiderBase
from traceback import format_exc
from bs4 import BeautifulSoup
CUR_PATH = os.path.dirname(os.path.abspath(__file__))

class Area(SpiderBase):

      def __init__(self):
            super(Area, self).__init__()
            self.area_url = 'http://www.ziroom.com/z/nl/z3.html'
            self.peizhihzong_url = 'http://img.ziroom.com/pic/static/images/slist_1207/defaultPZZ/misu-loading.jpg_C_264_198_Q80.jpg'

      def get_area(self):
            html = self.http_get(self.area_url)
            soup = BeautifulSoup(html, "html.parser")
            filterList = soup.find_all(attrs={'class': 'filterList'})[0]
            district_list = filterList.find_all('li')
            area_data = {}
            for district in district_list:
                  district_name = district.a.string
                  district_url = 'http:' + district.a['href']
                  area_data[district_name] = {}
                  area_data[district_name]['url'] = district_url
                  area_data[district_name]['areas'] = {}
                  if district.div is None:
                        continue
                  areas = {}
                  for area in district.div.find_all('span'):
                        data = {}
                        area_name = area.a.string
                        area_url = 'http:' + area.a['href']
                        areas[area_name] = area_url
                  area_data[district_name]['areas'] = areas
            with open(CUR_PATH + '/areas.txt', 'w')as f:
                  txt = json.dumps(area_data, ensure_ascii=False, indent=4)
                  f.write(txt.encode('utf8'))

      def search_area(self,url,filepath):
            house_list = []
            next_page_url = url
            while next_page_url != None:
                  print "get %s" % next_page_url
                  html = self.http_get(next_page_url)
                  soup = BeautifulSoup(html, "html.parser")
                  next_page = soup.find_all(attrs={'class': 'pages'})[0].find_all(attrs={'class': 'next'})
                  if len(next_page) > 0:
                        next_page_url = 'http:' + next_page[0]['href']
                  else:
                        next_page_url = None
                  houseList = soup.find_all(attrs={'id': 'houseList'})[0]
                  houses = houseList.find_all('li')
                  for house in houses:
                        try:
                            house_img = 'http:' + house.a.img['_src']
                            house_url = 'http:' + house.h3.a['href']
                            house_name = house.h3.string.replace(' ','').split(u'·')
                            house_area = house.h4.string.strip(' ')
                            detail = house.find_all(attrs={'class': 'detail'})[0]
                            house_info = detail.find_all('span')
                            house_acreage = house_info[0].string
                            house_floor = house_info[1].string.replace(u'层','').replace(' ','').split('/')
                            house_type = house_info[2].string
                            if len(house_info)> 3:
                                  house_other = '|'.join((i.string for i in house_info[3:] if i.string is not None))
                            else:
                                  house_other = None
                            house_tags = []
                            room_tags = house.find_all(attrs={'class': 'room_tags'})[0]
                            for tag in room_tags.find_all('span'):
                                  house_tags.append(tag.string)
                            price = house.find_all(attrs={'class': 'price'})[0]
                            house_price = price.contents[0].strip('\n')
                            house_pay_type = price.span.string
                            house = {}
                            house['peizhizhong'] = 1 if 'misu-loading' in house_img else 0
                            house['keyuding'] = 1 if 'misu-loading' not in house_img else 0
                            house['url'] = house_url
                            house['brand'] = house_name[0]
                            house['position'] = house_name[1]
                            house['orientation'] = house_name[1].split('-')[-1]
                            house['area'] = house_area
                            house['acreage'] = float(house_acreage.strip(u' ㎡约'))
                            house['house_floor'] = int(house_floor[0])
                            house['sum_floor'] = int(house_floor[1])
                            house['bedrooms'] = int(house_type.split(u'室')[0])
                            house['type'] = house_type
                            house['other'] = house_other
                            house['tags'] = house_tags                        
                            house['pay_type'] = u'按月' if u'月' in house_pay_type else u'按天'
                            house['price'] = int(house_price.replace(' ','').strip(u'￥'))
                            if house['pay_type'] == u'按天':
                                  house['price'] *= 30
                            house_list.append(house)
                        except:
                        	print format_exc()
            with open(filepath, 'w')as f:
                  txt = json.dumps(house_list, ensure_ascii=False, indent=4)
                  f.write(txt.encode('utf8'))

      def search_all(self):
            now = datetime.datetime.now().strftime("%Y%m%d:%H")

            with open(CUR_PATH + '/areas.txt', 'r')as f:
                  data = json.loads(f.read())
            for district_name,district in data.items():
                path = '%s/data/%s/%s' % (CUR_PATH, now, district_name)
                if not os.path.exists(path):
                    os.makedirs(path)
                for area_name, url in district['areas'].items():
                	print district_name, area_name
                	if area_name == u'全部':
                		continue
                  filepath = "%s/%s.json" % (path,area_name)
                	self.search_area(url, filepath)





if __name__ == '__main__':
      area = Area()
      # area.get_area()
      area.search_all()