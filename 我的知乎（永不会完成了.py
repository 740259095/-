import requests
import re
import time
import os
import json
import rk


class login():
    def __init__(self,username,password):
        self.username=username
        self.password=password

    def get_xsrf(self,header,url):
        pattern = r'name="_xsrf" value="(.*?)"'
        response=session.get(url,headers=header,allow_redirects=False)
        self.Xsrf=re.findall(pattern,response.text)#这样行吗,还有正则仍然不会写
        return self.Xsrf[0]

    def req(self,postdata,header):
        url='http://www.zhihu.com/login/email'
        captchaurl='https://www.zhihu.com/captcha.gif?r='+str(int(time.time()*1000))+"&type=login"
        captcha=session.get(captchaurl,headers=header)
        with open('a.jpg','wb') as f:
            f.write(captcha.content)
            f.close()
        im = open('a.jpg', 'rb').read()
        rc=rk.RClient('***', '***','***','***')
        captchanum=rc.rk_create(im,3040)
        print(captchanum['Result'])
       # postdata.update({'captcha':str(captchanum['Result'])})
        #login_page=session.get(url,data=postdata,headers=header)
        #setting=session.get('https://www.zhihu.com/settings/profile',headers=header,allow_redirects=False)
        login_page = session.post(url, data=postdata, headers=header)
        if(1):
            captchaurl = 'https://www.zhihu.com/captcha.gif?r=' + str(int(time.time()*1000)) + "&type=login"
            captcha=session.get(captchaurl,headers=header)
            with open('a.jpg','wb') as f:
                f.write(captcha.content)
                f.close()
            im = open('a.jpg', 'rb').read()
            rc=rk.RClient('***', '***','***','***')
            captchanum=rc.rk_create(im,3040)
            print(captchanum['Result'])
            postdata.update({'captcha':str(captchanum['Result'])})
            login_page=session.get(url,data=postdata,headers=header)
            setting=session.get('https://www.zhihu.com/settings/profile',headers=header,allow_redirects=False)
            print(setting)
        print(login_page)



session=requests.Session()
agent = 'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:41.0) Gecko/20100101 Firefox/41.0'
header = {
    "Host": "www.zhihu.com",
    "Referer": "https://www.zhihu.com/",
    'User-Agent': agent
}
url='https://www.zhihu.com'


if(__name__=='__main__'):
    zhihu=login('***','***')
    postdata={'_xsrf': zhihu.get_xsrf(header,url),'password':zhihu.password,'captcha_type':'cn','email':zhihu.username}
    header['X-Xsrftoken']=zhihu.Xsrf[0]
    header['X-Requested-With']='XMLHttpRequest'
    zhihu.req(postdata,header)