import PySimpleGUI as sg
import src.pantallas.caracteristicas_generales as cg
from src.pantallas.menu_inicio_juego import crear_menu
from src.pantallas import configuracion as c_pantalla
import src.pantallas.cuentas as cuentas
from src.pantallas import puntajes
from src.pantallas import juego


def accion_usuario(usuario):
    sg.Popup(f"Usuario seleccionado: {usuario}")


def accion_dificultad(dificultad):
    sg.Popup(f"Dificultad seleccionada: {dificultad}")


def accion_jugar():
    ventana_juego = juego.armar_ventana()
    return ventana_juego


def accion_configuracion():
    ventana_config = c_pantalla.crear_ventana()
    return ventana_config


def accion_puntajes():
    ventana_puntajes = puntajes.armar_ventana()
    return ventana_puntajes


def accion_perfil():
    return cuentas.crear_cuentas({"tam_ventana": cg.TAM_VENTANA, "font_botones": "Verdana 25"})


conf_cuentas = {"perfiles": cuentas.cargar_perfiles(), "act": 0}
perfiles = list(map(lambda datos: datos['nombre'], conf_cuentas['perfiles']))
crear_menu(perfiles)
while True:
    current_window, event, values = sg.read_all_windows()
    if event == sg.WIN_CLOSED:
        current_window.close()
        break
    elif event == '-SALIR-':
        current_window.close()
        break
    elif event == '-USUARIOS-':
        accion_usuario(current_window['-USUARIOS-'].Get())
    elif event == '-DIFICULTAD-':
        accion_dificultad(current_window['-DIFICULTAD-'].Get())
    elif event == '-JUGAR-':
        accion_jugar()
        current_window.close()
    elif event == '-CONFIGURACION-':
        accion_configuracion()
        current_window.close()
    elif event == '-PUNTAJES-':
        accion_puntajes()
        current_window.close()
    elif event == '-PERFIL-':
        accion_perfil()
        current_window.close()
    elif event == '-VOLVER_AL_MENU-':
        crear_menu(perfiles)
        current_window.close()
    elif (event == '-JUEGO_ABANDONAR-' and
          cg.ventana_chequear_accion('Se darán por perdidas la ronda actual\ny las rondas restantes!\n\n'
                                     'Segurx que querés volver al menú?') == 'Sí'):
        crear_menu(perfiles)
        current_window.close()

    #  https://github.com/PySimpleGUI/PySimpleGUI/issues/3771
    elif event == (sg.WINDOW_CLOSE_ATTEMPTED_EVENT and
                   cg.ventana_chequear_accion() == 'Sí'):
        break

    elif event == '-VOLVER_CONFIG-':
        crear_menu(perfiles)
        current_window.close()

    elif event == "-VOLVER_PERFILES-":
        conf_cuentas = {"perfiles": cuentas.cargar_perfiles(), "act": 0}
        perfiles = list(map(lambda datos: datos['nombre'], conf_cuentas['perfiles']))
        crear_menu(perfiles)
        current_window.close()

    cuentas.analisis_event_cuentas(current_window, event, values,conf_cuentas)