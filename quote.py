import requests
from bs4 import BeautifulSoup
import json

sec_links = []
title = []
quotes = []
quotedict = {}
authors = []
links = []
#Change the value of 'j' to resume an interrupted execution. Check the last index in quote.json
j = 0 
clean_links = []

def get_json(quotes, authors):
    global j
    for i in range(len(quotes)):
        try:
            quotedict[j] = {'quote' : quotes[i],
                        'author' : authors[i]
            }
            j = j + 1
        except IndexError:
            pass
    outfile = open('quote.json','w+')
    json.dump(quotedict, outfile)

def get_quotes(quotes_url):
    print(quotes_url)
    quotes = []
    authors = []
    response = requests.get(quotes_url)
    soup = BeautifulSoup(response.text,'html.parser')
    quote_soup = soup.find_all('a',{'title':'view quote'})
    author_soup = soup.find_all('a',{'title':'view author'})
    for elem in quote_soup:
        quotes.append(elem.text)
    for elem in author_soup:
        authors.append(elem.text)
    get_json(quotes,authors)

def get_alpha(sec_url):
    links = []
    response = requests.get(sec_url)
    soup = BeautifulSoup(response.text,'html.parser')
    title_soup = soup.find_all('div',{'class':'bqLn'})
    for elem in title_soup:
        link = elem.find_all('a', href=True)
        try:
            links.append('https://www.brainyquote.com' + link[0].get('href'))
        except IndexError:
            pass
    links.remove('https://www.brainyquote.com/')
    for i in range(-20,0):
        del links[i]
    print("This link will take some time...... Wait")
    for quotes_url in links:
        get_quotes(quotes_url)

def main():
    url = "https://www.brainyquote.com/topics"
    response = requests.get(url).text
    soup = BeautifulSoup(response,'html.parser')
    category_soup = soup.find_all('div',{'class':'bqLn'})
    for elem in category_soup:
        link = elem.find_all('a', href=True)
        try:
            sec_links.append('https://www.brainyquote.com' + link[0].get('href'))
            title.append(link[0].text)
        except IndexError:
            pass
    for i in range(496,475,-1):
        del sec_links[i]
    for i in sec_links: 
        if i not in clean_links: 
            clean_links.append(i) 
    for link in clean_links:
        #Uncomment if you want to resume an interrupted execution. Replace "num" with the last link index.
        '''if clean_links.index(link) < num:
            pass
        else:'''
        print("Turn of", clean_links.index(link), "out of ", len(clean_links))
        if clean_links.index(link) <= 121:
            get_quotes(link)
        else:
            get_alpha(link)

main()
