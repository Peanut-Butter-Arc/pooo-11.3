# -*- coding: utf-8 -*-
#raul isaac santos ruiz
#silvana de alba uribe
#este modulo crea toda la interfaz grafica con tkinter conectada con coordinador y archivos

from pathlib import Path
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
#importamos tkinter, ttk, messagebox, path y pil para mostrar la imagen

from excepciones import AlumnoNoEncontradoError, RegistroDuplicadoError
from modelos import (
    Alumno,
    Coordinador,
    GestionRe,
    RequisitoAcademico,
    RequisitoCantidad,
    RequisitoEvento,
    gruposValidos
)
from persistencia import GestorArchivos
#importamos las clases del negocio, excepciones y gestor de archivos


#definimos la clase principal de la interfaz con todos sus atributos privados
class InterfazSistema:
    def __init__(self, gestorArchivos="", coordinador=""):
        if isinstance(gestorArchivos, GestorArchivos):
            self.setGestor(gestorArchivos)
        else:
            self.setGestor(GestorArchivos())

        if isinstance(coordinador, Coordinador):
            self.setCoordinador(coordinador)
        else:
            self.setCoordinador(Coordinador(self.getGestor()))

        self.setLogoTk("")
        self.setVentana("")
        self.setTabla("")
        self.setLblResumen("")
        self.setLblEstado("")
        self.setEntryBuscar("")
        self.setComboEstado("")
    #iniciamos las variables privadas del gestor, coordinador y controles de ventana

    def getGestor(self):
        return self.__gestor

    def setGestor(self, valor):
        self.__gestor = valor

    def getCoordinador(self):
        return self.__coordinador

    def setCoordinador(self, valor):
        self.__coordinador = valor

    def getLogoTk(self):
        return self.__logoTk

    def setLogoTk(self, valor):
        self.__logoTk = valor

    def getVentana(self):
        return self.__ventana

    def setVentana(self, valor):
        self.__ventana = valor

    def getTabla(self):
        return self.__tabla

    def setTabla(self, valor):
        self.__tabla = valor

    def getLblResumen(self):
        return self.__lblResumen

    def setLblResumen(self, valor):
        self.__lblResumen = valor

    def getLblEstado(self):
        return self.__lblEstado

    def setLblEstado(self, valor):
        self.__lblEstado = valor

    def getEntryBuscar(self):
        return self.__entryBuscar

    def setEntryBuscar(self, valor):
        self.__entryBuscar = valor

    def getComboEstado(self):
        return self.__comboEstado

    def setComboEstado(self, valor):
        self.__comboEstado = valor
    #arriba estan todos los getters y setters publicos de la interfaz

    def obtenerNombreError(self, error):
        if isinstance(error, RegistroDuplicadoError):
            return "RegistroDuplicadoError"
        elif isinstance(error, AlumnoNoEncontradoError):
            return "AlumnoNoEncontradoError"
        elif isinstance(error, ValueError):
            return "ValueError"
        elif isinstance(error, FileNotFoundError):
            return "FileNotFoundError"
        elif isinstance(error, PermissionError):
            return "PermissionError"
        else:
            return "OSError"
    #este metodo identifica con if el nombre de la excepcion para guardarlo en el log

    def registrarYMostrarError(self, padre, titulo, error, origen=""):
        tipoTexto = self.obtenerNombreError(error)
        self.__gestor.registrarError(tipoTexto, f"{origen}{error}")
        messagebox.showerror(titulo, str(error), parent=padre)
    #este metodo guarda el error en el archivo log y muestra un aviso claro al usuario

    def parsearEntero(self, texto, campo):
        textoLimpio = texto.strip()
        if textoLimpio == "":
            raise ValueError(f"El campo {campo} no puede estar vacio.")
        try:
            numero = int(textoLimpio)
            return numero
        except ValueError:
            raise ValueError(f"Ingresa un numero entero valido en {campo}.")
    #este metodo revisa que un campo numerico no este vacio y si sea entero

    def cargarLogo(self, padre):
        rutaBase = Path(__file__).resolve().parent
        rutaLogo = rutaBase / "logo.png"
        try:
            imagen = Image.open(rutaLogo)
            imagen = imagen.resize((192, 80))
            imagenTk = ImageTk.PhotoImage(imagen)
            self.setLogoTk(imagenTk)
            etiquetaLogo = tk.Label(padre, image=self.getLogoTk(), bg="#F7F5EE")
            etiquetaLogo.pack(pady=(8, 4))
        except FileNotFoundError as errorLogo:
            self.__gestor.registrarError("FileNotFoundError", f"No se cargo logo.png: {errorLogo}")
            etiquetaRespaldo = tk.Label(padre, text="Relaciones Estudiantiles - Anahuac", bg="#117A76", fg="white", font=("Arial", 13, "bold"), pady=8)
            etiquetaRespaldo.pack(fill="x", padx=16, pady=6)
        except OSError as errorLogo:
            self.__gestor.registrarError("OSError", f"No se cargo logo.png: {errorLogo}")
            etiquetaRespaldo = tk.Label(padre, text="Relaciones Estudiantiles - Anahuac", bg="#117A76", fg="white", font=("Arial", 13, "bold"), pady=8)
            etiquetaRespaldo.pack(fill="x", padx=16, pady=6)
    #cargamos el logo con pil y guardamos la referencia privada para que no se borre

    def refrescarTabla(self, evento=""):
        for filaId in self.__tabla.get_children():
            self.__tabla.delete(filaId)

        if self.__entryBuscar != "":
            textoFiltro = self.__entryBuscar.get()
        else:
            textoFiltro = ""

        if self.__comboEstado != "":
            estadoFiltro = self.__comboEstado.get()
        else:
            estadoFiltro = "Todos"

        listaAlumnos = self.__coordinador.buscarAlumnos(textoFiltro, estadoFiltro)
        for alumnoItem in listaAlumnos:
            if isinstance(alumnoItem, GestionRe):
                tipoTexto = "GestionRe"
            else:
                tipoTexto = "Alumno"

            if alumnoItem.verificarGraduacion() == True:
                dictamenTexto = "Cumple"
            else:
                dictamenTexto = "Pendiente"

            self.__tabla.insert(
                "",
                "end",
                values=(
                    alumnoItem.getIdAlumno(),
                    alumnoItem.getNombre(),
                    alumnoItem.semestre,
                    alumnoItem.getGrupo(),
                    tipoTexto,
                    f"{alumnoItem.porcentajeAvance:.0f}%",
                    dictamenTexto
                )
            )
        stats = self.__coordinador.obtenerEstadisticas()
        self.__lblResumen.config(text=f"Total: {stats['total']}  |  Cumplen: {stats['cumplen']}  |  Pendientes: {stats['pendientes']}  |  Promedio: {stats['promedio']}%")
    #limpiamos la tabla treeview y la llenamos otra vez con los alumnos filtrados

    def obtenerSeleccionado(self):
        seleccionTabla = self.__tabla.selection()
        if not seleccionTabla:
            raise ValueError("Selecciona primero un alumno de la tabla.")
        datosFila = self.__tabla.item(seleccionTabla[0], "values")
        idSeleccionado = str(datosFila[0])
        return self.__coordinador.buscarAlumnoPorId(idSeleccionado)
    #obtenemos el objeto alumno que el usuario selecciono con el mouse en la tabla

    def dobleClicTabla(self, evento=""):
        self.detalleSeleccionado()
    #esta funcion abre el detalle cuando dan doble clic sobre una fila

    def buscarPorId(self):
        try:
            textoId = self.__entryBuscar.get()
            alumnoBuscado = self.__coordinador.buscarAlumnoPorId(textoId)
        except ValueError as errorBusqueda:
            self.registrarYMostrarError(self.__ventana, "Consulta por ID", errorBusqueda, "Consulta: ")
        except AlumnoNoEncontradoError as errorBusqueda:
            self.registrarYMostrarError(self.__ventana, "Consulta por ID", errorBusqueda, "Consulta: ")
        else:
            self.abrirDetalle(alumnoBuscado)
    #buscamos un alumno exacto por id y abrimos su resumen o mostramos el error

    def abrirFormulario(self, alumnoEditar=""):
        esEdicion = isinstance(alumnoEditar, Alumno)
        ventanaForm = tk.Toplevel(self.__ventana)
        if esEdicion == True:
            ventanaForm.title("Modificar Alumno")
            textoTitulo = "Editar Alumno"
        else:
            ventanaForm.title("Registrar Alumno")
            textoTitulo = "Nuevo Alumno"
        ventanaForm.geometry("440x480")
        ventanaForm.resizable(False, False)
        ventanaForm.configure(bg="#F7F5EE")

        tk.Label(ventanaForm, text=textoTitulo, bg="#117A76", fg="white", font=("Arial", 11, "bold"), pady=7).pack(fill="x")
        frameCampos = tk.Frame(ventanaForm, bg="#F7F5EE", padx=16, pady=10)
        frameCampos.pack(fill="both", expand=True)

        if esEdicion == True:
            valId = alumnoEditar.getIdAlumno()
            valNombre = alumnoEditar.getNombre()
            valSemestre = str(alumnoEditar.semestre)
            valGrupo = alumnoEditar.getGrupo()
            valActividades = str(alumnoEditar.getActividades())
            valMentorias = str(alumnoEditar.getMentorias())
            valObligatorias = str(alumnoEditar.getObligatorias())
            valReprobadas = str(alumnoEditar.getMateriasReprobadas())
            if alumnoEditar.getSeminario() == True:
                valSeminario = "Si"
            else:
                valSeminario = "No"
        else:
            valId = ""
            valNombre = ""
            valSemestre = ""
            valGrupo = gruposValidos[0]
            valActividades = "0"
            valMentorias = "0"
            valObligatorias = "0"
            valReprobadas = "0"
            valSeminario = "No"

        if isinstance(alumnoEditar, GestionRe):
            valTipo = "GestionRe"
            valPeriodo = alumnoEditar.getPeriodo()
        else:
            valTipo = "Alumno"
            valPeriodo = "2026-2027"

        #este bloque crea todas las etiquetas, cajas entry y listas combobox del formulario
        tk.Label(frameCampos, text="ID Alumno:", bg="#F7F5EE", font=("Arial", 9, "bold")).grid(row=0, column=0, sticky="w", pady=4)
        entryId = tk.Entry(frameCampos, font=("Arial", 10), width=28)
        entryId.insert(0, valId)
        if esEdicion == True:
            entryId.config(state="readonly")
        entryId.grid(row=0, column=1, sticky="ew", padx=(8, 0), pady=4)

        tk.Label(frameCampos, text="Nombre:", bg="#F7F5EE", font=("Arial", 9, "bold")).grid(row=1, column=0, sticky="w", pady=4)
        entryNombre = tk.Entry(frameCampos, font=("Arial", 10), width=28)
        entryNombre.insert(0, valNombre)
        entryNombre.grid(row=1, column=1, sticky="ew", padx=(8, 0), pady=4)

        tk.Label(frameCampos, text="Semestre (1-13):", bg="#F7F5EE", font=("Arial", 9, "bold")).grid(row=2, column=0, sticky="w", pady=4)
        entrySemestre = tk.Entry(frameCampos, font=("Arial", 10), width=28)
        entrySemestre.insert(0, valSemestre)
        entrySemestre.grid(row=2, column=1, sticky="ew", padx=(8, 0), pady=4)

        tk.Label(frameCampos, text="Grupo:", bg="#F7F5EE", font=("Arial", 9, "bold")).grid(row=3, column=0, sticky="w", pady=4)
        comboGrupo = ttk.Combobox(frameCampos, values=gruposValidos, state="readonly", font=("Arial", 10), width=25)
        comboGrupo.set(valGrupo)
        comboGrupo.grid(row=3, column=1, sticky="ew", padx=(8, 0), pady=4)

        tk.Label(frameCampos, text="Actividades (meta 8):", bg="#F7F5EE", font=("Arial", 9, "bold")).grid(row=4, column=0, sticky="w", pady=4)
        entryActividades = tk.Entry(frameCampos, font=("Arial", 10), width=28)
        entryActividades.insert(0, valActividades)
        entryActividades.grid(row=4, column=1, sticky="ew", padx=(8, 0), pady=4)

        tk.Label(frameCampos, text="Mentorias (meta 2):", bg="#F7F5EE", font=("Arial", 9, "bold")).grid(row=5, column=0, sticky="w", pady=4)
        entryMentorias = tk.Entry(frameCampos, font=("Arial", 10), width=28)
        entryMentorias.insert(0, valMentorias)
        entryMentorias.grid(row=5, column=1, sticky="ew", padx=(8, 0), pady=4)

        tk.Label(frameCampos, text="Obligatorias (meta 2):", bg="#F7F5EE", font=("Arial", 9, "bold")).grid(row=6, column=0, sticky="w", pady=4)
        entryObligatorias = tk.Entry(frameCampos, font=("Arial", 10), width=28)
        entryObligatorias.insert(0, valObligatorias)
        entryObligatorias.grid(row=6, column=1, sticky="ew", padx=(8, 0), pady=4)

        tk.Label(frameCampos, text="Reprobadas:", bg="#F7F5EE", font=("Arial", 9, "bold")).grid(row=7, column=0, sticky="w", pady=4)
        entryReprobadas = tk.Entry(frameCampos, font=("Arial", 10), width=28)
        entryReprobadas.insert(0, valReprobadas)
        entryReprobadas.grid(row=7, column=1, sticky="ew", padx=(8, 0), pady=4)

        tk.Label(frameCampos, text="Seminario:", bg="#F7F5EE", font=("Arial", 9, "bold")).grid(row=8, column=0, sticky="w", pady=4)
        comboSeminario = ttk.Combobox(frameCampos, values=["No", "Si"], state="readonly", font=("Arial", 10), width=25)
        comboSeminario.set(valSeminario)
        comboSeminario.grid(row=8, column=1, sticky="ew", padx=(8, 0), pady=4)

        tk.Label(frameCampos, text="Tipo:", bg="#F7F5EE", font=("Arial", 9, "bold")).grid(row=9, column=0, sticky="w", pady=4)
        comboTipo = ttk.Combobox(frameCampos, values=["Alumno", "GestionRe"], state="readonly", font=("Arial", 10), width=25)
        comboTipo.set(valTipo)
        comboTipo.grid(row=9, column=1, sticky="ew", padx=(8, 0), pady=4)

        tk.Label(frameCampos, text="Periodo (GestionRe):", bg="#F7F5EE", font=("Arial", 9, "bold")).grid(row=10, column=0, sticky="w", pady=4)
        entryPeriodo = tk.Entry(frameCampos, font=("Arial", 10), width=28)
        entryPeriodo.insert(0, valPeriodo)
        entryPeriodo.grid(row=10, column=1, sticky="ew", padx=(8, 0), pady=4)

        def alternarPeriodo(evento=""):
            if comboTipo.get() == "GestionRe":
                entryPeriodo.config(state="normal")
            else:
                entryPeriodo.config(state="disabled")
        #habilitamos la caja de periodo solamente cuando se elige tipo gestion

        comboTipo.bind("<<ComboboxSelected>>", alternarPeriodo)
        alternarPeriodo()

        def guardarAlumno():
            try:
                self.__lblEstado.config(text="Guardando...")
                idDato = entryId.get()
                nombreDato = entryNombre.get()
                semestreDato = self.parsearEntero(entrySemestre.get(), "Semestre")
                grupoDato = comboGrupo.get()
                actDato = self.parsearEntero(entryActividades.get(), "Actividades")
                mentDato = self.parsearEntero(entryMentorias.get(), "Mentorias")
                obligDato = self.parsearEntero(entryObligatorias.get(), "Obligatorias RE")
                reprobDato = self.parsearEntero(entryReprobadas.get(), "Reprobadas")
                semDato = (comboSeminario.get() == "Si")

                if comboTipo.get() == "GestionRe":
                    if isinstance(alumnoEditar, GestionRe):
                        listaRequisitos = alumnoEditar.getRequisitos()
                    else:
                        listaRequisitos = []
                    objetoAlumno = GestionRe(
                        idDato,
                        nombreDato,
                        semestreDato,
                        grupoDato,
                        actDato,
                        mentDato,
                        obligDato,
                        reprobDato,
                        semDato,
                        entryPeriodo.get(),
                        listaRequisitos
                    )
                else:
                    objetoAlumno = Alumno(
                        idDato,
                        nombreDato,
                        semestreDato,
                        grupoDato,
                        actDato,
                        mentDato,
                        obligDato,
                        reprobDato,
                        semDato
                    )

                if esEdicion == True:
                    self.__coordinador.actualizarAlumno(alumnoEditar.getIdAlumno(), objetoAlumno)
                else:
                    self.__coordinador.darDeAltaAlumno(objetoAlumno)
            except ValueError as errorDato:
                self.registrarYMostrarError(ventanaForm, "Error de datos", errorDato, "Formulario: ")
            except RegistroDuplicadoError as errorDato:
                self.registrarYMostrarError(ventanaForm, "Error de datos", errorDato, "Formulario: ")
            except AlumnoNoEncontradoError as errorDato:
                self.registrarYMostrarError(ventanaForm, "Error de datos", errorDato, "Formulario: ")
            except OSError as errorArchivo:
                self.registrarYMostrarError(ventanaForm, "Error de archivo", errorArchivo, "Archivo: ")
            else:
                self.refrescarTabla()
                messagebox.showinfo("Exito", "Cambios guardados en alumnos.txt.", parent=ventanaForm)
                ventanaForm.destroy()
            finally:
                try:
                    self.__lblEstado.config(text="Listo.")
                except tk.TclError:
                    pass
        #esta funcion valida los campos del formulario, crea el objeto y guarda los cambios

        frameBotones = tk.Frame(ventanaForm, bg="#F7F5EE")
        frameBotones.pack(pady=8)
        botonGuardar = tk.Button(frameBotones, text="Guardar", command=guardarAlumno, bg="#1E8449", fg="white", font=("Arial", 10, "bold"), width=12)
        botonGuardar.grid(row=0, column=0, padx=6)
        botonCancelar = tk.Button(frameBotones, text="Cancelar", command=ventanaForm.destroy, bg="#566573", fg="white", font=("Arial", 10, "bold"), width=12)
        botonCancelar.grid(row=0, column=1, padx=6)

    def modificarSeleccionado(self):
        try:
            alumnoElegido = self.obtenerSeleccionado()
        except ValueError as errorSeleccion:
            self.registrarYMostrarError(self.__ventana, "Seleccion requerida", errorSeleccion, "Modificar: ")
        except AlumnoNoEncontradoError as errorSeleccion:
            self.registrarYMostrarError(self.__ventana, "Seleccion requerida", errorSeleccion, "Modificar: ")
        else:
            self.abrirFormulario(alumnoElegido)
    #abrimos el formulario con los datos del alumno marcado para editarlo

    def eliminarSeleccionado(self):
        try:
            alumnoElegido = self.obtenerSeleccionado()
            confirmado = messagebox.askyesno("Confirmar", f"Eliminar a {alumnoElegido.getNombre()} ({alumnoElegido.getIdAlumno()})?", parent=self.__ventana)
            if confirmado == False:
                return
            self.__coordinador.darDeBajaAlumno(alumnoElegido.getIdAlumno())
        except ValueError as errorEliminar:
            self.registrarYMostrarError(self.__ventana, "Error al eliminar", errorEliminar, "Eliminar: ")
        except AlumnoNoEncontradoError as errorEliminar:
            self.registrarYMostrarError(self.__ventana, "Error al eliminar", errorEliminar, "Eliminar: ")
        except OSError as errorEliminar:
            self.registrarYMostrarError(self.__ventana, "Error al eliminar", errorEliminar, "Eliminar: ")
        else:
            self.refrescarTabla()
            messagebox.showinfo("Eliminado", "Alumno eliminado correctamente.", parent=self.__ventana)
    #pedimos confirmacion y eliminamos al alumno seleccionado de la lista y del archivo

    def detalleSeleccionado(self):
        try:
            alumnoElegido = self.obtenerSeleccionado()
        except ValueError as errorSeleccion:
            self.registrarYMostrarError(self.__ventana, "Seleccion requerida", errorSeleccion, "Detalle: ")
        except AlumnoNoEncontradoError as errorSeleccion:
            self.registrarYMostrarError(self.__ventana, "Seleccion requerida", errorSeleccion, "Detalle: ")
        else:
            self.abrirDetalle(alumnoElegido)

    def abrirDetalle(self, alumno):
        ventanaDetalle = tk.Toplevel(self.__ventana)
        ventanaDetalle.title(f"Detalle - {alumno.getNombre()}")
        if isinstance(alumno, GestionRe):
            ventanaDetalle.geometry("640x560")
        else:
            ventanaDetalle.geometry("620x380")
        ventanaDetalle.configure(bg="#F7F5EE")

        cajaTexto = tk.Text(ventanaDetalle, font=("Consolas", 10), height=12, wrap="word")
        cajaTexto.pack(fill="both", expand=True, padx=12, pady=10)

        def pintarDetalle():
            if alumno.verificarGraduacion() == True:
                textoDictamen = "APROBADO PARA GRADUARSE"
            else:
                textoDictamen = "PENDIENTE"
            cajaTexto.config(state="normal")
            cajaTexto.delete("1.0", "end")
            cajaTexto.insert("end", f"Alumno: {alumno.getNombre()} (ID: {alumno.getIdAlumno()}) | Semestre: {alumno.semestre}\n")
            cajaTexto.insert("end", f"Grupo: {alumno.getGrupo()} - {alumno.getAreaObj().obtenerTipoGrupo()}\n")
            if isinstance(alumno, GestionRe):
                cajaTexto.insert("end", f"Periodo GestionRe: {alumno.getPeriodo()}\n")
            cajaTexto.insert("end", f"Avance: {alumno.porcentajeAvance}% | Dictamen: {textoDictamen}\n\n")

            listaCumplidos = alumno.obtenerCumplidos()
            cajaTexto.insert("end", "Cumplidos:\n")
            if not listaCumplidos:
                cajaTexto.insert("end", "  [OK] Ninguno\n")
            else:
                for itemCumplido in listaCumplidos:
                    cajaTexto.insert("end", f"  [OK] {itemCumplido}\n")

            listaPendientes = alumno.obtenerPendientes()
            cajaTexto.insert("end", "\nPendientes:\n")
            if not listaPendientes:
                cajaTexto.insert("end", "  [FALTA] Ninguno\n")
            else:
                for itemPendiente in listaPendientes:
                    cajaTexto.insert("end", f"  [FALTA] {itemPendiente}\n")

            cajaTexto.config(state="disabled")
        #esta funcion muestra en la caja de texto los rubros cumplidos, faltantes y avance

        pintarDetalle()

        if isinstance(alumno, GestionRe):
            marcoRequisitos = tk.LabelFrame(ventanaDetalle, text="Requisitos Especiales (GestionRe)", bg="#F7F5EE", font=("Arial", 9, "bold"), padx=8, pady=6)
            marcoRequisitos.pack(fill="x", padx=12, pady=(0, 6))
            listaRequisitosBox = tk.Listbox(marcoRequisitos, font=("Consolas", 9), height=4)
            listaRequisitosBox.pack(fill="x", pady=(0, 6))

            def refrescarRequisitos():
                listaRequisitosBox.delete(0, "end")
                for reqItem in alumno.getRequisitos():
                    listaRequisitosBox.insert("end", reqItem.obtenerDetalle())
                pintarDetalle()
                self.refrescarTabla()

            refrescarRequisitos()
            filaControles = tk.Frame(marcoRequisitos, bg="#F7F5EE")
            filaControles.pack()
            comboTipoReq = ttk.Combobox(filaControles, values=["Cantidad", "Evento", "Academico"], state="readonly", width=11)
            comboTipoReq.set("Cantidad")
            comboTipoReq.grid(row=0, column=0, padx=3)
            entryActividad = tk.Entry(filaControles, width=20)
            entryActividad.insert(0, "Taller extra")
            entryActividad.grid(row=0, column=1, padx=3)
            entryParametro = tk.Entry(filaControles, width=14)
            entryParametro.insert(0, "2")
            entryParametro.grid(row=0, column=2, padx=3)

            def cambiarEjemploParametro(evento=""):
                tipo = comboTipoReq.get()
                entryParametro.delete(0, "end")
                if tipo == "Cantidad":
                    entryParametro.insert(0, "2")
                elif tipo == "Evento":
                    entryParametro.insert(0, "15/11/2026")
                else:
                    entryParametro.insert(0, "0")

            comboTipoReq.bind("<<ComboboxSelected>>", cambiarEjemploParametro)

            def agregarRequisito():
                try:
                    tipoReq = comboTipoReq.get()
                    nombreReq = entryActividad.get()
                    parametroReq = entryParametro.get()
                    if tipoReq == "Cantidad":
                        meta = self.parsearEntero(parametroReq, "Meta")
                        nuevoReq = RequisitoCantidad(nombreReq, meta, 0)
                    elif tipoReq == "Evento":
                        nuevoReq = RequisitoEvento(nombreReq, parametroReq, False)
                    else:
                        reprob = self.parsearEntero(parametroReq, "Reprobadas")
                        nuevoReq = RequisitoAcademico(nombreReq, reprob)
                    alumno.agregarRequisito(nuevoReq)
                    self.__coordinador.guardarCambios()
                except ValueError as errorReq:
                    self.registrarYMostrarError(ventanaDetalle, "Error en requisito", errorReq, "Requisito: ")
                else:
                    refrescarRequisitos()

            def completarRequisito():
                try:
                    seleccionReq = listaRequisitosBox.curselection()
                    if not seleccionReq:
                        raise ValueError("Selecciona un requisito.")
                    reqActual = alumno.getRequisitos()[seleccionReq[0]]
                    if isinstance(reqActual, RequisitoCantidad):
                        reqActual.registrarAvance(reqActual.getCantidadRequerida())
                    elif isinstance(reqActual, RequisitoAcademico):
                        reqActual.actualizarMateriasReprobadas(0)
                    else:
                        reqActual.registrarAsistencia(True)
                    self.__coordinador.guardarCambios()
                except ValueError as errorReq:
                    self.registrarYMostrarError(ventanaDetalle, "Error", errorReq, "CompletarReq: ")
                else:
                    refrescarRequisitos()

            def quitarRequisito():
                try:
                    seleccionReq = listaRequisitosBox.curselection()
                    if not seleccionReq:
                        raise ValueError("Selecciona un requisito.")
                    alumno.eliminarRequisito(seleccionReq[0])
                    self.__coordinador.guardarCambios()
                except ValueError as errorReq:
                    self.registrarYMostrarError(ventanaDetalle, "Error", errorReq, "QuitarReq: ")
                else:
                    refrescarRequisitos()

            tk.Button(filaControles, text="Agregar", command=agregarRequisito, bg="#117A76", fg="white", font=("Arial", 8, "bold")).grid(row=0, column=3, padx=2)
            tk.Button(filaControles, text="Completar", command=completarRequisito, bg="#1E8449", fg="white", font=("Arial", 8, "bold")).grid(row=0, column=4, padx=2)
            tk.Button(filaControles, text="Quitar", command=quitarRequisito, bg="#A93226", fg="white", font=("Arial", 8, "bold")).grid(row=0, column=5, padx=2)
        #este bloque agrega los controles para administrar requisitos si el alumno es gestion

        botonCerrarDetalle = tk.Button(ventanaDetalle, text="Cerrar", command=ventanaDetalle.destroy, bg="#566573", fg="white", font=("Arial", 9, "bold"), width=12)
        botonCerrarDetalle.pack(pady=8)

    def verLog(self):
        ventanaLog = tk.Toplevel(self.__ventana)
        ventanaLog.title("log_errores.txt")
        ventanaLog.geometry("640x320")
        cajaLog = tk.Text(ventanaLog, font=("Consolas", 9), wrap="word")
        cajaLog.pack(fill="both", expand=True, padx=10, pady=10)
        cajaLog.insert("1.0", self.__gestor.leerLogErrores())
        cajaLog.config(state="disabled")
    #abrimos una ventana para mostrar el historial guardado en log de errores

    def iniciar(self):
        ventanaPrincipal = tk.Tk()
        self.setVentana(ventanaPrincipal)
        self.__ventana.title("Relaciones Estudiantiles")
        self.__ventana.geometry("880x560")
        self.__ventana.configure(bg="#F7F5EE")

        barraMenu = tk.Menu(self.__ventana)
        self.__ventana.config(menu=barraMenu)
        menuOpciones = tk.Menu(barraMenu, tearoff=0)
        barraMenu.add_cascade(label="Opciones", menu=menuOpciones)
        menuOpciones.add_command(label="Registrar Alumno", command=self.abrirFormulario)
        menuOpciones.add_command(label="Ver Log de Errores", command=self.verLog)
        menuOpciones.add_command(label="Salir", command=self.__ventana.destroy)
        #aqui creamos la barra de menu superior con sus opciones

        self.cargarLogo(self.__ventana)
        lblResumen = tk.Label(self.__ventana, text="", bg="#D1F2EB", fg="#0E5A56", font=("Arial", 10, "bold"), pady=6)
        self.setLblResumen(lblResumen)
        self.__lblResumen.pack(fill="x", padx=16, pady=4)

        frameBuscar = tk.Frame(self.__ventana, bg="#F7F5EE")
        frameBuscar.pack(fill="x", padx=16, pady=6)
        tk.Label(frameBuscar, text="ID / Nombre / Grupo:", bg="#F7F5EE", font=("Arial", 9, "bold")).pack(side="left")

        entryBuscar = tk.Entry(frameBuscar, font=("Arial", 10), width=22)
        self.setEntryBuscar(entryBuscar)
        self.__entryBuscar.pack(side="left", padx=6)
        self.__entryBuscar.bind("<KeyRelease>", self.refrescarTabla)

        comboEstado = ttk.Combobox(frameBuscar, values=["Todos", "Cumple", "Pendiente"], state="readonly", width=11)
        self.setComboEstado(comboEstado)
        self.__comboEstado.set("Todos")
        self.__comboEstado.pack(side="left", padx=4)
        self.__comboEstado.bind("<<ComboboxSelected>>", self.refrescarTabla)

        botonBuscarId = tk.Button(frameBuscar, text="Buscar por ID", command=self.buscarPorId, bg="#1F618D", fg="white", font=("Arial", 9, "bold"))
        botonBuscarId.pack(side="left", padx=6)
        #este bloque acomoda el buscador por texto, el filtro de estado y el boton buscar por id

        frameTabla = tk.Frame(self.__ventana, bg="#F7F5EE")
        frameTabla.pack(fill="both", expand=True, padx=16, pady=4)
        columnasTabla = ("id", "nombre", "sem", "grupo", "tipo", "avance", "dictamen")
        tabla = ttk.Treeview(frameTabla, columns=columnasTabla, show="headings", height=13)
        self.setTabla(tabla)

        self.__tabla.heading("id", text="ID")
        self.__tabla.column("id", width=80, anchor="center")
        self.__tabla.heading("nombre", text="Nombre")
        self.__tabla.column("nombre", width=200, anchor="w")
        self.__tabla.heading("sem", text="Sem")
        self.__tabla.column("sem", width=50, anchor="center")
        self.__tabla.heading("grupo", text="Grupo")
        self.__tabla.column("grupo", width=170, anchor="w")
        self.__tabla.heading("tipo", text="Tipo")
        self.__tabla.column("tipo", width=85, anchor="center")
        self.__tabla.heading("avance", text="Avance")
        self.__tabla.column("avance", width=70, anchor="center")
        self.__tabla.heading("dictamen", text="Dictamen")
        self.__tabla.column("dictamen", width=90, anchor="center")

        barraScroll = ttk.Scrollbar(frameTabla, orient="vertical", command=self.__tabla.yview)
        self.__tabla.configure(yscrollcommand=barraScroll.set)
        barraScroll.pack(side="right", fill="y")
        self.__tabla.pack(side="left", fill="both", expand=True)
        self.__tabla.bind("<Double-1>", self.dobleClicTabla)
        #este bloque configura las siete columnas de la tabla y su barra vertical

        frameBotones = tk.Frame(self.__ventana, bg="#F7F5EE")
        frameBotones.pack(pady=8)
        botonRegistrar = tk.Button(frameBotones, text="Registrar", command=self.abrirFormulario, bg="#117A76", fg="white", font=("Arial", 10, "bold"), width=15, pady=4)
        botonRegistrar.grid(row=0, column=0, padx=4)
        botonModificar = tk.Button(frameBotones, text="Modificar", command=self.modificarSeleccionado, bg="#1E8449", fg="white", font=("Arial", 10, "bold"), width=15, pady=4)
        botonModificar.grid(row=0, column=1, padx=4)
        botonEliminar = tk.Button(frameBotones, text="Eliminar", command=self.eliminarSeleccionado, bg="#A93226", fg="white", font=("Arial", 10, "bold"), width=15, pady=4)
        botonEliminar.grid(row=0, column=2, padx=4)
        botonDetalle = tk.Button(frameBotones, text="Detalle y Calculo", command=self.detalleSeleccionado, bg="#1F618D", fg="white", font=("Arial", 10, "bold"), width=15, pady=4)
        botonDetalle.grid(row=0, column=3, padx=4)
        botonLog = tk.Button(frameBotones, text="Ver Log", command=self.verLog, bg="#566573", fg="white", font=("Arial", 10, "bold"), width=15, pady=4)
        botonLog.grid(row=0, column=4, padx=4)
        #este bloque acomoda los cinco botones principales abajo de la tabla

        lblEstado = tk.Label(self.__ventana, text="Listo.", bg="#F7F5EE", fg="#566573", font=("Arial", 8), anchor="w")
        self.setLblEstado(lblEstado)
        self.__lblEstado.pack(fill="x", padx=16, pady=(0, 6))

        self.refrescarTabla()
        self.__ventana.mainloop()
    #cargamos la tabla inicial y arrancamos la ventana principal


def iniciarInterfaz():
    sistema = InterfazSistema()
    sistema.iniciar()
#esta funcion publica crea la interfaz y ejecuta todo el sistema
