# -*- coding: utf8 -*-

import pandas as pd
import os
import datetime


#klasa tworzaca tabele z danymi o zapotrzebowaniu na moc w KSE
class Dane_zapotrzebowanie():

    def __init__(self, rok, miesiac, dzien,
                 godzina, zapotrzebowanie):
        self.rok = rok
        self.miesiac = miesiac
        self.dzien = dzien
        self.godzina = godzina
        self.zapotrzebowanie = zapotrzebowanie


#klasa tworzaca tabele z danymi meteorologicznymi
class Dane_meteo():

    def __init__(self, id_stacji, rok, miesiac, dzien,
                 godzina, zachmurzenie, kierunek_wiatru,
                 predkosc_wiatru, temperatura, wilgotnosc,
                 cisnienie, id_pomiaru):
        self.id_stacji = id_stacji
        self.rok = rok
        self.miesiac = miesiac
        self.dzien = dzien
        self.godzina = godzina
        self.zachmurzenie = zachmurzenie
        self.kierunek_wiatru = kierunek_wiatru
        self.predkosc_wiatru = predkosc_wiatru
        self.temperatura = temperatura
        self.wilgotnosc = wilgotnosc
        self.cisnienie = cisnienie
        self.id_pomiaru = id_pomiaru


#metoda odczytująca dane meteorologiczne
def pobierz_dane_meteo(plikcsv, dict_dane_meteo, station_number):


    #zmianna pomocnicza do przypisywania id_pomiaru
    i=1
    
    if os.path.isfile(plikcsv):  # sprawdzenie czy plik istnieje na dysku
        with open(plikcsv, "r", encoding="latin-1") as zawartosc:  # otwarcie plik do odczytu
            for linia in zawartosc:
                linia = linia.replace("\n", "")  # usuniecie znakow konca linii
                linia = linia.replace("\r", "")  # usuniecie znakow konca linii
                linia = linia.replace('\"', "")
                krotka = linia.split(",")

                #stworzenie instancji klasy Dane_meteo
                dane = Dane_meteo(id_stacji=int(krotka[0]),
                                    rok=int(krotka[2]),
                                    miesiac=int(krotka[3]),
                                    dzien=int(krotka[4]),
                                    godzina=int(krotka[5]),
                                    zachmurzenie=int(krotka[21]),
                                    kierunek_wiatru=int(krotka[23]),
                                    predkosc_wiatru=int(krotka[25]),
                                    temperatura=float(krotka[29]),
                                    wilgotnosc=int(krotka[37]),
                                    cisnienie=float(krotka[41]),
                                    id_pomiaru=i)
                i+=1
                
                #dodanie danych z instancji klasy do slownika
                txt = "%d" % dane.id_stacji
                if txt.endswith("%d" % station_number):
                    dict_dane_meteo.setdefault("id_stacji", []).append(dane.id_stacji)
                    dict_dane_meteo.setdefault("rok", []).append(dane.rok)
                    dict_dane_meteo.setdefault("miesiac", []).append(dane.miesiac)
                    dict_dane_meteo.setdefault("dzien", []).append(dane.dzien)
                    dict_dane_meteo.setdefault("godzina", []).append(dane.godzina)
                    dict_dane_meteo.setdefault("dzien_tygodnia", []).append(datetime.date(dane.rok, dane.miesiac, dane.dzien).weekday())
                    dict_dane_meteo.setdefault("zachmurzenie_%d" % (dane.id_stacji), []).append(dane.zachmurzenie)
                    dict_dane_meteo.setdefault("kierunek_wiatru_%d" % (dane.id_stacji), []).append(dane.kierunek_wiatru)
                    dict_dane_meteo.setdefault("predkosc_wiatru_%d" % (dane.id_stacji), []).append(dane.predkosc_wiatru)
                    dict_dane_meteo.setdefault("temperatura_%d" % (dane.id_stacji), []).append(dane.temperatura)
                    dict_dane_meteo.setdefault("wilgotnosc_%d" % (dane.id_stacji), []).append(dane.wilgotnosc)
                    dict_dane_meteo.setdefault("cisnienie_%d" % (dane.id_stacji), []).append(dane.cisnienie)
                    
                
    else:
        print("Plik z danymi", plikcsv, "nie istnieje!") #wyswietla komunikat, jezeli nie znaleziono pliku

    i=1

    return 1


#funkcja odczytujaca dane z pliku csv
def pobierz_dane_moc(plikcsv, dict_dane_moc):


    if os.path.isfile(plikcsv):  # sprawdzenie czy plik istnieje na dysku
        with open(plikcsv, "r") as zawartosc:  # otwarcie plik do odczytu
            for linia in zawartosc:
                linia = linia.replace("\n", "")  # usuniecie znakow konca linii
                linia = linia.replace("\r", "")  # usuniecie znakow konca linii
                linia = linia.replace('\"', "")
                linia = linia.replace(",", ".")
                krotka = linia.split(";")
                data=krotka[0]

                #sprawdzenie, czy nie ma brakujacych wartosci.
                #Jezeli pojawia sie brak wartosci rzeczywistej, zastepowana jest wartoscia prognozowana
                if krotka[3] == "-":
                    krotka[3] = krotka[2]

                rok=int(data[0:4])
                miesiac=int(data[4:6])
                dzien=int(data[6:8])
                
                #stworzenie instancji klasy Network_data
                dane = Dane_zapotrzebowanie(rok = int(rok),
                                            miesiac = int(miesiac),
                                            dzien = int(dzien),
                                            godzina = int(krotka[1]) - 1,
                                            zapotrzebowanie = float(krotka[3]))
                
                #dodanie danych z instancji klasy do slownika
                dict_dane_moc.setdefault("rok", []).append(dane.rok)
                dict_dane_moc.setdefault("miesiac", []).append(dane.miesiac)
                dict_dane_moc.setdefault("dzien", []).append(dane.dzien)
                dict_dane_moc.setdefault("godzina", []).append(dane.godzina)
                dict_dane_moc.setdefault("zapotrzebowanie_moc", []).append(dane.zapotrzebowanie)

               
    else:
        print("Plik z danymi", plikcsv, "nie istnieje!") #wyswietla komunikat , jezeli nie znaleziono pliku

    return 1


# odczytanie danych meteorologicznych z poszczegolnych stacji

os.chdir("D:\\Studia\\Energetyka\\Praca_inzynierska\\siec_neuronowa\\dane_testowe")
dict_dane_meteo={}

for l in range(100,800): # l-numer stacji
    dict_dane_meteo={}
    for month in range(1, 13):
        pobierz_dane_meteo("s_t_%d_2019.csv" % month, dict_dane_meteo, l)
    
     #zamiana zwroconego przez funkcje slownika na DataFrame oraz zapis wyniku do pliku csv
    df=pd.DataFrame(dict_dane_meteo)
    df.to_csv("D:\\Studia\\Energetyka\\Praca_inzynierska\\siec_neuronowa\\dane_testowe\\pre_s_t_%d_2019.csv" % (l), index = False)
    print(l)


# odczytanie danych o zapotrzebowanie na moc w KSE

dict_dane_moc = {}
for k in range(2019, 2020): # k-rok
    os.chdir("D:\\Studia\\Energetyka\\Praca_inzynierska\\siec_neuronowa\\dane_testowe")
    for l in range(1, 13): # l-miesiac
        if os.path.isfile('KSE_%d_%d.csv' % (k, l)):
            print(k, l)
            pobierz_dane_moc('KSE_%d_%d.csv' % (k, l), dict_dane_moc)
            
             #zamiana zwroconego przez funkcje slownika na DataFrame oraz zapis wyniku do pliku csv
            df = pd.DataFrame(dict_dane_moc)
            df.to_csv("D:\\Studia\\Energetyka\\Praca_inzynierska\\siec_neuronowa\\dane_testowe\\dane_moc.csv")


##########################################################################################################

# czesc programu laczaca tabele z danymi ze wszystkich stacji l dla danego roku k

#stworzenie zmiennych pomocniczych
df_file = pd.DataFrame()
df = pd.DataFrame()

#odczyt poszczegolnych tabeli i przypisanie do zmiennych pomocniczych dwoch pierwszych stacji
os.chdir("D:\\Studia\\Energetyka\\Praca_inzynierska\\siec_neuronowa\\dane_testowe")
df_file = pd.read_csv("D:\\Studia\\Energetyka\\Praca_inzynierska\\siec_neuronowa\\dane_testowe\\pre_s_t_105_2019.csv")
df = pd.read_csv("D:\\Studia\\Energetyka\\Praca_inzynierska\\siec_neuronowa\\dane_testowe\\pre_s_t_100_2019.csv")

#usuniecie kolumny z numerem wiersza
df_file = df.drop(df_file.columns[0], axis=1)
df = df.drop(df.columns[0], axis=1)

#wykonanie zlaczenia wewnetrznego tabel
df = pd.merge(df, df_file, left_on=["rok", "miesiac", "dzien", "godzina", "dzien_tygodnia"], right_on=["rok", "miesiac", "dzien", "godzina", "dzien_tygodnia"])


# odczyt danych i wykonanie zlaczenia wewnetrznego kolejnych tabel dla wszystkich stacji analogicznie jak powyzej

for l in range(106,800):
    if os.path.isfile('pre_s_t_%d_2019.csv' % (l)):
        df_file = pd.DataFrame()
        df_file = pd.read_csv("D:\\Studia\\Energetyka\\Praca_inzynierska\\siec_neuronowa\\dane_testowe\\pre_s_t_%d_2019.csv" % l)
        df_file = df_file.drop(df_file.columns[0], axis=1)
        
        df = pd.merge(df, df_file, left_on=["rok", "miesiac", "dzien", "godzina", "dzien_tygodnia"], right_on=["rok", "miesiac", "dzien", "godzina", "dzien_tygodnia"])

        df.reset_index(drop = True, inplace = True)



#zapis tabeli do pliku csv
df.to_csv("D:\\Studia\\Energetyka\\Praca_inzynierska\\siec_neuronowa\\dane_testowe\\test_data_meteo.csv")

###################################################################################################

#czesc programu laczaca dane meteorologiczne i zapotrzebowania na moc w KSE z lat 2016-2018 

#odczyt tabeli z danymi meteorologicznymi z pliu csv
df_meteo = pd.read_csv("D:\\Studia\\Energetyka\\Praca_inzynierska\\siec_neuronowa\\dane_testowe\\test_data_meteo.csv")

df = pd.DataFrame()
df = df.append(df_meteo)
df = df.drop(df.columns[0], axis=1)


#odczyt tabeli z danumi o zapotrzebowaniu na moc w KSE
df_moc = pd.read_csv("D:\\Studia\\Energetyka\\Praca_inzynierska\\siec_neuronowa\\dane_testowe\\dane_moc.csv")

df_moc = df_moc.drop(df_moc.columns[0], axis=1)
df_moc.reset_index(drop = True, inplace = True)


#wykonanie zlaczenia wenwnetrznego tabel
df = pd.merge(df, df_moc, left_on=["rok", "miesiac", "dzien", "godzina"], right_on=["rok", "miesiac", "dzien", "godzina"])
    
#podzial tabli na czesc wejsciowa i czesc wyjsciowa sieci neuronowej
df_X = df.iloc[:, :347 ]
df_y = df.iloc[:, 347 ]


#zapis tabeli do plikow csv
df.to_csv("D:\\Studia\\Energetyka\\Praca_inzynierska\\siec_neuronowa\\dane_testowe\\test__data.csv")

df_X.to_csv("D:\\Studia\\Energetyka\\Praca_inzynierska\\siec_neuronowa\\dane_testowe\\test_data_X.csv")
df_y.to_csv("D:\\Studia\\Energetyka\\Praca_inzynierska\\siec_neuronowa\\dane_testowe\\test_data_y.csv")

#zapis danych wyjsciowych sieci jako arkusz kalkulacyjny
df_y.to_excel("D:\\Studia\\Energetyka\\Praca_inzynierska\\siec_neuronowa\\dane_testowe\\test_data_y.xlsx")
