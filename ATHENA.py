import pandas as pd
import numpy as np
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split

class AthenaBot:
    def __init__(self):
        self.modelo_riesgo = KNeighborsClassifier(n_neighbors=3)

    def cargar_datos_inversiones(self, archivo):
        """
        Cargar datos de perfiles de inversión y riesgo.
        """
        self.datos = pd.read_csv(archivo)
        print("Datos de inversión cargados.")
    
    def analizar_perfil_riesgo(self, datos_cliente):
        """
        Asignar un perfil de riesgo basado en los datos del cliente.
        """
        X = self.datos[['Edad', 'Ingresos', 'Experiencia']]
        y = self.datos['Riesgo']
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        self.modelo_riesgo.fit(X_train, y_train)
        score = self.modelo_riesgo.score(X_test, y_test)
        print(f"Precisión del análisis de riesgo: {score:.2f}")
        
        prediccion = self.modelo_riesgo.predict([datos_cliente])
        return prediccion

    def generar_estrategia_inversion(self, perfil_riesgo):
        """
        Generar recomendaciones de inversión según el perfil de riesgo.
        """
        if perfil_riesgo == 'Bajo':
            return "Recomendamos inversiones conservadoras en bonos del Estado."
        elif perfil_riesgo == 'Medio':
            return "Recomendamos una mezcla balanceada de bonos e índices bursátiles."
        elif perfil_riesgo == 'Alto':
            return "Recomendamos inversiones agresivas en acciones de alto rendimiento."
        else:
            return "Por favor, proporcione un perfil de riesgo válido."

# Ejemplo de uso
athena = AthenaBot()
athena.cargar_datos_inversiones('datos_inversiones.csv')
perfil_riesgo = athena.analizar_perfil_riesgo([35, 70000, 5])  # Edad, Ingresos, Experiencia
estrategia = athena.generar_estrategia_inversion(perfil_riesgo)
print(estrategia)
