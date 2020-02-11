# Дим, доброе время суток))
#  Напиши пожалуйста когда закончится наш курс и будет защита диплома? 
#  И когда это будет у следующего курса?
# Закрою Нейронки будет больше времени)
# C уважением Александр

from bs4 import BeautifulSoup
import requests
import re
import csv

def read_url3(url_):
    page = requests.get(url_)
    soup = BeautifulSoup(page.text, 'html.parser')
    parts = soup.find_all('h2', class_ = 'product-name')
    prices = soup.find_all('div', class_ = 'price-box')

    basax=[]
    for it in range(len(parts)):
        basax.append([parts[it].text, prices[it].text])

    return   basax     

def read_url1(url_):
    page = requests.get(url_)
    soup = BeautifulSoup(page.text, 'html.parser')
    
    parts = soup.find_all('div', class_ = 'offer')
    prices = soup.find_all('div', class_ = 'price')
    gidro = soup.find_all('a', class_ = 'kakh3')

    basax=[]
    for it in range(len(parts)):
        cont=parts[it].contents
        basax.append((gidro[it].text, cont[5].string, cont[7].string, prices[it].text))
    return   basax     


def men_wumen(z0):
    z1 = ""
    if "мужской" in z0: z1='мужской'
    elif "женский" in z0: z1='женский'
    else: z1='для всех'
    return z1

def conv3(x):
    prisex = lambda a : int(a.split(',')[0])
    rez=[]
    s0=r'\n'
    s1=r'\xa0'
    r2=r'\s\d?.?\d.?[м]+' #\s??\
    for item in range (len(x)):
        z0= re.sub(s0, '', x[item][0])
        s_=x[item][1];
        z3 = re.split(s1, str(re.sub(s0, '', s_)))
        prise=0
        if "Специальная цена" in s_:
            z30 = int(re.split(r'\r',  z3[0])[1].replace(' ',''))*1000
            prise=z30 + prisex(z3[1])
        elif "Начиная от:" in s_:
            prise=prisex(z3[1])
        else:
            prise=int(z3[0])*1000 + prisex(z3[1])

        z1 = men_wumen(z0)

        z2=re.findall(r2, z0)[0]
        
        rez+=[[z0, z1, z2, prise]]
    return rez

def conv1(x):
    rez=[]
    r1=r'\s\d?.?\d.?[м]+'
    r2=r'\s\d?\d?.?\d\d\d'
    for item in range (len(x)):
        name = x[item][0]
        prise = int(str(re.findall(r2, x[item][3])[0]).replace(" ",""))
        z1 = men_wumen(name)
        z2=re.findall(r1, name)[0]
        rez+=[[name, z1, z2, prise]]
    return rez

def csv_writer(data, path):
    with open(path, "w", newline='') as csv_file:
        writer = csv.writer(csv_file, delimiter=';')
        for line in data:
            writer.writerow(line)


if __name__ == "__main__":
    print("scubamarket")
    _url1="https://www.scubamarket.ru/catalog/wet-5-mm/"
    z0= conv1(read_url1(_url1))
    csv_writer(z0, "scubamarket.csv")

    print("batiskaf")
    _url3="https://www.batiskaf.ru/suits-108.html"
    z1= conv3(read_url3(_url3))
    csv_writer(z1, "batiskaf.csv")


