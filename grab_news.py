from newspaper import Article
import nltk
import xml.etree.ElementTree as ET
import traceback
import requests
import sys
import jsonlines
from datetime import datetime
import time
from langdetect import detect

def get_links_from_rss_feed(link_to_rss_feed):
    list_of_articles = []
    try:
        raw = requests.get(link_to_rss_feed).text

        tree = ET.ElementTree(ET.fromstring(raw))

        root = tree.getroot()

        for child in root.findall('./channel/item'):
               for item in child:
                   if (item.tag == 'link'):
                       list_of_articles.append(item.text)
    except KeyboardInterrupt:
        raise
    except:
        pass
    return list_of_articles

def timeout_setter(ar,one=30):
    ar.config.request_timeout = one
    ar.config.thread_timeout_seconds = one
    return ar

def get_news_json_for_RSS(line):
    links = []
    jlines = []
    links = get_links_from_rss_feed(line)
    if links == []:
        return []
    for link in links:
        article = Article(link)
        article.download()
        article.parse()
        article.nlp()
        temp_dict = {}
        temp_dict["authors"] = article.authors
        temp_dict["publish_date"] = article.publish_date.strftime("%m/%d/%Y, %H:%M:%S")
        temp_dict["article_text"] = article.text
        temp_dict["keywords"] = article.keywords
        temp_dict["summary"] = article.summary
        jlines.append(temp_dict)
    return jlines

def grab_news_from_RSS(inputpath,outpath,opn='write'):

    all_links = []
    jlines = []

    with open(inputpath,'r') as filer:
        lines = filer.readlines()
        lines = [line.strip() for line in lines]


    # for line in lines:
    #     temp_list = get_links_from_rss_feed(line)
    #     if temp_list != []:
    #         all_links.append(temp_list)

    # print("Done Parsing XML_Files")

    with jsonlines.open(outpath,'w') as op:
        for i_1,rss_link in enumerate(lines):
            print('processing RSS link ',i_1)
            list_al = get_links_from_rss_feed(rss_link)
            for i,link in enumerate(list_al):
                # print(link)
                try:
                    t1 = time.time()
                    article = Article(link)
                    article = timeout_setter(article,100)
                    article.download()
                    article.parse()
                    article.nlp()
                    temp_dict = {}
                    temp_dict["authors"] = article.authors
                    if article.publish_date:
                        temp_dict["publish_date"] = article.publish_date.strftime("%m/%d/%Y, %H:%M:%S")
                    else:
                        temp_dict['publish_date'] = 'nil'
                    temp_dict["text"] = article.text
                    temp_dict["keywords"] = article.keywords
                    temp_dict["summary"] = article.summary
                    temp_dict['url'] = article.url
                    temp_dict['rss_link'] = rss_link
                    temp_dict['title'] = article.title
                    t2 = time.time()
                    
                    if article.title != '':
                        if(detect(article.title) != 'en'):
                            continue ## or whatever thing you wish to do in this case
                    if article.text != '':
                        if(detect(article.text) != 'en'):
                            continue ## or whatever thing you wish to do in this case
                    if(i%50 == 0):
                        print('time taken',str(t2-t1))
                    if(opn == 'write'):
                       op.write(temp_dict)
                    else:
                        jlines.append(temp_dict)
                except Exception as E:
                    print(E)
                    print(traceback.format_exc())
                    pass
    if (opn != 'write'):
        return jlines

def main():
    inputpath = sys.argv[1]
    outputpath = sys.argv[2]
    grab_news_from_RSS(inputpath,outputpath,'write')

if __name__ == '__main__':
    main()
