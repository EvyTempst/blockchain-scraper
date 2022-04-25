import requests
from bs4 import BeautifulSoup

def clean_data(rawdata):
    rawdata = rawdata.replace("Hash","")
    rawdata = rawdata.replace("Time"," ")
    rawdata = rawdata.replace("Amount","")
    rawdata = rawdata.replace("(BTC)","")
    rawdata = rawdata.replace("BTC","")
    rawdata = rawdata.replace(" (USD)","")
       
    return rawdata


url = "https://www.blockchain.com/btc/unconfirmed-transactions"

lijst = []
highest = 0
tijd= ""

while True:
    request = requests.get(url)
    soupbs = BeautifulSoup(request.text, "html.parser")
    f = open("biggest_hashes.log", "a")
    texts = soupbs.find_all("div", {"class" : "sc-1g6z4xm-0 hXyplo"})

    for t in texts:
        text = t.get_text()
        text = clean_data(text)
        text = text.split(" ")
        lijst.append(text)

    lijst.reverse()

    if len(tijd) == 0:
            tijd = text[1]  
    for l in lijst:    
        if l[1] == tijd: 
            if float(l[2]) > highest:
                highest = float(l[2])
                hoogstehash = l[0]
                hashtime = l[1]
                btc = l[2]
                usd = l[3]
        if l[1] > tijd: 
            f.write("Time: " + hashtime + " Hash: " + hoogstehash + " BTC value: " + btc + " USD value: " + usd + "\n")
            tijd = l[1]
            highest = 0 
            hoogstetekst = 0 
            lijst = []
                    

    f.close()