#-*-coding:utf-8-*- 

import MeCab
from collections import Counter
from glob import glob
import neologdn
import json
import re
import os
import argparse

#READ_FILE_LIST = ['./text_dir/A1-1.txt']
#READ_FILE_LIST = glob('./text_dir/*')
READ_FILE_LIST = ['./text_b4_2017/all.txt']

WRITE_DIR = './ana_b4_2017/'
if not os.path.exists(WRITE_DIR):
    os.mkdir(WRITE_DIR)

def get_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-n', dest='n', type=int, default=1, metavar='NUM',help='n is ngram param')
    parser.add_argument('-fl', dest='fl', type=str , default="ngram", metavar='FLAG_LAST',help='fl is flag_last.')
    return parser

def text2mecab(text):
    text = neologdn.normalize(str(text))
    chasen = MeCab.Tagger("-Ochasen")
    chasen_list = chasen.parse(text)
    chasen_list = chasen_list.split("\n")
    word_list = []
    for cha_list in chasen_list:
        cha_list = cha_list.split("\t")
        if len(cha_list) > 2:
            word_list.append(cha_list[0])
    return word_list

def remove_word(word_list):    
    new_word_list = []
    for word in word_list:
        word = re.sub('[，,]','、',word)
        word = re.sub('[．.]','。',word)
        len_ja = len(re.findall('[0-9a-zA-Zぁ-んァ-ヶ一-龥々ー、。]', word))
        if len(word) != (len_ja):
            continue
        new_word_list.append(word)
    return new_word_list

def make_ngram(word_list,n,flag_last):
    
    new_word_list = []
    if n == 1:
        new_word_list = word_list
    else:
        for i in range(len(word_list[:1-n])):
            
            new_word = ""
            for j in range(n):
                new_word += word_list[i+j-1]

            flag_pass = 0

            if flag_last != "ngram":
                if new_word[-1] not in re.findall('[、。]', new_word):
                    flag_pass = 1 
            for j in range(len(new_word)-1):
                if len(re.findall('[、。]', new_word[j])) == 1 and len(re.findall('[、。]', new_word[j+1])) == 1:
                    flag_pass = 1
                    break

            if flag_pass == 1:
                continue
            
            new_word_list.append(new_word)

    return new_word_list


if __name__ == '__main__':

    n = get_parser().parse_args().n
    flag_last = get_parser().parse_args().fl
    
    all_word_list = []
    for i, read_file in enumerate(READ_FILE_LIST):

        with open(read_file,"r") as fread:
            read_text_list = fread.readlines()

        for read_text in read_text_list:
            word_list = text2mecab(read_text)
            word_list = remove_word(word_list)
            all_word_list += make_ngram(word_list,n,flag_last)

    counter = Counter(all_word_list)
    index_dict = {}
    for index, (word, count) in enumerate(counter.most_common()):
        if count < 2:
            continue
        index_dict[word] = (index,count)
    
    print(index_dict)
    with open(WRITE_DIR+"analize_"+str(n)+"_"+str(flag_last)+".json","w") as fwrite:
        json.dump(index_dict, fwrite, indent = 4, ensure_ascii = False)
