# -*- coding: utf-8 -*-


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


#funkcja odczytująca dane meteorologiczne z pliku csv
def pobierz_dane_meteo(plikcsv, dict_dane_meteo):


    #zmienna pomocnicza do przypisywania id_pomiaru
    i=1
    
    if os.path.isfile(plikcsv):  # sprawdzenie czy plik istnieje na dysku
        with open(plikcsv, "r") as zawartosc:  # otwarcie plik do odczytu
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
        print("Plik z danymi", plikcsv, "nie istnieje!") #wyswietla komentarz, jezeli nie znaleziono pliku

    i=1

    return 1


#funkcja odczytujaca dane o mocy w KSE z pliku csv
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
                
                #stworzenie instancji klasy Dane_zapotrzebowanie
                dane = Dane_zapotrzebowanie(rok = int(rok),
                                            miesiac = int(miesiac),
                                            dzien = int(dzien),
                                            godzina = int(krotka[1]) - 1,
                                            zapotrzebowanie = float(krotka[3]))
                
                # dodanie danych z instancji klasy do slownika
                dict_dane_moc.setdefault("rok", []).append(dane.rok)
                dict_dane_moc.setdefault("miesiac", []).append(dane.miesiac)
                dict_dane_moc.setdefault("dzien", []).append(dane.dzien)
                dict_dane_moc.setdefault("godzina", []).append(dane.godzina)
                dict_dane_moc.setdefault("zapotrzebowanie_moc", []).append(dane.zapotrzebowanie)

               
    else:
        print("Plik z danymi", plikcsv, "nie istnieje!") #wyswietla komentarz, jezeli nie znaleziono pliku

    return 1


# odczytywanie danych meteorologicznych z lat 2016-2018 z poszczegolnych stacji za pomoca funkcji pobierz_dane_meteo
for k in range(2016,2019):  # k-rok
    os.chdir("D:\\Studia\\Energetyka\\Praca_inzynierska\\siec_neuronowa\\dane_uczenie\\%d" % k)

    for l in range(100,800): # l-numer stacji
        dict_dane_meteo={}
        if os.path.isfile('s_t_%d_%d.csv' % (l, k)):
            pobierz_dane_meteo('s_t_%d_%d.csv' % (l, k), dict_dane_meteo)
            
            
            #zamiana zwroconego przez funkcje slownika na DataFrame oraz zapis wyniku do pliku csv
            df = pd.DataFrame(dict_dane_meteo)
            df.to_csv("D:\\Studia\\Energetyka\\Praca_inzynierska\\siec_neuronowa\\dane_uczenie\\dane_uczenie_przygotowanie\\%d\\pre_s_t_%d_%d.csv" % (k, l, k))



# odczytanie danych o zapotrzebowanie na moc w KSE z lat 2016-2018 za pomoca funkcji pobierz_dane_moc
dict_dane_moc = {}
for k in range(2016, 2019):  # k-rok
    os.chdir("D:\\Studia\\Energetyka\\Praca_inzynierska\\siec_neuronowa\\dane_uczenie\\%d" % (k))
    for l in range(1, 13):  # l-miesiac
        if os.path.isfile('KSE_%d_%d.csv' % (k, l)):
            print(k, l)
            pobierz_dane_moc('KSE_%d_%d.csv' % (k, l), dict_dane_moc)
            
            #zamiana zwroconego przez funkcje slownika na DataFrame oraz zapis wyniku do pliku csv
            df = pd.DataFrame(dict_dane_moc)
            df.to_csv("D:\\Studia\\Energetyka\\Praca_inzynierska\\siec_neuronowa\\dane_uczenie\\dane_uczenie_przygotowanie\\dane_moc.csv")


##########################################################################################
            
# czesc programu laczaca tabele z danymi ze wszystkich stacji l dla danego roku k
for k in range(2016, 2019): # k-rok
    file1 = pd.DataFrame() # zmienna pomocnicza
    file2 = pd.DataFrame() # zmienna pomocnicza
    
    os.chdir("D:\\Studia\Energetyka\\Praca_inzynierska\\siec_neuronowa\\dane_uczenie\\dane_uczenie_przygotowanie\\%d" % k)
    
    #odczyt poszczegolnych tabeli i przypisanie do zmiennych pomocniczych dwoch pierwszych stacji
    file1 = pd.read_csv("D:\\Studia\Energetyka\\Praca_inzynierska\\siec_neuronowa\\dane_uczenie\\dane_uczenie_przygotowanie\\%d\\pre_s_t_100_%d.csv" % (k, k))
    file2 = pd.read_csv("D:\\Studia\Energetyka\\Praca_inzynierska\\siec_neuronowa\\dane_uczenie\\dane_uczenie_przygotowanie\\%d\\pre_s_t_105_%d.csv" % (k, k))
    
    #usuniecie kolumny z numerem wiersza
    file1 = file1.drop(file1.columns[0], axis=1)
    file2 = file2.drop(file2.columns[0], axis=1)
    
    #wykonanie zlaczenia wewnetrznego tabel
    df = pd.merge(file1, file2, left_on=["rok", "miesiac", "dzien", "godzina", "dzien_tygodnia"], right_on=["rok", "miesiac", "dzien", "godzina", "dzien_tygodnia"])
    
    # odczyt danych i wykonanie zlaczenia wewnetrznego kolejnych tabel dla wszystkich stacji analogicznie jak powyzej
    os.chdir("D:\\Studia\Energetyka\\Praca_inzynierska\\siec_neuronowa\\dane_uczenie\\dane_uczenie_przygotowanie\\%d" % k)
    for l in range(106, 900): # l-numer staji
            
        if os.path.isfile('pre_s_t_%d_%d.csv' % (l, k)):
            
            file1 = pd.read_csv("D:\\Studia\Energetyka\\Praca_inzynierska\\siec_neuronowa\\dane_uczenie\\dane_uczenie_przygotowanie\\%d\\pre_s_t_%d_%d.csv" % (k, l, k))
            file1 = file1.drop(file1.columns[0], axis=1)
        
            df = pd.merge(df, file1, left_on=["rok", "miesiac", "dzien", "godzina", "dzien_tygodnia"], right_on=["rok", "miesiac", "dzien", "godzina", "dzien_tygodnia"])
            
    #zapis otrzymanej tabeli do pliku csv
    df.to_csv("D:\\Studia\\Energetyka\\Praca_inzynierska\\siec_neuronowa\\dane_uczenie\\dane_uczenie_przygotowanie\\pre_data_%d.csv" % k)
    
    
#####################################################################################################

#czesc programu laczaca dane meteorologiczne i zapotrzebowania na moc w KSE z lat 2016-2018 

#odczytanie tabeli z plikow csv
df2016 = pd.read_csv("D:\\Studia\\Energetyka\\Praca_inzynierska\\siec_neuronowa\\dane_uczenie\\dane_uczenie_przygotowanie\\pre_data_2016.csv")
df2017 = pd.read_csv("D:\\Studia\\Energetyka\\Praca_inzynierska\\siec_neuronowa\\dane_uczenie\\dane_uczenie_przygotowanie\\pre_data_2017.csv")
df2018 = pd.read_csv("D:\\Studia\\Energetyka\\Praca_inzynierska\\siec_neuronowa\\dane_uczenie\\dane_uczenie_przygotowanie\\pre_data_2018.csv")
df_moc = pd.read_csv("D:\\Studia\\Energetyka\\Praca_inzynierska\\siec_neuronowa\\dane_uczenie\\dane_uczenie_przygotowanie\\dane_moc.csv")

#polaczenie tabeli zawierajacych dane meteorologiczne 
df = pd.DataFrame()

df = df.append(df2016)
df = df.append(df2017)
df = df.append(df2018)

#usuniecie kolumny z numerami wierszy
df = df.drop(df.columns[0], axis=1)

#ponowne indeksowanie wierszy tabeli
df.reset_index(drop = True, inplace = True)

#wykonanie zlaczenia wewnetrznego tabeli z danymi meteorologicznymi z tabela z danymi zapotrzebowania na moc w KSE 
df = pd.merge(df, df_moc, left_on=["rok", "miesiac", "dzien", "godzina"], right_on=["rok", "miesiac", "dzien", "godzina"])
df = df.drop(df.columns[347], axis=1)

#podzielenie tabeli ze wszystkimi danymi na dane wejsciowe X oraz na dany wyjsciowe Y
df_X = df.iloc[:, :347 ]
df_y = df.iloc[:, 347 ]

#zapis glownej tabeli z danymi do pliku csv
df.to_csv("D:\\Studia\\Energetyka\\Praca_inzynierska\\siec_neuronowa\\dane_uczenie\\dane_uczenie_przygotowanie\\train_data.csv")

#zapis tabeli z danymi wejsciowymi X oraz tabeli z danymi wyjsciowymi Y
df_X.to_csv("D:\\Studia\\Energetyka\\Praca_inzynierska\\siec_neuronowa\\dane_uczenie\\dane_uczenie_przygotowanie\\train_data_X.csv")
df_y.to_csv("D:\\Studia\\Energetyka\\Praca_inzynierska\\siec_neuronowa\\dane_uczenie\\dane_uczenie_przygotowanie\\train_data_y.csv")