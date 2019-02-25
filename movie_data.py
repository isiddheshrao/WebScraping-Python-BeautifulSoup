import urllib
import sys
import re
from bs4 import BeautifulSoup as bs
import requests

max_theaters = 0
max_theaters_movie_name = 0
avg = 0
flag = 0
try:
    print("Erasing data from precious movies.txt file")
    f = open("movies.txt", "w")
    f.write('')
    f.close()
except:
    print("creating a txt file named movies.txt")

pages = [str(i) for i in range(1, 10)]
_YEAR = input("Enter the Year you are interested in getting data: ")
if str(1980) <= _YEAR <= str(2018):
    for page in pages:
        try:
            _URL = 'https://www.boxofficemojo.com/yearly/chart/?view=releasedate&view2=domestic&page=' + page + '&yr=' + _YEAR + '&p=.htm'
            page = urllib.request.urlopen(_URL)
            soup = bs(page, 'html.parser')

            # functional
            header = soup.find(text="Rank")
            table = header.find_parent("table")
            table1 = []
            f = requests.get(_URL)
            get_id = re.findall('\S+></form></table><a></a></.+', f.text)
            join_text = ''.join(get_id)
            mid = join_text.split('movies/')

            for row in table.find_all("tr"):
                table1.append([cell.get_text(strip=True) for cell in row.find_all("td")])

            with open('movies.txt', 'a', encoding='utf-8') as f_out:
                movie_ids = []
                for key in mid:
                    o = '?id='
                    if o in key:
                        p = re.findall('/?id=.+?>', key)
                        q = ''.join(p)
                        r = q.split('.')
                        x = r[0]
                        s = ''.join(x)
                        t = s.split('=')
                        movie_ids.append(t[1])

                movie_ids_index = 0
                for x in table1[2:len(table1) - 4]:
                    if x[4] == 'N/A':
                        x[4] = '0'
                    if int(x[4].replace(',', '')) > max_theaters:
                        max_theaters = int(x[4].replace(',', ''))
                        max_theaters_movie_name = x[1]
                    for i in range(2):
                        f_out.write(str(x[i]) + " , ")
                    # appending the movie_id at column-index 3
                    f_out.write(movie_ids[movie_ids_index] + " , ")

                    for i in range(4, len(x)):
                        f_out.write(str(x[i]) + " , ")
                    f_out.write("\n")
                    movie_ids_index += 1

                for y in table1[len(table1) - 3:len(table1) - 1]:
                    for j in range(0, 2):
                        f_out.write(str(y[j]) + ",")
                        avg = y[1]
                    f_out.write("\n")
                f_out.close()
        except:
            flag = 1

    print("The average Total Gross Earnings for", _YEAR, "is: ", avg)
    print("The Movie(s) that had the maximum number of theaters for ", _YEAR, "is: ", max_theaters_movie_name, "Shown in: ",
          max_theaters, "Theaters!")
else:
    print("Enter Correct Year!")
