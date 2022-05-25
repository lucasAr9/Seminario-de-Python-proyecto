import PySimpleGUI as sg
import src.pantallas.caracteristicas_generales as cg
from src.pantallas.menu_inicio_juego import crear_menu
from src.pantallas import configuracion as c_pantalla
from src.pantallas.cuentas import Perfiles


def accion_usuario(usuario):
    sg.Popup(f"Usuario seleccionado: {usuario}")


def accion_dificultad(dificultad):
    sg.Popup(f"Dificultad seleccionada: {dificultad}")


def accion_jugar():
    layout = [
        [sg.Text('ACA SE JUEGA :)', font=cg.FUENTE_INDICADOR)],
        [sg.Button("SALIR", key='-VOLVER_AL_MENU-', font=cg.FUENTE_BOTONES)]
    ]
    return sg.Window("Ventana de juego", layout, finalize=True)


def accion_configuracion():
    ventana_config = c_pantalla.crear_ventana()
    return ventana_config


def accion_puntajes():
    layout = [
        [sg.Text('ACA SE PUNTUA B)', font=FONT_TEXTOS)],
        [sg.Button("SALIR", key='-VOLVER_AL_MENU-', font=FONT_BOTONES)]
    ]
    return sg.Window("Ventana de juego", layout, finalize=True)


def accion_perfil(perfil):
    return perfil.crear_pantalla({"tam_ventana": cg.TAM_VENTANA, "font_botones": "Verdana 25"})


perfil = Perfiles()
crear_menu(perfil.perfiles())
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
        accion_perfil(perfil)
        current_window.close()
    elif event == '-VOLVER_AL_MENU-':
        crear_menu(perfil.perfiles())
        current_window.close()

    elif event == '-VOLVER_CONFIG-':
        crear_menu(perfil.perfiles())
        current_window.close()

    elif event == "-VOLVER_PERFILES-":
        lista_usuarios = perfil.perfiles()
        crear_menu(perfil.perfiles())
        current_window.close()

    perfil.analisis_event_editar(current_window, event, values)
