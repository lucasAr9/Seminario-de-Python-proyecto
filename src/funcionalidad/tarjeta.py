import rutas
import csv
import random
import os

from src.pantallas import caracteristicas_generales as cg


def datos_tarjeta(dataset, cant_pistas):
    """"""
    with (open(os.path.join(rutas.DATOS_DIR, f'dataset_{dataset}.csv'), 'r', encoding='utf=8', newline='')) as archivo:
        csv_reader = csv.reader(archivo)
        cabecera, contenido = csv_reader.__next__(), [linea for linea in csv_reader]

    linea_dataset = contenido[random.randrange(len(contenido))]

    respuesta_correcta = linea_dataset[-1]
    x = [linea[-1] for linea in contenido]
    x.remove(respuesta_correcta)
    respuestas_posibles = random.choices(x, k=cg.CANT_RESPUESTAS - 1)
    respuestas_posibles.insert(random.randrange(cg.CANT_RESPUESTAS), respuesta_correcta)
    dicc_respuestas = {'Titulo': cabecera[-1], 'Correcta': respuesta_correcta, 'Posibles': respuestas_posibles}

    dicc_pistas = {tipo: dato for tipo, dato in zip(cabecera[:cant_pistas], linea_dataset[:cant_pistas])}

    return dicc_pistas, dicc_respuestas