import numpy as np
import pandas as pd

def seventh_network():
    
    #wczytanie danych
    dataset_input = pd.read_csv("D:\\Studia\\Energetyka\\Praca_inzynierska\\siec_neuronowa\\dane_uczenie\\dane_uczenie_prepreparation\\train_data_X.csv") #You need to change #directory accordingly
    dataset_input = dataset_input.drop(dataset_input.columns[0], axis=1)
  
    dataset_output = pd.read_csv("D:\\Studia\\Energetyka\\Praca_inzynierska\\siec_neuronowa\\dane_uczenie\\dane_uczenie_prepreparation\\train_data_y.csv")
   
    
    
    #Zamiana DataFrame na numpy array
    X = dataset_input.iloc[:].values
    y = dataset_output.iloc[:].values
    
    #Normalizowanie danych
    from sklearn.preprocessing import StandardScaler
    sc = StandardScaler()
    X = sc.fit_transform(X)
    y = sc.fit_transform(y)
    
    #Implementacja sieci neuronowej
    from keras.models import Sequential
    from keras.layers import Dense
    
    model = Sequential()
    model.add(Dense(630, input_dim=347, activation="tanh"))
    model.add(Dense(512, activation="tanh"))
    model.add(Dense(512, activation="tanh"))
    model.add(Dense(448, activation="tanh"))
    model.add(Dense(448, activation="tanh"))
    model.add(Dense(384, activation="tanh"))
    model.add(Dense(384, activation="tanh"))
    model.add(Dense(320, activation="tanh"))
    model.add(Dense(320, activation="tanh"))
    model.add(Dense(256, activation="tanh"))
    model.add(Dense(256, activation="tanh"))
    model.add(Dense(192, activation="tanh"))
    model.add(Dense(192, activation="tanh"))
    model.add(Dense(128, activation="tanh"))
    model.add(Dense(128, activation="tanh"))
    model.add(Dense(96, activation="tanh"))
    model.add(Dense(96, activation="tanh"))
    model.add(Dense(80, activation="tanh"))
    model.add(Dense(80, activation="tanh"))
    model.add(Dense(64, activation="tanh"))
    model.add(Dense(64, activation="tanh"))
    model.add(Dense(48, activation="tanh"))
    model.add(Dense(48, activation="tanh"))
    model.add(Dense(40, activation="tanh"))
    model.add(Dense(40, activation="tanh"))
    model.add(Dense(32, activation="tanh"))
    model.add(Dense(32, activation="tanh"))
    model.add(Dense(24, activation="tanh"))
    model.add(Dense(24, activation="tanh"))
    model.add(Dense(16, activation="tanh"))
    model.add(Dense(16, activation="tanh"))
    model.add(Dense(12, activation="tanh"))
    model.add(Dense(12, activation="tanh"))
    model.add(Dense(8, activation="tanh"))
    model.add(Dense(8, activation="tanh"))
    model.add(Dense(4, activation="tanh"))
    model.add(Dense(4, activation="tanh"))
    model.add(Dense(2, activation="tanh"))
    model.add(Dense(2, activation="tanh"))
    model.add(Dense(1, activation="linear"))
    
    model.compile(loss='mean_squared_error', optimizer='SGD', metrics=['accuracy'])
    
    #uczenie sieci
    history = model.fit(X, y, epochs=4000, batch_size=1024)
    
    #zapis modelu wraz z wagami
    model.save("D:\\Studia\\Energetyka\\Praca_inzynierska\\siec_neuronowa\\seventh_model.h5")