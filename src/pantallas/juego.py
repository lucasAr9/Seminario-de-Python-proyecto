import PySimpleGUI as sg
import random
from src.pantallas import caracteristicas_generales as cgen
from src.juego import dificultad as dificultad
from src.pantallas import rutas
from src.juego import tarjeta


def armar_layout(datos, dificultad_elegida, usuario_elegido):
    """"""
    # dataset_elegido = random.choice(cgen.datasets)
    dataset_elegido = 'volcanes'
    pistas, respuestas = tarjeta.datos_tarjeta(dataset_elegido, datos.nivel)
    titulos = ['Pregunta', 'Resultado']
    resultados = ['Bien', 'Mal', 'Bien', 'Mal', 'Bien', 'Mal', 'Bien', 'Mal', 'Bien', 'Mal']

    columna_izq = [[sg.Frame('Dificultad',
                             [[sg.Text(dificultad_elegida, font=cgen.FUENTE_COMBO)]],
                             expand_x=True)],
                   [sg.Frame('Tema',
                             [[sg.Text(dataset_elegido.title(), font=cgen.FUENTE_OPCIONES),
                               sg.Image(rutas.ruta_imagen(dataset_elegido))]])],
                   [sg.VPush()],
                   [sg.Button('Abandonar',
                              key='-JUEGO_ABANDONAR-',
                              tooltip='Volver al menú principal',
                              font=cgen.FUENTE_OPCIONES)]
                   ]
    columna_centro = [[sg.Frame('Tiempo restante',
                                [[sg.Text(f'00:00', key='-JUEGO_TIEMPO-',
                                  font=cgen.FUENTE_COMBO),
                                  sg.ProgressBar(datos.tiempo,
                                                 orientation='h',
                                                 size=(18, 20),
                                                 key='-JUEGO_BARRA-')
                                  ]])],
                      [sg.Frame('Tarjeta',
                                [[sg.Text(f'{nombre}: {dato}', font=cgen.FUENTE_OPCIONES)]
                                 for nombre, dato in pistas.items()] +
                                [[sg.Text(f'{respuestas["Titulo"]}: ', pad=5, font=cgen.FUENTE_COMBO)]] +
                                [[sg.Radio(respuestas['Posibles'][i], group_id='respuestas',
                                           font=cgen.FUENTE_OPCIONES, key=f'-JUEGO_RESPUESTA{str(i)}-')]
                                 for i in range(cgen.CANT_RESPUESTAS)] +
                                [[sg.Ok(pad=15, font=cgen.FUENTE_COMBO),
                                  sg.Push(),
                                  sg.Button('Pasar >', pad=15, key='-JUEGO_PASAR-', font=cgen.FUENTE_COMBO)]],
                                expand_x=True
                                )]
                      ]
    columna_der = [[sg.Frame('Usuario',
                             [[sg.Text(usuario_elegido, font=cgen.FUENTE_COMBO)]],
                             expand_x=True)],
                   [sg.Table(values=list(enumerate(resultados, start=1)),
                             headings=titulos, max_col_width=25,
                             auto_size_columns=False, justification='center',
                             num_rows=10, key='-JUEGO_TABLA-',
                             row_height=25, font=cgen.FUENTE_OPCIONES, expand_x=True)]
                   ]

    layout = [[sg.Text('FiguRace',
                       justification='c', expand_x=True,
                       font=cgen.FUENTE_TITULO)],
              [sg.HSep(pad=10)],
              # [sg.Button('Comenzar', key='-JUEGO_COMENZAR-')],
              [sg.Push(),
               sg.Column(columna_izq, expand_y=True),
               sg.Push(),
               sg.Column(columna_centro, expand_y=True),
               sg.Push(),
               sg.Column(columna_der, expand_y=True),
               sg.Push()],
              [sg.Sizegrip()]
              ]

    layout_encuadre = [[sg.Frame('', layout, expand_x=True, expand_y=True)]]

    return layout_encuadre


def armar_ventana(dificultad_elegida, usuario_elegido):
    sg.theme(cgen.TEMA)
    datos = dificultad.Dificultad('-' + dificultad_elegida.upper() + '-')
    window = sg.Window('Juego', armar_layout(datos, dificultad_elegida, usuario_elegido),
                       size=cgen.TAM_VENTANA, resizable=True, no_titlebar=True,
                       grab_anywhere=True, finalize=True)
    return window

# if __name__ == '__main__':
#     window = armar_ventana()
#     tiempo_comienzo = time.time()
#     while True:
#          event, values = window.read(timeout=1000)
#          if ((event == '-JUEGO_ABANDONAR-') and
#              (cgen.ventana_chequear_accion('Se darán por perdidas la ronda actual\ny las rondas restantes!\n\n'
#                                           'Segurx que querés volver al menú?') == 'Sí')):
#              break
#          delta_tiempo = time.time() - tiempo_comienzo
#          current_time = int(seg_por_respuesta - delta_tiempo)
#          minutos, segundos = divmod(current_time, 60)
#          tiempo = f'{minutos:02d}:{segundos:02d}'
#          window['-JUEGO_TIEMPO-'].update(f'{minutos:02d}:{segundos:02d}')
#          window['-JUEGO_BARRA-'].update(current_count=delta_tiempo+1)
#
#     window.close()
