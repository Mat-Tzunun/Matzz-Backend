import torch
import numpy as np
from sklearn.preprocessing import StandardScaler

# 1. Clase que define el modelo


class ModeloIA(torch.nn.Module):
    def __init__(self):
        super(ModeloIA, self).__init__()
        # Capa de entrada con 4 características y 16 neuronas
        self.layer1 = torch.nn.Linear(4, 16)
        self.layer2 = torch.nn.Linear(16, 8)   # Capa oculta con 8 unidades
        self.output_layer = torch.nn.Linear(
            8, 3)  # Capa de salida con 3 clases

    def forward(self, x):
        x = torch.relu(self.layer1(x))
        x = torch.relu(self.layer2(x))
        x = self.output_layer(x)
        return x

# 2. Clase para manejar las predicciones y encapsular la lógica del modelo


class Prediccion:
    def __init__(self):
        # Cargar el modelo
        self.modelo = ModeloIA()
        try:
            state_dict = torch.load(
                'SRC/Core/modelo_decision_niveles.pth', weights_only=True)
            self.modelo.load_state_dict(state_dict)
            self.modelo.eval()
        except RuntimeError as e:
            print(f"Error al cargar el modelo: {e}")

        # Configurar el escalador
        self.escalador = StandardScaler()

        # Asegúrate de que el escalador esté ajustado a los datos de entrenamiento
        # Datos de entrenamiento reales
        X_train = np.array(
            [[12, 13.2, 55, 2], [11, 14.0, 60, 3], [10, 12.0, 50, 1]])
        # Ajustar el escalador con los datos de entrenamiento
        self.escalador.fit(X_train)

    def predecir(self, tupla):
        # Normalizar los datos de entrada
        # Convertir a array y dar forma (1, 4)
        data_input = np.array(tupla).reshape(1, -1)
        data_input_escalada = self.escalador.transform(
            data_input)  # Escalar los datos

        # Convertir a tensor
        data_input_tensor = torch.tensor(
            data_input_escalada, dtype=torch.float32)

        # Realizar la predicción
        with torch.no_grad():
            y_pred = self.modelo(data_input_tensor)

        # Interpretar la predicción
        y_pred_clase = torch.argmax(y_pred, dim=1)
        y_pred_clase = torch.where(y_pred_clase == 0, torch.tensor(-1.0),
                                   torch.where(y_pred_clase == 1, torch.tensor(0.0), torch.tensor(1.0)))

        return y_pred_clase.item()  # Retorna el valor escalar de la predicción

# # Crear una instancia de la clase Prediccion y hacer la predicción con la tupla deseada
# prediccion = Prediccion()
# tupla_de_prueba = (12, 5.2, 55, 1)  # Ejemplo de entrada
# resultado = prediccion.predecir(tupla_de_prueba)

# # Imprimir la predicción
# print(f"Predicción para la entrada {tupla_de_prueba}: {resultado}")
