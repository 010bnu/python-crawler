import scrapy
import datetime

def get_date(date):
    # parm: '2017-01-03'
    # rtype: '2017-01-04'
    date=datetime.datetime.strptime(date,'%Y-%m-%d')
    date+=datetime.timedelta(days=1)
    date=str(date).split(' ')[0]
    return date
    
class NewsPapers(scrapy.Spider):
    name="newspapers"
    
    def start_requests(self):
        url='http://navi.cnki.net/knavi/NPaperDetail/GetArticleDataXsltByDate'
            
        headers={'Host': 'navi.cnki.net', 'Connection': 'keep-alive','Accept': '*/*', 'Origin': 'http://navi.cnki.net', 'X-Requested-With': 'XMLHttpRequest', 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36', 'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8', 'Referer': 'http://navi.cnki.net/knavi/NPaperDetail?pcode=CCND&bzpym=GMRB', 'Accept-Encoding': 'gzip, deflate', 'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7', 'Cookie': 'Ecp_ClientId=5190122222701448691; cnkiUserKey=79f9941f-d5eb-fef7-42a9-c04b118d324a; Ecp_IpLoginFail=190305113.110.193.198; ASP.NET_SessionId=5u1kpwn2xgh5amvozqc5vzlm; SID_navi=120161; _pk_ref=%5B%22%22%2C%22%22%2C1551804652%2C%22http%3A%2F%2Fnavi.cnki.net%2Fknavi%2FNPaper.html%22%5D'}
        
        data={'py': 'GMRB', 'pcode': 'CCND', 'pageIndex': '1', 'pageSize': '20', 'date':'0'}
        date_start = datetime.datetime.strptime('2001-01-01','%Y-%m-%d')       
        date_end  =  datetime.datetime.strptime('2001-01-02','%Y-%m-%d')
        
        date=date_start
        while date<date_end:
            
            date_str=str(date).split(' ')[0]
            data['date']=date_str
            date+=datetime.timedelta(days=1)
            yield scrapy.FormRequest(url,callback=self.parse,method='post',formdata=data,headers=headers)
            
    def parse(self,response):
        for href in response.css('td.name a::attr(href)'):
            s=href.extract()
            dbCode,filename,dbname=list(map(lambda x:x.split('=')[-1],s.split('?')[-1].split('&')))[1:]
            tmp_url='http://kns.cnki.net/kcms/detail/detail.aspx?dbcode=%s&filename=%s&dbname=%s' % (dbCode,filename,dbname)
            print(tmp_url)
            yield scrapy.Request(tmp_url,callback=self.parse_content)
            
     
    def parse_content(self,response):
        title=response.css('div.wxTitle >h2::text').extract()
        info=response.css('div.wxBaseinfo >p::text').extract()
        
        print(info,title)
        # print(title,DATE)