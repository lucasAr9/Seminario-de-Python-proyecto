import PySimpleGUI as sg
import os
import json
import sys

sys.path.append(os.getcwd())

import src.pantallas.caracteristicas_generales as fs


def cargar_perfiles():
    """
    Carga como valor privado de la clase los perfiles.
    :return: Los datos de cada perfil que hay.
    """
    try:
        archivo_url = os.path.join(os.path.realpath('..'), "recursos", "datos", "perfiles.json")
        try:
            with open(archivo_url, "r", encoding="utf-8") as arch_perfiles:
                perfiles = json.load(arch_perfiles)
        except FileNotFoundError:
            with open(archivo_url, "w", encoding="utf-8") as arch_perfiles:
                perfiles = []
                json.dump(perfiles, arch_perfiles)
    except FileNotFoundError:
        archivo_url = os.path.join(os.getcwd(), "recursos", "datos", "perfiles.json")
        try:
            with open(archivo_url, "r", encoding="utf-8") as arch_perfiles:
                perfiles = json.load(arch_perfiles)
        except FileNotFoundError:
            with open(archivo_url, "w", encoding="utf-8") as arch_perfiles:
                perfiles = []
                json.dump(perfiles, arch_perfiles)
    return perfiles


def actualizar_perfiles(perfiles, nuevo_perfil=None):
    """
    Actualiza el archivo json de perfiles.
    :param 
        perfiles: los datos de todos los perfiles.
        nuevo_perfil: diccionario con la informacion del perfil nuevo ingresada por el usuario.
    :return: los datos actualizados de los perfiles.
    """
    if nuevo_perfil is not None:
        perfiles.append(nuevo_perfil)

    try:
        archivo_url = os.path.join(os.getcwd(), "recursos", "datos", "perfiles.json")
        with open(archivo_url, "w", encoding="utf-8") as arch_perfiles:
            json.dump(perfiles, arch_perfiles)
    except FileNotFoundError:
        archivo_url = os.path.join(os.path.realpath('..'), "recursos", "datos", "perfiles.json")
        with open(archivo_url, "w", encoding="utf-8") as arch_perfiles:
            json.dump(perfiles, arch_perfiles)
    return perfiles


def comprobar_y_cargar(window, values, op, conf):
    """
    Verifica si los datos ingresados son correctos, si lo son carga el perfil, sino envia un mensaje al usuario.
    :param
        window: variable para actualizar el contenido de la pantalla.
        values: variable para acceder a los valores de la pantalla.
        op: variable que indica si la llamada proviende de la creacion o edicion de un perfil.
        conf: las variables internas de la pantalla configuracion.
    :return: False si la informacion no es correcta, True de lo contrario.
    """
    if op == 1:
        if values["-INPUT_EDAD-"] == "" or values["-INPUT_GENERO-"] == "":
            window["-MSJ_EDITAR-"].update(value="*Ingrese todos los datos.")
            return False
        elif list(filter(lambda x: x > "9" or x < "0", values["-INPUT_EDAD-"])):
            window["-MSJ_EDITAR-"].update(value="*La edad no es correcta.")
            return False
        else:
            conf["perfiles"][conf["act"]]["edad"] = values["-INPUT_EDAD-"]
            conf["perfiles"][conf["act"]]["genero"] = values["-INPUT_GENERO-"]
            conf["perfiles"] = actualizar_perfiles(conf["perfiles"])
            return True
    elif op == 2:
        if values["-NUEVO_NOMBRE-"] == "" or values["-NUEVO_EDAD-"] == "" or values["-NUEVO_GENERO-"] == "":
            window["-MSJ_CREAR-"].update(value="*Ingrese todos los datos.")
            return False
        elif [x for x in conf["perfiles"] if x["nombre"] == values["-NUEVO_NOMBRE-"]]:
            window["-MSJ_CREAR-"].update(value="*El nick ya existe.")
            return False
        elif list(filter(lambda x: x > "9" or x < "0", values["-NUEVO_EDAD-"])):
            window["-MSJ_CREAR-"].update(value="*La edad no es correcta.")
            return False
        else:
            nuevo_perfil = {
                "nombre": values["-NUEVO_NOMBRE-"],
                "edad": values["-NUEVO_EDAD-"],
                "genero": values["-NUEVO_GENERO-"]
            }
            conf["perfiles"] = actualizar_perfiles(conf["perfiles"], nuevo_perfil)
            return True


def crear_cuentas(conf):
    """
    Genera los elementos para la pantalla de creacion/edicion de perfil.
    :return: el sg.Window para ejecutar la pantalla.
    """
    conf["perfiles"] = cargar_perfiles()
    sg.theme('figurace_tema')
    crear = [
        [sg.Text("Ingrese un Nick:    ", font=fs.FUENTE_BOTONES),
            sg.Input("", key="-NUEVO_NOMBRE-", font=fs.FUENTE_BOTONES)],
        [sg.Text("Ingrese su Edad:    ", font=fs.FUENTE_BOTONES),
            sg.Input("", key="-NUEVO_EDAD-", font=fs.FUENTE_BOTONES)],
        [sg.Text("Ingrese su Genero:  ", font=fs.FUENTE_BOTONES),
            sg.Input("", key="-NUEVO_GENERO-", font=fs.FUENTE_BOTONES)],
        [sg.Text("Ingrese una edad valida", key="-MSJ_CREAR-", visible=False, font=fs.FUENTE_BOTONES)],
        [sg.Text()],
        [sg.Button("Crear", key="-BTN_CREAR-", font=fs.FUENTE_BOTONES),
            sg.Button("Cancelar", key="-BTN_CANCELAR_CREAR-", font=fs.FUENTE_BOTONES)]
    ]

    datos = [
            [sg.Text("Nick:    ", font=fs.FUENTE_BOTONES),
                sg.Text("", key="-NOMBRE_MOSTRAR-", font=fs.FUENTE_BOTONES)],
            [sg.Text("Edad:    ", font=fs.FUENTE_BOTONES),
                sg.Text("", key="-EDAD_MOSTRAR-", font=fs.FUENTE_BOTONES)],
            [sg.Text("Genero:  ", font=fs.FUENTE_BOTONES),
                sg.Text("", key="-GENERO_MOSTRAR-", font=fs.FUENTE_BOTONES)]
    ]

    editar = [
        [sg.pin(sg.Button("Editar", key="-BTN_EDITAR-", font=fs.FUENTE_BOTONES)),
            sg.pin(sg.Button("Eliminar", key="-BTN_EDITAR_ELIMINAR-", font=fs.FUENTE_BOTONES)),
            sg.pin(sg.Button("Cancelar", key="-BTN_EDITAR_CANCELAR-", font=fs.FUENTE_BOTONES)),
            sg.pin(sg.Button("Aplicar", key="-BTN_APLICAR_EDICION-", font=fs.FUENTE_BOTONES))]
    ]

    datos_edit = [
            [sg.Text("Nick:    ", font=fs.FUENTE_BOTONES),
                sg.Text("", key="-INPUT_NOMBRE-", font=fs.FUENTE_BOTONES)],
            [sg.Text("Edad:    ", font=fs.FUENTE_BOTONES),
                sg.Input("", key="-INPUT_EDAD-", font=fs.FUENTE_BOTONES)],
            [sg.Text("Genero:  ", font=fs.FUENTE_BOTONES),
                sg.Input("", key="-INPUT_GENERO-", font=fs.FUENTE_BOTONES)],
            [sg.Text("Ingrese una edad valida", key="-MSJ_EDITAR-", visible=False, font=fs.FUENTE_BOTONES)]
    ]

    menu_prin = [
        [sg.Push(), sg.Listbox([a["nombre"] for a in conf["perfiles"]], size=(fs.TAM_COLUMNAS[0]//10,
                                                                              fs.TAM_COLUMNAS[0]//80),
                               key="-PERFILES-", font=fs.FUENTE_BOTONES)],
        [sg.Push(), sg.Button("Aceptar", key="-ACEPTAR_PERFIL-", font=fs.FUENTE_BOTONES),
            sg.Button("Crear Perfil", key="-PERFIL_NUEVO-", font=fs.FUENTE_BOTONES), sg.Push()]
    ]

    layout = [
            [sg.Push(), sg.Text("Editar Perfil", font=fs.FUENTE_TITULO), sg.Push()],
            [sg.VPush()],
            [sg.Push(), sg.pin(sg.Col(menu_prin, key="-BTN_PRIN-", visible=True)), sg.Push()],
            [sg.VPush()],
            [sg.pin(sg.Col(crear, key="-NUEVO_USUARIO-", visible=False))],
            [sg.Push(), sg.pin(sg.Col(datos, key="-MOSTRAR_DATOS-", visible=False)), sg.Push(), sg.Push()],
            [sg.pin(sg.Col(datos_edit, key="-EDITAR_DATOS-", visible=False))],
            [sg.VPush()],
            [sg.Push(), sg.Push(), sg.pin(sg.Col(editar, key="-BTNS_EDITAR-", visible=False)), sg.Push()],
            [sg.VPush()],
            [sg.Button("Volver", key='-VOLVER_PERFILES-', font=fs.FUENTE_BOTONES), sg.Push()]
        ]
    ruta_titlebar_icon = os.path.join(os.getcwd(), "recursos", "imagenes", "cartas_icon.png")
    if os.path.exists(ruta_titlebar_icon):
        ruta_icon = os.path.join(os.getcwd(), "recursos", "imagenes", "cartas_icon.ico")
    else:
        ruta_titlebar_icon = os.path.join(os.path.realpath('..'), "recursos", "imagenes", "cartas_icon.png")
        ruta_icon = os.path.join(os.path.realpath('..'), "recursos", "imagenes", "cartas_icon.ico")

    return sg.Window("FiguRace - Edición de Perfil", layout, size=fs.TAM_VENTANA, finalize=True,
                     use_custom_titlebar=True, titlebar_icon=ruta_titlebar_icon, icon=ruta_icon)


def analisis_event_cuentas(window, event, values, conf):
    """
    Verifica los eventos y ejecuta los cambios correspondientes
    :param
        window, event y values: variables para controlar y acceder a los componentes de la pantalla.
    :return: variable perf si no se cierra la pantalla, lo contrario una lista con los nombres de los perfiles.
    """
    if event == "-PERFIL_NUEVO-":
        window["-NUEVO_USUARIO-"].update(visible=True)
        window["-BTN_PRIN-"].update(visible=False)
        window["-MOSTRAR_DATOS-"].update(visible=False)
        window["-BTNS_EDITAR-"].update(visible=False)

    elif event == "-BTN_CANCELAR_CREAR-":
        window["-NUEVO_NOMBRE-"].update(value="")
        window["-NUEVO_EDAD-"].update(value="")
        window["-NUEVO_GENERO-"].update(value="")

        window["-NUEVO_USUARIO-"].update(visible=False)
        window["-BTN_PRIN-"].update(visible=True)
        window["-MSJ_CREAR-"].update(visible=False)

    elif event == "-BTN_CREAR-":
        if comprobar_y_cargar(window, values, 2, conf):
            window["-NUEVO_NOMBRE-"].update(value="")
            window["-NUEVO_EDAD-"].update(value="")
            window["-NUEVO_GENERO-"].update(value="")

            window["-NUEVO_USUARIO-"].update(visible=False)
            window["-BTN_PRIN-"].update(visible=True)
            window["-PERFILES-"].update(values=[a["nombre"] for a in conf["perfiles"]])
        else:
            window["-MSJ_CREAR-"].update(visible=True)

    elif event == "-ACEPTAR_PERFIL-":
        if len(values["-PERFILES-"]) == 1:
            conf["act"] = 0
            while conf["act"] != len(conf["perfiles"]) and \
                    conf["perfiles"][conf["act"]]["nombre"] != values["-PERFILES-"][0]:
                conf["act"] += 1
            if conf["perfiles"][conf["act"]]["nombre"] == values["-PERFILES-"][0]:
                window["-MOSTRAR_DATOS-"].update(visible=True)
                window["-BTNS_EDITAR-"].update(visible=True)

                window["-NOMBRE_MOSTRAR-"].update(value=conf["perfiles"][conf["act"]]["nombre"])
                window["-EDAD_MOSTRAR-"].update(value=conf["perfiles"][conf["act"]]["edad"])
                window["-GENERO_MOSTRAR-"].update(value=conf["perfiles"][conf["act"]]["genero"])

                window["-BTN_APLICAR_EDICION-"].update(visible=False)
                window["-BTN_EDITAR_CANCELAR-"].update(visible=False)
                window["-BTN_EDITAR-"].update(visible=True)
                window["-BTN_EDITAR_ELIMINAR-"].update(visible=True)

    elif event == "-BTN_EDITAR-":
        window["-MOSTRAR_DATOS-"].update(visible=False)
        window["-BTN_APLICAR_EDICION-"].update(visible=True)
        window["-BTN_PRIN-"].update(visible=False)
        window["-BTN_EDITAR-"].update(visible=False)
        window["-BTN_EDITAR_CANCELAR-"].update(visible=True)
        window["-BTN_EDITAR_ELIMINAR-"].update(visible=False)

        window["-INPUT_NOMBRE-"].update(value=conf["perfiles"][conf["act"]]["nombre"])
        window["-INPUT_EDAD-"].update(value=conf["perfiles"][conf["act"]]["edad"])
        window["-INPUT_GENERO-"].update(value=conf["perfiles"][conf["act"]]["genero"])

        window["-BTN_EDITAR_CANCELAR-"].update(visible=True)
        window["-EDITAR_DATOS-"].update(visible=True)

    elif event == "-BTN_EDITAR_CANCELAR-":
        window["-MOSTRAR_DATOS-"].update(visible=True)
        window["-BTN_APLICAR_EDICION-"].update(visible=False)
        window["-BTN_PRIN-"].update(visible=True)
        window["-BTN_EDITAR-"].update(visible=True)
        window["-BTN_EDITAR_ELIMINAR-"].update(visible=True)

        window["-BTN_EDITAR_CANCELAR-"].update(visible=False)
        window["-EDITAR_DATOS-"].update(visible=False)
        window["-MSJ_EDITAR-"].update(visible=False)

    elif event == "-BTN_APLICAR_EDICION-":
        if comprobar_y_cargar(window, values, 1, conf):
            window["-MOSTRAR_DATOS-"].update(visible=True)
            window["-BTN_APLICAR_EDICION-"].update(visible=False)
            window["-BTN_PRIN-"].update(visible=True)
            window["-BTN_EDITAR-"].update(visible=True)
            window["-BTN_EDITAR_ELIMINAR-"].update(visible=True)

            window["-EDAD_MOSTRAR-"].update(value=conf["perfiles"][conf["act"]]["edad"])
            window["-GENERO_MOSTRAR-"].update(value=conf["perfiles"][conf["act"]]["genero"])

            window["-BTN_EDITAR_CANCELAR-"].update(visible=False)
            window["-EDITAR_DATOS-"].update(visible=False)
        else:
            window["-MSJ_EDITAR-"].update(visible=True)

    elif event == "-BTN_EDITAR_ELIMINAR-":
        window["-BTN_APLICAR_EDICION-"].update(visible=True)
        window["-BTN_EDITAR_CANCELAR-"].update(visible=True)
        window["-BTN_EDITAR-"].update(visible=False)
        window["-BTN_EDITAR_ELIMINAR-"].update(visible=False)
        window["-MOSTRAR_DATOS-"].update(visible=False)
        window["-BTNS_EDITAR-"].update(visible=False)

        conf["perfiles"] = [x for x in conf["perfiles"] if x["nombre"] != conf["perfiles"][conf["act"]]["nombre"]]
        conf["perfiles"] = actualizar_perfiles(conf["perfiles"])
        window["-PERFILES-"].update(values=[a["nombre"] for a in conf["perfiles"]])