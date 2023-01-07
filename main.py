# script pentru a genera date de intrare pentru baza de date de la proiect
# Autor: Liviu-Ioan Zecheru
# Data: 26.11.2022
# M-am folosit de judete.json pentru a genera adresele conductorilor;
# Credits: https://github.com/virgil-av/judet-oras-localitati-romania/blob/master/judete.json


import random
import string
import re
import json
from datetime import timedelta, datetime
from dateutil.relativedelta import relativedelta
from anyascii import anyascii
from bs4 import BeautifulSoup
import requests as req
from faker import Faker
import pandas as pd

fake = Faker()

################## pastrare id-uri unice ##################

id_conductori = []
dict_conductori = {}
id_clienti = []
id_locomotive = []
id_marfuri = []
id_transporturi = []
id_vagoane = []
lista_nume_romanesti = []

############################################################

################## generare nume de familie romanesti ##################

url = "https://www.hartanumeromanesti.eu/rang_numelor_de_familie.php?p=1"
page = req.get(url)
soup = BeautifulSoup(page.content, 'html.parser')
randuri_tabel = soup.find_all('table')[0].find_all('table')[0].find_all('tr')
for index, rand in enumerate(randuri_tabel):
    if index != 0 and index != len(randuri_tabel) - 1:
        coloane = rand.find_all('td')
        if len(coloane) > 0:
            nume = coloane[1].text
            lista_nume_romanesti.append(nume.title())
url = "https://www.hartanumeromanesti.eu/rang_numelor_de_familie.php?p=2"
page = req.get(url)
soup = BeautifulSoup(page.content, 'html.parser')
randuri_tabel = soup.find_all('table')[0].find_all('table')[0].find_all('tr')
for index, rand in enumerate(randuri_tabel):
    if index != 0 and index != len(randuri_tabel) - 1:
        coloane = rand.find_all('td')
        if len(coloane) > 0:
            nume = coloane[1].text
            lista_nume_romanesti.append(nume.title())
url = "https://www.hartanumeromanesti.eu/rang_numelor_de_familie.php?p=3"
page = req.get(url)
soup = BeautifulSoup(page.content, 'html.parser')
randuri_tabel = soup.find_all('table')[0].find_all('table')[0].find_all('tr')
for index, rand in enumerate(randuri_tabel):
    if index != 0:
        coloane = rand.find_all('td')
        if len(coloane) > 0:
            nume = coloane[1].text
            lista_nume_romanesti.append(nume.title())

############################################################

################## generare prenume romanesti pe sexe ##################

lista_prenume_baieti = []
lista_prenume_fete = []
with open('prenume_baieti.txt', 'r') as f:
    for line in f:
        lista_prenume_baieti.append(line.strip())
with open('prenume_fete.txt', 'r') as f:
    for line in f:
        lista_prenume_fete.append(line.strip())

############################################################

################## generare adrese romanesti pe baza judete.json ##################

judete_localitati = {}
with open('venv/judete.json', 'r', encoding='utf-8') as f:
    judete = json.load(f)
    lista_judete = []
    lista_localitati = []
    for i in range(0, len(judete['judete'])):
        judet = anyascii(judete['judete'][i]['nume'])
        lista_judete.append(judet)
        localitati = []
        for j in range(0, len(judete['judete'][i]['localitati'])):
            try:
                localitate = judete['judete'][i]['localitati'][j]['simplu']
            except KeyError:
                localitate = judete['judete'][i]['localitati'][j]['nume']
            localitati.append(localitate)
        lista_localitati.append(localitati)
    judete_localitati = dict(zip(lista_judete, lista_localitati))

############################################################

################## dictionar pentru a determina localitatile dintr-un judet ##################

url = 'https://ro.wikipedia.org/wiki/Cod_numeric_personal_(Rom%C3%A2nia)'
page = req.get(url)
soup = BeautifulSoup(page.content, 'html.parser')
table = soup.find_all('table')[3]
rows = table.find_all('tr')
lista_judete = []
lista_coduri = []
for row in rows:
    rand = row.find('td')
    if rand:
        lista_coduri.append(str(rand.text).replace('\n', ''))
    judet = row.find_next('td').find_next('td').text
    lista_judete.append(anyascii(judet.replace('\n', '')))
lista_judete.pop(0)
coduri_judete = dict(zip(lista_coduri, lista_judete))

############################################################

################## generare firme romanesti de pe topfirme.ro ##################

lista_firme_romanesti = []

for i in range(0, int(input("Introduceti numarul de pagini de pe care se va face scraping pentru firme romanesti: "))):
    url = f"https://www.topfirme.com/profit/?pagina={str(i + 1)}"
    page = req.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    results = soup.find_all('a', class_='mdl-card__item mdl-card--border link_firma')
    for result in results:
        a = result.select('div.truncate')
        lista_firme_romanesti.append(anyascii(a[0].text.replace('  ', ' ').replace("'", "''").replace('&', '\&')))

############################################################

################## providerii de email ##################

email_providers = ["@gmail.com", "@yahoo.com", "@hotmail.com", "@aol.com",
                   "@aim.com",
                   "@icloud.com",
                   "@protonmail.com",
                   "@pm.com", "@zoho.com",
                   "@yandex.com",
                   "@titan.email",
                   "@gmx.com",
                   "@hubspot.com",
                   "@mail.com",
                   "@tutanota.com",
                   "@outlook.com"]

email_middle_parts = [".", "_", ""]

############################################################

############ parsare locomotive ############

url = 'https://ro.wikipedia.org/wiki/Material_rulant_al_CFR_C%C4%83l%C4%83tori'
page = req.get(url)
soup = BeautifulSoup(page.content, 'html.parser')
lista_locomotive_electrice = []
lista_producatori_electrice = []
lista_descrieri_electrice = []
lista_viteze_electrice = []
tabel_locomotive_diesel = soup.find('table', class_='toccolours').find_all('tr')
del tabel_locomotive_diesel[0]  # elimin capul de tabel
for linie in tabel_locomotive_diesel:
    text_bf = linie.find('td').text.replace('\n', '')
    text_bf = re.sub(r'\[.*?\]', '', text_bf)
    lista_locomotive_electrice.append(text_bf)
for rand in tabel_locomotive_diesel:
    producator = rand.find('td').find_next_sibling('td').text.replace('\n', '')
    lista_producatori_electrice.append(anyascii(producator))
for rand in tabel_locomotive_diesel:
    descriere = rand.find('td').find_next_sibling('td').find_next_sibling('td').text.replace('\n', '').replace("'",
                                                                                                               "''")
    descriere = re.sub(r'\[.*?\]', '', descriere)
    lista_descrieri_electrice.append(anyascii(descriere))
for rand in tabel_locomotive_diesel:
    viteza = rand.find('td').find_next_sibling('td').find_next_sibling('td').find_next_sibling('td').text.split(
        " ")[0]
    lista_viteze_electrice.append(int(viteza))
lista_specificatii_locomotive = dict(zip(lista_locomotive_electrice, zip(zip(lista_producatori_electrice,
                                                                             lista_descrieri_electrice),
                                                                         lista_viteze_electrice)))

####################################################################################################

############ parsare locomotive de pe stfp.net ############

# locomotive_romanesti = {}
# for i in range(1, 952, 25):
#     URL = f"http://cfr.stfp.net/?sta={i}&class=E*&ppr=5&sel=N"
#
#     # Incarcam continutul paginii web
#     r = requests.get(URL)
#
#     # Cream un obiect BeautifulSoup
#     soup = BeautifulSoup(r.content, "html.parser")
#
#     # Extragem toate elementele de tip <tr>
#
#     rows = soup.find_all("tr")
#     del rows[0]
#     for row in rows:
#         cols = row.find_all("td")
#         for col in cols:
#             string = str(col.text).replace("\n", " ").replace("Clasa", " Clasa").replace("(", " (").replace("  ",
#                                                                                                             " ")
#             string = string.replace("[640] ", "").replace("[800] ", "").replace("[1024] ", "").replace("[1280] ",
#                                                                                                        "").replace("["
#                                                                                                                    "original] ", "")
#             regex1 = re.compile(r"(Clasa [0-9]+)")
#             try:
#                 string1 = regex1.search(string).group(0)
#             except AttributeError:
#                 string1 = "Clasa 48"
#             regex = re.compile(r"([A-Za-z0-9]+( [A-Za-z0-9]+)+\-[0-9]+)")
#             try:
#                 string = regex.match(string).group(0)
#             except AttributeError:
#                 regex = re.compile(r"([0-9]+(-[0-9]+)+)")
#                 try:
#                     string = regex.match(string).group(0)
#                 except AttributeError:
#                     regex = re.compile(r"([0-9]+( [0-9]+)+)")
#                     try:
#                         string = regex.search(string).group(0)
#                     except AttributeError:
#                         string = ""
#             locomotive_romanesti[string] = string1

# Metoda asta nu are decat numele locomotivei si clasa, nu are descriere si producator
####################################################################################################

############ zona de marfuri ############

df = pd.read_csv('marfuri.csv', encoding='windows-1252')

####################################################################################################

############ parsare lista gari ############

url = "https://ro.wikipedia.org/wiki/Lista_sta%C8%9Biilor_de_cale_ferat%C4%83_din_Rom%C3%A2nia"
page = req.get(url)
lista_gari = []
soup = BeautifulSoup(page.content, 'html.parser')
tabel_locomotive_diesel = soup.find('table', class_='wikitable sortable')
randuri = tabel_locomotive_diesel.find_all('tr')
for rand in randuri:
    coloane = rand.find_all('td')
    if len(coloane) > 0:
        gara = anyascii(coloane[0].text.replace('\n', ''))
        lista_gari.append(gara)

####################################################################################################

# scrie tot in fisierul de iesire
fisier_iesire = open("fisier_iesire.txt", "w")


####################################### zona de functii ############################################


# functie pentru a genera date de intrare pentru tabela Conductori
def genereaza_conductor(x):
    # generam un CNP valid
    # CNP-ul este format din 13 cifre
    # prima cifra reprezinta sexul (1 - barbat, 2 - femeie)
    # urmatoarele 2 cifre reprezinta anul nasterii (ex: 99 pentru 1999)
    # urmatoarele 2 cifre reprezinta luna nasterii (ex: 12 pentru decembrie)
    # urmatoarele 2 cifre reprezinta ziua nasterii
    # urmatoarele 2 cifre reprezinta judetul de domiciliu
    # urmatoarea  3 cifre reprezinta seria
    # ultimele cifra reprezinta cifra de control

    sexul = random.randint(1, 2)
    anul_nasterii = random.randint(57, 99)
    luna_nasterii = random.randint(1, 12)
    ziua_nasterii = random.randint(1, 28)
    judetul = list(range(1, 41))
    judetul.extend([51, 52])
    judetul = random.choice(judetul)
    secventa = random.randint(1, 9)
    judet_string = ''
    cnp = str(sexul)
    if anul_nasterii < 10:
        cnp += "0" + str(anul_nasterii)
    else:
        cnp += str(anul_nasterii)
    if luna_nasterii < 10:
        cnp += "0" + str(luna_nasterii)
    else:
        cnp += str(luna_nasterii)
    if ziua_nasterii < 10:
        cnp += "0" + str(ziua_nasterii)
    else:
        cnp += str(ziua_nasterii)
    if judetul < 10:
        judet_string += "0" + str(judetul)
    else:
        judet_string += str(judetul)
    cnp += judet_string
    cnp += str(secventa)
    secventa = random.randint(1, 9)
    cnp += str(secventa)
    secventa = random.randint(1, 9)
    cnp += str(secventa)
    # calculam cifra de control
    constanta = 279146358279
    suma = 0
    for i in range(0, 12):
        suma += int(cnp[i]) * int(str(constanta)[i])
    cifra_control = suma % 11
    if cifra_control == 10:
        cifra_control = 1
    cnp += str(cifra_control)
    # generam un nume valid
    # numele este format dintr-un cuvant
    # numele va fi ales dintr-o lista de nume romanesti

    nume = random.choice(lista_nume_romanesti)

    # generam un prenume valid
    # prenumele este format dintr-un cuvant
    # prenumele va fi ales dintr-o lista de prenume romanesti

    if sexul == 1:
        prenume = random.choice(lista_prenume_baieti)
    else:
        prenume = random.choice(lista_prenume_fete)

    # generam un email valid
    # email-ul este format din 2 cuvinte
    # email-ul va fi construit pe baza numelui si prenumelui ales anterior
    # email-ul va fi de forma: nume + random.choice([".", "_"]) + prenume + random.choice(["gmail", "yahoo",
    # "hotmail", "outlook"]) + random.choice([".com", ".ro", ".net"])

    email = nume.lower() + random.choice(email_middle_parts) + prenume.lower() + random.choice(email_providers)

    # generam un numar de telefon valid
    # numarul de telefon este format din 10 cifre

    numar_telefon = "07"
    for i in range(0, 8):
        numar_telefon += str(random.randint(0, 9))

    # generarea unei adrese valide
    # adresa este formata din oras, strada, numarul casei, numarul apartamentului
    # orasul va fi preluat dintr-un dictionar de orase din Romania
    # strada va fi preluata dintr-un dictionar de strazi din Romania
    # numarul casei va fi generat aleator
    # numarul apartamentului va fi generat aleator

    strazi = ["Mihai Eminescu", "Tudor Vladimirescu", "Nicolae Balcescu", "Primaverii", "Libertatii",
              "Trandafirilor", "Garii", "Florilor", "Avram Iancu", "1 Mai", "Unirii", "Liliacului", "George Cosbuc",
              "Ion Creanga", "Zorilor", "Horea", "Viilor", "Stefan cel Mare", "Teilor", "Vasile Alecsandri",
              "Campului", "Gheorghe Doja", "Mihail Kogalniceanu", "Crisan", "Crinului", "Closca", "Marasesti",
              "Oituz", "Mihai Viteazu", "Stadionului", "Independentei", "Plopilor", "Republicii", "Victoriei",
              "Pacii", "Tineretului", "Aurel Vlaicu", "Decebal", "Salcamilor", "Morii", "Eroilor", "Bradului",
              "Lalelelor", "Castanilor", "I. L. Caragiale", "Rozelor", "Viitorului", "Traian", "Stejarului",
              "Nicolae Iorga", "Mihail Sadoveanu", "Cuza Voda", "Narciselor", "Izvorului", "Muncii"]

    # generare oras in functie de judet_string
    oras_key = coduri_judete[judet_string]
    oras = random.choice(judete_localitati[oras_key])
    strada = random.choice(strazi)
    numar_casa = random.randint(1, 100)
    numar_bloc = random.randint(1, 100)
    numar_apartament = random.randint(1, 100)
    casa_bloc = random.choice(["casa", "bloc"])
    are_email = random.randint(0, 1)
    scara = random.randint(1, 10)
    if sexul == 1:
        litera_sex = 'M'
    else:
        litera_sex = 'F'
    if casa_bloc == "casa":
        adresa = oras + ", Strada " + strada + ", nr. " + str(numar_casa)
    else:
        adresa = oras + ", Strada " + strada + ", nr. " + str(numar_casa) + ", bl. " + str(numar_bloc) + \
                 random.choice([random.choice(string.ascii_uppercase), ""]) + ", sc. " + str(scara) + ", ap. " + str(
            numar_apartament)
    id_conductor = x
    id_conductori.append(id_conductor)
    dict_conductori[id_conductor] = datetime(anul_nasterii + 1900, luna_nasterii, ziua_nasterii)
    identitate = "values(" + str(id_conductor) + ", "
    if are_email == 0:
        identitate += "'" + nume + "', '" + prenume + "', '" + cnp + "', '" + litera_sex + "', '" + adresa + "', null, '" + numar_telefon + "'"
    else:
        identitate += "'" + nume + "', '" + prenume + "', '" + cnp + "', '" + litera_sex + "', '" + adresa + "', '" + email + "', " \
                                                                                                                              "'" + numar_telefon + "'"
    salariul = random.randint(3000, 99999)
    identitate += ", " + str(salariul) + ");\n"
    fisier_iesire.write("insert into conductori(id_conductor, nume, prenume, cnp, sex, adresa, email, telefon, "
                        "salariul)\n")
    fisier_iesire.write(identitate)


# functie pentru a genera date de intrare pentru tabela Clienti

def genereaza_client(x):
    id_client = x
    id_clienti.append(id_client)
    nume = random.choice(lista_nume_romanesti)
    prenume = random.choice([random.choice(lista_prenume_baieti), random.choice(lista_prenume_fete)])
    # numele companiei va fi format din doua cuvinte
    # primul cuvant va fi numele unei companii romanesti
    # al doilea cuvant va fi rangul firmei, ex: SRL, SA, SCS, SCA
    denumire_firma = random.choice(lista_firme_romanesti)
    numar_telefon = "07"
    for i in range(0, 8):
        numar_telefon += str(random.randint(0, 9))
    email = nume.lower() + random.choice(email_middle_parts) + prenume.lower() + random.choice(email_providers)
    fisier_iesire.write("insert into clienti1(id_client, nume, prenume, denumire_firma, telefon, email)\n")
    rezultat = "values(" + str(id_client) + ", '" + nume + "', '" + prenume + "', '" + denumire_firma + "', " \
                                                                                                        "'" + \
               numar_telefon + "', '" + email + "');\n"
    fisier_iesire.write(rezultat)


# functie pentru a genera date de intrare pentru tabela locomotive

def genereaza_locomotiva(x):
    id_locomotiva = x
    id_locomotive.append(id_locomotiva)
    clasa_key = random.choice(list(lista_specificatii_locomotive.keys()))
    nume = clasa_key
    clasa = clasa_key.split(" ")[1]
    producator = lista_specificatii_locomotive[clasa_key][0][0]
    descriere = lista_specificatii_locomotive[clasa_key][0][1]
    viteza_maxima = lista_specificatii_locomotive[clasa_key][1]
    putere = int(lista_specificatii_locomotive[clasa_key][0][1].split(" ")[0].replace(".", ""))
    curent_maxim = random.randint(1000, 5000)
    tensiune_maxima = random.randint(1000, 5000)
    fisier_iesire.write("insert into locomotive(id_locomotiva, nume, clasa, producator, descriere, putere, "
                        "viteza_maxima, "
                        "curent_maxim, tensiune_maxima)\n")
    rezultat = "values(" + str(id_locomotiva) + ", '" + nume + "', '" + clasa + "', '" + producator + "', '" \
                                                                                                      "" + descriere \
               + "', " + str(putere) + ", " \
               + str(viteza_maxima) + ", " + str(curent_maxim) + ", " + str(tensiune_maxima) + ");\n"
    fisier_iesire.write(rezultat)


# functie pentru a genera date pentru tabela Marfuri

def genereaza_marfuri():
    for index_, marfa in df.iterrows():
        id_marfa = index_
        id_marfuri.append(id_marfa)
        nume_marfa = marfa[0].replace("'", "''")
        descriere_marfa = marfa[1].replace("'", "''")
        um_marfa = marfa[2]
        pret = marfa[3]
        fisier_iesire.write("insert into marfuri_noi(id_marfa, denumire, descriere, um, pret_unitar)\n")
        rezultat = "values(" + str(id_marfa) + ", '" + nume_marfa + "', '" + descriere_marfa + "', '" + um_marfa + "', " \
                                                                                                              "" + \
                   str(pret) + ");\n"
        fisier_iesire.write(rezultat)



# functie pentru a genera date de intrare pentru tabela Detalii_Transporturi

def genereaza_detalii_transporturi(x):
    id_transport = x
    id_transporturi.append(id_transport)
    id_locomotiva = random.choice(id_locomotive)
    id_conductor = random.choice(id_conductori)
    id_client = random.choice(id_clienti)
    # stabilirea datei de plecare ca fiind la cel putin 18 ani dupa anul nasterii conductorului
    data_inceput = dict_conductori[id_conductor] + relativedelta(years=18)
    data_plecare = fake.date_between(start_date=data_inceput, end_date="today")
    data_sosire = fake.date_between(start_date=data_plecare, end_date=data_plecare + timedelta(days=14))
    gara_plecare = random.choice(lista_gari)
    gara_sosire = random.choice(lista_gari)
    while gara_sosire == gara_plecare:
        gara_sosire = random.choice(lista_gari)
    fisier_iesire.write("insert into detalii_transporturi(id_transport, id_locomotiva, id_conductor, id_client, "
                        "data_plecare, "
                        "data_sosire, gara_plecare, gara_sosire)\n")
    rezultat = "values(" + str(id_transport) + ", " + str(id_locomotiva) + ", " + str(id_conductor) + ", " \
                                                                                                      "" + str(
        id_client) + ", to_date('" + str(data_plecare) + "', 'yyyy-mm-dd'), to_date('" + str(data_sosire) + "', " \
                                                                                                            "'yyyy-mm-dd'), " \
                                                                                                            "'" + gara_plecare \
               + "', " \
                 "'" + \
               gara_sosire + "');\n"
    fisier_iesire.write(rezultat)


# functie pentru a genera date de intrare pentru tabela Vagoane

def genereaza_vagoane(x):
    id_vagon = x
    id_vagoane.append(id_vagon)
    id_marfa = random.choice(id_marfuri)
    id_transport = random.choice(id_transporturi)
    capacitate = random.randint(1, 100)
    cantitate = random.randint(1, capacitate)
    fisier_iesire.write("insert into vagoane(id_vagon, id_marfa, id_transport, capacitate, cantitate)\n")
    rezultat = "values(" + str(id_vagon) + ", " + str(id_marfa) + ", " + str(id_transport) + ", " + str(capacitate) + \
               ", " + str(cantitate) + ");\n"
    fisier_iesire.write(rezultat)


# script principal

genereaza_marfuri()
for i in range(1, int(input("Introduceti numarul de conductori: ")) + 1):
    genereaza_conductor(i)
for i in range(1, int(input("Introduceti numarul de clienti: ")) + 1):
    genereaza_client(i)
for i in range(1, int(input("Introduceti numarul de locomotive: ")) + 1):
    genereaza_locomotiva(i)
for i in range(1, int(input("Introduceti numarul de transporturi: ")) + 1):
    genereaza_detalii_transporturi(i)
for i in range(1, int(input("Introduceti numarul de vagoane: ")) + 1):
    genereaza_vagoane(i)
fisier_iesire.close()
