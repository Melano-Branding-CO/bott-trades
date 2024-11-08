from modelos.lstm_xgboost_hybrid import modelo_hibrido_lstm_xgboost
from modelos.fine_tuning_bert import fine_tune_bert
from modelos.transfer_learning_gans import ajustar_gan
from modelos.federated_learning import modelo_federado
import time
import numpy as np
import matplotlib.pyplot as plt

def mostrar_progreso(mensaje, duracion=2):
    print(mensaje, end="", flush=True)
    for _ in range(3):
        print(".", end="", flush=True)
        time.sleep(duracion)
    print(" ¡Hecho!")

def ejecutar_orion_ai():
    print("\n=== BIENVENIDO A ORION AI ===\n")
    
    # Ejecutar la predicción del mercado con el modelo híbrido
    mostrar_progreso("Ejecutando predicción de mercado con LSTM + XGBoost", 1)
    data = np.sin(np.linspace(0, 50, 100)) + np.random.normal(0, 0.1, 100)  # Datos simulados
    modelo_hibrido_lstm_xgboost(data)
    
    # Fine-tuning de BERT para análisis de sentimiento financiero
    mostrar_progreso("Fine-Tuning de BERT en datos financieros", 1)
    fine_tune_bert()
    
    # Transfer Learning en GANs para simulación de escenarios
    mostrar_progreso("Transfer Learning en GANs", 1)
    ajustar_gan()
    
    # Federated Learning para entrenamiento distribuido
    mostrar_progreso("Iniciando entrenamiento Federated Learning", 1)
    modelo_federado()

    print("\n=== ORION AI TERMINADO ===\n")

if __name__ == "__main__":
    ejecutar_orion_ai()
