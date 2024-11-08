import numpy as np
import pandas as pd
from sklearn.svm import SVR
from sklearn.model_selection import train_test_split
import yfinance as yf

class NemesisBot:
    def __init__(self):
        self.modelo = SVR(kernel='rbf')

    def cargar_datos_mercado(self, simbolo, periodo):
        """
        Cargar datos de mercado de Yahoo Finance.
        """
        self.datos = yf.download(simbolo, period=periodo)
        print(f"Datos de {simbolo} descargados exitosamente.")
    
    def entrenar_modelo(self, columna_objetivo='Close'):
        """
        Entrenar el modelo de trading con los datos históricos.
        """
        X = np.array(self.datos.index.strftime('%Y%m%d')).reshape(-1, 1)
        y = self.datos[columna_objetivo].values
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        self.modelo.fit(X_train, y_train)
        score = self.modelo.score(X_test, y_test)
        print(f"Modelo entrenado con precisión: {score:.2f}")

    def predecir_precio(self, fecha):
        """
        Predecir el precio de mercado en una fecha futura.
        """
        prediccion = self.modelo.predict(np.array([[int(fecha.strftime('%Y%m%d'))]]))
        print(f"Predicción del precio: {prediccion[0]}")
        return prediccion

# Ejemplo de uso
nemesis = NemesisBot()
nemesis.cargar_datos_mercado('AAPL', '1y')
nemesis.entrenar_modelo()
prediccion = nemesis.predecir_precio(pd.to_datetime('2024-12-01'))
