# -*- coding: utf-8 -*-


import pandas as pd

#wczytanie danych
dataset_input = pd.read_csv("D:\\Studia\\Energetyka\\Praca_inzynierska\\siec_neuronowa\\dane_testowe\\test_random_data_X.csv") 
dataset_input = dataset_input.drop(dataset_input.columns[0], axis=1)

dataset_output = pd.read_csv("D:\\Studia\\Energetyka\\Praca_inzynierska\\siec_neuronowa\\dane_testowe\\test_random_data_y.csv")
dataset_output = dataset_output.drop(dataset_output.columns[0], axis=1)



#Zamiana DataFrame na numpy array
X = dataset_input.iloc[:].values
y = dataset_output.iloc[:].values

#Normalizowanie danych 
from sklearn.preprocessing import StandardScaler
sc = StandardScaler()
X = sc.fit_transform(X)
y = sc.fit_transform(y)



from keras.models import load_model

#wczytanie modelu
model = load_model("D:\\Studia\\Energetyka\\Praca_inzynierska\\siec_neuronowa\\ninth_model.h5")

#prognozowanie
output_data = model.predict(X)

#Przywrocenie poprzedniej skali wartosci danych
output_data = sc.inverse_transform(output_data)

#zamiana numpy array na DataFrame 
true_data = pd.DataFrame(dataset_output.iloc[:].values)
pred_data = pd.DataFrame(output_data)

#zapis wynikow prognozy jako arkusz kalkulacyjny
pred_data.to_excel("D:\\Studia\\Energetyka\\Praca_inzynierska\\siec_neuronowa\\dane_testowe\\pred_random_data.xlsx")

