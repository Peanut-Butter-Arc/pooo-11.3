# -*- coding: utf-8 -*-
#raul isaac santos ruiz
#silvana de alba uribe
#este modulo administra solamente los archivos de texto del sistema

from datetime import datetime
from pathlib import Path
from modelos import Alumno, GestionRe, RequisitoAcademico, RequisitoCantidad, RequisitoEvento
#importamos fecha, rutas y las clases del negocio para guardar y cargar objetos


#definimos la clase gestor archivos que concentra el uso de open
class GestorArchivos:
    def __init__(self, carpeta=""):
        if carpeta == "":
            baseCarpeta = Path(__file__).resolve().parent
        else:
            baseCarpeta = Path(carpeta)
        self.setRutaAlumnos(baseCarpeta / "alumnos.txt")
        self.setRutaLog(baseCarpeta / "log_errores.txt")
    #este constructor prepara las rutas privadas para alumnos y log de errores

    def getRutaAlumnos(self):
        return self.__rutaAlumnos

    def setRutaAlumnos(self, ruta):
        if str(ruta).strip() == "":
            raise ValueError("La ruta de alumnos no puede estar vacia.")
        self.__rutaAlumnos = Path(ruta)

    def getRutaLog(self):
        return self.__rutaLog

    def setRutaLog(self, ruta):
        if str(ruta).strip() == "":
            raise ValueError("La ruta del log no puede estar vacia.")
        self.__rutaLog = Path(ruta)

    def registrarError(self, tipoError, detalle):
        fechaHora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        lineaLog = f"{fechaHora} | ERROR | {tipoError} | {detalle}\n"
        try:
            with open(self.__rutaLog, "a", encoding="utf-8") as file:
                file.write(lineaLog)
        except OSError as errorArchivo:
            print("Error al escribir log:", errorArchivo)
    #esta funcion escribe al final del archivo log cada error con fecha y hora

    def serializarRequisitos(self, requisitos):
        if not requisitos:
            return "SIN_REQUISITOS"
        texto = ""
        for req in requisitos:
            if isinstance(req, RequisitoCantidad):
                bloque = f"CANT~{req.getNombreActividad()}~{req.getCantidadRequerida()}~{req.getCantidadRealizada()}"
            elif isinstance(req, RequisitoEvento):
                bloque = f"EVT~{req.getNombreActividad()}~{req.getFecha()}~{req.getCompletado()}"
            elif isinstance(req, RequisitoAcademico):
                bloque = f"ACAD~{req.getNombreActividad()}~{req.getMateriasReprobadas()}"
            else:
                bloque = ""
            if bloque != "":
                if texto == "":
                    texto = bloque
                else:
                    texto = texto + ";" + bloque
        return texto
    #convertimos la lista de requisitos especiales en texto para guardarla

    def reconstruirRequisitos(self, texto):
        if texto == "" or texto == "SIN_REQUISITOS":
            return []
        lista = []
        for bloque in texto.split(";"):
            datos = bloque.strip().split("~")
            if datos[0] == "CANT" and len(datos) == 4:
                lista.append(RequisitoCantidad(datos[1], int(datos[2]), int(datos[3])))
            elif datos[0] == "EVT" and len(datos) == 4:
                asistio = (datos[3] == "True")
                lista.append(RequisitoEvento(datos[1], datos[2], asistio))
            elif datos[0] == "ACAD" and len(datos) == 3:
                lista.append(RequisitoAcademico(datos[1], int(datos[2])))
        return lista
    #leemos el texto guardado y volvemos a crear los objetos de cada requisito

    def serializarAlumno(self, alumno):
        lineaBase = (
            f"{alumno.getIdAlumno()}|{alumno.getNombre()}|{alumno.semestre}|"
            f"{alumno.getGrupo()}|{alumno.getActividades()}|{alumno.getMentorias()}|"
            f"{alumno.getObligatorias()}|{alumno.getMateriasReprobadas()}|{alumno.getSeminario()}"
        )
        if isinstance(alumno, GestionRe):
            textoReqs = self.serializarRequisitos(alumno.getRequisitos())
            return f"GESTION|{lineaBase}|{alumno.getPeriodo()}|{textoReqs}"
        else:
            return f"ALUMNO|{lineaBase}"
    #armamos la linea completa de texto separada por barras para guardar en el archivo

    def reconstruirAlumno(self, linea):
        datos = linea.split("|")
        if datos[0] == "ALUMNO" and len(datos) == 10:
            seminario = (datos[9] == "True")
            return Alumno(datos[1], datos[2], int(datos[3]), datos[4], int(datos[5]), int(datos[6]), int(datos[7]), int(datos[8]), seminario)
        if datos[0] == "GESTION" and len(datos) == 12:
            seminario = (datos[9] == "True")
            listaReqs = self.reconstruirRequisitos(datos[11])
            return GestionRe(datos[1], datos[2], int(datos[3]), datos[4], int(datos[5]), int(datos[6]), int(datos[7]), int(datos[8]), seminario, datos[10], listaReqs)
        raise ValueError(f"Formato invalido: {linea}")
    #esta funcion toma una linea del archivo y reconstruye el objeto alumno o gestion

    def guardarAlumnos(self, listaAlumnos):
        try:
            with open(self.__rutaAlumnos, "w", encoding="utf-8") as file:
                for alumno in listaAlumnos:
                    linea = self.serializarAlumno(alumno)
                    file.write(linea + "\n")
        except PermissionError as errorArchivo:
            self.registrarError("PermissionError", f"No se pudo guardar {self.__rutaAlumnos.name}: {errorArchivo}")
            raise
        except OSError as errorArchivo:
            self.registrarError("OSError", f"No se pudo guardar {self.__rutaAlumnos.name}: {errorArchivo}")
            raise
    #guardamos toda la lista en el archivo de texto y si hay error de permisos se registra

    def cargarAlumnos(self):
        alumnosCargados = []
        try:
            with open(self.__rutaAlumnos, "r", encoding="utf-8") as file:
                lineas = file.readlines()
        except FileNotFoundError as errorArchivo:
            self.registrarError("FileNotFoundError", f"Archivo no encontrado ({self.__rutaAlumnos.name}): {errorArchivo}")
            self.guardarAlumnos([])
        except PermissionError as errorArchivo:
            self.registrarError("PermissionError", f"Error de permisos al leer {self.__rutaAlumnos.name}: {errorArchivo}")
        except OSError as errorArchivo:
            self.registrarError("OSError", f"Error al leer {self.__rutaAlumnos.name}: {errorArchivo}")
        else:
            for indice, linea in enumerate(lineas, start=1):
                lineaLimpia = linea.strip()
                if lineaLimpia != "":
                    try:
                        obj = self.reconstruirAlumno(lineaLimpia)
                        alumnosCargados.append(obj)
                    except ValueError as errorDato:
                        self.registrarError("ValueError", f"Linea {indice} ignorada: {errorDato}")
                    except IndexError as errorDato:
                        self.registrarError("IndexError", f"Linea {indice} ignorada: {errorDato}")
        return alumnosCargados
    #al abrir el programa leemos todas las lineas y si no existe el archivo lo creamos vacio

    def leerLogErrores(self):
        try:
            with open(self.__rutaLog, "r", encoding="utf-8") as file:
                return file.read()
        except FileNotFoundError:
            return "No hay errores registrados todavia."
        except OSError as errorArchivo:
            return f"No se pudo leer el log: {errorArchivo}"
    #leemos todo el archivo de errores para mostrarlo en la ventana de bitacora
