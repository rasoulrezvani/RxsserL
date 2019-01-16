from creepy import Crawler
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import urllib
import mechanize
import os
import time
from selenium.webdriver.common.keys import Keys
from Tkinter import *
#from PIL import ImageTk,Image
#from threading import Timer
#import multiprocessing

#Author : rasoul_rezvanijalal
#date : 17/12/2018
r = Tk()
r.geometry("300x280")
r.title("RxsserL")
r.configure(background="gray")
r.resizable(False,False)

def start():
    if len(str(t.get())) == 0:
        print "url input can't be empty"
    else:
        main_url = str(t.get())
        project_name = str(t1.get())
        file_name = project_name + ".txt"
        urls = []
        tags = []
        j = 1
        b = open("vulnerabilities.txt", "w")
        b.write("num       ")
        b.write("vulnerable url     " + "   ELEMENT ID " + "\n")
        b.write(
            "---------------------------------------------------------------------------------------------------------")
        b.close()

        class MyCrawler(Crawler):
            def process_document(self, doc):
                if doc.status == 200:
                    #print  str(doc.url) + "\n"
                    urls.append(doc.url)
                    f = open(file_name, "a")
                    if doc.url in open(file_name).read():
                        print "this url:" + urllib.unquote(doc.url).decode('utf8') + " exist in file"
                    else:
                        f.write(urllib.unquote(doc.url).decode('utf8') + "\n")

                    #we have  doc.text,doc.url,doc.status . use them as you need
                else:
                    pass

        crawler = MyCrawler()
        crawler.crawl(main_url)
        ##########################
        # urls gathering complete#
        ##########################

        print "urls listed in url.txt in your path"
        for url in urls:
            page = requests.get(url).text
            soup = BeautifulSoup(page, 'lxml')
            inputs = soup.findAll('input', attrs={'type': 'text'})

            if (len(inputs)) > 0:
                dr = webdriver.Firefox(log_path='geckodriver.log')
                dr.get(url)

                tags = dr.find_elements_by_css_selector(("input[type='text']"))
                #####################################################
                # find all related elements to xss means all "inputs"#
                #####################################################

                for i in range(len(tags)):

                    tags[i].send_keys("<script>document.write('hello how are you!');</script>")
                    tags[i].send_keys(Keys.ENTER)
                    time.sleep(2)
                    y = dr.page_source
                    if len(y) == 111:

                        dr.back()
                        print "a vulnerability found in " + url
                        op = open("vulnerabilities.txt", "a")
                        op.write("\n" + str(j) + "- \t")
                        op.write(url + "\t")
                        op.write(str(tags[i].get_attribute('id')))
                        op.close()
                        j = j + 1
                    else:
                        print "this url: " + url + " is safe"
                    ####################################
                    # test attack scenario for any input#
                    ####################################
                    time.sleep(2)
                dr.close()
        print ("it's done")
l = Label(r,text="Enter url: ",width=15,anchor=W,bg="gray").grid(row=0,column=0,pady=5)
t = Entry(r)
t.grid(row=0,column=1,pady=5,padx=4)
l1 = Label(r,text="Enter project name: ",width=15,anchor=W,bg="gray").grid(row=1,column=0,pady=10)
t1 = Entry(r)
t1.grid(row=1,column=1,pady=10,padx=4)


b = Button(r, height=1, width=10, text="start",bg="#42f474",borderwidth=0 ,command=start).grid(sticky=W+N+E+S,columnspan=2,pady=5)

b1 = Button(r, text='exit', command=r.destroy,bg="#ff2723",borderwidth=0).grid(sticky=W+N+E+S,columnspan=2)



r.mainloop()
