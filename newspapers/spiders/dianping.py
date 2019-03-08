import scrapy
from bs4 import BeautifulSoup
from .decode_str import decode_str
import re

class DianPing(scrapy.Spider):
    name='dianping'
    
    def start_requests(self):
        
        headers={'Host': 'www.dianping.com', 'Connection': 'keep-alive', 'Cache-Control': 'max-age=0', 'Upgrade-Insecure-Requests': '1', 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36', 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8', 'Referer': 'http://www.dianping.com/', 'Accept-Encoding': 'gzip, deflate', 'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7'}
        
        # url='https://www.dianping.com/search/keyword/7/'  #小吃         
        # keyword=getattr(self,'keyword',None)    #设置参数
        # if keyword is not None:
            # url = url +'0_' + keyword
            
        url='http://www.dianping.com/search/keyword/7/0_%E5%B0%8F%E5%90%83'
        yield scrapy.FormRequest(url=url,callback=self.parse,headers=headers,cookies={'s_ViewType':'10','s_ViewType':'10'})
        
    def parse(self,response):
        
        headers={'Host': 'www.dianping.com', 'Connection': 'keep-alive', 'Upgrade-Insecure-Requests': '1', 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36', 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8', 'Referer': 'http://www.dianping.com/', 'Accept-Encoding': 'gzip, deflate, br', 'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7', 'Cookie': '_lxsdk_cuid=1638c782a28c1-060b7078f17cd1-737356c-f0000-1638c782a2b6; _lxsdk=1638c782a28c1-060b7078f17cd1-737356c-f0000-1638c782a2b6; _hc.v=77a57625-077f-9d19-f06c-52f3eaf1daaf.1527070078; Hm_lvt_e6f449471d3527d58c46e24efb4c343e=1535963577; __utma=1.400172591.1543659040.1543659040.1543659040.1; __utmz=1.1543659040.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); cy=7; cye=shenzhen; _lx_utm=utm_source%3Dbing%26utm_medium%3Dorganic; s_ViewType=10; _dp.ac.v=8517687d-de87-4910-b573-649ba38e2202; dper=05de58eb7fe5840a0d1fe7a6b16b45aee87f45a5c1ac17e8d001715e442f82e707556b2d5942398b325eab563ba236b9229327e1e48b95fbd96ad1360055000679edfb531fe30883be194e101696cc22c45e36aeb837c89f2456a38e3edcf2b8; ua=%E5%85%AD%E5%85%AD%E5%85%AD12; ctu=c38fc82dbd6baaa96bf64718b9f32f793e7dcb70ee6575760c7c2561ecccf1d6; ll=7fd06e815b796be3df069dec7836c3df; _lxsdk_s=1695cc841c7-4d5-e20-a25%7C%7C77'}
        
        hrefs=response.css('div.tit a::attr(href)').extract()
        
        # for title in response.css('div.tit h4::text').extract():
            # print(title)
            
        for href in hrefs:
            if not 'waimai' in href:    #去掉同一家店的两个链接
                yield scrapy.FormRequest(url=href,callback=self.parse_content,headers=headers)
        
        next_page = response.css('a.next::attr(href)').extract_first()   #下一页
        if next_page is not None:
            yield scrapy.FormRequest(next_page,callback=self.parse,headers=headers)
            
    def parse_content(self,response):        
        soup=BeautifulSoup(response.text,'lxml')        
        shop_name=soup.select_one('h1.shop-name').text.split(' ')[1] #店名
        result=shop_name
        
        def tihuan(s,label):
            pattern=re.compile('<%s class="([a-z0-9]{6})"></%s>' % (label,label))
            l=pattern.findall(s)
            for tmp in l:
                s=s.replace('<%s class="%s"></%s>' % (label,tmp,label),decode_str(tmp))
            return s
        
        ele=soup.select_one('div.brief-info')    
        title=ele.select('span')[0].attrs['title']   #星级
        i=0
        
        for item in ele.select('span.item'):
            tmp_soup=BeautifulSoup(tihuan(str(item),'d'),'lxml')            
            result+=','+tmp_soup.select_one('span').text.split()[0 if i==0 else 1]  #评分
            i+=1
        
        tmp_soup=BeautifulSoup(tihuan(str(soup.select_one('span#address')),'e'),'lxml')
        result+=','+tmp_soup.select_one('span').text     #地址
        
        tmp_soup=BeautifulSoup(tihuan(str(soup.select_one('p.expand-info')),'d'),'lxml')
        result+=','+tmp_soup.select_one('p').text.split(' ')[-2]  #电话
        print(result)
        with open('./dianping.csv','a',encoding='gbk') as f:
            f.write(result+'\n')
        