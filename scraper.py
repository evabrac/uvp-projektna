from bs4 import BeautifulSoup
import requests
import csv
import os
from datetime import date, timedelta, datetime

rezultati = []

# generiram vse datume med 1.1.2018 in 1.1.2026, ki so torek ali petek
start = date(2018, 1, 1)
end = date(2026, 1, 1)

datumi = []
trenuten = start

#pred while loopom sem dodala pogoj, da se datumi po 25.3.2022 dodajajo tudi ob torkih, ker so se takrat spremenili dnevi žrebanja
while trenuten <= end:
    if trenuten.weekday() == 4:
        datumi.append(trenuten.strftime("%d-%m-%Y"))
    if trenuten >= date(2022, 3, 25) and trenuten.weekday() == 1:
        datumi.append(trenuten.strftime("%d-%m-%Y"))
    trenuten += timedelta(days=1)


# naredim seznam slovarjev za vsak dan
for datum in datumi:

    datum_url = f"https://www.euro-jackpot.net/results/{datum}"
    page = requests.get(datum_url)
    soup = BeautifulSoup(page.content, 'html.parser')

    # prvih pet številk
    prve_tags = soup.find_all('li', class_='ball')
    prve = [tag.text.strip() for tag in prve_tags]
    prve = prve[:5]

    # zadnji dve 
    zadne_tags = soup.find_all('li', class_='euro')
    zadne = [tag.text.strip() for tag in zadne_tags]
    zadne = zadne[:2]

    # zmagovalci
    tabela = soup.find("table", class_="table-alt")
    nagrade = ""
    zmagovalci = ""
    if tabela:
        for tr in tabela.find_all("tr"):
            tds = tr.find_all("td")
            if not tds:
                continue
            if "Total" in tds[0].get_text():
                zmagovalci = tds[-1].get_text(strip=True)
                break
    
    #sodelujoči
    p_tags = soup.find_all("p")
    sodelujoci = ""
    for p in p_tags:
        if "In total there were" in p.get_text():
            strong_tag = p.find("strong")
            if strong_tag:
                sodelujoci = strong_tag.text.strip()
            break
    
    rezultat = {
        "datum": datum,
        "prvih_pet": prve,
        "zadnji_dve": zadne,
        "zmagovalci": zmagovalci,
        "sodelujoči": sodelujoci
    }
    rezultati.append(rezultat)

# prepišem v csv
with open("loterija.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["datum", "prvih_pet", "zadnji_dve", "zmagovalci", "sodelujoči"])

    for row in rezultati:
        writer.writerow([
            row["datum"],
            ",".join(row["prvih_pet"]),
            ",".join(row["zadnji_dve"]),
            row["zmagovalci"],
            row["sodelujoči"]
        ])
