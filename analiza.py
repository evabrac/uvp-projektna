import pandas as pd
from collections import Counter
from itertools import combinations
import numpy as np


df = pd.read_csv(
    r"C:\Users\evabr\Desktop\school\uvp-projektna\loterija.csv",
)

df["zmagovalci"] = df["zmagovalci"].astype(str).str.replace(",", "").astype(int)
df["sodelujoči"] = df["sodelujoči"].astype(str).str.replace(",", "").astype(int)
df["datum"] = pd.to_datetime(df["datum"], format="%d-%m-%Y")

igralci_na_mesec = df.groupby(df["datum"].dt.to_period("M"))["sodelujoči"].sum()
povprecno_igralcev_na_mesec = df.groupby(df["datum"].dt.to_period("M"))["sodelujoči"].mean()

prvih_pet_counter = Counter()
zadnji_dve_counter = Counter()

# Preštej pogostost številk iz "prvih pet" in "zadnji dve"
for vrstica in df["prvih_pet"]:
    stevilke = [int(x.strip()) for x in vrstica.split(",")]
    prvih_pet_counter.update(stevilke)

for vrstica in df["zadnji_dve"]:
    stevilke = [int(x.strip()) for x in vrstica.split(",")]
    zadnji_dve_counter.update(stevilke)

# Shranim kot DataFrame za lažjo uporabo v notebooku
top_prvih_pet = pd.DataFrame(
    prvih_pet_counter.most_common(5), columns=["stevilka", "pogostost"]
)
najmanj_prvih_pet = pd.DataFrame(
    prvih_pet_counter.most_common()[-5:],
    columns=["stevilka", "pogostost"]
)

top_zadnji_dve = pd.DataFrame(
    zadnji_dve_counter.most_common(5), columns=["stevilka", "pogostost"]
)
najmanj_zadnji_dve = pd.DataFrame(
    zadnji_dve_counter.most_common()[-5:],
    columns=["stevilka", "pogostost"]
)

# Preštej pogostost vsote petih izžrebanih številk
vsota_counter = Counter()

for vrstica in df["prvih_pet"]:
    stevilke = [int(x.strip()) for x in vrstica.split(",")]
    vsota_counter[sum(stevilke)] += 1


#najpogostejši pari
pari_counter = Counter()

for vrstica in df["prvih_pet"]:
    stevilke = sorted(int(x.strip()) for x in vrstica.split(","))
    pari_counter.update(combinations(stevilke, 2))

top10_pari = pd.DataFrame(
    pari_counter.most_common(10), columns=["par", "pogostost"]
)


# Ustvari 50x50 matriko pogostosti parov (simetrična)
matrika_parov = np.zeros((50, 50), dtype=int)

for (a, b), pogostost in pari_counter.items():
    matrika_parov[a - 1, b - 1] = pogostost
    matrika_parov[b - 1, a - 1] = pogostost


#vsota igralcev za vsak mesec
df_meseci = df.copy()
df_meseci["mesec_stevilka"] = df_meseci["datum"].dt.month
vsota_po_mesecu = df_meseci.groupby("mesec_stevilka")["sodelujoči"].sum()

imena_mesecev = ["Jan", "Feb", "Mar", "Apr", "Maj", "Jun", "Jul", "Avg", "Sep", "Okt", "Nov", "Dec"]

