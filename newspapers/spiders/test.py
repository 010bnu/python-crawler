# if __name__=='__main__':
    # from bs4 import BeautifulSoup
    # import re
    # from decode_str import decode_str
    # with open('test.html',encoding='utf8') as f:
        # s=f.read()
    # soup=BeautifulSoup(s,'lxml')        
    # soup=BeautifulSoup(response.text,'lxml')        
    # shop_name=soup.select_one('h1.shop-name').text.split(' ')[1] #店名
    # result=shop_name
    
    # def tihuan(s,label):
        # pattern=re.compile('<%s class="([a-z0-9]{6})"></%s>' % (label,label))
        # l=pattern.findall(s)
        
        # for tmp in l:
            # s=s.replace('<%s class="%s"></%s>' % (label,tmp,label),decode_str(tmp))
        # return s
    
    # ele=soup.select_one('div.brief-info')    
    # title=ele.select('span')[0].attrs['title']   #星级
    # i=0
    
    # for item in ele.select('span.item'):
        # tmp_soup=BeautifulSoup(tihuan(str(item),'d'),'lxml')            
        # result+=','+tmp_soup.select_one('span').text.split()[0 if i==0 else 1]  #评分
        # i+=1
    
    # tmp_soup=BeautifulSoup(tihuan(str(soup.select_one('span#address')),'e'),'lxml')
    # result+=','+tmp_soup.select_one('span').text     #地址
    
    # tmp_soup=BeautifulSoup(tihuan(str(soup.select_one('p.expand-info')),'d'),'lxml')
    # result+=','+tmp_soup.select_one('p').text.split(' ')[-2]  #电话
    
    # with open('dianping.csv',encoding='gbk','a') as f:
        # f.write(result+'\n')
    