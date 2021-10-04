from bs4 import BeautifulSoup
import requests
import lxml


#headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/601.3.9 (KHTML, like Gecko) Version/9.0.2 Safari/601.3.9'}

headers = {'User-Agent':'Mozilla/5.0 (iPhone; CPU iPhone OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 Safari/601.3.9'}


url = 'https://www.booking.com/searchresults.es.html?ac_click_type=b&ac_position=0&checkin_month=9&checkin_monthday=5&checkin_year=2021&checkout_month=9&checkout_monthday=6&checkout_year=2021&class_interval=1&dest_id=-389593&dest_type=city&dtdisc=0&from_sf=1&group_adults=2&group_children=0&iata=RJL&inac=0&index_postcard=0&label=gen173nr-1DCAEoggI46AdIM1gEaEaIAQGYAQq4ARfIAQzYAQPoAQH4AQOIAgGoAgO4Ar6404kGwAIB0gIkOGUwZGQ2MTQtZGY1Mi00YTdkLTg2MjctZTM1NTQ4MGJlOTFl2AIE4AIB&label_click=undef&logged_out=1&no_rooms=1&offset=0&postcard=0&raw_dest_type=city&room1=A%2CA&sb_price_type=total&search_selected=1&shw_aparth=1&sid=83b597818f2aeaaa4955941a88e07bea&slp_r_match=0&src=index&src_elem=sb&srpvid=0a3469e62c270050&ss=Logro%C3%B1o%2C%20La%20Rioja%2C%20Espa%C3%B1a&ss_all=0&ss_raw=logro%C3%B1o&ssb=empty&sshis=0&ssne=Aranjuez&ssne_untouched=Aranjuez&tmpl=searchresults&top_ufis=1'
response=requests.get(url,headers=headers)
soup=BeautifulSoup(response.content,'lxml')

#print(soup)
#print(soup.select('.a-carousel-card')[0].get_text())
"""for item in soup.select('.sr_property_block'):
    #print(item)
    try:
        print('----------------------------------------')
        print('----------------------------------------')
        print(item.select('.sr-hotel__name')[0].get_text().strip())
        print(item.select('.bui-u-sr-only')[1].get_text().strip())
        print(item.select('.bui-badge__text')[0].get_text().strip())


    except:
        pass"""



for item in soup.select('._9e8b1151c5'):
    print('ey')
    #print(item)

    print('----------------------------------------')
    print('----------------------------------------')
    print(item)
    """print(item.select('.bui-u-sr-only')[1].get_text().strip())
    print(item.select('.bui-badge__text')[0].get_text().strip())"""
