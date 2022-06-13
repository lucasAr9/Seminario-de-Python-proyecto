import PySimpleGUI as sg
import time

from src.pantallas import caracteristicas_generales as cg
from src.funcionalidad import dificultad as dificultad
from src.pantallas.menu_inicio_juego import crear_menu
from src.pantallas import configuracion as c_pantalla
from src.pantallas import cuentas as cuentas
from src.pantallas import puntajes
from src.pantallas import juego


def nivel(window_dificultad, elegido):
    """Crear la ventana que muestra las características de cada nivel no modificable."""
    window_otra = c_pantalla.nivel_elegida(elegido)
    window_dificultad.hide()
    event, values = window_otra.read()
    if event == '-VOLVER_VALORES-':
        window_otra.close()
    window_dificultad.un_hide()


def abrir_configuracion():
    """Crear la ventana de configuración y responder a los eventos en la misma."""
    window_dificultad = c_pantalla.crear_ventana()
    while True:
        event, values = window_dificultad.read()
        if event in (sg.WIN_CLOSED, '-VOLVER_CONFIG-'):
            break
        if event == '-FACIL-':
            nivel(window_dificultad, '-FACIL-')
        elif event == '-NORMAL-':
            nivel(window_dificultad, '-NORMAL-')
        elif event == '-DIFICIL-':
            nivel(window_dificultad, '-DIFICIL-')

        elif event == '-PERSONALIZADO-':
            window_otra = c_pantalla.dificultad_personalizada()
            window_dificultad.hide()
            while True:
                event, values2 = window_otra.read()
                if event in (sg.WIN_CLOSED, '-VOLVER_PERSONALIZADO-'):
                    break
                if event == '-CAMBIOS_CONFIRMADOS-':
                    dificultad.guardar_nivel_personalizado(values2)
            if event == '-VOLVER_PERSONALIZADO-':
                window_otra.close()
            window_dificultad.un_hide()
    window_dificultad.close()


def abrir_puntajes():
    """Crear la ventana de puntajes y responder a los eventos en la misma."""
    window = puntajes.armar_ventana()
    while True:
        event, values = window.read()
        if event in (sg.WIN_CLOSED, '-VOLVER_AL_MENU-'):
            break
    window.close()


def abrir_perfiles():
    """Crear la ventana de perfiles y responder a los eventos en la misma."""
    conf_cuentas = {"perfiles": cuentas.cargar_perfiles(), "act": 0}
    window = cuentas.crear_cuentas(conf_cuentas)
    while True:
        event, values = window.read()
        if event in (sg.WIN_CLOSED, '-VOLVER_PERFILES-'):
            conf_cuentas["perfiles"] = cuentas.cargar_perfiles()
            nicks_perfiles = [x["nombre"] for x in conf_cuentas["perfiles"]]
            break
        elif event == '-ACEPTAR_PERFIL-':
            cuentas.seleccionar_perfil(window, values, conf_cuentas)
        elif event == '-PERFIL_NUEVO-':
            cuentas.crear_perfil(window)
        elif event == '-BTN_EDITAR-':
            cuentas.editar_perfil(window, conf_cuentas)
        elif event == '-BTN_EDITAR_ELIMINAR-':
            cuentas.eliminar_perfil(window, conf_cuentas)
        elif event == '-BTN_CREAR-':
            cuentas.aceptar_crear(window, values, conf_cuentas)
        elif event == '-BTN_CANCELAR_CREAR-':
            cuentas.cancelar_crear(window)
        elif event == '-BTN_EDITAR_CANCELAR-':
            cuentas.cancelar_edicion(window)
        elif event == '-BTN_APLICAR_EDICION-':
            cuentas.aplicar_edicion(window, values, conf_cuentas)
    window.close()
    return nicks_perfiles


def abrir_juego(dificultad_elegida, usuario_elegido):
    """Crear la ventana de juego y responder a los eventos en la misma."""
    window = juego.armar_ventana(dificultad_elegida, usuario_elegido)
    tiempo_comienzo = time.time()
    while True:
        event, values = window.read(timeout=100)
        if ((event == '-JUEGO_ABANDONAR-') and
                (cg.ventana_chequear_accion(window, 'Se darán por perdidas la ronda actual\ny las rondas restantes!\n\n'
                                                    'Segurx que querés volver al menú?') == 'Sí')):
            break
        delta_tiempo = time.time() - tiempo_comienzo
        tiempo_transcurrido = int(5 - delta_tiempo)
        minutos, segundos = divmod(tiempo_transcurrido, 60)
        window['-JUEGO_TIEMPO-'].update(f'{minutos:02d}:{segundos:02d}')
        window['-JUEGO_BARRA-'].update(current_count=delta_tiempo + 1)
    window.close()


def main():
    """Crear la ventana menú inicial y responder a los eventos en la misma."""
    usuario_elegido = False
    dificultad_elegida = False
    indicador_visible = False
    niveles = ['Fácil', 'Medio', 'Difícil', 'Experto']
    perfiles = cuentas.nombre_perfiles()
    window = crear_menu(perfiles)
    while True:
        event, values = window.read(timeout=100)
        if (event in (sg.WINDOW_CLOSE_ATTEMPTED_EVENT, '-SALIR-') and
                (cg.ventana_chequear_accion(window) == 'Sí')):
            break
        match event:
            case '-USUARIOS-':
                usuario_elegido = window['-USUARIOS-'].Get()
            case '-DIFICULTAD-':
                dificultad_elegida = window['-DIFICULTAD-'].Get()
                if dificultad_elegida == 'Personalizado':
                    window['-AVISO_PER-'].update(visible=True)
                else:
                    window['-AVISO_PER-'].update(visible=False)
            case '-JUGAR-':
                if usuario_elegido and dificultad_elegida:
                    window.hide()
                    abrir_juego(dificultad_elegida, usuario_elegido)
                    window.un_hide()
                else:
                    cg.ventana_popup(window, 'Por favor seleccione una dificultad y usuario, antes de comenzar a jugar.')
            case '-CONFIGURACION-':
                window.hide()
                abrir_configuracion()
                window.un_hide()
            case '-PUNTAJES-':
                window.hide()
                abrir_puntajes()
                window.un_hide()
            case '-PERFIL-':
                window.hide()
                perfiles = abrir_perfiles()
                window.un_hide()
                window['-USUARIOS-'].update('Seleccione su usuario', values=perfiles)
                usuario_elegido = ''
        # Control de indicador_perfiles
        if not perfiles and not indicador_visible:
            window['-INDICADOR-'].update(visible=True)
            indicador_visible = True
        elif perfiles:
            window['-INDICADOR-'].update(visible=False)
            indicador_visible = False

    window.close()


if __name__ == "__main__":
    main()
