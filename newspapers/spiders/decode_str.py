import requests
import re
from bs4 import BeautifulSoup

def decode_str(s):

    pattern=re.compile('\.%s\{background:-(\d{1,4})\.0px -(\d{1,4})\.0px;\}' % s)
    with open('./meituan.txt','r') as f:
        x,y=pattern.findall(f.read())[0]
    if 'oul' in s:
        with open('./numbers.svg','r') as f:
            text=f.read()            
    elif 'pzs' in s:
        with open('./word.svg','r',encoding='utf8') as f:
            text=f.read()
    
    pattern1=re.compile('y="(\d{1,4})"')
    l=pattern1.findall(text)
    l.append(y)
    l=list(map(int,l))
    l=sorted(l)    
    
    #插入后排序找到第几行,然后由列的位置得到
    soup=BeautifulSoup(text,'lxml')
    return soup.select('text')[l.index(int(y))].text[int(x)//14]

if __name__=='__main__':
    print(decode_str('oul4ha'))
    print(decode_str('pzsxgh'))