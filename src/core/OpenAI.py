from openai import OpenAI
from src.constants import exercises_default
import json
import re
import random


class MattzunuIA:

    def __init__(self, api_key):
        self.mode = "development"
        self.client = OpenAI(api_key=api_key)
        self.context_exercises = """
        Tema: Inteligencia Aritifial para ayudar a ninos a aprender matematicas basicas

        Eres una inteligencia artificial llamada "Matzununu" que ayuda a los ninos a aprender matematicas basicas.

        - Formato de la respuesta:
            - La respuesta debe ser varios bloques, el primero dentro de una etiqueta <operation></operation>, esta etiqueta debe contener las caracteristicas de la operacion en formato JSON, la primer propiedad es un array de numeros llamada "numbers" el cual tiene los numeros a realizar la operacion, el segundo es "operation" el cual tiene el tipo de ejercicio suma, resta, multiplicacion o division, el siguiente es level este indica el nivel de dificultad del ejercicio desde el 1 hasta el 10 que serian los ejercicios de mayor nivel para ninos de segundo de primaria. el ultimo es el result, que seria el resultado esperado de la operacion.
            - El segundo bloque debe ser una etiqueta <message></message> el cual es un mensaje amigable muy corto para el nino para motivarlo a resolver la operacion.
            - El tercer bloque debe ser una etiqueta <messageSuccess></messageSuccess> el cual es un mensaje amigable muy corto para el nino para mostrar que ha resuelto la operacion correctamente.
            - El cuarto bloque debe ser una etiqueta <messageFailure></messageFailure> el cual es un mensaje amigable muy corto para el nino para mostrar que la respuesta a la operacion fue incorrecta.
        """

    def extract_content(self, message: str):
        try:
            if not isinstance(message, str):
                raise ValueError("El mensaje no es del tipo string.")

            # Incluimos el modificador re.DOTALL para que . capture saltos de línea
            regexOperation = r'<operation>(.*?)</operation>'
            regexMessage = r'<message>(.*?)</message>'
            regexMessageSuccess = r'<messageSuccess>(.*?)</messageSuccess>'
            regexMessageFailure = r'<messageFailure>(.*?)</messageFailure>'

            # No sobrescribimos la variable `message`
            operation = re.findall(regexOperation, message, re.DOTALL)
            extractedMessage = re.findall(regexMessage, message, re.DOTALL)
            messageSuccess = re.findall(
                regexMessageSuccess, message, re.DOTALL)
            messageFailure = re.findall(
                regexMessageFailure, message, re.DOTALL)

            return {
                "operation": operation[0] if operation else None,
                "message": extractedMessage[0] if extractedMessage else None,
                "messageSuccess": messageSuccess[0] if messageSuccess else None,
                "messageFailure": messageFailure[0] if messageFailure else None,
            }
        except Exception as error:
            print(error)
            return None

    def convert_to_json(self, message: str):
        try:
            parse_message = json.loads(message)
            return parse_message
        except Exception as error:
            print(error)
            return message

    def generate_exercise(self, level: int):
        try:
            self.stream = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "system", "content": self.context_exercises}, {
                    "role": "user", "content": f"Genera un nuevo ejercicio de nivel {level}"}],
                stream=False,
            )

            message = self.stream.choices[0].message
            return message

        except Exception as error:
            # print(error)
            print("Error al generar ejercicio con IA")

            if (self.mode == "development"):
                default_message = random.choice(exercises_default)

                content = self.extract_content(default_message)
                content["operation"] = self.convert_to_json(
                    content["operation"])
                return content
