# import libraries
import urllib.request  as urllib2
from bs4 import BeautifulSoup
import csv
from datetime import datetime

urls = []
labels = []
maxpage=20
brojac=-1
savefile="imgFileMemes1.csv"
with open('config.txt') as f:
    content = f.readlines()
    for line in content:
        brojac+=1
        if brojac==0:
            delici = line.split(',')
            maxpage = int(delici[0])
            savefle = delici[1]
            savefle = savefle[:-1]
        else:
            line = line[:-1]
            parts = line.split(",")
            labels.append(parts[0])
            urls.append(parts[1])

brojac=-1
for url in urls:
    brojac+=1

    #url = url+1
    all_url = []

    for i in range(1,maxpage+1) :
        all_url.append(url+str(i))



    for url in all_url:


        print(url)
        # query the website and return the html to the variable ‘page’
        req = urllib2.Request(url, headers={'User-Agent' : "Magic Browser"})
        page = urllib2.urlopen( req )


        # parse the html using beautiful soup and store in variable `soup`
        soup = BeautifulSoup(page, 'html.parser')

        # Take out the <div> of name and get its value
        all_memes = soup.findAll('img', attrs={'class': 'base-img'})

        all_count_info = soup.findAll('div', attrs={'class': 'base-view-count'})


        data = soup.findAll('div', attrs={'class': 'base-unit clearfix'})

        i=0

        skip =[]
        for d in data:
            d= str(d)
            if "base-nsfw-msg" in d:
                skip.append(i)
            i=i+1

        #Ostalo je dodati sve forove

        #print(full_meme)

        txt = []

        for idx, full_meme in enumerate(all_memes):

            full_meme = str(full_meme)

            i = full_meme.index('|')

            try:
                meme_text = full_meme[ i+2: full_meme.index('|',i+1)-1]
                txt.append(meme_text.replace('&quot', '"').upper())
            except:
                skip.append(idx)

            #print(meme_text)


        #print(all_count_info)

        v =[]
        u = []
        c = []
        for count_info in all_count_info:
            count_info = str(count_info)

            i = count_info.index('<')
            j = count_info.find('>')
            h = count_info.find("<", i+1)



            #Sve informacije o pregledima, lajkovima i komentarima
            number_info = count_info[j+1 : h]


            #print(number_info)

            try:
                i = number_info.find(' ')

                views = number_info[0:i]
                v.append(int(views.replace(',', '')))
            except:
                v.append(0)

           # print(views)
            try:
                j = number_info.index(' ', i+1)

                h = number_info.index(' ', j+1)

                upvotes = number_info[j+1: h]
                u.append(int(upvotes.replace(',', '')))
            except:
                u.append(0)
            #print(upvotes)

            try:
                j = number_info.index(' ', h+1)

                h = number_info.index(' ', j+1)
                comments = number_info[j + 1:h]
                c.append(int(comments.replace(',', '')))
            except:
                comments =0
                c.append(int(comments))




           # print(comments)



        skipAdd =0
        # open a csv file with append, so old data will not be erased


        with open(savefle, 'a', encoding="utf-8") as csv_file:
            writer = csv.writer(csv_file)
            for idx, item in enumerate(txt):
                if idx in skip:
                    skipAdd = skipAdd + 1
                writer.writerow([labels[brojac], item, v[idx + skipAdd], u[idx + skipAdd], c[idx + skipAdd]])


