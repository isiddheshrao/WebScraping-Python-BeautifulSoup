import urllib
import sys
from bs4 import BeautifulSoup as bs
import requests
max_movies=0
actor_name=0
actor_name_1=0
high_avg_earning=0
flag = 0

try:
    print("Erasing data from previous actors.txt file")
    f = open("actors.txt","w")
    f.write('')
    f.close()
except:
    print("creating a txt file named actors.txt")

pages = [str(i) for i in range(1, 15)]
for page in pages:
    try:
        _URL = 'https://www.boxofficemojo.com/people/?view=Actor&pagenum='+page+'&sort=sumgross&order=DESC&&p=.htm'
        page = urllib.request.urlopen(_URL)
        soup = bs(page,'html.parser')

        # functional
        header = soup.find(text="Row")
        table = header.find_parent("table")
        table2=[]
        for row in table.find_all("tr"):
            table2.append([cell.get_text(strip=True) for cell in row.find_all("td")])

        with open('actors.txt', 'a', encoding='utf-8') as f_out:
            for x in table2[1:len(table2)]:
                if int(x[3].replace(',', '')) > max_movies:
                    max_movies = int(x[3].replace(',', ''))
                    actor_name = x[1]
                if float(x[4].strip('$|k')) > high_avg_earning:
                    high_avg_earning = float(x[4].strip('$|k'))
                    actor_name_1 = x[1]
                for i in range(len(x)):
                    f_out.write(str(x[i])+" , ")
                f_out.write("\n")
            f_out.close()
    except:
        flag = 1
print("The actor(s) with the maximum number of movies is: ", actor_name, "with: ", max_movies, "Movies!")
print("The actor(s) with the highest average earnings per movie is: ", actor_name_1," with: $", high_avg_earning)
