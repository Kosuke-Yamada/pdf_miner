#-*-coding:utf-8-*- 

from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from io import StringIO
from glob import glob
import os

READ_FILE_LIST = glob('./pdf_b4_2017/*') # PDFファイル取り込み
WRITE_DIR = './text_b4_2017/'
if not os.path.exists(WRITE_DIR):
    os.mkdir(WRITE_DIR)

print(READ_FILE_LIST)

def pdf2text(path):
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    laparams = LAParams()
    laparams.detect_vertical = True # Trueにすることで綺麗にテキストを抽出できる
    device = TextConverter(rsrcmgr, retstr, codec='utf-8', laparams=laparams)

    interpreter = PDFPageInterpreter(rsrcmgr, device)
    device.close()

    pagenos = set()
    with open(path, 'rb') as fread:
        for page in PDFPage.get_pages(fread, pagenos, maxpages=0, caching=True, check_extractable=True):
            interpreter.process_page(page)
            all_text = retstr.getvalue()
    retstr.close()

    return all_text

if __name__ == '__main__':

    result_list = []
    file_name_list = []
    for read_path in READ_FILE_LIST:
        result_text = pdf2text(read_path)

        write_file = WRITE_DIR+read_path.split('/')[-1].split('.')[0]+".txt"
        with open(write_file, 'w') as fwrite:
            fwrite.write(result_text)
        
        result_list.append(result_text)
    all_text = ','.join(result_list) # PDFごとのテキストが配列に格納されているので連結する

    with open(WRITE_DIR+'all.txt', 'w') as fwrite: #書き込みモードでオープン
        fwrite.write(all_text)
