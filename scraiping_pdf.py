#-*-coding:utf-8-*-

from urllib import request
from bs4 import BeautifulSoup
import requests
import os

WRITE_DIR = "./pdf_b4_2017/"
if os.path.exists(WRITE_DIR) == False:
    os.mkdir(WRITE_DIR)

def get_pdf(soup):
    pdf_list = []
    for a in soup.find_all('a'):
        if isinstance(a.get('href'), str) == True:
            if "pdf" in str(a.get('href')):
                pdf_list.append(a.get('href'))
    return pdf_list

if __name__ == '__main__':

    #url = "http://www.nuie.nagoya-u.ac.jp/******/****/"

    html = request.urlopen(url).read()
    soup = BeautifulSoup(html, 'html.parser')
    pdf_list = get_pdf(soup)
    
    for pdf_file in pdf_list:
        file_name = pdf_file.split("/")[-1]
        req = requests.get(url+file_name)
        if req.status_code == 200:
            print(req)
            with open(WRITE_DIR+file_name, "wb") as fwrite:
                fwrite.write(req.content)
    
