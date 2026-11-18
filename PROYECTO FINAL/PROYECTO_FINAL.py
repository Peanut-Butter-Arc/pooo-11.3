#PROYECTO FINAL POO

#Raul Isaac Santos ruiz
#Silvana De Alba Uribe


#===========================
#       LIBRERIAS
#==========================

import sqlite3
from pathlib import Path
from datetime import datetime
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk

#QUE HACE CADA LIBRERIA
"""                         
    pathlib = raiz de archivo y ceacion (ecencial)
    datetime = hora para el log
    tkinter y custom tkinter = para ventanas
    tkinter = para msgbox para mostrar errores
    pil = imagen para el programa
                                """

carpetaBase = Path(__file__).resolve().parent if "__file__" in locals() else Path.cwd()
archivoAlumnosDefault = str(carpetaBase / "alumnos.txt")
archivoLogDefault = str(carpetaBase / "log_errores.txt")
archivoCuentasDefault = str(carpetaBase / "cuentas.txt")
archivoDbDefault = str(carpetaBase / "sistema_re.db")

#que hace cada uno de estos
"""
carpeta base da el lugar donde se encuentra el py para crear los archivos ahi
archivo alumnosdefault = alumnos.txt el archivo en donde se guarda la base de datos de los alumnos
archivo log defaul = arhcivo donde se guarda el log
archivo cuentas default = archivo donde se guardan las cuentas



"""

indiceWhile = 1 #ECENCIAL

areasValidas = [
    "ASUA",
    "FESAL",
    "ADEFA",
    "Presidencias ASUA",
    "Sociedades de alumnos",
    "Asociaciones por estado",
    "Clubs Anahuac"
]

asociacionesPorEstadoValidas = [
    "Sonora",
    "Sinaloa",
    "Guanajuato",
    "Baja California",
    "Michoacan",
    "Extranjeros"
]

clubsAnahuacValidos = [
    "Ajedrez",
    "Juegos de mesa",
    "Cocina",
    "Lectura",
    "Videojuegos"
]

estatusValidos = [
    "Activo",
    "En Proceso",
    "Pendiente",
    "Graduado",
    "Finalizado",
    "Inactivo"
]

#areas donde se tienen las areas de las cuales los alumnos pueden pertenecer

cuentas = [] #array de cuentas
coordinadorActual = "" #coordinador que guarda str


#variables ecenciales
registrado = 1
limiteActividades = 8
limiteTalleres = 2
limiteVfi = 2
limiteDesarrolloPersonal = 2
limiteIntegracion = 2
limiteMentorias = 2
limiteActividadesObligatorias = 2
maxSemestre = 13
maxActividades = 100
maxSubActividades = 25
maxMentorias = 50
maxObligatorias = 50
maxReprobadas = 50
maxCantidadRequisito = 1000


class SistemaREError(Exception):
    def __init__(self, mensaje="Error general del sistema de Relaciones Estudiantiles"):
        super().__init__(mensaje)


class ValidacionError(SistemaREError):
    def __init__(self, mensaje="Error de validacion en los datos"):
        super().__init__(mensaje)


class CampoVacioError(ValidacionError):
    def __init__(self, mensaje="Un campo obligatorio se encuentra vacio"):
        super().__init__(mensaje)


class TipoDatoInvalidoError(ValidacionError):
    def __init__(self, mensaje="El tipo de dato proporcionado no es valido"):
        super().__init__(mensaje)


class FormatoInvalidoError(ValidacionError):
    def __init__(self, mensaje="El formato del dato ingresado no es valido"):
        super().__init__(mensaje)


class CaracterProhibidoError(FormatoInvalidoError):
    def __init__(self, mensaje="El texto contiene caracteres prohibidos"):
        super().__init__(mensaje)


class LongitudInvalidaError(ValidacionError):
    def __init__(self, mensaje="La longitud del texto esta fuera del rango permitido"):
        super().__init__(mensaje)


class IdInvalidoError(ValidacionError):
    def __init__(self, mensaje="El formato del ID ingresado no es valido"):
        super().__init__(mensaje)


class NombreInvalidoError(ValidacionError):
    def __init__(self, mensaje="El nombre ingresado no es valido"):
        super().__init__(mensaje)


class SemestreInvalidoError(ValidacionError):
    def __init__(self, mensaje="El semestre ingresado no es valido"):
        super().__init__(mensaje)


class SemestreFueraDeRangoError(SemestreInvalidoError):
    def __init__(self, mensaje="El semestre debe estar entre 1 y 13"):
        super().__init__(mensaje)


class ValorNegativoError(ValidacionError):
    def __init__(self, mensaje="El valor numerico no puede ser negativo"):
        super().__init__(mensaje)


class CantidadExcedidaError(ValidacionError):
    def __init__(self, mensaje="La cantidad ingresada excede el maximo permitido"):
        super().__init__(mensaje)


class CalificacionInvalidaError(ValidacionError):
    def __init__(self, mensaje="La calificacion debe estar entre 0 y 100"):
        super().__init__(mensaje)


class FechaInvalidaError(ValidacionError):
    def __init__(self, mensaje="La fecha del evento no es valida"):
        super().__init__(mensaje)


class PeriodoInvalidoError(ValidacionError):
    def __init__(self, mensaje="El periodo de gestion no es valido"):
        super().__init__(mensaje)


class EstatusInvalidoError(ValidacionError):
    def __init__(self, mensaje="El estatus de gestion no es valido"):
        super().__init__(mensaje)


class SemestresAdminInvalidoError(ValidacionError):
    def __init__(self, mensaje="Los semestres como administrador deben ser 1 o 2"):
        super().__init__(mensaje)


class PlanFormativoDesbalanceadoError(ValidacionError):
    def __init__(self, mensaje="El desglose del Plan Formativo no coincide con el total de actividades"):
        super().__init__(mensaje)


class AreaInvalidaError(ValidacionError):
    def __init__(self, mensaje="El grupo seleccionado no pertenece a Relaciones Estudiantiles"):
        super().__init__(mensaje)


class SubgrupoRequeridoError(AreaInvalidaError):
    def __init__(self, mensaje="Debes seleccionar una opcion especifica de la lista de estados o clubs"):
        super().__init__(mensaje)


class FacultadInvalidaError(ValidacionError):
    def __init__(self, mensaje="La carrera o facultad de la sociedad de alumnos no es valida"):
        super().__init__(mensaje)


class EstadoRepresentadoInvalidoError(ValidacionError):
    def __init__(self, mensaje="El estado representado no pertenece a las asociaciones validas"):
        super().__init__(mensaje)


class CategoriaClubInvalidaError(ValidacionError):
    def __init__(self, mensaje="El club seleccionado no pertenece a la lista de Clubs Anahuac"):
        super().__init__(mensaje)


class TipoGestionInvalidoError(ValidacionError):
    def __init__(self, mensaje="El tipo de gestion del alumno no es valido"):
        super().__init__(mensaje)


class CantidadRequeridaInvalidaError(ValidacionError):
    def __init__(self, mensaje="La cantidad requerida debe ser mayor a cero"):
        super().__init__(mensaje)


class BooleanoInvalidoError(ValidacionError):
    def __init__(self, mensaje="El valor debe ser booleano (True o False)"):
        super().__init__(mensaje)


class TipoRequisitoInvalidoError(ValidacionError):
    def __init__(self, mensaje="El tipo de requisito especificado no es valido"):
        super().__init__(mensaje)


class DominioError(SistemaREError):
    def __init__(self, mensaje="Error en la logica del sistema"):
        super().__init__(mensaje)


class AlumnoNoEncontradoError(DominioError):#alumno no encontrado error
    def __init__(self, mensaje="El alumno no fue encontrado en el sistema"):
        super().__init__(mensaje)
        #aqui heredamos de exception mensaje adentro del codigo de python uno puede hacer esto
        #para agarrar el mensaje del error asi te ahorras varias lineas de codigo 


class AlumnoDuplicadoError(DominioError):
    def __init__(self, mensaje="Ya existe un alumno registrado con ese ID"):
        super().__init__(mensaje)


class AlumnoNuloError(DominioError):
    def __init__(self, mensaje="El objeto alumno no puede ser nulo o de otro tipo"):
        super().__init__(mensaje)


class SinAlumnosRegistradosError(DominioError):
    def __init__(self, mensaje="No hay alumnos registrados en el sistema"):
        super().__init__(mensaje)


class CambioSinModificacionesError(DominioError):
    def __init__(self, mensaje="No se detectaron cambios respecto a los datos actuales"):
        super().__init__(mensaje)


class OperacionNoPermitidaError(DominioError):
    def __init__(self, mensaje="La operacion solicitada no esta permitida para este registro"):
        super().__init__(mensaje)


class GrupoNoEncontradoError(DominioError):
    def __init__(self, mensaje="El grupo solicitado no se encuentra registrado"):
        super().__init__(mensaje)


class AlumnoYaEnGrupoError(DominioError):
    def __init__(self, mensaje="El alumno ya se encuentra inscrito en este grupo"):
        super().__init__(mensaje)


class RequisitoInvalidoError(DominioError):
    def __init__(self, mensaje="El objeto proporcionado no es una instancia valida de Requisito"):
        super().__init__(mensaje)


class RequisitoDuplicadoError(DominioError):
    def __init__(self, mensaje="Ya existe un requisito con la misma actividad y periodo"):
        super().__init__(mensaje)


class RequisitoNoEncontradoError(DominioError):
    def __init__(self, mensaje="No se encontro el requisito especificado"):
        super().__init__(mensaje)


class RequisitoYaCompletadoError(DominioError):
    def __init__(self, mensaje="El requisito ya se encuentra completado"):
        super().__init__(mensaje)


class SinRequisitosError(DominioError):
    def __init__(self, mensaje="El estudiante no cuenta con requisitos especiales registrados"):
        super().__init__(mensaje)


class CoordinadorInvalidoError(DominioError):
    def __init__(self, mensaje="Los datos del coordinador no son validos"):
        super().__init__(mensaje)


class ContrasenaInvalidaError(CoordinadorInvalidoError):
    def __init__(self, mensaje="La contraseña del coordinador debe tener al menos 4 caracteres"):
        super().__init__(mensaje)


class AnioAdministracionInvalidoError(CoordinadorInvalidoError):
    def __init__(self, mensaje="El año de administracion debe estar entre 2000 y 2100"):
        super().__init__(mensaje)


class AutenticacionError(CoordinadorInvalidoError):
    def __init__(self, mensaje="ID o contraseña del coordinador incorrectos"):
        super().__init__(mensaje)


class AccesoDenegadoError(CoordinadorInvalidoError):
    def __init__(self, mensaje="Acceso denegado: debes iniciar sesion como coordinador registrado"):
        super().__init__(mensaje)


class CoordinadorNoEncontradoError(CoordinadorInvalidoError):
    def __init__(self, mensaje="El coordinador solicitado no se encuentra registrado"):
        super().__init__(mensaje)


class CoordinadorDuplicadoError(CoordinadorInvalidoError):
    def __init__(self, mensaje="Ya existe un coordinador registrado con ese ID"):
        super().__init__(mensaje)


class CoordinadorActivoError(CoordinadorInvalidoError):
    def __init__(self, mensaje="No se puede eliminar al coordinador que se encuentra activo"):
        super().__init__(mensaje)


class PersistenciaError(SistemaREError):
    def __init__(self, mensaje="Error de persistencia de datos"):
        super().__init__(mensaje)


class BaseDatosError(PersistenciaError):
    def __init__(self, mensaje="Error general en la base de datos SQLite"):
        super().__init__(mensaje)


class ConexionBaseDatosError(BaseDatosError):
    def __init__(self, mensaje="No fue posible conectar con la base de datos SQLite"):
        super().__init__(mensaje)


class TablaBaseDatosError(BaseDatosError):
    def __init__(self, mensaje="Error al inicializar o verificar tablas en SQLite"):
        super().__init__(mensaje)


class ConsultaBaseDatosError(BaseDatosError):
    def __init__(self, mensaje="Error al ejecutar una consulta en la base de datos"):
        super().__init__(mensaje)


class IntegridadBaseDatosError(BaseDatosError):
    def __init__(self, mensaje="Violacion de integridad en la base de datos SQLite"):
        super().__init__(mensaje)


class TransaccionBaseDatosError(BaseDatosError):
    def __init__(self, mensaje="Error durante la transaccion en la base de datos"):
        super().__init__(mensaje)


class MigracionDatosError(BaseDatosError):
    def __init__(self, mensaje="Error al migrar datos desde el archivo de texto"):
        super().__init__(mensaje)


class ArchivoNoEncontradoError(PersistenciaError):
    def __init__(self, mensaje="No se encontro el archivo solicitado"):
        super().__init__(mensaje)


class PermisoArchivoError(PersistenciaError):
    def __init__(self, mensaje="No se tienen permisos suficientes sobre el archivo"):
        super().__init__(mensaje)


class EscrituraArchivoError(PersistenciaError):
    def __init__(self, mensaje="No se pudo escribir en el archivo"):
        super().__init__(mensaje)


class LecturaArchivoError(PersistenciaError):
    def __init__(self, mensaje="No se pudo leer el archivo"):
        super().__init__(mensaje)


class FormatoArchivoCorruptoError(PersistenciaError):
    def __init__(self, mensaje="El archivo contiene una linea con formato incompleto o corrupto"):
        super().__init__(mensaje)


class SerializacionRequisitoError(PersistenciaError):
    def __init__(self, mensaje="No se pudo reconstruir un requisito almacenado"):
        super().__init__(mensaje)


class InterfazError(SistemaREError):
    def __init__(self, mensaje="Error en la interfaz grafica"):
        super().__init__(mensaje)


class RecursoImagenError(InterfazError):
    def __init__(self, mensaje="No se pudo cargar la imagen institucional"):
        super().__init__(mensaje)


class SeleccionInvalidaError(InterfazError):
    def __init__(self, mensaje="Debe seleccionar un elemento valido de la lista"):
        super().__init__(mensaje)


class VentanaCerradaError(InterfazError):
    def __init__(self, mensaje="La ventana ya no se encuentra disponible"):
        super().__init__(mensaje)


def contieneCaracterProhibido(texto):
    prohibidos = ["|", "~", ";", "\n", "\r"]
    for car in prohibidos:
        if car in texto:
            return True
    return False


def validarTextoBasico(valor, nombreCampo, minLen=1, maxLen=100, permitirDelimitadores=False):
    if valor is None:
        raise TipoDatoInvalidoError(f"El campo {nombreCampo} no puede ser nulo")
    if not isinstance(valor, str):
        raise TipoDatoInvalidoError(f"El campo {nombreCampo} debe ser texto")
    limpio = valor.strip()
    if not limpio:
        raise CampoVacioError(f"El campo {nombreCampo} no puede estar vacio")
    if not permitirDelimitadores and contieneCaracterProhibido(limpio):
        raise CaracterProhibidoError(f"El campo {nombreCampo} contiene caracteres no permitidos (|, ~, ;)")
    if len(limpio) < minLen or len(limpio) > maxLen:
        raise LongitudInvalidaError(f"El campo {nombreCampo} debe tener entre {minLen} y {maxLen} caracteres")
    return limpio


def validarIdTexto(valor, nombreCampo="ID", minLen=2, maxLen=20):
    limpio = validarTextoBasico(valor, nombreCampo, minLen, maxLen)
    if " " in limpio:
        raise IdInvalidoError(f"El {nombreCampo} no puede contener espacios")
    for c in limpio:
        if not (c.isalnum() or c in "-_"):
            raise IdInvalidoError(f"El {nombreCampo} solo permite letras, numeros, guion (-) y guion bajo (_)")
    return limpio


def validarNombrePersona(valor, nombreCampo="Nombre"):
    limpio = validarTextoBasico(valor, nombreCampo, 3, 100)
    if limpio.isdigit():
        raise NombreInvalidoError(f"El {nombreCampo} no puede estar formado solo por numeros")
    cantidadLetras = 0
    for c in limpio:
        if c.isdigit():
            raise NombreInvalidoError(f"El {nombreCampo} no puede contener numeros")
        if c.isalpha():
            cantidadLetras += 1
        elif c not in " .-'":
            raise NombreInvalidoError(f"El {nombreCampo} contiene caracteres no validos: {c}")
    if cantidadLetras < 2:
        raise NombreInvalidoError(f"El {nombreCampo} debe contener al menos 2 letras")
    return limpio


def validarEntero(valor, nombreCampo, minimo=0, maximo=100, excFueraRango=None):
    if valor is None:
        raise TipoDatoInvalidoError(f"El campo {nombreCampo} no puede ser nulo")
    if isinstance(valor, bool) or not isinstance(valor, int):
        raise TipoDatoInvalidoError(f"El campo {nombreCampo} debe ser un numero entero")
    if valor < 0:
        raise ValorNegativoError(f"El campo {nombreCampo} no puede ser negativo")
    if valor < minimo:
        if excFueraRango is not None:
            raise excFueraRango(f"El campo {nombreCampo} debe estar entre {minimo} y {maximo}")
        raise ValorNegativoError(f"El campo {nombreCampo} debe ser al menos {minimo}")
    if valor > maximo:
        if excFueraRango is not None:
            raise excFueraRango(f"El campo {nombreCampo} debe estar entre {minimo} y {maximo}")
        raise CantidadExcedidaError(f"El campo {nombreCampo} no puede superar {maximo}")
    return valor


def parsearEnteroTexto(texto, nombreCampo, minimo=0, maximo=100, excFueraRango=None):
    if texto is None or not isinstance(texto, str):
        raise TipoDatoInvalidoError(f"El campo {nombreCampo} debe ser texto numerico")
    limpio = texto.strip()
    if not limpio:
        raise CampoVacioError(f"El campo {nombreCampo} no puede estar vacio")
    if limpio.startswith("-") and len(limpio) > 1 and limpio[1:].isdigit():
        raise ValorNegativoError(f"El campo {nombreCampo} no puede ser negativo")
    if not limpio.isdigit():
        raise TipoDatoInvalidoError(f"El campo {nombreCampo} debe ser un numero entero valido")
    numero = int(limpio)
    return validarEntero(numero, nombreCampo, minimo, maximo, excFueraRango)


def validarFlotante(valor, nombreCampo, minimo=0.0, maximo=100.0):
    if valor is None:
        raise TipoDatoInvalidoError(f"El campo {nombreCampo} no puede ser nulo")
    if isinstance(valor, bool) or not isinstance(valor, (int, float)):
        raise TipoDatoInvalidoError(f"El campo {nombreCampo} debe ser numerico")
    num = float(valor)
    if num < minimo or num > maximo:
        raise CalificacionInvalidaError(f"El campo {nombreCampo} debe estar entre {minimo} y {maximo}")
    return num


def parsearFlotanteTexto(texto, nombreCampo, minimo=0.0, maximo=100.0):
    if texto is None or not isinstance(texto, str):
        raise TipoDatoInvalidoError(f"El campo {nombreCampo} debe ser texto numerico")
    limpio = texto.strip()
    if not limpio:
        raise CampoVacioError(f"El campo {nombreCampo} no puede estar vacio")
    try:
        num = float(limpio)
    except ValueError:
        raise TipoDatoInvalidoError(f"El campo {nombreCampo} debe ser un numero decimal valido")
    return validarFlotante(num, nombreCampo, minimo, maximo)


def validarBooleano(valor, nombreCampo):
    if not isinstance(valor, bool):
        raise BooleanoInvalidoError(f"El campo {nombreCampo} debe ser booleano (True o False)")
    return valor


def validarFechaTexto(fechaTexto):
    limpio = validarTextoBasico(fechaTexto, "Fecha del evento", 8, 20)
    fechaObj = None
    try:
        fechaObj = datetime.strptime(limpio, "%d/%m/%Y")
    except ValueError:
        try:
            fechaObj = datetime.strptime(limpio, "%Y-%m-%d")
        except ValueError:
            raise FechaInvalidaError("La fecha debe tener formato DD/MM/AAAA o AAAA-MM-DD y existir en el calendario")
    if fechaObj.year < 2000 or fechaObj.year > 2100:
        raise FechaInvalidaError("El año de la fecha debe estar entre 2000 y 2100")
    return limpio


def validarPeriodoTexto(periodoTexto):
    limpio = validarTextoBasico(periodoTexto, "Periodo", 4, 30)
    if "-" in limpio:
        partes = limpio.split("-")
        if len(partes) == 2 and partes[0].strip().isdigit() and partes[1].strip().isdigit():
            anioInicio = int(partes[0].strip())
            anioFin = int(partes[1].strip())
            if anioInicio < 2000 or anioFin > 2100 or anioFin < anioInicio:
                raise PeriodoInvalidoError("El periodo debe tener un rango de años valido (ej. 2026-2027)")
    return limpio


def validarEstatusGestion(estatusTexto):
    limpio = validarTextoBasico(estatusTexto, "Estatus", 3, 30)
    if limpio not in estatusValidos:
        raise EstatusInvalidoError(f"El estatus '{limpio}' no es valido")
    return limpio


def validarAreaTexto(areaTexto):
    if areaTexto is None:
        raise AreaInvalidaError("Debe seleccionar un grupo de Relaciones Estudiantiles")
    if not isinstance(areaTexto, str):
        raise TipoDatoInvalidoError("El grupo debe ser texto")
    limpio = areaTexto.strip()
    if not limpio or limpio == "Selecciona un grupo":
        raise AreaInvalidaError("Debes seleccionar un grupo valido")
    if limpio not in areasValidas:
        raise AreaInvalidaError(f"El grupo '{limpio}' no pertenece a los grupos validos de la universidad")
    return limpio


def validarSubgrupoArea(areaDeRe, subgrupo, obligatorio=False):
    if subgrupo is None:
        limpio = ""
    elif not isinstance(subgrupo, str):
        raise TipoDatoInvalidoError("El subgrupo debe ser texto")
    else:
        limpio = subgrupo.strip()
    if contieneCaracterProhibido(limpio):
        raise CaracterProhibidoError("El subgrupo contiene caracteres no permitidos")

    if areaDeRe == "Clubs Anahuac":
        if not limpio or limpio == "Selecciona un club" or limpio == "No aplica":
            if obligatorio:
                raise SubgrupoRequeridoError("Debes seleccionar un club de la lista de Clubs Anahuac")
            return ""
        if limpio not in clubsAnahuacValidos:
            raise CategoriaClubInvalidaError(f"El club '{limpio}' no pertenece a los Clubs Anahuac validos")
        return limpio

    if areaDeRe == "Asociaciones por estado":
        if not limpio or limpio == "Selecciona un estado" or limpio == "No aplica":
            if obligatorio:
                raise SubgrupoRequeridoError("Debes seleccionar un estado de la lista de Asociaciones por estado")
            return ""
        if limpio not in asociacionesPorEstadoValidas:
            raise EstadoRepresentadoInvalidoError(f"La asociacion '{limpio}' no pertenece a las asociaciones validas")
        return limpio

    if areaDeRe == "Sociedades de alumnos":
        if not limpio or limpio == "No aplica":
            return "General"
        if len(limpio) < 2 or len(limpio) > 60:
            raise FacultadInvalidaError("La facultad debe tener entre 2 y 60 caracteres")
        return limpio

    return ""


class AreaRE:#clase areaRe

    def __init__(self, idArea, nombreArea):
        #inicializamos el area
        if idArea is None:
            raise TipoDatoInvalidoError("El ID del area no puede ser nulo")
        if isinstance(idArea, bool) or not isinstance(idArea, int):
            raise TipoDatoInvalidoError("El ID del area debe ser un numero entero")
        if idArea <= 0:
            raise ValorNegativoError("El ID del area debe ser mayor a cero")
        limpioNombre = validarTextoBasico(nombreArea, "Nombre del area", 2, 80)

        self._idArea = idArea
        self._nombreArea = limpioNombre
        self._alumnos = []
        #si no entra a ningun error inicializa las variables


    def getIdArea(self):
        return self._idArea

    def getNombreArea(self):
        return self._nombreArea

    def getAlumnos(self):
        return self._alumnos

    def obtenerTipoGrupo(self):
        return f"Area de Relaciones Estudiantiles ({self._nombreArea})"


    #====================
    #      GETTERS
    #===================

    def agregarAlumno(self, alumno):
        if alumno is None or not isinstance(alumno, Alumno):
            raise AlumnoNuloError("El objeto agregado debe ser una instancia valida de Alumno")
        for existente in self._alumnos:
            if existente.getId() == alumno.getId():
                raise AlumnoYaEnGrupoError(f"El alumno {alumno.getId()} ya pertenece al grupo {self._nombreArea}")
        self._alumnos.append(alumno)
        #funcion agregar alumno si no entra a vacio usa append

    def eliminarAlumno(self, idAlumno):
        idLimpio = validarIdTexto(idAlumno, "ID del alumno")
        for a in self._alumnos:
            if a.getId() == idLimpio:
                self._alumnos.remove(a)
                return True
        raise AlumnoNoEncontradoError(f"El alumno con ID {idLimpio} no se encuentra en el grupo {self._nombreArea}")
        #funcion eliminar alumno inicia al principio y verifica hasta que llega al id  y cuanod llegue lo elimina
        # despues regresa True para la funcion del promgrama principal

    def limpiarAlumnos(self):
        self._alumnos = []

    def __str__(self):
        return f"ID {self._idArea} | Grupo: {self._nombreArea} | Inscritos: {len(self._alumnos)}"
        #str para cuando lo mandemos a pantalla mande esto

class ASUA(AreaRE):
    def __init__(self, idArea=1, nombreArea="ASUA"):
        super().__init__(idArea, nombreArea)

    def obtenerTipoGrupo(self):
        return "Accion Social Universidad Anahuac"
        #herencia de ASUA con areaRE

class FESAL(AreaRE):
    def __init__(self, idArea=2, nombreArea="FESAL"):
        super().__init__(idArea, nombreArea)

    def obtenerTipoGrupo(self):
        return "Federacion de Sociedades de Alumnos"
        #Herencia de fesal con areaRE


class ADEFA(AreaRE):
    def __init__(self, idArea=3, nombreArea="ADEFA"):
        super().__init__(idArea, nombreArea)

    def obtenerTipoGrupo(self):
        return "Asociacion de Estudiantes Foraneos Anahuac"
        #Herencia de ADEFA con areaEre


class PresidenciasASUA(ASUA):
    def __init__(self, idArea=4, nombreArea="Presidencias ASUA"):
        super().__init__(idArea, nombreArea)

    def obtenerTipoGrupo(self):
        return "Direccion y Presidencias ASUA"
        #Herencia de Presidencia Asua con asua

class SociedadesDeAlumnos(AreaRE):
    def __init__(self, idArea=5, nombreArea="Sociedades de alumnos", carrera="General"):
        super().__init__(idArea, nombreArea)
        if carrera is None or not isinstance(carrera, str) or not carrera.strip():
            raise FacultadInvalidaError("La carrera de la sociedad de alumnos no puede estar vacia")
        self._facultad = validarTextoBasico(carrera, "Facultad", 2, 60)

    def getDetalle(self):
        return self._facultad

    def obtenerTipoGrupo(self):
        return f"Sociedad de Alumnos ({self._facultad})"
        #Herencia de sociedades de alumnos con area rea


class AsociacionesPorEstado(AreaRE):
    def __init__(self, idArea=6, nombreArea="Asociaciones por estado", estadoRepresentado="Sonora"):
        super().__init__(idArea, nombreArea)
        if estadoRepresentado is None or not isinstance(estadoRepresentado, str) or not estadoRepresentado.strip():
            raise EstadoRepresentadoInvalidoError("El estado representado no puede estar vacio")
        estadoLimpio = validarTextoBasico(estadoRepresentado, "Estado representado", 2, 60)
        if estadoLimpio not in asociacionesPorEstadoValidas:
            raise EstadoRepresentadoInvalidoError(f"El estado '{estadoLimpio}' no pertenece a las asociaciones validas")
        self._estadoRepresentado = estadoLimpio

    def getDetalle(self):
        return self._estadoRepresentado

    def obtenerTipoGrupo(self):
        return f"Asociacion Estatal ({self._estadoRepresentado})"
        #herencia de asocianoes por estado de area re


class AsociacionSonora(AsociacionesPorEstado):
    def __init__(self, idArea=8, nombreArea="Asociacion Sonora", estadoRepresentado="Sonora"):
        super().__init__(idArea, nombreArea, estadoRepresentado)


class AsociacionSinaloa(AsociacionesPorEstado):
    def __init__(self, idArea=9, nombreArea="Asociacion Sinaloa", estadoRepresentado="Sinaloa"):
        super().__init__(idArea, nombreArea, estadoRepresentado)


class AsociacionGuanajuato(AsociacionesPorEstado):
    def __init__(self, idArea=10, nombreArea="Asociacion Guanajuato", estadoRepresentado="Guanajuato"):
        super().__init__(idArea, nombreArea, estadoRepresentado)


class AsociacionBajaCalifornia(AsociacionesPorEstado):
    def __init__(self, idArea=11, nombreArea="Asociacion Baja California", estadoRepresentado="Baja California"):
        super().__init__(idArea, nombreArea, estadoRepresentado)


class AsociacionMichoacan(AsociacionesPorEstado):
    def __init__(self, idArea=12, nombreArea="Asociacion Michoacan", estadoRepresentado="Michoacan"):
        super().__init__(idArea, nombreArea, estadoRepresentado)


class AsociacionExtranjeros(AsociacionesPorEstado):
    def __init__(self, idArea=13, nombreArea="Asociacion Extranjeros", estadoRepresentado="Extranjeros"):
        super().__init__(idArea, nombreArea, estadoRepresentado)


class ClubsAnahuac(AreaRE):
    def __init__(self, idArea=7, nombreArea="Clubs Anahuac", categoriaClub="Ajedrez"):
        super().__init__(idArea, nombreArea)
        if categoriaClub is None or not isinstance(categoriaClub, str) or not categoriaClub.strip():
            raise CategoriaClubInvalidaError("La categoria del club no puede estar vacia")
        catLimpia = validarTextoBasico(categoriaClub, "Categoria del club", 2, 60)
        if catLimpia not in clubsAnahuacValidos:
            raise CategoriaClubInvalidaError(f"El club '{catLimpia}' no pertenece a los Clubs Anahuac validos")
        self._categoriaClub = catLimpia
        #herencia de clubs anahuac de area re

    def getDetalle(self):
        return self._categoriaClub

    def obtenerTipoGrupo(self):
        return f"Club Universitario ({self._categoriaClub})"


class ClubAjedrez(ClubsAnahuac):
    def __init__(self, idArea=14, nombreArea="Club Ajedrez", categoriaClub="Ajedrez"):
        super().__init__(idArea, nombreArea, categoriaClub)


class ClubJuegosDeMesa(ClubsAnahuac):
    def __init__(self, idArea=15, nombreArea="Club Juegos de mesa", categoriaClub="Juegos de mesa"):
        super().__init__(idArea, nombreArea, categoriaClub)


class ClubCocina(ClubsAnahuac):
    def __init__(self, idArea=16, nombreArea="Club Cocina", categoriaClub="Cocina"):
        super().__init__(idArea, nombreArea, categoriaClub)


class ClubLectura(ClubsAnahuac):
    def __init__(self, idArea=17, nombreArea="Club Lectura", categoriaClub="Lectura"):
        super().__init__(idArea, nombreArea, categoriaClub)


class ClubVideojuegos(ClubsAnahuac):
    def __init__(self, idArea=18, nombreArea="Club Videojuegos", categoriaClub="Videojuegos"):
        super().__init__(idArea, nombreArea, categoriaClub)


gruposDisponibles = {
    1: ASUA(),
    2: FESAL(),
    3: ADEFA(),
    4: PresidenciasASUA(),
    5: SociedadesDeAlumnos(),
    6: AsociacionesPorEstado(),
    7: ClubsAnahuac()
}
    #mandamos a llamar todo y lo guardamos en un diccionario con cada funcion

asociacionesEstadoDisponibles = {
    "Sonora": AsociacionSonora(),
    "Sinaloa": AsociacionSinaloa(),
    "Guanajuato": AsociacionGuanajuato(),
    "Baja California": AsociacionBajaCalifornia(),
    "Michoacan": AsociacionMichoacan(),
    "Extranjeros": AsociacionExtranjeros()
}

clubsDisponibles = {
    "Ajedrez": ClubAjedrez(),
    "Juegos de mesa": ClubJuegosDeMesa(),
    "Cocina": ClubCocina(),
    "Lectura": ClubLectura(),
    "Videojuegos": ClubVideojuegos()
}


def sincronizarGruposConCatalogo(listaAlumnos):
    for grupo in gruposDisponibles.values():
        grupo.limpiarAlumnos()
    for asoc in asociacionesEstadoDisponibles.values():
        asoc.limpiarAlumnos()
    for club in clubsDisponibles.values():
        club.limpiarAlumnos()
    if listaAlumnos is None:
        return
    for alumno in listaAlumnos:
        for grupo in gruposDisponibles.values():
            if grupo.getNombreArea() == alumno.getArea():
                try:
                    grupo.agregarAlumno(alumno)
                except AlumnoYaEnGrupoError:
                    pass
                break
        if alumno.getArea() == "Asociaciones por estado" and alumno.getSubgrupo() in asociacionesEstadoDisponibles:
            try:
                asociacionesEstadoDisponibles[alumno.getSubgrupo()].agregarAlumno(alumno)
            except AlumnoYaEnGrupoError:
                pass
        elif alumno.getArea() == "Clubs Anahuac" and alumno.getSubgrupo() in clubsDisponibles:
            try:
                clubsDisponibles[alumno.getSubgrupo()].agregarAlumno(alumno)
            except AlumnoYaEnGrupoError:
                pass


def buscarGrupoPorId(idArea):
    idVal = validarEntero(idArea, "ID del grupo", 1, 100)
    if idVal not in gruposDisponibles:
        raise GrupoNoEncontradoError(f"No existe un grupo registrado con ID {idVal}")
    return gruposDisponibles[idVal]


def buscarGrupoPorNombre(nombreArea):
    nombreLimpio = validarTextoBasico(nombreArea, "Nombre del grupo", 2, 80)
    for grupo in gruposDisponibles.values():
        if grupo.getNombreArea() == nombreLimpio:
            return grupo
    raise GrupoNoEncontradoError(f"No existe un grupo registrado con el nombre '{nombreLimpio}'")


class Coordinador:
    def __init__(self, idNombre, contrasena, nombre, catalogoAlumnos, area="General", anioAdministracion=2026, gestorBd=None):
        try:
            idLimpio = validarIdTexto(idNombre, "ID del coordinador", 2, 30)
        except ValidacionError as e:
            raise CoordinadorInvalidoError(str(e))
        if contrasena is None or not isinstance(contrasena, str):
            raise ContrasenaInvalidaError("La contraseña debe ser texto")
        passLimpia = contrasena.strip()
        if not passLimpia:
            raise CampoVacioError("La contraseña del coordinador no puede estar vacia")
        if len(passLimpia) < 4 or len(passLimpia) > 50:
            raise ContrasenaInvalidaError("La contraseña del coordinador debe tener entre 4 y 50 caracteres")
        if contieneCaracterProhibido(passLimpia):
            raise CaracterProhibidoError("La contraseña contiene caracteres no permitidos")
        nombreLimpio = validarNombrePersona(nombre, "Nombre del coordinador")
        areaLimpia = validarTextoBasico(area if area is not None else "General", "Area del coordinador", 2, 60)
        anioVal = validarEntero(anioAdministracion, "Año de administracion", 2000, 2100, AnioAdministracionInvalidoError)
        if catalogoAlumnos is not None and not isinstance(catalogoAlumnos, list):
            raise TipoDatoInvalidoError("El catalogo de alumnos debe ser una lista")

        self._idNombre = idLimpio
        self._contrasena = passLimpia
        self._nombre = nombreLimpio
        self._catalogoAlumnos = catalogoAlumnos if catalogoAlumnos is not None else []
        self._area = areaLimpia
        self._anioAdministracion = anioVal
        self._gestorBd = gestorBd
        sincronizarGruposConCatalogo(self._catalogoAlumnos)

    def getIdNombre(self):
        return self._idNombre

    def getContrasena(self):
        return self._contrasena

    def getNombre(self):
        return self._nombre

    def getArea(self):
        return self._area

    def getAnioAdministracion(self):
        return self._anioAdministracion

    def setGestorBd(self, gestorBd):
        self._gestorBd = gestorBd

    def verificarContrasena(self, contrasena):
        if contrasena is None or not isinstance(contrasena, str) or not contrasena.strip():
            raise CampoVacioError("Debe ingresar la contraseña del coordinador")
        if contrasena.strip() != self._contrasena:
            raise AutenticacionError("La contraseña ingresada es incorrecta")
        return True

    def buscarAlumnoPorId(self, idAlumno):
        idLimpio = validarIdTexto(idAlumno, "ID del alumno")
        for alumno in self._catalogoAlumnos:
            if alumno.getId() == idLimpio:
                return alumno
        raise AlumnoNoEncontradoError(f"Alumno {idLimpio} no encontrado")

    def darDeAltaAlumno(self, alumno):
        if alumno is None or not isinstance(alumno, Alumno):
            raise AlumnoNuloError("No se puede registrar un alumno vacio o invalido")
        for existente in self._catalogoAlumnos:
            if existente.getId() == alumno.getId():
                raise AlumnoDuplicadoError(f"Ya existe un alumno registrado con el ID {alumno.getId()}")
        if self._gestorBd is not None:
            self._gestorBd.guardarAlumno(alumno)
            self._gestorBd.registrarHistorial(self._idNombre, "ALTA_ALUMNO", alumno.getId(), f"Registro de {alumno.getNombre()} en {alumno.getArea()}")
        self._catalogoAlumnos.append(alumno)
        sincronizarGruposConCatalogo(self._catalogoAlumnos)
        return True

    def actualizarAlumno(self, alumnoActualizado):
        if alumnoActualizado is None or not isinstance(alumnoActualizado, Alumno):
            raise AlumnoNuloError("El alumno actualizado no es valido")
        indiceEncontrado = -1
        indice = 0
        for existente in self._catalogoAlumnos:
            if existente.getId() == alumnoActualizado.getId():
                indiceEncontrado = indice
                break
            indice += 1
        if indiceEncontrado == -1:
            raise AlumnoNoEncontradoError(f"No se encontro al alumno con ID {alumnoActualizado.getId()} para actualizar")
        if self._gestorBd is not None:
            self._gestorBd.actualizarAlumno(alumnoActualizado)
            self._gestorBd.registrarHistorial(self._idNombre, "ACTUALIZACION_ALUMNO", alumnoActualizado.getId(), f"Actualizacion de datos y progreso de {alumnoActualizado.getNombre()}")
        self._catalogoAlumnos[indiceEncontrado] = alumnoActualizado
        sincronizarGruposConCatalogo(self._catalogoAlumnos)
        return True

    def darDeBajaAlumno(self, idAlumno):
        idLimpio = validarIdTexto(idAlumno, "ID del alumno")
        for alumno in self._catalogoAlumnos:
            if alumno.getId() == idLimpio:
                if self._gestorBd is not None:
                    self._gestorBd.eliminarAlumno(idLimpio)
                    self._gestorBd.registrarHistorial(self._idNombre, "BAJA_ALUMNO", idLimpio, f"Baja del alumno {alumno.getNombre()}")
                self._catalogoAlumnos.remove(alumno)
                sincronizarGruposConCatalogo(self._catalogoAlumnos)
                return True
        raise AlumnoNoEncontradoError(f"No se encontro al alumno con ID {idLimpio}")

    def mostrarAlumno(self, idAlumno):
        alumno = self.buscarAlumnoPorId(idAlumno)
        print(alumno)
        return alumno

    def mostrarAlumnosCumplimiento(self):
        lista = []
        for a in self._catalogoAlumnos:
            if a.verificarGraduacion() == "S":
                lista.append(a)
        return lista

    def mostrarAlumnosConRequisitosPendientes(self):
        lista = []
        for a in self._catalogoAlumnos:
            if a.verificarGraduacion() != "S":
                lista.append(a)
        return lista

    def obtenerTodosLosAlumnos(self):
        lista = []
        for a in self._catalogoAlumnos:
            lista.append(a)
        return lista

    def filtrarAlumnosPorGrupo(self, areaDeRe, subgrupo=""):
        areaLimpia = validarAreaTexto(areaDeRe)
        subLimpio = "" if subgrupo is None else subgrupo.strip()
        resultado = []
        for a in self._catalogoAlumnos:
            if a.getArea() == areaLimpia:
                if not subLimpio or subLimpio == "Todos" or a.getSubgrupo() == subLimpio:
                    resultado.append(a)
        return resultado

    def __str__(self):
        return f"Coordinador: {self._nombre} | Area: {self._area} | Administracion: {self._anioAdministracion}"


class Alumno:
    def __init__(self, idAlumno, nombre, semestre, areaDeRe, gestion, materiasReprobadas, actividades=0, mentorias=0, actividadesObligatorias=0, seminario=False, talleres=None, actividadesVfi=None, desarrolloPersonal=None, integracion=None, subgrupo=""):
        idLimpio = validarIdTexto(idAlumno, "ID del alumno")
        nombreLimpio = validarNombrePersona(nombre, "Nombre del alumno")
        semestreVal = validarEntero(semestre, "Semestre", 1, maxSemestre, SemestreFueraDeRangoError)
        areaLimpia = validarAreaTexto(areaDeRe)
        subgrupoLimpio = validarSubgrupoArea(areaLimpia, subgrupo, False)
        try:
            gestionLimpia = validarTextoBasico(gestion, "Tipo de gestion", 3, 60)
        except ValidacionError as e:
            raise TipoGestionInvalidoError(str(e))
        reprobadasVal = validarEntero(materiasReprobadas, "Materias reprobadas", 0, maxReprobadas)
        actividadesVal = validarEntero(actividades, "Actividades", 0, maxActividades)
        mentoriasVal = validarEntero(mentorias, "Mentorias", 0, maxMentorias)
        obligatoriasVal = validarEntero(actividadesObligatorias, "Actividades obligatorias", 0, maxObligatorias)
        seminarioVal = validarBooleano(seminario, "Seminario")

        usaDesglose = False
        talleresVal = 0
        vfiVal = 0
        desarrolloVal = 0
        integracionVal = 0
        if talleres is not None or actividadesVfi is not None or desarrolloPersonal is not None or integracion is not None:
            talleresVal = validarEntero(0 if talleres is None else talleres, "Talleres", 0, maxSubActividades)
            vfiVal = validarEntero(0 if actividadesVfi is None else actividadesVfi, "Actividades VFI", 0, maxSubActividades)
            desarrolloVal = validarEntero(0 if desarrolloPersonal is None else desarrolloPersonal, "Desarrollo personal", 0, maxSubActividades)
            integracionVal = validarEntero(0 if integracion is None else integracion, "Integracion", 0, maxSubActividades)
            sumaDesglose = talleresVal + vfiVal + desarrolloVal + integracionVal
            if sumaDesglose > 0:
                if actividadesVal > 0 and actividadesVal != sumaDesglose:
                    raise PlanFormativoDesbalanceadoError(f"El total de actividades ({actividadesVal}) no coincide con la suma del Plan Formativo ({sumaDesglose})")
                actividadesVal = sumaDesglose
                usaDesglose = True

        self._idAlumno = idLimpio
        self._nombre = nombreLimpio
        self._semestre = semestreVal
        self._areaDeRe = areaLimpia
        self._subgrupo = subgrupoLimpio
        self._gestionRe = gestionLimpia
        self._materiasReprobadas = reprobadasVal
        self._actividades = actividadesVal
        self._talleres = talleresVal
        self._actividadesVfi = vfiVal
        self._desarrolloPersonal = desarrolloVal
        self._integracion = integracionVal
        self._usaDesglose = usaDesglose
        self._mentorias = mentoriasVal
        self._actividadesObligatorias = obligatoriasVal
        self._seminario = seminarioVal

    def getId(self):
        return self._idAlumno

    def getNombre(self):
        return self._nombre

    def getSemestre(self):
        return self._semestre

    def getArea(self):
        return self._areaDeRe

    def getSubgrupo(self):
        return self._subgrupo

    def getAreaCompleta(self):
        if self._subgrupo:
            return f"{self._areaDeRe} ({self._subgrupo})"
        return self._areaDeRe

    def getGestionRe(self):
        return self._gestionRe

    def getMateriasReprobadas(self):
        return self._materiasReprobadas

    def getActividades(self):
        return self._actividades

    def getTalleres(self):
        return self._talleres

    def getActividadesVfi(self):
        return self._actividadesVfi

    def getDesarrolloPersonal(self):
        return self._desarrolloPersonal

    def getIntegracion(self):
        return self._integracion

    def getUsaDesglose(self):
        return self._usaDesglose

    def getMentorias(self):
        return self._mentorias

    def getActividadesObligatorias(self):
        return self._actividadesObligatorias

    def getSeminario(self):
        return self._seminario

    def actualizarDatos(self, nombre, semestre, areaDeRe, gestion=None, subgrupo=None):
        nombreLimpio = validarNombrePersona(nombre, "Nombre del alumno")
        semestreVal = validarEntero(semestre, "Semestre", 1, maxSemestre, SemestreFueraDeRangoError)
        areaLimpia = validarAreaTexto(areaDeRe)
        subVal = self._subgrupo if subgrupo is None else subgrupo
        subgrupoLimpio = validarSubgrupoArea(areaLimpia, subVal, False)
        gestionLimpia = self._gestionRe
        if gestion is not None:
            try:
                gestionLimpia = validarTextoBasico(gestion, "Tipo de gestion", 3, 60)
            except ValidacionError as e:
                raise TipoGestionInvalidoError(str(e))
        self._nombre = nombreLimpio
        self._semestre = semestreVal
        self._areaDeRe = areaLimpia
        self._subgrupo = subgrupoLimpio
        self._gestionRe = gestionLimpia

    def actualizarProgreso(self, actividades, mentorias, actividadesObligatorias, materiasReprobadas, seminario=None, talleres=None, actividadesVfi=None, desarrolloPersonal=None, integracion=None):
        actividadesVal = validarEntero(actividades, "Actividades", 0, maxActividades)
        mentoriasVal = validarEntero(mentorias, "Mentorias", 0, maxMentorias)
        obligatoriasVal = validarEntero(actividadesObligatorias, "Actividades obligatorias", 0, maxObligatorias)
        reprobadasVal = validarEntero(materiasReprobadas, "Materias reprobadas", 0, maxReprobadas)
        seminarioVal = self._seminario
        if seminario is not None:
            seminarioVal = validarBooleano(seminario, "Seminario")

        usaDesglose = False
        talleresVal = 0
        vfiVal = 0
        desarrolloVal = 0
        integracionVal = 0
        if talleres is not None or actividadesVfi is not None or desarrolloPersonal is not None or integracion is not None:
            talleresVal = validarEntero(0 if talleres is None else talleres, "Talleres", 0, maxSubActividades)
            vfiVal = validarEntero(0 if actividadesVfi is None else actividadesVfi, "Actividades VFI", 0, maxSubActividades)
            desarrolloVal = validarEntero(0 if desarrolloPersonal is None else desarrolloPersonal, "Desarrollo personal", 0, maxSubActividades)
            integracionVal = validarEntero(0 if integracion is None else integracion, "Integracion", 0, maxSubActividades)
            sumaDesglose = talleresVal + vfiVal + desarrolloVal + integracionVal
            if sumaDesglose > 0:
                if actividadesVal > 0 and actividadesVal != sumaDesglose:
                    raise PlanFormativoDesbalanceadoError(f"El total de actividades ({actividadesVal}) no coincide con la suma del Plan Formativo ({sumaDesglose})")
                actividadesVal = sumaDesglose
                usaDesglose = True

        self._actividades = actividadesVal
        self._talleres = talleresVal
        self._actividadesVfi = vfiVal
        self._desarrolloPersonal = desarrolloVal
        self._integracion = integracionVal
        self._usaDesglose = usaDesglose
        self._mentorias = mentoriasVal
        self._actividadesObligatorias = obligatoriasVal
        self._materiasReprobadas = reprobadasVal
        self._seminario = seminarioVal

    def verificarActividades(self, cantidadActividades=None):
        try:
            if cantidadActividades is not None:
                cant = validarEntero(cantidadActividades, "Actividades", 0, maxActividades)
                return cant >= limiteActividades
            cant = validarEntero(self._actividades, "Actividades", 0, maxActividades)
            if self._usaDesglose:
                return (
                    self._talleres >= limiteTalleres and
                    self._actividadesVfi >= limiteVfi and
                    self._desarrolloPersonal >= limiteDesarrolloPersonal and
                    self._integracion >= limiteIntegracion and
                    cant >= limiteActividades
                )
            return cant >= limiteActividades
        except (SistemaREError, TypeError, ValueError) as e:
            enviarError(e)
            raise

    def verificarMentorias(self, cantidadMentorias=None):
        try:
            if cantidadMentorias is not None:
                cant = validarEntero(cantidadMentorias, "Mentorias", 0, maxMentorias)
            else:
                cant = validarEntero(self._mentorias, "Mentorias", 0, maxMentorias)
            return cant >= limiteMentorias
        except (SistemaREError, TypeError, ValueError) as e:
            enviarError(e)
            raise

    def verificarSeminario(self):
        return self._seminario

    def verificarSituacionAcademica(self):
        try:
            reprobadas = validarEntero(self._materiasReprobadas, "Materias reprobadas", 0, maxReprobadas)
            return reprobadas == 0
        except (SistemaREError, TypeError, ValueError) as e:
            enviarError(e)
            raise

    def verificarActividadesObligatorias(self):
        try:
            obligatorias = validarEntero(self._actividadesObligatorias, "Actividades obligatorias", 0, maxObligatorias)
            return obligatorias >= limiteActividadesObligatorias
        except (SistemaREError, TypeError, ValueError) as e:
            enviarError(e)
            raise

    def obtenerCumplidos(self):
        cumplidos = []
        if self.verificarActividades():
            if self._usaDesglose:
                cumplidos.append(f"Plan Formativo ({self._actividades}/{limiteActividades})")
            else:
                cumplidos.append(f"Actividades ({self._actividades}/{limiteActividades})")
        if self.verificarSeminario():
            cumplidos.append("Seminario intermedio")
        if self.verificarMentorias():
            cumplidos.append(f"Mentorias ({self._mentorias}/{limiteMentorias})")
        if self.verificarSituacionAcademica():
            cumplidos.append("Situacion academica (0 reprobadas)")
        if self.verificarActividadesObligatorias():
            cumplidos.append(f"Actividades Obligatorias ({self._actividadesObligatorias}/{limiteActividadesObligatorias})")
        return cumplidos

    def obtenerPendientes(self):
        pendientes = []
        if not self.verificarActividades():
            if self._usaDesglose:
                faltantes = []
                if self._talleres < limiteTalleres:
                    faltantes.append(f"Talleres {self._talleres}/{limiteTalleres}")
                if self._actividadesVfi < limiteVfi:
                    faltantes.append(f"VFI {self._actividadesVfi}/{limiteVfi}")
                if self._desarrolloPersonal < limiteDesarrolloPersonal:
                    faltantes.append(f"Des.Pers {self._desarrolloPersonal}/{limiteDesarrolloPersonal}")
                if self._integracion < limiteIntegracion:
                    faltantes.append(f"Integ {self._integracion}/{limiteIntegracion}")
                pendientes.append("Plan Formativo (" + ", ".join(faltantes) + ")")
            else:
                pendientes.append(f"Actividades ({self._actividades}/{limiteActividades})")
        if not self.verificarSeminario():
            pendientes.append("Seminario intermedio")
        if not self.verificarMentorias():
            pendientes.append(f"Mentorias ({self._mentorias}/{limiteMentorias})")
        if not self.verificarSituacionAcademica():
            pendientes.append(f"Materias Reprobadas ({self._materiasReprobadas})")
        if not self.verificarActividadesObligatorias():
            pendientes.append(f"Actividades Obligatorias ({self._actividadesObligatorias}/{limiteActividadesObligatorias})")
        return pendientes

    def verificarGraduacion(self):
        pendientes = self.obtenerPendientes()
        if len(pendientes) == 0:
            return "S"
        return pendientes

    def calcularPorcentajeAvance(self):
        cumplidos = len(self.obtenerCumplidos())
        return (cumplidos / 5.0) * 100.0

    def mostrarProgreso(self):
        return f"{self._nombre}|Area:{self.getAreaCompleta()}|Act:{self._actividades}/{limiteActividades}|Seminario:{self._seminario}|Ment:{self._mentorias}/{limiteMentorias}|Oblig:{self._actividadesObligatorias}/{limiteActividadesObligatorias}|Reprobadas:{self._materiasReprobadas}"

    def __str__(self):
        return f"{self._idAlumno}|{self._nombre}|{self._semestre}|{self._areaDeRe}|{self._gestionRe}|{self._materiasReprobadas}|{self._actividades}|{self._mentorias}|{self._actividadesObligatorias}|{self._seminario}"


class GestionRe(Alumno):
    def __init__(self, idAlumno, nombre, semestre, areaDeRe, gestion, materiasReprobadas, periodo, estatus, semestresComoAdmin=1, actividades=0, mentorias=0, actividadesObligatorias=0, requisitos=None, seminario=False, talleres=None, actividadesVfi=None, desarrolloPersonal=None, integracion=None, subgrupo=""):
        super().__init__(idAlumno, nombre, semestre, areaDeRe, gestion, materiasReprobadas, actividades, mentorias, actividadesObligatorias, seminario, talleres, actividadesVfi, desarrolloPersonal, integracion, subgrupo)
        periodoLimpio = validarPeriodoTexto(periodo)
        estatusLimpio = validarEstatusGestion(estatus)
        semAdminVal = validarEntero(semestresComoAdmin, "Semestres como administrador", 1, 2, SemestresAdminInvalidoError)

        requisitosValidados = []
        if requisitos is not None:
            if not isinstance(requisitos, list):
                raise TipoDatoInvalidoError("La lista de requisitos debe ser una coleccion de tipo list")
            for r in requisitos:
                if not isinstance(r, Requisito):
                    raise RequisitoInvalidoError("Todos los elementos de requisitos deben ser instancias de Requisito")
                for previo in requisitosValidados:
                    if previo.getNombreActividad().lower() == r.getNombreActividad().lower() and previo.getPeriodo().lower() == r.getPeriodo().lower():
                        raise RequisitoDuplicadoError(f"Requisito duplicado: {r.getNombreActividad()} ({r.getPeriodo()})")
                requisitosValidados.append(r)

        self._periodo = periodoLimpio
        self._estatus = estatusLimpio
        self._semestresComoAdmin = semAdminVal
        self._requisitos = requisitosValidados

    def getPeriodo(self):
        return self._periodo

    def getEstatus(self):
        return self._estatus

    def getSemestresComoAdmin(self):
        return self._semestresComoAdmin

    def getRequisitos(self):
        return self._requisitos

    def actualizarDatosGestion(self, periodo, estatus, semestresComoAdmin):
        self._periodo = validarPeriodoTexto(periodo)
        self._estatus = validarEstatusGestion(estatus)
        self._semestresComoAdmin = validarEntero(semestresComoAdmin, "Semestres como administrador", 1, 2, SemestresAdminInvalidoError)

    def buscarRequisito(self, nombreActividad, periodo=None):
        nombreLimpio = validarTextoBasico(nombreActividad, "Nombre de la actividad", 2, 100)
        for r in self._requisitos:
            coincideNombre = r.getNombreActividad().lower() == nombreLimpio.lower()
            coincidePeriodo = True if periodo is None else r.getPeriodo().lower() == str(periodo).strip().lower()
            if coincideNombre and coincidePeriodo:
                return r
        raise RequisitoNoEncontradoError(f"No se encontro el requisito '{nombreLimpio}'")

    def agregarRequisito(self, requisito):
        if requisito is None or not isinstance(requisito, Requisito):
            raise RequisitoInvalidoError("El objeto agregado debe ser una instancia de Requisito")
        for existente in self._requisitos:
            if existente.getNombreActividad().lower() == requisito.getNombreActividad().lower() and existente.getPeriodo().lower() == requisito.getPeriodo().lower():
                raise RequisitoDuplicadoError(f"El requisito '{requisito.getNombreActividad()}' en el periodo '{requisito.getPeriodo()}' ya existe")
        self._requisitos.append(requisito)

    def eliminarRequisito(self, nombreActividad, periodo=None):
        requisito = self.buscarRequisito(nombreActividad, periodo)
        self._requisitos.remove(requisito)
        return True

    def obtenerCumplidos(self):
        cumplidos = super().obtenerCumplidos()
        for r in self._requisitos:
            if r.verificarCumplimiento():
                cumplidos.append(f"Req: {r.getNombreActividad()} ({r.getPeriodo()})")
        return cumplidos

    def obtenerPendientes(self):
        pendientes = super().obtenerPendientes()
        for r in self._requisitos:
            if not r.verificarCumplimiento():
                pendientes.append(f"Req: {r.getNombreActividad()} ({r.getPeriodo()})")
        return pendientes

    def verificarGraduacion(self):
        pendientes = self.obtenerPendientes()
        if len(pendientes) == 0:
            return "S"
        return pendientes

    def calcularPorcentajeAvance(self):
        cumplidosBase = len(super().obtenerCumplidos())
        totalEvaluados = 5 + len(self._requisitos)
        cumplidosReq = 0
        for r in self._requisitos:
            if r.verificarCumplimiento():
                cumplidosReq += 1
        return ((cumplidosBase + cumplidosReq) / float(totalEvaluados)) * 100.0

    def mostrarProgreso(self):
        base = super().mostrarProgreso()
        return f"{base}|Periodo:{self._periodo}|Estatus:{self._estatus}|AdminSem:{self._semestresComoAdmin}|ReqEsp:{len(self._requisitos)}"

    def serializarRequisitos(self):
        if len(self._requisitos) == 0:
            return "SIN_REQUISITOS"
        partes = []
        for r in self._requisitos:
            if isinstance(r, RequisitoCantidad):
                partes.append(f"REQ_CANT~{r._nombreActividad}~{r._periodo}~{r._cantidadRequerida}~{r._cantidadRealizada}")
            elif isinstance(r, RequisitoEvento):
                partes.append(f"REQ_EVT~{r._nombreActividad}~{r._periodo}~{r._fechaEvento}~{r._completado}")
            elif isinstance(r, RequisitoAcademico):
                partes.append(f"REQ_ACAD~{r._nombreActividad}~{r._periodo}~{r._calificacionMinima}~{r._completado}")
            else:
                partes.append(f"REQ~{r._nombreActividad}~{r._periodo}~{r._completado}")
        return ";".join(partes)

    def __str__(self):
        return f"{super().__str__()}|{self._periodo}|{self._estatus}|SemestresAdmin:{self._semestresComoAdmin}|{self.serializarRequisitos()}"


class Requisito:
    def __init__(self, nombreActividad, periodo, completado=False):
        nombreLimpio = validarTextoBasico(nombreActividad, "Nombre de la actividad", 2, 100)
        periodoLimpio = validarPeriodoTexto(periodo)
        completadoVal = validarBooleano(completado, "Estado del requisito")
        self._nombreActividad = nombreLimpio
        self._periodo = periodoLimpio
        self._completado = completadoVal

    def getNombreActividad(self):
        return self._nombreActividad

    def getPeriodo(self):
        return self._periodo

    def getCompletado(self):
        return self._completado

    def verificarCumplimiento(self):
        return self._completado

    def obtenerEstado(self):
        if self.verificarCumplimiento():
            return "Completado"
        else:
            return "Pendiente"

    def registrarAvance(self, estado=True):
        self._completado = validarBooleano(estado, "Estado del requisito")

    def __str__(self):
        return f"{self._nombreActividad} ({self._periodo}) - {self.obtenerEstado()}"


class RequisitoCantidad(Requisito):
    def __init__(self, nombreActividad, periodo, cantidadRequerida, cantidadRealizada=0):
        super().__init__(nombreActividad, periodo)
        if cantidadRequerida is None or isinstance(cantidadRequerida, bool) or not isinstance(cantidadRequerida, int):
            raise TipoDatoInvalidoError("La cantidad requerida debe ser un numero entero")
        if cantidadRequerida <= 0 or cantidadRequerida > maxCantidadRequisito:
            raise CantidadRequeridaInvalidaError(f"La cantidad requerida debe estar entre 1 y {maxCantidadRequisito}")
        realizadaVal = validarEntero(cantidadRealizada, "Cantidad realizada", 0, maxCantidadRequisito)
        self._cantidadRequerida = cantidadRequerida
        self._cantidadRealizada = realizadaVal
        self._completado = self._cantidadRealizada >= self._cantidadRequerida

    def getCantidadRequerida(self):
        return self._cantidadRequerida

    def getCantidadRealizada(self):
        return self._cantidadRealizada

    def registrarAvance(self, cantidad):
        cantidadVal = validarEntero(cantidad, "Cantidad realizada", 0, maxCantidadRequisito)
        self._cantidadRealizada = cantidadVal
        self._completado = self._cantidadRealizada >= self._cantidadRequerida

    def verificarCumplimiento(self):
        return self._cantidadRealizada >= self._cantidadRequerida

    def obtenerEstado(self):
        if self.verificarCumplimiento():
            return "Completado"
        return "Pendiente"

    def __str__(self):
        return f"Cantidad: {self._nombreActividad} ({self._periodo}) | {self._cantidadRealizada}/{self._cantidadRequerida} | {self.obtenerEstado()}"


class RequisitoEvento(Requisito):
    def __init__(self, nombreActividad, periodo, fechaEvento="", completado=False):
        super().__init__(nombreActividad, periodo, completado)
        fechaLimpia = validarFechaTexto(fechaEvento)
        self._fechaEvento = fechaLimpia
        self._asistencia = self._completado

    def getFechaEvento(self):
        return self._fechaEvento

    def registrarAsistencia(self, asistio=True):
        val = validarBooleano(asistio, "Asistencia al evento")
        self._asistencia = val
        self._completado = val

    def registrarAvance(self, estado=True):
        self.registrarAsistencia(estado)

    def verificarCumplimiento(self):
        return self._completado

    def __str__(self):
        return f"Evento: {super().__str__()} | Fecha: {self._fechaEvento}"


class RequisitoAcademico(Requisito):
    def __init__(self, nombreActividad, periodo, calificacionMinima=70, materiasReprobadas=0, completado=False):
        super().__init__(nombreActividad, periodo, completado)
        califVal = validarFlotante(calificacionMinima, "Calificacion minima", 0.0, 100.0)
        repVal = validarEntero(materiasReprobadas, "Materias reprobadas del requisito", 0, maxReprobadas)
        self._calificacionMinima = califVal
        self._materiasReprobadas = repVal

    def getCalificacionMinima(self):
        return self._calificacionMinima

    def getMateriasReprobadas(self):
        return self._materiasReprobadas

    def actualizarMateriasReprobadas(self, cantidad):
        repVal = validarEntero(cantidad, "Materias reprobadas del requisito", 0, maxReprobadas)
        self._materiasReprobadas = repVal
        self._completado = repVal == 0

    def verificarCumplimiento(self):
        return self._completado and self._materiasReprobadas == 0

    def __str__(self):
        return f"Academico: {super().__str__()} | Minimo: {self._calificacionMinima} | Reprobadas: {self._materiasReprobadas}"


class GestorArchivos:
    def __init__(self, archivoAlumnos=archivoAlumnosDefault, archivoLog=archivoLogDefault):
        self._archivoAlumnos = archivoAlumnos
        self._archivoLog = archivoLog

    def registrarError(self, tipoError, mensaje):
        fechaHora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        linea = f"{fechaHora} | ERROR | {tipoError}: {mensaje}\n"
        try:
            with open(self._archivoLog, "a", encoding="utf-8") as archivo:
                archivo.write(linea)
        except PermissionError:
            print("No se tienen permisos para escribir en el archivo de log")
        except OSError:
            print("No se pudo escribir en el archivo de log")

    def guardarAlumnos(self, listaAlumnos, rutaDestino=None):
        ruta = self._archivoAlumnos if rutaDestino is None else rutaDestino
        try:
            with open(ruta, "w", encoding="utf-8") as archivo:
                for alumno in listaAlumnos:
                    archivo.write(str(alumno) + "\n")
        except PermissionError as e:
            self.registrarError("PermissionError", str(e))
            raise PermisoArchivoError("No se tienen permisos para guardar el archivo de alumnos")
        except OSError as e:
            self.registrarError("OSError", str(e))
            raise EscrituraArchivoError(f"Error al escribir el archivo de respaldo: {e}")

    def reconstruirRequisitos(self, textoRequisitos):
        listaReq = []
        if not textoRequisitos or textoRequisitos == "SIN_REQUISITOS":
            return listaReq
        for bloque in textoRequisitos.split(";"):
            bloqueLimpio = bloque.strip()
            if not bloqueLimpio:
                continue
            partes = bloqueLimpio.split("~")
            tipo = partes[0]
            if tipo == "REQ_CANT" and len(partes) >= 5:
                req = RequisitoCantidad(partes[1], partes[2], int(partes[3]), int(partes[4]))
                listaReq.append(req)
            elif tipo == "REQ_EVT" and len(partes) >= 5:
                req = RequisitoEvento(partes[1], partes[2], partes[3], partes[4] == "True")
                listaReq.append(req)
            elif tipo == "REQ_ACAD" and len(partes) >= 5:
                req = RequisitoAcademico(partes[1], partes[2], float(partes[3]), 0, partes[4] == "True")
                listaReq.append(req)
            elif tipo == "REQ" and len(partes) >= 4:
                req = Requisito(partes[1], partes[2], partes[3] == "True")
                listaReq.append(req)
            else:
                raise SerializacionRequisitoError(f"Formato invalido en requisito serializado: {bloqueLimpio}")
        return listaReq

    def cargarAlumnos(self):
        lista = []
        try:
            with open(self._archivoAlumnos, "r", encoding="utf-8") as archivo:
                for linea in archivo:
                    lineaLimpia = linea.strip()
                    if not lineaLimpia:
                        continue
                    try:
                        datos = lineaLimpia.split("|")
                        if len(datos) >= 13:
                            semestresAdmin = int(datos[12].split(":")[-1])
                            requisitosCargados = self.reconstruirRequisitos(datos[13]) if len(datos) >= 14 else []
                            alumno = GestionRe(
                                datos[0],
                                datos[1],
                                int(datos[2]),
                                datos[3],
                                datos[4],
                                int(datos[5]),
                                datos[10],
                                datos[11],
                                semestresAdmin,
                                int(datos[6]),
                                int(datos[7]),
                                int(datos[8]),
                                requisitos=requisitosCargados,
                                seminario=(datos[9] == "True")
                            )
                            lista.append(alumno)
                        elif len(datos) >= 10:
                            alumno = Alumno(
                                datos[0],
                                datos[1],
                                int(datos[2]),
                                datos[3],
                                datos[4],
                                int(datos[5]),
                                int(datos[6]),
                                int(datos[7]),
                                int(datos[8]),
                                datos[9] == "True"
                            )
                            lista.append(alumno)
                        elif len(datos) >= 9:
                            alumno = Alumno(
                                datos[0],
                                datos[1],
                                int(datos[2]),
                                datos[3],
                                datos[4],
                                int(datos[5]),
                                int(datos[6]),
                                int(datos[7]),
                                int(datos[8])
                            )
                            lista.append(alumno)
                        else:
                            raise FormatoArchivoCorruptoError(f"Linea incompleta en archivo de alumnos: {lineaLimpia}")
                    except (SistemaREError, ValueError, TypeError, IndexError) as errLinea:
                        self.registrarError(type(errLinea).__name__, f"Linea ignorada ({lineaLimpia}): {errLinea}")
        except FileNotFoundError as e:
            self.registrarError("FileNotFoundError", str(e))
            try:
                with open(self._archivoAlumnos, "w", encoding="utf-8") as archivo:
                    pass
            except OSError:
                pass
        except PermissionError as e:
            self.registrarError("PermissionError", str(e))
            print("No se tienen permisos para leer el archivo de alumnos")
        except OSError as e:
            self.registrarError("OSError", str(e))
            print("Error de lectura en el archivo de alumnos")
        return lista

    def __str__(self):
        return f"GestorArchivos(Alumnos: {self._archivoAlumnos}, Log: {self._archivoLog})"


class GestorBaseDatos:
    def __init__(self, archivoDb=archivoDbDefault):
        if archivoDb is None or not isinstance(archivoDb, str) or not archivoDb.strip():
            raise ConexionBaseDatosError("La ruta de la base de datos SQLite no puede estar vacia")
        self._archivoDb = archivoDb.strip()
        self.inicializarTablas()
        self.sincronizarAreas()
        self.asegurarCoordinadorDefault()

    def obtenerConexion(self):
        try:
            conn = sqlite3.connect(self._archivoDb)
            conn.execute("PRAGMA foreign_keys = ON")
            return conn
        except sqlite3.Error as e:
            raise ConexionBaseDatosError(f"No se pudo abrir la base de datos SQLite: {e}")

    def _crearTablaAlumnosActualizada(self, cursor):
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS alumnos (
                id_alumno TEXT PRIMARY KEY,
                nombre TEXT NOT NULL,
                semestre INTEGER NOT NULL CHECK(semestre >= 1 AND semestre <= 13),
                area_de_re TEXT NOT NULL,
                subgrupo TEXT NOT NULL DEFAULT '',
                gestion_re TEXT NOT NULL,
                materias_reprobadas INTEGER NOT NULL DEFAULT 0 CHECK(materias_reprobadas >= 0),
                actividades INTEGER NOT NULL DEFAULT 0 CHECK(actividades >= 0),
                talleres INTEGER NOT NULL DEFAULT 0 CHECK(talleres >= 0),
                actividades_vfi INTEGER NOT NULL DEFAULT 0 CHECK(actividades_vfi >= 0),
                desarrollo_personal INTEGER NOT NULL DEFAULT 0 CHECK(desarrollo_personal >= 0),
                integracion INTEGER NOT NULL DEFAULT 0 CHECK(integracion >= 0),
                usa_desglose INTEGER NOT NULL DEFAULT 0 CHECK(usa_desglose IN (0, 1)),
                mentorias INTEGER NOT NULL DEFAULT 0 CHECK(mentorias >= 0),
                actividades_obligatorias INTEGER NOT NULL DEFAULT 0 CHECK(actividades_obligatorias >= 0),
                seminario INTEGER NOT NULL DEFAULT 0 CHECK(seminario IN (0, 1)),
                es_gestion_re INTEGER NOT NULL DEFAULT 0 CHECK(es_gestion_re IN (0, 1)),
                periodo TEXT,
                estatus TEXT,
                semestres_como_admin INTEGER,
                fecha_registro TEXT NOT NULL,
                ultima_actualizacion TEXT NOT NULL
            )
            """
        )

    def _crearTablaRequisitosActualizada(self, cursor):
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS requisitos (
                id_requisito INTEGER PRIMARY KEY AUTOINCREMENT,
                id_alumno TEXT NOT NULL,
                tipo_requisito TEXT NOT NULL,
                nombre_actividad TEXT NOT NULL,
                periodo TEXT NOT NULL,
                completado INTEGER NOT NULL DEFAULT 0 CHECK(completado IN (0, 1)),
                cantidad_requerida INTEGER,
                cantidad_realizada INTEGER,
                fecha_evento TEXT,
                calificacion_minima REAL,
                materias_reprobadas INTEGER DEFAULT 0,
                FOREIGN KEY (id_alumno) REFERENCES alumnos(id_alumno) ON DELETE CASCADE,
                UNIQUE (id_alumno, nombre_actividad, periodo)
            )
            """
        )

    def _migrarEsquemaAlumnosSiNecesario(self, conn, cursor):
        cursor.execute("SELECT sql FROM sqlite_master WHERE type='table' AND name='alumnos'")
        filaSql = cursor.fetchone()
        if filaSql is None:
            return
        cursor.execute("PRAGMA table_info(alumnos)")
        columnas = cursor.fetchall()
        nombresCol = []
        for c in columnas:
            nombresCol.append(c[1])
        necesitaMigracion = ("subgrupo" not in nombresCol) or ("semestre <= 16" in filaSql[0])
        if not necesitaMigracion:
            return

        cursor.execute("PRAGMA foreign_keys = OFF")
        cursor.execute("SELECT * FROM alumnos")
        alumnosPrevios = cursor.fetchall()
        cursor.execute("SELECT id_alumno, tipo_requisito, nombre_actividad, periodo, completado, cantidad_requerida, cantidad_realizada, fecha_evento, calificacion_minima, materias_reprobadas FROM requisitos")
        reqsPrevios = cursor.fetchall()

        cursor.execute("DROP TABLE IF EXISTS requisitos")
        cursor.execute("DROP TABLE IF EXISTS alumnos")
        self._crearTablaAlumnosActualizada(cursor)
        self._crearTablaRequisitosActualizada(cursor)

        idsValidos = []
        idxSub = nombresCol.index("subgrupo") if "subgrupo" in nombresCol else -1
        for row in alumnosPrevios:
            semVal = int(row[2])
            if semVal < 1 or semVal > maxSemestre:
                continue
            subVal = row[idxSub] if idxSub != -1 else ""
            if idxSub == -1:
                cursor.execute(
                    """
                    INSERT INTO alumnos (
                        id_alumno, nombre, semestre, area_de_re, subgrupo, gestion_re,
                        materias_reprobadas, actividades, talleres, actividades_vfi,
                        desarrollo_personal, integracion, usa_desglose, mentorias,
                        actividades_obligatorias, seminario, es_gestion_re,
                        periodo, estatus, semestres_como_admin, fecha_registro, ultima_actualizacion
                    )
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        row[0], row[1], row[2], row[3], "", row[4],
                        row[5], row[6], row[7], row[8],
                        row[9], row[10], row[11], row[12],
                        row[13], row[14], row[15],
                        row[16], row[17], row[18], row[19], row[20]
                    )
                )
            else:
                cursor.execute(
                    """
                    INSERT INTO alumnos VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    row
                )
            idsValidos.append(row[0])

        for rq in reqsPrevios:
            if rq[0] in idsValidos:
                cursor.execute(
                    """
                    INSERT INTO requisitos (
                        id_alumno, tipo_requisito, nombre_actividad, periodo, completado,
                        cantidad_requerida, cantidad_realizada, fecha_evento, calificacion_minima, materias_reprobadas
                    )
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    rq
                )
        cursor.execute("PRAGMA foreign_keys = ON")

    def inicializarTablas(self):
        conn = None
        try:
            conn = self.obtenerConexion()
            cursor = conn.cursor()
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS areas_re (
                    id_area INTEGER PRIMARY KEY,
                    nombre_area TEXT UNIQUE NOT NULL,
                    tipo_grupo TEXT NOT NULL,
                    subtipo_clase TEXT NOT NULL,
                    detalle TEXT NOT NULL DEFAULT ''
                )
                """
            )
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS coordinadores (
                    id_nombre TEXT PRIMARY KEY,
                    contrasena TEXT NOT NULL,
                    nombre TEXT NOT NULL,
                    area TEXT NOT NULL,
                    anio_administracion INTEGER NOT NULL,
                    activo INTEGER NOT NULL DEFAULT 1
                )
                """
            )
            self._crearTablaAlumnosActualizada(cursor)
            self._crearTablaRequisitosActualizada(cursor)
            self._migrarEsquemaAlumnosSiNecesario(conn, cursor)
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS logs_errores (
                    id_log INTEGER PRIMARY KEY AUTOINCREMENT,
                    fecha_hora TEXT NOT NULL,
                    tipo_error TEXT NOT NULL,
                    mensaje TEXT NOT NULL,
                    origen TEXT NOT NULL DEFAULT 'Sistema'
                )
                """
            )
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS historial_acciones (
                    id_accion INTEGER PRIMARY KEY AUTOINCREMENT,
                    fecha_hora TEXT NOT NULL,
                    coordinador_id TEXT NOT NULL,
                    accion TEXT NOT NULL,
                    id_alumno TEXT,
                    detalle TEXT NOT NULL
                )
                """
            )
            conn.commit()
        except sqlite3.Error as e:
            if conn is not None:
                conn.rollback()
            raise TablaBaseDatosError(f"Error al crear las tablas en SQLite: {e}")
        finally:
            if conn is not None:
                conn.close()

    def sincronizarAreas(self):
        conn = None
        try:
            conn = self.obtenerConexion()
            cursor = conn.cursor()
            todasAreas = []
            for idArea, areaObj in gruposDisponibles.items():
                todasAreas.append((idArea, areaObj))
            for asocObj in asociacionesEstadoDisponibles.values():
                todasAreas.append((asocObj.getIdArea(), asocObj))
            for clubObj in clubsDisponibles.values():
                todasAreas.append((clubObj.getIdArea(), clubObj))

            for idArea, areaObj in todasAreas:
                detalle = ""
                if isinstance(areaObj, SociedadesDeAlumnos):
                    detalle = areaObj.getDetalle()
                elif isinstance(areaObj, AsociacionesPorEstado):
                    detalle = areaObj.getDetalle()
                elif isinstance(areaObj, ClubsAnahuac):
                    detalle = areaObj.getDetalle()
                cursor.execute(
                    """
                    INSERT OR REPLACE INTO areas_re (id_area, nombre_area, tipo_grupo, subtipo_clase, detalle)
                    VALUES (?, ?, ?, ?, ?)
                    """,
                    (idArea, areaObj.getNombreArea(), areaObj.obtenerTipoGrupo(), type(areaObj).__name__, detalle)
                )
            conn.commit()
        except sqlite3.Error as e:
            if conn is not None:
                conn.rollback()
            raise ConsultaBaseDatosError(f"Error al sincronizar areas en SQLite: {e}")
        finally:
            if conn is not None:
                conn.close()

    def asegurarCoordinadorDefault(self):
        conn = None
        try:
            conn = self.obtenerConexion()
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM coordinadores")
            total = cursor.fetchone()[0]
            if total == 0:
                cursor.execute(
                    """
                    INSERT INTO coordinadores (id_nombre, contrasena, nombre, area, anio_administracion, activo)
                    VALUES (?, ?, ?, ?, ?, 1)
                    """,
                    ("C001", "1234", "Coordinacion RE", "General", 2026)
                )
                conn.commit()
        except sqlite3.Error as e:
            if conn is not None:
                conn.rollback()
            raise ConsultaBaseDatosError(f"Error al verificar coordinador inicial en SQLite: {e}")
        finally:
            if conn is not None:
                conn.close()

    def cargarCoordinadores(self):
        conn = None
        lista = []
        try:
            conn = self.obtenerConexion()
            cursor = conn.cursor()
            cursor.execute("SELECT id_nombre, contrasena, nombre, area, anio_administracion FROM coordinadores ORDER BY id_nombre")
            filas = cursor.fetchall()
            for fila in filas:
                coord = Coordinador(fila[0], fila[1], fila[2], [], fila[3], fila[4])
                lista.append(coord)
            return lista
        except sqlite3.Error as e:
            raise ConsultaBaseDatosError(f"Error al consultar coordinadores en SQLite: {e}")
        finally:
            if conn is not None:
                conn.close()

    def guardarCoordinador(self, coordinador):
        if coordinador is None or not isinstance(coordinador, Coordinador):
            raise CoordinadorInvalidoError("El objeto coordinador no es valido")
        conn = None
        try:
            conn = self.obtenerConexion()
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO coordinadores (id_nombre, contrasena, nombre, area, anio_administracion, activo)
                VALUES (?, ?, ?, ?, ?, 1)
                """,
                (
                    coordinador.getIdNombre(),
                    coordinador.getContrasena(),
                    coordinador.getNombre(),
                    coordinador.getArea(),
                    coordinador.getAnioAdministracion()
                )
            )
            conn.commit()
        except sqlite3.IntegrityError:
            if conn is not None:
                conn.rollback()
            raise CoordinadorDuplicadoError(f"Ya existe un coordinador con el ID {coordinador.getIdNombre()}")
        except sqlite3.Error as e:
            if conn is not None:
                conn.rollback()
            raise ConsultaBaseDatosError(f"Error al guardar coordinador en SQLite: {e}")
        finally:
            if conn is not None:
                conn.close()

    def autenticarCoordinador(self, idNombre, contrasena, catalogoAlumnos):
        idLimpio = validarIdTexto(idNombre, "ID del coordinador", 2, 30)
        if contrasena is None or not isinstance(contrasena, str) or not contrasena.strip():
            raise CampoVacioError("Debe ingresar la contraseña del coordinador")
        conn = None
        try:
            conn = self.obtenerConexion()
            cursor = conn.cursor()
            cursor.execute(
                "SELECT id_nombre, contrasena, nombre, area, anio_administracion FROM coordinadores WHERE id_nombre = ?",
                (idLimpio,)
            )
            fila = cursor.fetchone()
            if fila is None:
                raise CoordinadorNoEncontradoError(f"No existe ningun coordinador registrado con el ID '{idLimpio}'. Acceso denegado.")
            if fila[1] != contrasena.strip():
                raise AutenticacionError("La contraseña del coordinador es incorrecta. Acceso denegado.")
            return Coordinador(fila[0], fila[1], fila[2], catalogoAlumnos, fila[3], fila[4], self)
        except sqlite3.Error as e:
            raise ConsultaBaseDatosError(f"Error al autenticar coordinador en SQLite: {e}")
        finally:
            if conn is not None:
                conn.close()

    def eliminarCoordinador(self, idNombre, idActivo=None):
        idLimpio = validarIdTexto(idNombre, "ID del coordinador", 2, 30)
        if idActivo is not None and idLimpio == idActivo:
            raise CoordinadorActivoError("No puedes eliminar al coordinador que esta actualmente en sesion")
        conn = None
        try:
            conn = self.obtenerConexion()
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM coordinadores")
            total = cursor.fetchone()[0]
            if total <= 1:
                raise OperacionNoPermitidaError("Debe existir al menos un coordinador en el sistema")
            cursor.execute("DELETE FROM coordinadores WHERE id_nombre = ?", (idLimpio,))
            if cursor.rowcount == 0:
                raise CoordinadorNoEncontradoError(f"No existe el coordinador {idLimpio} en SQLite")
            conn.commit()
            return True
        except (CoordinadorNoEncontradoError, OperacionNoPermitidaError):
            if conn is not None:
                conn.rollback()
            raise
        except sqlite3.Error as e:
            if conn is not None:
                conn.rollback()
            raise ConsultaBaseDatosError(f"Error al eliminar coordinador en SQLite: {e}")
        finally:
            if conn is not None:
                conn.close()

    def _insertarRequisitoEnCursor(self, cursor, idAlumno, req):
        if isinstance(req, RequisitoCantidad):
            cursor.execute(
                """
                INSERT INTO requisitos (
                    id_alumno, tipo_requisito, nombre_actividad, periodo, completado,
                    cantidad_requerida, cantidad_realizada, fecha_evento, calificacion_minima, materias_reprobadas
                )
                VALUES (?, 'REQ_CANT', ?, ?, ?, ?, ?, NULL, NULL, 0)
                """,
                (
                    idAlumno,
                    req.getNombreActividad(),
                    req.getPeriodo(),
                    1 if req.verificarCumplimiento() else 0,
                    req.getCantidadRequerida(),
                    req.getCantidadRealizada()
                )
            )
        elif isinstance(req, RequisitoEvento):
            cursor.execute(
                """
                INSERT INTO requisitos (
                    id_alumno, tipo_requisito, nombre_actividad, periodo, completado,
                    cantidad_requerida, cantidad_realizada, fecha_evento, calificacion_minima, materias_reprobadas
                )
                VALUES (?, 'REQ_EVT', ?, ?, ?, NULL, NULL, ?, NULL, 0)
                """,
                (
                    idAlumno,
                    req.getNombreActividad(),
                    req.getPeriodo(),
                    1 if req.verificarCumplimiento() else 0,
                    req.getFechaEvento()
                )
            )
        elif isinstance(req, RequisitoAcademico):
            cursor.execute(
                """
                INSERT INTO requisitos (
                    id_alumno, tipo_requisito, nombre_actividad, periodo, completado,
                    cantidad_requerida, cantidad_realizada, fecha_evento, calificacion_minima, materias_reprobadas
                )
                VALUES (?, 'REQ_ACAD', ?, ?, ?, NULL, NULL, NULL, ?, ?)
                """,
                (
                    idAlumno,
                    req.getNombreActividad(),
                    req.getPeriodo(),
                    1 if req.getCompletado() else 0,
                    req.getCalificacionMinima(),
                    req.getMateriasReprobadas()
                )
            )
        else:
            cursor.execute(
                """
                INSERT INTO requisitos (
                    id_alumno, tipo_requisito, nombre_actividad, periodo, completado,
                    cantidad_requerida, cantidad_realizada, fecha_evento, calificacion_minima, materias_reprobadas
                )
                VALUES (?, 'REQ', ?, ?, ?, NULL, NULL, NULL, NULL, 0)
                """,
                (
                    idAlumno,
                    req.getNombreActividad(),
                    req.getPeriodo(),
                    1 if req.verificarCumplimiento() else 0
                )
            )

    def guardarAlumno(self, alumno):
        if alumno is None or not isinstance(alumno, Alumno):
            raise AlumnoNuloError("No se puede guardar un alumno nulo o invalido")
        conn = None
        ahora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        esGestion = 1 if isinstance(alumno, GestionRe) else 0
        periodoVal = alumno.getPeriodo() if esGestion == 1 else None
        estatusVal = alumno.getEstatus() if esGestion == 1 else None
        semAdminVal = alumno.getSemestresComoAdmin() if esGestion == 1 else None
        try:
            conn = self.obtenerConexion()
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO alumnos (
                    id_alumno, nombre, semestre, area_de_re, subgrupo, gestion_re,
                    materias_reprobadas, actividades, talleres, actividades_vfi,
                    desarrollo_personal, integracion, usa_desglose, mentorias,
                    actividades_obligatorias, seminario, es_gestion_re,
                    periodo, estatus, semestres_como_admin, fecha_registro, ultima_actualizacion
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    alumno.getId(),
                    alumno.getNombre(),
                    alumno.getSemestre(),
                    alumno.getArea(),
                    alumno.getSubgrupo(),
                    alumno.getGestionRe(),
                    alumno.getMateriasReprobadas(),
                    alumno.getActividades(),
                    alumno.getTalleres(),
                    alumno.getActividadesVfi(),
                    alumno.getDesarrolloPersonal(),
                    alumno.getIntegracion(),
                    1 if alumno.getUsaDesglose() else 0,
                    alumno.getMentorias(),
                    alumno.getActividadesObligatorias(),
                    1 if alumno.getSeminario() else 0,
                    esGestion,
                    periodoVal,
                    estatusVal,
                    semAdminVal,
                    ahora,
                    ahora
                )
            )
            if esGestion == 1:
                for req in alumno.getRequisitos():
                    self._insertarRequisitoEnCursor(cursor, alumno.getId(), req)
            conn.commit()
        except sqlite3.IntegrityError:
            if conn is not None:
                conn.rollback()
            raise AlumnoDuplicadoError(f"Ya existe en la base de datos un alumno con el ID {alumno.getId()}")
        except sqlite3.OperationalError as e:
            if conn is not None:
                conn.rollback()
            raise ConsultaBaseDatosError(f"Error de operacion SQLite al guardar alumno: {e}")
        except sqlite3.Error as e:
            if conn is not None:
                conn.rollback()
            raise BaseDatosError(f"Error SQLite al guardar alumno: {e}")
        finally:
            if conn is not None:
                conn.close()

    def actualizarAlumno(self, alumno):
        if alumno is None or not isinstance(alumno, Alumno):
            raise AlumnoNuloError("No se puede actualizar un alumno nulo o invalido")
        conn = None
        ahora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        esGestion = 1 if isinstance(alumno, GestionRe) else 0
        periodoVal = alumno.getPeriodo() if esGestion == 1 else None
        estatusVal = alumno.getEstatus() if esGestion == 1 else None
        semAdminVal = alumno.getSemestresComoAdmin() if esGestion == 1 else None
        try:
            conn = self.obtenerConexion()
            cursor = conn.cursor()
            cursor.execute(
                """
                UPDATE alumnos
                SET nombre = ?, semestre = ?, area_de_re = ?, subgrupo = ?, gestion_re = ?,
                    materias_reprobadas = ?, actividades = ?, talleres = ?, actividades_vfi = ?,
                    desarrollo_personal = ?, integracion = ?, usa_desglose = ?, mentorias = ?,
                    actividades_obligatorias = ?, seminario = ?, es_gestion_re = ?,
                    periodo = ?, estatus = ?, semestres_como_admin = ?, ultima_actualizacion = ?
                WHERE id_alumno = ?
                """,
                (
                    alumno.getNombre(),
                    alumno.getSemestre(),
                    alumno.getArea(),
                    alumno.getSubgrupo(),
                    alumno.getGestionRe(),
                    alumno.getMateriasReprobadas(),
                    alumno.getActividades(),
                    alumno.getTalleres(),
                    alumno.getActividadesVfi(),
                    alumno.getDesarrolloPersonal(),
                    alumno.getIntegracion(),
                    1 if alumno.getUsaDesglose() else 0,
                    alumno.getMentorias(),
                    alumno.getActividadesObligatorias(),
                    1 if alumno.getSeminario() else 0,
                    esGestion,
                    periodoVal,
                    estatusVal,
                    semAdminVal,
                    ahora,
                    alumno.getId()
                )
            )
            if cursor.rowcount == 0:
                raise AlumnoNoEncontradoError(f"No se encontro al alumno con ID {alumno.getId()} en SQLite")
            cursor.execute("DELETE FROM requisitos WHERE id_alumno = ?", (alumno.getId(),))
            if esGestion == 1:
                for req in alumno.getRequisitos():
                    self._insertarRequisitoEnCursor(cursor, alumno.getId(), req)
            conn.commit()
        except AlumnoNoEncontradoError:
            if conn is not None:
                conn.rollback()
            raise
        except sqlite3.IntegrityError as e:
            if conn is not None:
                conn.rollback()
            raise IntegridadBaseDatosError(f"Error de integridad al actualizar alumno: {e}")
        except sqlite3.Error as e:
            if conn is not None:
                conn.rollback()
            raise ConsultaBaseDatosError(f"Error SQLite al actualizar alumno: {e}")
        finally:
            if conn is not None:
                conn.close()

    def eliminarAlumno(self, idAlumno):
        idLimpio = validarIdTexto(idAlumno, "ID del alumno")
        conn = None
        try:
            conn = self.obtenerConexion()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM alumnos WHERE id_alumno = ?", (idLimpio,))
            if cursor.rowcount == 0:
                raise AlumnoNoEncontradoError(f"No existe el alumno con ID {idLimpio} en SQLite")
            conn.commit()
            return True
        except AlumnoNoEncontradoError:
            if conn is not None:
                conn.rollback()
            raise
        except sqlite3.Error as e:
            if conn is not None:
                conn.rollback()
            raise ConsultaBaseDatosError(f"Error SQLite al eliminar alumno: {e}")
        finally:
            if conn is not None:
                conn.close()

    def cargarRequisitosAlumno(self, idAlumno, connExistente=None):
        idLimpio = validarIdTexto(idAlumno, "ID del alumno")
        conn = connExistente
        cerrarAlFinal = False
        lista = []
        try:
            if conn is None:
                conn = self.obtenerConexion()
                cerrarAlFinal = True
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT tipo_requisito, nombre_actividad, periodo, completado,
                       cantidad_requerida, cantidad_realizada, fecha_evento,
                       calificacion_minima, materias_reprobadas
                FROM requisitos
                WHERE id_alumno = ?
                ORDER BY id_requisito
                """,
                (idLimpio,)
            )
            filas = cursor.fetchall()
            for fila in filas:
                tipo = fila[0]
                nombreAct = fila[1]
                periodo = fila[2]
                completado = fila[3] == 1
                if tipo == "REQ_CANT":
                    req = RequisitoCantidad(nombreAct, periodo, int(fila[4]), int(fila[5]))
                    lista.append(req)
                elif tipo == "REQ_EVT":
                    req = RequisitoEvento(nombreAct, periodo, fila[6], completado)
                    lista.append(req)
                elif tipo == "REQ_ACAD":
                    rep = 0 if fila[8] is None else int(fila[8])
                    req = RequisitoAcademico(nombreAct, periodo, float(fila[7]), rep, completado)
                    lista.append(req)
                else:
                    req = Requisito(nombreAct, periodo, completado)
                    lista.append(req)
            return lista
        except sqlite3.Error as e:
            raise ConsultaBaseDatosError(f"Error al cargar requisitos de {idLimpio}: {e}")
        finally:
            if cerrarAlFinal and conn is not None:
                conn.close()

    def _construirAlumnoDesdeFila(self, fila, conn):
        usaDesglose = fila[12] == 1
        talleres = fila[8] if usaDesglose else None
        vfi = fila[9] if usaDesglose else None
        desarrollo = fila[10] if usaDesglose else None
        integracion = fila[11] if usaDesglose else None
        esGestion = fila[16] == 1
        if esGestion:
            reqs = self.cargarRequisitosAlumno(fila[0], conn)
            return GestionRe(
                fila[0],
                fila[1],
                int(fila[2]),
                fila[3],
                fila[5],
                int(fila[6]),
                fila[17],
                fila[18],
                int(fila[19]),
                int(fila[7]),
                int(fila[13]),
                int(fila[14]),
                requisitos=reqs,
                seminario=(fila[15] == 1),
                talleres=talleres,
                actividadesVfi=vfi,
                desarrolloPersonal=desarrollo,
                integracion=integracion,
                subgrupo=fila[4]
            )
        return Alumno(
            fila[0],
            fila[1],
            int(fila[2]),
            fila[3],
            fila[5],
            int(fila[6]),
            int(fila[7]),
            int(fila[13]),
            int(fila[14]),
            fila[15] == 1,
            talleres=talleres,
            actividadesVfi=vfi,
            desarrolloPersonal=desarrollo,
            integracion=integracion,
            subgrupo=fila[4]
        )

    def cargarAlumnos(self):
        conn = None
        lista = []
        try:
            conn = self.obtenerConexion()
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT id_alumno, nombre, semestre, area_de_re, subgrupo, gestion_re,
                       materias_reprobadas, actividades, talleres, actividades_vfi,
                       desarrollo_personal, integracion, usa_desglose, mentorias,
                       actividades_obligatorias, seminario, es_gestion_re,
                       periodo, estatus, semestres_como_admin
                FROM alumnos
                ORDER BY id_alumno
                """
            )
            filas = cursor.fetchall()
            for fila in filas:
                try:
                    alumno = self._construirAlumnoDesdeFila(fila, conn)
                    lista.append(alumno)
                except (SistemaREError, ValueError, TypeError) as errRegistro:
                    self.registrarError(type(errRegistro).__name__, f"Registro corrupto en BD ({fila[0]}): {errRegistro}", "SQLite")
            return lista
        except sqlite3.Error as e:
            raise ConsultaBaseDatosError(f"Error al cargar alumnos desde SQLite: {e}")
        finally:
            if conn is not None:
                conn.close()

    def buscarAlumnoPorId(self, idAlumno):
        idLimpio = validarIdTexto(idAlumno, "ID del alumno")
        conn = None
        try:
            conn = self.obtenerConexion()
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT id_alumno, nombre, semestre, area_de_re, subgrupo, gestion_re,
                       materias_reprobadas, actividades, talleres, actividades_vfi,
                       desarrollo_personal, integracion, usa_desglose, mentorias,
                       actividades_obligatorias, seminario, es_gestion_re,
                       periodo, estatus, semestres_como_admin
                FROM alumnos
                WHERE id_alumno = ?
                """,
                (idLimpio,)
            )
            fila = cursor.fetchone()
            if fila is None:
                raise AlumnoNoEncontradoError(f"Alumno {idLimpio} no encontrado en SQLite")
            return self._construirAlumnoDesdeFila(fila, conn)
        except sqlite3.Error as e:
            raise ConsultaBaseDatosError(f"Error al buscar alumno en SQLite: {e}")
        finally:
            if conn is not None:
                conn.close()

    def migrarDesdeTxt(self, gestorArchivos):
        conn = None
        try:
            conn = self.obtenerConexion()
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM alumnos")
            total = cursor.fetchone()[0]
        except sqlite3.Error as e:
            raise MigracionDatosError(f"Error al verificar migracion inicial: {e}")
        finally:
            if conn is not None:
                conn.close()

        if total > 0:
            return 0
        if not Path(gestorArchivos._archivoAlumnos).exists():
            return 0

        alumnosTxt = gestorArchivos.cargarAlumnos()
        migrados = 0
        for alumno in alumnosTxt:
            try:
                self.guardarAlumno(alumno)
                self.registrarHistorial("SISTEMA", "MIGRACION_TXT", alumno.getId(), f"Migrado desde alumnos.txt ({alumno.getNombre()})")
                migrados += 1
            except SistemaREError as e:
                self.registrarError(type(e).__name__, f"No se pudo migrar alumno {alumno.getId()}: {e}", "Migracion")
        return migrados

    def registrarError(self, tipoError, mensaje, origen="Sistema"):
        conn = None
        fechaHora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        try:
            conn = self.obtenerConexion()
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO logs_errores (fecha_hora, tipo_error, mensaje, origen)
                VALUES (?, ?, ?, ?)
                """,
                (fechaHora, str(tipoError), str(mensaje), str(origen))
            )
            conn.commit()
        except sqlite3.Error:
            if conn is not None:
                conn.rollback()
        finally:
            if conn is not None:
                conn.close()

    def obtenerErrores(self, limite=100):
        conn = None
        try:
            conn = self.obtenerConexion()
            cursor = conn.cursor()
            cursor.execute(
                "SELECT id_log, fecha_hora, tipo_error, mensaje, origen FROM logs_errores ORDER BY id_log DESC LIMIT ?",
                (limite,)
            )
            return cursor.fetchall()
        except sqlite3.Error as e:
            raise ConsultaBaseDatosError(f"Error al consultar bitacora de errores en SQLite: {e}")
        finally:
            if conn is not None:
                conn.close()

    def registrarHistorial(self, coordinadorId, accion, idAlumno, detalle):
        conn = None
        fechaHora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        try:
            conn = self.obtenerConexion()
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO historial_acciones (fecha_hora, coordinador_id, accion, id_alumno, detalle)
                VALUES (?, ?, ?, ?, ?)
                """,
                (fechaHora, str(coordinadorId), str(accion), "" if idAlumno is None else str(idAlumno), str(detalle))
            )
            conn.commit()
        except sqlite3.Error as e:
            if conn is not None:
                conn.rollback()
            raise ConsultaBaseDatosError(f"Error al registrar historial en SQLite: {e}")
        finally:
            if conn is not None:
                conn.close()

    def obtenerHistorial(self, limite=100):
        conn = None
        try:
            conn = self.obtenerConexion()
            cursor = conn.cursor()
            cursor.execute(
                "SELECT id_accion, fecha_hora, coordinador_id, accion, id_alumno, detalle FROM historial_acciones ORDER BY id_accion DESC LIMIT ?",
                (limite,)
            )
            return cursor.fetchall()
        except sqlite3.Error as e:
            raise ConsultaBaseDatosError(f"Error al consultar historial en SQLite: {e}")
        finally:
            if conn is not None:
                conn.close()

    def __str__(self):
        return f"GestorBaseDatos(SQLite: {self._archivoDb})"


gestorGlobal = GestorArchivos()
gestorBdGlobal = GestorBaseDatos()


def enviarError(error, origen="Sistema"):
    tipo = type(error).__name__
    mensaje = str(error)
    gestorGlobal.registrarError(tipo, mensaje)
    gestorBdGlobal.registrarError(tipo, mensaje, origen)


def inicializarCoordinadorSistema():
    gestorBdGlobal.migrarDesdeTxt(gestorGlobal)
    alumnosIniciales = gestorBdGlobal.cargarAlumnos()
    coordinadores = gestorBdGlobal.cargarCoordinadores()
    if len(coordinadores) > 0:
        primero = coordinadores[0]
        return Coordinador(
            primero.getIdNombre(),
            primero.getContrasena(),
            primero.getNombre(),
            alumnosIniciales,
            primero.getArea(),
            primero.getAnioAdministracion(),
            gestorBdGlobal
        )
    return Coordinador("C001", "1234", "Coordinacion RE", alumnosIniciales, "General", 2026, gestorBdGlobal)


coordinadorActual = inicializarCoordinadorSistema()


def cargarLogoEnVentana(ventanaPadre, ancho=220, alto=75):
    rutaLogo = carpetaBase / "logo.png"
    try:
        if not rutaLogo.exists():
            raise RecursoImagenError("No se encontro el archivo logo.png en la carpeta del proyecto")
        imagen = Image.open(rutaLogo)
        imagen = imagen.resize((ancho, alto))
        imagenTk = ImageTk.PhotoImage(imagen)
        etiquetaLogo = tk.Label(ventanaPadre, image=imagenTk, bg="beige")
        etiquetaLogo.image = imagenTk
        etiquetaLogo.pack(pady=4)
    except (RecursoImagenError, FileNotFoundError, OSError, Exception) as error:
        enviarError(error, "Interfaz")
        etiquetaLogo = tk.Label(
            ventanaPadre,
            text="Sistema de Seguimiento - Relaciones Estudiantiles",
            bg="#117A76",
            fg="white",
            font=("Helvetica", 13, "bold"),
            pady=8
        )
        etiquetaLogo.pack(fill="x", padx=20, pady=6)


def mostrarVentanaLogin():
    resultado = {"coordinador": None}
    ventanaLogin = tk.Tk()
    ventanaLogin.title("Acceso Coordinador - Relaciones Estudiantiles")
    ventanaLogin.geometry("480x400")
    ventanaLogin.resizable(False, False)
    ventanaLogin.configure(bg="beige")

    cargarLogoEnVentana(ventanaLogin, 200, 65)

    tk.Label(
        ventanaLogin,
        text="Portal Exclusivo de Administracion (Coordinador)",
        bg="#E8F6F3",
        fg="#0E5A56",
        font=("Helvetica", 10, "bold"),
        pady=5
    ).pack(fill="x", padx=20, pady=4)

    frameCard = tk.LabelFrame(
        ventanaLogin,
        text="Inicio de Sesion",
        bg="beige",
        fg="#117A76",
        font=("Helvetica", 10, "bold"),
        padx=18,
        pady=14
    )
    frameCard.pack(fill="both", expand=True, padx=24, pady=8)

    tk.Label(frameCard, text="ID Coordinador:", bg="beige", fg="#1B2631", font=("Helvetica", 10, "bold")).grid(row=0, column=0, sticky="w", pady=8)
    entryId = tk.Entry(frameCard, font=("Helvetica", 11), width=24)
    entryId.grid(row=0, column=1, pady=8, padx=8)
    entryId.focus_set()

    tk.Label(frameCard, text="Contraseña:", bg="beige", fg="#1B2631", font=("Helvetica", 10, "bold")).grid(row=1, column=0, sticky="w", pady=8)
    entryPass = tk.Entry(frameCard, font=("Helvetica", 11), width=24, show="*")
    entryPass.grid(row=1, column=1, pady=8, padx=8)

    estadoPass = {"visible": False}

    def alternarVisibilidadPass():
        if estadoPass["visible"]:
            entryPass.config(show="*")
            btnVerPass.config(text="Mostrar")
            estadoPass["visible"] = False
        else:
            entryPass.config(show="")
            btnVerPass.config(text="Ocultar")
            estadoPass["visible"] = True

    btnVerPass = tk.Button(frameCard, text="Mostrar", command=alternarVisibilidadPass, bg="#D5DBDB", fg="#1B2631", font=("Arial", 8, "bold"), width=8)
    btnVerPass.grid(row=1, column=2, padx=4)

    lblEstado = tk.Label(frameCard, text="Ingresa tu ID y contraseña registrados en SQLite", bg="beige", fg="#566573", font=("Helvetica", 9))
    lblEstado.grid(row=2, column=0, columnspan=3, pady=8)

    def intentarEntrar(evento=None):
        try:
            alumnosActuales = gestorBdGlobal.cargarAlumnos()
            coordValidado = gestorBdGlobal.autenticarCoordinador(entryId.get(), entryPass.get(), alumnosActuales)
            gestorBdGlobal.registrarHistorial(coordValidado.getIdNombre(), "LOGIN_EXITOSO", "", f"Ingreso al sistema de {coordValidado.getNombre()}")
            resultado["coordinador"] = coordValidado
            ventanaLogin.destroy()
        except (SistemaREError, ValueError, TypeError, sqlite3.Error) as e:
            enviarError(e, "Login")
            lblEstado.config(text=str(e), fg="#A93226")
            entryPass.delete(0, "end")
            messagebox.showerror("Acceso Denegado", str(e))
        except Exception as e:
            enviarError(e, "Login")
            messagebox.showerror("Error inesperado", str(e))

    def salirLogin():
        resultado["coordinador"] = None
        ventanaLogin.destroy()

    entryPass.bind("<Return>", intentarEntrar)
    entryId.bind("<Return>", intentarEntrar)
    ventanaLogin.protocol("WM_DELETE_WINDOW", salirLogin)

    frameBotones = tk.Frame(ventanaLogin, bg="beige")
    frameBotones.pack(pady=10)
    tk.Button(frameBotones, text="Entrar al Sistema", command=intentarEntrar, bg="#117A76", fg="white", font=("Arial", 10, "bold"), width=18, pady=4).grid(row=0, column=0, padx=8)
    tk.Button(frameBotones, text="Salir", command=salirLogin, bg="#A93226", fg="white", font=("Arial", 10, "bold"), width=12, pady=4).grid(row=0, column=1, padx=8)

    ventanaLogin.mainloop()
    return resultado["coordinador"]


def mostrarVentanaPrincipal(coordAutenticado):
    estadoCoord = {"actual": coordAutenticado}
    accionSalida = {"cerrarSesion": False}

    ventana = tk.Tk()
    ventana.title("Sistema de Relaciones Estudiantiles - Panel Coordinador")
    ventana.geometry("820x660")
    ventana.minsize(780, 620)
    ventana.configure(bg="beige")

    cargarLogoEnVentana(ventana, 210, 65)

    frameBarraSuperior = tk.Frame(ventana, bg="#E8F6F3", pady=5, padx=12)
    frameBarraSuperior.pack(fill="x", padx=20, pady=2)

    etiquetaCoord = tk.Label(
        frameBarraSuperior,
        text=f"Admin: {estadoCoord['actual'].getNombre()} ({estadoCoord['actual'].getIdNombre()}) | Area: {estadoCoord['actual'].getArea()} | BD: sistema_re.db",
        bg="#E8F6F3",
        fg="#0E5A56",
        font=("Helvetica", 9, "bold")
    )
    etiquetaCoord.pack(side="left")

    etiquetaSaludo = tk.Label(ventana, text="Selecciona una seccion para comenzar", bg="beige", fg="#2C3E50", font=("Helvetica", 9, "bold"))
    etiquetaSaludo.pack(fill="x", padx=20, pady=3)

    frameContenido = tk.Frame(ventana, bg="beige")
    frameContenido.pack(fill="both", expand=True, padx=20, pady=6)

    def limpiarContenedor():
        for widget in frameContenido.winfo_children():
            widget.destroy()

    def cerrarSesion():
        confirmar = messagebox.askyesno("Cerrar Sesion", "¿Deseas cerrar sesion y regresar a la pantalla de acceso?")
        if not confirmar:
            return
        try:
            gestorBdGlobal.registrarHistorial(estadoCoord["actual"].getIdNombre(), "LOGOUT", "", f"Cierre de sesion de {estadoCoord['actual'].getNombre()}")
        except SistemaREError:
            pass
        accionSalida["cerrarSesion"] = True
        ventana.destroy()

    def salirDelSistema():
        accionSalida["cerrarSesion"] = False
        ventana.destroy()

    ventana.protocol("WM_DELETE_WINDOW", salirDelSistema)

    tk.Button(frameBarraSuperior, text="Salir", command=salirDelSistema, bg="#A93226", fg="white", font=("Arial", 8, "bold"), width=7).pack(side="right", padx=3)
    tk.Button(frameBarraSuperior, text="Cerrar Sesion", command=cerrarSesion, bg="#B9770E", fg="white", font=("Arial", 8, "bold"), width=13).pack(side="right", padx=3)

    def abrirVentanaResumen(titulo, listaAlumnos):
        ventanaResumen = tk.Toplevel(ventana)
        ventanaResumen.title(titulo)
        ventanaResumen.geometry("980x520")
        ventanaResumen.configure(bg="#E8F6F3")

        total = len(listaAlumnos)
        cumplenCount = 0
        for al in listaAlumnos:
            if al.verificarGraduacion() == "S":
                cumplenCount += 1
        pendientesCount = total - cumplenCount

        tk.Label(
            ventanaResumen,
            text=f"{titulo} | Total: {total} | Cumplen: {cumplenCount} | Pendientes: {pendientesCount}",
            font=("Arial", 11, "bold"),
            bg="#117A76",
            fg="white",
            pady=8
        ).pack(fill="x")

        contenedor = tk.Frame(ventanaResumen, bg="#E8F6F3")
        contenedor.pack(fill="both", expand=True, padx=10, pady=8)

        canvas = tk.Canvas(contenedor, bg="#E8F6F3", highlightthickness=0)
        scrollbarY = tk.Scrollbar(contenedor, orient="vertical", command=canvas.yview)
        scrollbarX = tk.Scrollbar(contenedor, orient="horizontal", command=canvas.xview)
        frameDatos = tk.Frame(canvas, bg="#E8F6F3")

        def ajustarScroll(evento=None):
            canvas.configure(scrollregion=canvas.bbox("all"))
        frameDatos.bind("<Configure>", ajustarScroll)

        canvas.create_window((0, 0), window=frameDatos, anchor="nw")
        canvas.configure(yscrollcommand=scrollbarY.set, xscrollcommand=scrollbarX.set)

        scrollbarY.pack(side="right", fill="y")
        scrollbarX.pack(side="bottom", fill="x")
        canvas.pack(side="left", fill="both", expand=True)

        encabezados = ["ID", "Nombre", "Tipo", "Sem.", "Grupo / Subgrupo", "Avance", "Cumplidos", "Pendientes", "Estatus"]
        col = 0
        for enc in encabezados:
            tk.Label(frameDatos, text=enc, font=("Arial", 10, "bold"), bg="#D1F2EB", fg="#0E5A56", padx=8, pady=5).grid(row=0, column=col, sticky="ew", padx=2, pady=2)
            col += 1

        if total == 0:
            tk.Label(
                frameDatos,
                text="No hay alumnos que coincidan con este criterio.",
                font=("Arial", 10, "italic"),
                bg="#E8F6F3",
                fg="#566573",
                pady=20
            ).grid(row=1, column=0, columnspan=9)
        else:
            fila = 1
            for a in listaAlumnos:
                estado = "Cumple" if a.verificarGraduacion() == "S" else "Pendiente"
                colorEstado = "#117A76" if estado == "Cumple" else "#A93226"
                tipoTxt = "GestionRe" if isinstance(a, GestionRe) else "Alumno"
                cumplidosTxt = ", ".join(a.obtenerCumplidos())
                if not cumplidosTxt:
                    cumplidosTxt = "Ninguno"
                pendientesLista = a.obtenerPendientes()
                pendientesTxt = ", ".join(pendientesLista) if len(pendientesLista) > 0 else "Ninguno"
                porcentaje = int(a.calcularPorcentajeAvance())

                tk.Label(frameDatos, text=a.getId(), font=("Arial", 9, "bold"), bg="#E8F6F3", padx=6).grid(row=fila, column=0, pady=4, sticky="w")
                tk.Label(frameDatos, text=a.getNombre(), font=("Arial", 9), bg="#E8F6F3", padx=6).grid(row=fila, column=1, pady=4, sticky="w")
                tk.Label(frameDatos, text=tipoTxt, font=("Arial", 9), bg="#E8F6F3", padx=6).grid(row=fila, column=2, pady=4)
                tk.Label(frameDatos, text=str(a.getSemestre()), font=("Arial", 9), bg="#E8F6F3", padx=6).grid(row=fila, column=3, pady=4)
                tk.Label(frameDatos, text=a.getAreaCompleta(), font=("Arial", 9), bg="#E8F6F3", padx=6).grid(row=fila, column=4, pady=4, sticky="w")
                tk.Label(frameDatos, text=f"{porcentaje}%", font=("Arial", 9, "bold"), bg="#E8F6F3", padx=6).grid(row=fila, column=5, pady=4)
                tk.Label(frameDatos, text=cumplidosTxt, font=("Arial", 8), bg="#E8F6F3", fg="#196F3D", wraplength=210, justify="left", padx=6).grid(row=fila, column=6, pady=4, sticky="w")
                tk.Label(frameDatos, text=pendientesTxt, font=("Arial", 8), bg="#E8F6F3", fg="#922B21", wraplength=210, justify="left", padx=6).grid(row=fila, column=7, pady=4, sticky="w")
                tk.Label(frameDatos, text=estado, font=("Arial", 9, "bold"), bg="#E8F6F3", fg=colorEstado, padx=6).grid(row=fila, column=8, pady=4)
                fila += 1

        tk.Button(
            ventanaResumen,
            text="Cerrar",
            command=ventanaResumen.destroy,
            bg="#117A76",
            fg="white",
            font=("Arial", 10, "bold"),
            width=14
        ).pack(pady=10)

    def mostrarTodosGui():
        try:
            todos = estadoCoord["actual"].obtenerTodosLosAlumnos()
            if len(todos) == 0:
                raise SinAlumnosRegistradosError("No hay alumnos registrados en la base de datos")
            abrirVentanaResumen("Todos los Alumnos", todos)
        except SinAlumnosRegistradosError as e:
            enviarError(e, "GUI")
            messagebox.showinfo("Sin registros", str(e))
        except Exception as e:
            enviarError(e, "GUI")
            messagebox.showerror("Error", str(e))

    def mostrarCumplimientoGui():
        try:
            todos = estadoCoord["actual"].obtenerTodosLosAlumnos()
            if len(todos) == 0:
                raise SinAlumnosRegistradosError("No hay alumnos registrados en la base de datos")
            cumplidos = estadoCoord["actual"].mostrarAlumnosCumplimiento()
            abrirVentanaResumen("Alumnos en Cumplimiento", cumplidos)
        except SinAlumnosRegistradosError as e:
            enviarError(e, "GUI")
            messagebox.showinfo("Sin registros", str(e))
        except Exception as e:
            enviarError(e, "GUI")
            messagebox.showerror("Error", str(e))

    def mostrarPendientesGui():
        try:
            todos = estadoCoord["actual"].obtenerTodosLosAlumnos()
            if len(todos) == 0:
                raise SinAlumnosRegistradosError("No hay alumnos registrados en la base de datos")
            pendientes = estadoCoord["actual"].mostrarAlumnosConRequisitosPendientes()
            abrirVentanaResumen("Alumnos con Requisitos Pendientes", pendientes)
        except SinAlumnosRegistradosError as e:
            enviarError(e, "GUI")
            messagebox.showinfo("Sin registros", str(e))
        except Exception as e:
            enviarError(e, "GUI")
            messagebox.showerror("Error", str(e))

    def abrirVentanaRequisitos():
        venReq = tk.Toplevel(ventana)
        venReq.title("Gestion de Requisitos Especiales (GestionRe)")
        venReq.geometry("690x540")
        venReq.configure(bg="beige")

        frameTop = tk.Frame(venReq, bg="beige")
        frameTop.pack(fill="x", padx=15, pady=10)

        tk.Label(frameTop, text="ID Alumno GestionRe:", bg="beige", font=("Helvetica", 10, "bold")).grid(row=0, column=0, sticky="w")
        entryIdReq = tk.Entry(frameTop, font=("Helvetica", 10), width=18)
        entryIdReq.grid(row=0, column=1, padx=6)

        lblAlumnoReq = tk.Label(venReq, text="Carga un alumno de tipo GestionRe para administrar sus requisitos", bg="#E8F6F3", fg="#0E5A56", font=("Helvetica", 9, "bold"), pady=5)
        lblAlumnoReq.pack(fill="x", padx=15, pady=2)

        listaBox = tk.Listbox(venReq, font=("Consolas", 9), height=8)
        listaBox.pack(fill="x", padx=15, pady=6)

        estadoLocal = {"alumno": None}

        def refrescarListaReq():
            listaBox.delete(0, "end")
            al = estadoLocal["alumno"]
            if al is None:
                return
            lblAlumnoReq.config(text=f"{al.getNombre()} ({al.getId()}) | Periodo: {al.getPeriodo()} | Avance: {int(al.calcularPorcentajeAvance())}%")
            for r in al.getRequisitos():
                listaBox.insert("end", str(r))

        def cargarAlumnoReq():
            try:
                al = estadoCoord["actual"].buscarAlumnoPorId(entryIdReq.get())
                if not isinstance(al, GestionRe):
                    raise TipoGestionInvalidoError(f"El alumno {al.getId()} no es de tipo GestionRe. Cambia su tipo y actualiza primero.")
                estadoLocal["alumno"] = al
                refrescarListaReq()
            except (SistemaREError, ValueError, TypeError) as e:
                enviarError(e, "GUI")
                messagebox.showerror("Error", str(e))

        tk.Button(frameTop, text="Cargar Requisitos", command=cargarAlumnoReq, bg="#117A76", fg="white", font=("Arial", 9, "bold")).grid(row=0, column=2, padx=6)

        frameNuevoReq = tk.LabelFrame(venReq, text="Agregar / Actualizar Requisito", bg="beige", fg="#117A76", font=("Helvetica", 9, "bold"), padx=10, pady=8)
        frameNuevoReq.pack(fill="x", padx=15, pady=6)

        tk.Label(frameNuevoReq, text="Tipo:", bg="beige", font=("Helvetica", 9)).grid(row=0, column=0, sticky="w", pady=3)
        comboTipoReq = ttk.Combobox(frameNuevoReq, values=["Cantidad", "Evento", "Academico", "General"], state="readonly", width=14)
        comboTipoReq.set("Cantidad")
        comboTipoReq.grid(row=0, column=1, padx=5, pady=3)

        tk.Label(frameNuevoReq, text="Actividad:", bg="beige", font=("Helvetica", 9)).grid(row=0, column=2, sticky="w", pady=3)
        entryNomReq = tk.Entry(frameNuevoReq, width=24)
        entryNomReq.grid(row=0, column=3, padx=5, pady=3)

        tk.Label(frameNuevoReq, text="Periodo:", bg="beige", font=("Helvetica", 9)).grid(row=1, column=0, sticky="w", pady=3)
        entryPerReq = tk.Entry(frameNuevoReq, width=16)
        entryPerReq.insert(0, "2026-2027")
        entryPerReq.grid(row=1, column=1, padx=5, pady=3)

        tk.Label(frameNuevoReq, text="Meta / Fecha / Calif:", bg="beige", font=("Helvetica", 9)).grid(row=1, column=2, sticky="w", pady=3)
        entryParamReq = tk.Entry(frameNuevoReq, width=24)
        entryParamReq.grid(row=1, column=3, padx=5, pady=3)

        tk.Label(frameNuevoReq, text="Avance / Estado (Si/No o num):", bg="beige", font=("Helvetica", 9)).grid(row=2, column=0, columnspan=2, sticky="w", pady=3)
        entryAvanceReq = tk.Entry(frameNuevoReq, width=24)
        entryAvanceReq.insert(0, "0")
        entryAvanceReq.grid(row=2, column=2, columnspan=2, sticky="w", padx=5, pady=3)

        def agregarReqGui():
            try:
                al = estadoLocal["alumno"]
                if al is None:
                    raise SeleccionInvalidaError("Primero carga un alumno GestionRe")
                tipo = comboTipoReq.get().strip()
                nomAct = entryNomReq.get()
                perAct = entryPerReq.get()
                param = entryParamReq.get()
                avance = entryAvanceReq.get().strip()

                if tipo == "Cantidad":
                    reqCant = parsearEnteroTexto(param, "Cantidad requerida", 1, maxCantidadRequisito, CantidadRequeridaInvalidaError)
                    realCant = parsearEnteroTexto(avance if avance else "0", "Cantidad realizada", 0, maxCantidadRequisito)
                    nuevoReq = RequisitoCantidad(nomAct, perAct, reqCant, realCant)
                elif tipo == "Evento":
                    estadoBool = True if avance.lower() in ["si", "true", "1"] else False
                    nuevoReq = RequisitoEvento(nomAct, perAct, param, estadoBool)
                elif tipo == "Academico":
                    calif = parsearFlotanteTexto(param if param.strip() else "70", "Calificacion minima", 0.0, 100.0)
                    if avance.isdigit():
                        repReq = parsearEnteroTexto(avance, "Materias reprobadas del requisito", 0, maxReprobadas)
                        nuevoReq = RequisitoAcademico(nomAct, perAct, calif, repReq, repReq == 0)
                    else:
                        estadoBool = True if avance.lower() in ["si", "true", "1"] else False
                        nuevoReq = RequisitoAcademico(nomAct, perAct, calif, 0, estadoBool)
                elif tipo == "General":
                    estadoBool = True if avance.lower() in ["si", "true", "1"] else False
                    nuevoReq = Requisito(nomAct, perAct, estadoBool)
                else:
                    raise TipoRequisitoInvalidoError("Tipo de requisito no reconocido")

                al.agregarRequisito(nuevoReq)
                estadoCoord["actual"].actualizarAlumno(al)
                gestorBdGlobal.registrarHistorial(estadoCoord["actual"].getIdNombre(), "ALTA_REQUISITO", al.getId(), f"Se agrego requisito {nuevoReq.getNombreActividad()}")
                entryNomReq.delete(0, "end")
                entryParamReq.delete(0, "end")
                entryAvanceReq.delete(0, "end")
                entryAvanceReq.insert(0, "0")
                refrescarListaReq()
                messagebox.showinfo("Exito", "Requisito agregado y guardado en SQLite")
            except (SistemaREError, ValueError, TypeError, sqlite3.Error) as e:
                enviarError(e, "GUI_Requisitos")
                messagebox.showerror("Error", str(e))

        def actualizarAvanceReqGui():
            try:
                al = estadoLocal["alumno"]
                if al is None:
                    raise SeleccionInvalidaError("Primero carga un alumno GestionRe")
                seleccion = listaBox.curselection()
                if len(seleccion) == 0:
                    raise SeleccionInvalidaError("Selecciona un requisito de la lista para actualizar su avance")
                req = al.getRequisitos()[seleccion[0]]
                avance = entryAvanceReq.get().strip()
                if isinstance(req, RequisitoCantidad):
                    cant = parsearEnteroTexto(avance, "Cantidad realizada", 0, maxCantidadRequisito)
                    req.registrarAvance(cant)
                elif isinstance(req, RequisitoEvento):
                    if avance.lower() not in ["si", "no", "true", "false", "1", "0"]:
                        raise BooleanoInvalidoError("Para evento indica Si o No en avance")
                    req.registrarAsistencia(avance.lower() in ["si", "true", "1"])
                elif isinstance(req, RequisitoAcademico):
                    if avance.isdigit():
                        req.actualizarMateriasReprobadas(int(avance))
                    elif avance.lower() in ["si", "no", "true", "false"]:
                        req.registrarAvance(avance.lower() in ["si", "true"])
                    else:
                        raise TipoDatoInvalidoError("Para academico indica cantidad de reprobadas o Si/No")
                else:
                    if avance.lower() not in ["si", "no", "true", "false", "1", "0"]:
                        raise BooleanoInvalidoError("Indica Si o No en avance")
                    req.registrarAvance(avance.lower() in ["si", "true", "1"])

                estadoCoord["actual"].actualizarAlumno(al)
                gestorBdGlobal.registrarHistorial(estadoCoord["actual"].getIdNombre(), "AVANCE_REQUISITO", al.getId(), f"Actualizo requisito {req.getNombreActividad()}")
                refrescarListaReq()
                messagebox.showinfo("Exito", "Avance de requisito actualizado en SQLite")
            except (SistemaREError, ValueError, TypeError, sqlite3.Error) as e:
                enviarError(e, "GUI_Requisitos")
                messagebox.showerror("Error", str(e))

        def eliminarReqGui():
            try:
                al = estadoLocal["alumno"]
                if al is None:
                    raise SeleccionInvalidaError("Primero carga un alumno GestionRe")
                seleccion = listaBox.curselection()
                if len(seleccion) == 0:
                    raise SeleccionInvalidaError("Selecciona un requisito de la lista para eliminar")
                req = al.getRequisitos()[seleccion[0]]
                al.eliminarRequisito(req.getNombreActividad(), req.getPeriodo())
                estadoCoord["actual"].actualizarAlumno(al)
                gestorBdGlobal.registrarHistorial(estadoCoord["actual"].getIdNombre(), "ELIMINAR_REQUISITO", al.getId(), f"Elimino requisito {req.getNombreActividad()}")
                refrescarListaReq()
                messagebox.showinfo("Eliminado", "Requisito eliminado de SQLite")
            except (SistemaREError, ValueError, TypeError, sqlite3.Error) as e:
                enviarError(e, "GUI_Requisitos")
                messagebox.showerror("Error", str(e))

        frameBotReq = tk.Frame(venReq, bg="beige")
        frameBotReq.pack(pady=8)
        tk.Button(frameBotReq, text="Agregar Requisito", command=agregarReqGui, bg="#117A76", fg="white", font=("Arial", 9, "bold"), width=17).grid(row=0, column=0, padx=5)
        tk.Button(frameBotReq, text="Actualizar Avance", command=actualizarAvanceReqGui, bg="#117A76", fg="white", font=("Arial", 9, "bold"), width=17).grid(row=0, column=1, padx=5)
        tk.Button(frameBotReq, text="Eliminar Requisito", command=eliminarReqGui, bg="#A93226", fg="white", font=("Arial", 9, "bold"), width=17).grid(row=0, column=2, padx=5)
        tk.Button(frameBotReq, text="Cerrar", command=venReq.destroy, bg="#566573", fg="white", font=("Arial", 9, "bold"), width=12).grid(row=0, column=3, padx=5)

    def abrirVentanaCoordinador():
        venCoord = tk.Toplevel(ventana)
        venCoord.title("Administrar Coordinadores (SQLite)")
        venCoord.geometry("540x450")
        venCoord.configure(bg="beige")

        tk.Label(venCoord, text="Gestion de Coordinadores Autorizados", bg="#117A76", fg="white", font=("Helvetica", 11, "bold"), pady=6).pack(fill="x")

        listaCoords = tk.Listbox(venCoord, font=("Consolas", 9), height=6)
        listaCoords.pack(fill="x", padx=15, pady=8)

        def refrescarCoords():
            listaCoords.delete(0, "end")
            try:
                coords = gestorBdGlobal.cargarCoordinadores()
                for c in coords:
                    marca = " [ACTIVO]" if c.getIdNombre() == estadoCoord["actual"].getIdNombre() else ""
                    listaCoords.insert("end", f"{c.getIdNombre()} | {c.getNombre()} | Area: {c.getArea()} | {c.getAnioAdministracion()}{marca}")
            except SistemaREError as e:
                enviarError(e, "GUI_Coordinador")

        refrescarCoords()

        frameC = tk.Frame(venCoord, bg="beige", padx=15, pady=5)
        frameC.pack(fill="both", expand=True)

        tk.Label(frameC, text="ID Coordinador:", bg="beige", font=("Helvetica", 9, "bold")).grid(row=0, column=0, sticky="w", pady=4)
        eIdC = tk.Entry(frameC, width=28)
        eIdC.grid(row=0, column=1, pady=4)

        tk.Label(frameC, text="Contraseña:", bg="beige", font=("Helvetica", 9, "bold")).grid(row=1, column=0, sticky="w", pady=4)
        ePassC = tk.Entry(frameC, show="*", width=28)
        ePassC.grid(row=1, column=1, pady=4)

        tk.Label(frameC, text="Nombre:", bg="beige", font=("Helvetica", 9, "bold")).grid(row=2, column=0, sticky="w", pady=4)
        eNomC = tk.Entry(frameC, width=28)
        eNomC.grid(row=2, column=1, pady=4)

        tk.Label(frameC, text="Area:", bg="beige", font=("Helvetica", 9, "bold")).grid(row=3, column=0, sticky="w", pady=4)
        eAreaC = tk.Entry(frameC, width=28)
        eAreaC.insert(0, "General")
        eAreaC.grid(row=3, column=1, pady=4)

        tk.Label(frameC, text="Año Admin (2000-2100):", bg="beige", font=("Helvetica", 9, "bold")).grid(row=4, column=0, sticky="w", pady=4)
        eAnioC = tk.Entry(frameC, width=28)
        eAnioC.insert(0, "2026")
        eAnioC.grid(row=4, column=1, pady=4)

        def registrarCoord():
            try:
                anioNum = parsearEnteroTexto(eAnioC.get(), "Año de administracion", 2000, 2100, AnioAdministracionInvalidoError)
                nuevo = Coordinador(eIdC.get(), ePassC.get(), eNomC.get(), [], eAreaC.get(), anioNum)
                gestorBdGlobal.guardarCoordinador(nuevo)
                gestorBdGlobal.registrarHistorial(estadoCoord["actual"].getIdNombre(), "ALTA_COORDINADOR", "", f"Registro nuevo coordinador {nuevo.getIdNombre()}")
                refrescarCoords()
                messagebox.showinfo("Coordinador registrado", f"Coordinador {nuevo.getIdNombre()} guardado en SQLite")
            except (SistemaREError, ValueError, TypeError, sqlite3.Error) as e:
                enviarError(e, "GUI_Coordinador")
                messagebox.showerror("Error", str(e))

        def eliminarCoord():
            try:
                idBorrar = validarIdTexto(eIdC.get(), "ID del coordinador", 2, 30)
                gestorBdGlobal.eliminarCoordinador(idBorrar, estadoCoord["actual"].getIdNombre())
                gestorBdGlobal.registrarHistorial(estadoCoord["actual"].getIdNombre(), "BAJA_COORDINADOR", "", f"Elimino coordinador {idBorrar}")
                refrescarCoords()
                messagebox.showinfo("Coordinador eliminado", f"Coordinador {idBorrar} eliminado de SQLite")
            except (SistemaREError, ValueError, TypeError, sqlite3.Error) as e:
                enviarError(e, "GUI_Coordinador")
                messagebox.showerror("Error", str(e))

        frameBotC = tk.Frame(venCoord, bg="beige")
        frameBotC.pack(pady=10)
        tk.Button(frameBotC, text="Registrar Nuevo", command=registrarCoord, bg="#117A76", fg="white", font=("Arial", 9, "bold"), width=15).grid(row=0, column=0, padx=6)
        tk.Button(frameBotC, text="Eliminar por ID", command=eliminarCoord, bg="#A93226", fg="white", font=("Arial", 9, "bold"), width=15).grid(row=0, column=1, padx=6)
        tk.Button(frameBotC, text="Cerrar", command=venCoord.destroy, bg="#566573", fg="white", font=("Arial", 9, "bold"), width=10).grid(row=0, column=2, padx=6)

    def abrirVentanaRegistrosBd(titulo, tipoRegistro):
        try:
            if tipoRegistro == "errores":
                filas = gestorBdGlobal.obtenerErrores(100)
            else:
                filas = gestorBdGlobal.obtenerHistorial(100)
            venLogs = tk.Toplevel(ventana)
            venLogs.title(titulo)
            venLogs.geometry("760x420")
            venLogs.configure(bg="#E8F6F3")

            tk.Label(venLogs, text=f"{titulo} (Ultimos {len(filas)} registros en SQLite)", bg="#117A76", fg="white", font=("Arial", 10, "bold"), pady=6).pack(fill="x")

            cajaTexto = tk.Text(venLogs, font=("Consolas", 9), wrap="word")
            scroll = tk.Scrollbar(venLogs, command=cajaTexto.yview)
            cajaTexto.configure(yscrollcommand=scroll.set)
            scroll.pack(side="right", fill="y")
            cajaTexto.pack(fill="both", expand=True, padx=10, pady=8)

            if len(filas) == 0:
                cajaTexto.insert("end", "No hay registros almacenados aun.")
            else:
                for fila in filas:
                    if tipoRegistro == "errores":
                        cajaTexto.insert("end", f"[{fila[0]}] {fila[1]} | {fila[4]} | {fila[2]}: {fila[3]}\n")
                    else:
                        cajaTexto.insert("end", f"[{fila[0]}] {fila[1]} | Coord: {fila[2]} | {fila[3]} | Alumno: {fila[4]} | {fila[5]}\n")
            cajaTexto.config(state="disabled")
            tk.Button(venLogs, text="Cerrar", command=venLogs.destroy, bg="#117A76", fg="white", font=("Arial", 9, "bold"), width=14).pack(pady=6)
        except (SistemaREError, sqlite3.Error) as e:
            enviarError(e, "GUI_Logs")
            messagebox.showerror("Error", str(e))

    def verLogsErroresGui():
        abrirVentanaRegistrosBd("Bitacora de Errores (SQLite)", "errores")

    def verHistorialGui():
        abrirVentanaRegistrosBd("Historial de Acciones (SQLite)", "historial")

    def exportarRespaldoTxtGui():
        try:
            todos = estadoCoord["actual"].obtenerTodosLosAlumnos()
            if len(todos) == 0:
                raise SinAlumnosRegistradosError("No hay alumnos para exportar")
            gestorGlobal.guardarAlumnos(todos)
            gestorBdGlobal.registrarHistorial(estadoCoord["actual"].getIdNombre(), "EXPORTAR_TXT", "", f"Respaldo exportado de {len(todos)} alumnos")
            messagebox.showinfo("Respaldo exitoso", f"Se exportaron {len(todos)} alumnos a {archivoAlumnosDefault}")
        except (SistemaREError, OSError) as e:
            enviarError(e, "GUI_Exportar")
            messagebox.showerror("Error al exportar", str(e))

    def abrirExploradorGrupos(modoExplorador):
        venExp = tk.Toplevel(ventana)
        venExp.geometry("760x470")
        venExp.configure(bg="beige")

        if modoExplorador == "clubs":
            venExp.title("Clubs Anahuac - Catalogo y Lista de Clubs")
            encabezadoTxt = "Clubs Anahuac (Selecciona un club de la lista para ver sus inscritos)"
            subtituloIzq = "Lista de Clubs Anahuac"
        elif modoExplorador == "estados":
            venExp.title("Asociaciones por Estado")
            encabezadoTxt = "Asociaciones por Estado (Selecciona un estado para ver sus inscritos)"
            subtituloIzq = "Asociaciones Registradas"
        else:
            venExp.title("Grupos de Relaciones Estudiantiles")
            encabezadoTxt = "Grupos de Relaciones Estudiantiles (AreaRE)"
            subtituloIzq = "Areas de Relaciones Estudiantiles"

        tk.Label(venExp, text=encabezadoTxt, bg="#117A76", fg="white", font=("Arial", 10, "bold"), pady=7).pack(fill="x")

        panelCuerpo = tk.Frame(venExp, bg="beige")
        panelCuerpo.pack(fill="both", expand=True, padx=14, pady=10)

        panelIzq = tk.Frame(panelCuerpo, bg="beige")
        panelIzq.pack(side="left", fill="y", padx=(0, 12))
        tk.Label(panelIzq, text=subtituloIzq, bg="beige", fg="#1B2631", font=("Helvetica", 10, "bold")).pack(anchor="w", pady=3)
        listaIzq = tk.Listbox(panelIzq, font=("Helvetica", 10), width=30, height=16)
        listaIzq.pack(fill="y", expand=True)

        panelDer = tk.Frame(panelCuerpo, bg="#E8F6F3", padx=12, pady=10)
        panelDer.pack(side="right", fill="both", expand=True)

        lblTituloDer = tk.Label(panelDer, text="Selecciona un elemento de la lista", bg="#E8F6F3", fg="#0E5A56", font=("Helvetica", 11, "bold"), anchor="w")
        lblTituloDer.pack(fill="x", pady=4)

        lblInfoDer = tk.Label(panelDer, text="", bg="#E8F6F3", fg="#2C3E50", font=("Helvetica", 9), anchor="w")
        lblInfoDer.pack(fill="x", pady=2)

        listaAlumnosDer = tk.Listbox(panelDer, font=("Consolas", 9), height=14)
        listaAlumnosDer.pack(fill="both", expand=True, pady=6)

        claves = []
        if modoExplorador == "clubs":
            for nombreClub in clubsAnahuacValidos:
                clubObj = clubsDisponibles[nombreClub]
                claves.append(nombreClub)
                listaIzq.insert("end", f"{nombreClub} ({len(clubObj.getAlumnos())})")
        elif modoExplorador == "estados":
            for nombreEstado in asociacionesPorEstadoValidas:
                asocObj = asociacionesEstadoDisponibles[nombreEstado]
                claves.append(nombreEstado)
                listaIzq.insert("end", f"{nombreEstado} ({len(asocObj.getAlumnos())})")
        else:
            for idAr, areaObj in gruposDisponibles.items():
                claves.append(idAr)
                listaIzq.insert("end", f"{idAr}. {areaObj.getNombreArea()} ({len(areaObj.getAlumnos())})")

        def alSeleccionarElemento(evento=None):
            sel = listaIzq.curselection()
            if len(sel) == 0:
                return
            clave = claves[sel[0]]
            listaAlumnosDer.delete(0, "end")
            if modoExplorador == "clubs":
                obj = clubsDisponibles[clave]
                lblTituloDer.config(text=f"Clubs Anahuac -> {clave}")
                lblInfoDer.config(text=f"Tipo: {obj.obtenerTipoGrupo()} | Inscritos: {len(obj.getAlumnos())}")
                alumnos = obj.getAlumnos()
            elif modoExplorador == "estados":
                obj = asociacionesEstadoDisponibles[clave]
                lblTituloDer.config(text=f"Asociaciones por estado -> {clave}")
                lblInfoDer.config(text=f"Tipo: {obj.obtenerTipoGrupo()} | Inscritos: {len(obj.getAlumnos())}")
                alumnos = obj.getAlumnos()
            else:
                obj = gruposDisponibles[clave]
                lblTituloDer.config(text=f"{obj.getNombreArea()} (ID {obj.getIdArea()})")
                lblInfoDer.config(text=f"Descripcion: {obj.obtenerTipoGrupo()} | Inscritos: {len(obj.getAlumnos())}")
                alumnos = obj.getAlumnos()

            if len(alumnos) == 0:
                listaAlumnosDer.insert("end", "No hay alumnos inscritos en esta categoria.")
            else:
                for al in alumnos:
                    est = "Cumple" if al.verificarGraduacion() == "S" else "Pendiente"
                    listaAlumnosDer.insert("end", f"{al.getId()} | {al.getNombre()} | Sem {al.getSemestre()} | {est}")

        listaIzq.bind("<<ListboxSelect>>", alSeleccionarElemento)
        if len(claves) > 0:
            listaIzq.selection_set(0)
            alSeleccionarElemento()

        tk.Button(venExp, text="Cerrar", command=venExp.destroy, bg="#117A76", fg="white", font=("Arial", 9, "bold"), width=14).pack(pady=8)

    def mostrarFormularioAlumno(modo, idInicial=""):
        limpiarContenedor()
        tituloModo = "Registrar Nuevo Alumno / GestionRe" if modo == "nuevo" else "Buscar y Actualizar Alumno"
        etiquetaSaludo.config(text=f"Modulo Alumnos: {tituloModo}", fg="#1B2631")

        barraNav = tk.Frame(frameContenido, bg="beige")
        barraNav.pack(fill="x", pady=(0, 6))
        tk.Label(barraNav, text=f"Inicio > Gestion de Alumnos > {tituloModo}", bg="beige", fg="#117A76", font=("Helvetica", 10, "bold")).pack(side="left")
        tk.Button(barraNav, text="<- Volver a Gestion de Alumnos", command=mostrarSubmenuAlumnos, bg="#566573", fg="white", font=("Arial", 8, "bold")).pack(side="right")

        frameForm = tk.Frame(frameContenido, bg="beige")
        frameForm.pack(fill="x", pady=2)
        frameForm.columnconfigure(1, weight=1)
        frameForm.columnconfigure(3, weight=1)

        tk.Label(frameForm, text="ID Alumno:", fg="#1B2631", bg="beige", font=("Helvetica", 9, "bold")).grid(row=0, column=0, sticky="w", pady=3, padx=(0, 6))
        entryMat = tk.Entry(frameForm, font=("Helvetica", 10))
        entryMat.grid(row=0, column=1, sticky="ew", pady=3, padx=(0, 12))
        if idInicial:
            entryMat.insert(0, idInicial)

        tk.Label(frameForm, text="Semestre (1-13):", fg="#1B2631", bg="beige", font=("Helvetica", 9, "bold")).grid(row=0, column=2, sticky="w", pady=3, padx=(0, 6))
        entrySem = tk.Entry(frameForm, font=("Helvetica", 10))
        entrySem.grid(row=0, column=3, sticky="ew", pady=3)

        tk.Label(frameForm, text="Nombre completo:", fg="#1B2631", bg="beige", font=("Helvetica", 9, "bold")).grid(row=1, column=0, sticky="w", pady=3, padx=(0, 6))
        entryNom = tk.Entry(frameForm, font=("Helvetica", 10))
        entryNom.grid(row=1, column=1, columnspan=3, sticky="ew", pady=3)

        tk.Label(frameForm, text="Grupo:", fg="#1B2631", bg="beige", font=("Helvetica", 9, "bold")).grid(row=2, column=0, sticky="w", pady=3, padx=(0, 6))
        comboCarr = ttk.Combobox(frameForm, values=areasValidas, state="readonly", font=("Helvetica", 10))
        comboCarr.set("Selecciona un grupo")
        comboCarr.grid(row=2, column=1, sticky="ew", pady=3, padx=(0, 12))

        lblSubgrupo = tk.Label(frameForm, text="Club / Estado:", fg="#1B2631", bg="beige", font=("Helvetica", 9, "bold"))
        lblSubgrupo.grid(row=2, column=2, sticky="w", pady=3, padx=(0, 6))
        comboSubgrupo = ttk.Combobox(frameForm, values=["No aplica"], state="disabled", font=("Helvetica", 10))
        comboSubgrupo.set("No aplica")
        comboSubgrupo.grid(row=2, column=3, sticky="ew", pady=3)

        tk.Label(frameForm, text="Tipo Registro:", fg="#1B2631", bg="beige", font=("Helvetica", 9, "bold")).grid(row=3, column=0, sticky="w", pady=3, padx=(0, 6))
        comboTipo = ttk.Combobox(frameForm, values=["Alumno", "GestionRe"], state="readonly", font=("Helvetica", 10))
        comboTipo.set("Alumno")
        comboTipo.grid(row=3, column=1, sticky="ew", pady=3, padx=(0, 12))

        tk.Label(frameForm, text="Rol / Gestion:", fg="#1B2631", bg="beige", font=("Helvetica", 9, "bold")).grid(row=3, column=2, sticky="w", pady=3, padx=(0, 6))
        entryGestion = tk.Entry(frameForm, font=("Helvetica", 10))
        entryGestion.insert(0, "Miembro General")
        entryGestion.grid(row=3, column=3, sticky="ew", pady=3)

        def actualizarListaSubgrupo(evento=None):
            areaSel = comboCarr.get().strip()
            if areaSel == "Clubs Anahuac":
                lblSubgrupo.config(text="Lista de Clubs:")
                comboSubgrupo.config(state="readonly", values=clubsAnahuacValidos)
                if comboSubgrupo.get() not in clubsAnahuacValidos:
                    comboSubgrupo.set("Selecciona un club")
            elif areaSel == "Asociaciones por estado":
                lblSubgrupo.config(text="Estado Asociacion:")
                comboSubgrupo.config(state="readonly", values=asociacionesPorEstadoValidas)
                if comboSubgrupo.get() not in asociacionesPorEstadoValidas:
                    comboSubgrupo.set("Selecciona un estado")
            elif areaSel == "Sociedades de alumnos":
                lblSubgrupo.config(text="Facultad / Carrera:")
                comboSubgrupo.config(state="normal", values=["General", "Ingenieria", "Medicina", "Derecho", "Negocios", "Arquitectura"])
                if comboSubgrupo.get() in ["No aplica", "Selecciona un club", "Selecciona un estado", ""]:
                    comboSubgrupo.set("General")
            else:
                lblSubgrupo.config(text="Club / Estado:")
                comboSubgrupo.config(state="normal", values=["No aplica"])
                comboSubgrupo.set("No aplica")
                comboSubgrupo.config(state="disabled")

        comboCarr.bind("<<ComboboxSelected>>", actualizarListaSubgrupo)

        frameProgreso = tk.LabelFrame(frameContenido, text="Avance de Requisitos", bg="beige", fg="#117A76", font=("Helvetica", 9, "bold"), padx=10, pady=5)
        frameProgreso.pack(fill="x", pady=5)

        tk.Label(frameProgreso, text="Actividades (min 8):", bg="beige", font=("Helvetica", 9, "bold")).grid(row=0, column=0, sticky="w", pady=2)
        entryAct = tk.Entry(frameProgreso, font=("Helvetica", 10), width=7)
        entryAct.insert(0, "0")
        entryAct.grid(row=0, column=1, padx=4, pady=2)

        tk.Label(frameProgreso, text="Mentorias (min 2):", bg="beige", font=("Helvetica", 9, "bold")).grid(row=0, column=2, sticky="w", pady=2)
        entryMent = tk.Entry(frameProgreso, font=("Helvetica", 10), width=7)
        entryMent.insert(0, "0")
        entryMent.grid(row=0, column=3, padx=4, pady=2)

        tk.Label(frameProgreso, text="Obligatorias (min 2):", bg="beige", font=("Helvetica", 9, "bold")).grid(row=0, column=4, sticky="w", pady=2)
        entryOblig = tk.Entry(frameProgreso, font=("Helvetica", 10), width=7)
        entryOblig.insert(0, "0")
        entryOblig.grid(row=0, column=5, padx=4, pady=2)

        tk.Label(frameProgreso, text="Reprobadas:", bg="beige", font=("Helvetica", 9, "bold")).grid(row=1, column=0, sticky="w", pady=2)
        entryRep = tk.Entry(frameProgreso, font=("Helvetica", 10), width=7)
        entryRep.insert(0, "0")
        entryRep.grid(row=1, column=1, padx=4, pady=2)

        tk.Label(frameProgreso, text="Seminario:", bg="beige", font=("Helvetica", 9, "bold")).grid(row=1, column=2, sticky="w", pady=2)
        comboSeminario = ttk.Combobox(frameProgreso, values=["No", "Si"], state="readonly", font=("Helvetica", 9), width=6)
        comboSeminario.set("No")
        comboSeminario.grid(row=1, column=3, sticky="w", padx=4, pady=2)

        frameDesglose = tk.LabelFrame(frameContenido, text="Desglose Plan Formativo (opcional, 2 de cada uno = 8)", bg="beige", fg="#117A76", font=("Helvetica", 9, "bold"), padx=10, pady=4)
        frameDesglose.pack(fill="x", pady=4)

        tk.Label(frameDesglose, text="Talleres:", bg="beige", font=("Helvetica", 9)).grid(row=0, column=0, sticky="w")
        entryTalleres = tk.Entry(frameDesglose, font=("Helvetica", 9), width=6)
        entryTalleres.insert(0, "0")
        entryTalleres.grid(row=0, column=1, padx=5)

        tk.Label(frameDesglose, text="VFI:", bg="beige", font=("Helvetica", 9)).grid(row=0, column=2, sticky="w")
        entryVfi = tk.Entry(frameDesglose, font=("Helvetica", 9), width=6)
        entryVfi.insert(0, "0")
        entryVfi.grid(row=0, column=3, padx=5)

        tk.Label(frameDesglose, text="Des. Personal:", bg="beige", font=("Helvetica", 9)).grid(row=0, column=4, sticky="w")
        entryDesPers = tk.Entry(frameDesglose, font=("Helvetica", 9), width=6)
        entryDesPers.insert(0, "0")
        entryDesPers.grid(row=0, column=5, padx=5)

        tk.Label(frameDesglose, text="Integracion:", bg="beige", font=("Helvetica", 9)).grid(row=0, column=6, sticky="w")
        entryInteg = tk.Entry(frameDesglose, font=("Helvetica", 9), width=6)
        entryInteg.insert(0, "0")
        entryInteg.grid(row=0, column=7, padx=5)

        frameGestion = tk.LabelFrame(frameContenido, text="Datos GestionRe (solo si Tipo Registro es GestionRe)", bg="beige", fg="#117A76", font=("Helvetica", 9, "bold"), padx=10, pady=4)
        frameGestion.pack(fill="x", pady=4)

        tk.Label(frameGestion, text="Periodo:", bg="beige", font=("Helvetica", 9)).grid(row=0, column=0, sticky="w")
        entryPeriodo = tk.Entry(frameGestion, font=("Helvetica", 9), width=12)
        entryPeriodo.insert(0, "2026-2027")
        entryPeriodo.grid(row=0, column=1, padx=6)

        tk.Label(frameGestion, text="Estatus:", bg="beige", font=("Helvetica", 9)).grid(row=0, column=2, sticky="w")
        comboEstatus = ttk.Combobox(frameGestion, values=estatusValidos, state="readonly", font=("Helvetica", 9), width=12)
        comboEstatus.set("Activo")
        comboEstatus.grid(row=0, column=3, padx=6)

        tk.Label(frameGestion, text="Sem. Admin (1-2):", bg="beige", font=("Helvetica", 9)).grid(row=0, column=4, sticky="w")
        entrySemAdmin = tk.Entry(frameGestion, font=("Helvetica", 9), width=6)
        entrySemAdmin.insert(0, "1")
        entrySemAdmin.grid(row=0, column=5, padx=6)

        def actualizarEstadoCamposGestion(evento=None):
            tipoSel = comboTipo.get().strip()
            if tipoSel == "GestionRe":
                entryPeriodo.config(state="normal")
                comboEstatus.config(state="readonly")
                entrySemAdmin.config(state="normal")
                if entryGestion.get().strip() == "Miembro General":
                    entryGestion.delete(0, "end")
                    entryGestion.insert(0, "Directivo GestionRe")
            else:
                entryPeriodo.config(state="disabled")
                comboEstatus.config(state="disabled")
                entrySemAdmin.config(state="disabled")
                if entryGestion.get().strip() == "Directivo GestionRe":
                    entryGestion.delete(0, "end")
                    entryGestion.insert(0, "Miembro General")

        comboTipo.bind("<<ComboboxSelected>>", actualizarEstadoCamposGestion)
        actualizarEstadoCamposGestion()

        def limpiarCampos():
            entryMat.delete(0, "end")
            entryNom.delete(0, "end")
            entrySem.delete(0, "end")
            comboCarr.set("Selecciona un grupo")
            actualizarListaSubgrupo()
            comboTipo.set("Alumno")
            entryGestion.delete(0, "end")
            entryGestion.insert(0, "Miembro General")
            entryAct.delete(0, "end")
            entryAct.insert(0, "0")
            entryMent.delete(0, "end")
            entryMent.insert(0, "0")
            entryOblig.delete(0, "end")
            entryOblig.insert(0, "0")
            entryRep.delete(0, "end")
            entryRep.insert(0, "0")
            comboSeminario.set("No")
            entryTalleres.delete(0, "end")
            entryTalleres.insert(0, "0")
            entryVfi.delete(0, "end")
            entryVfi.insert(0, "0")
            entryDesPers.delete(0, "end")
            entryDesPers.insert(0, "0")
            entryInteg.delete(0, "end")
            entryInteg.insert(0, "0")
            entryPeriodo.config(state="normal")
            entryPeriodo.delete(0, "end")
            entryPeriodo.insert(0, "2026-2027")
            comboEstatus.config(state="readonly")
            comboEstatus.set("Activo")
            entrySemAdmin.config(state="normal")
            entrySemAdmin.delete(0, "end")
            entrySemAdmin.insert(0, "1")
            actualizarEstadoCamposGestion()

        def cargarAlumnoEnFormulario(alumno):
            limpiarCampos()
            entryMat.insert(0, alumno.getId())
            entryNom.insert(0, alumno.getNombre())
            entrySem.insert(0, str(alumno.getSemestre()))
            comboCarr.set(alumno.getArea())
            actualizarListaSubgrupo()
            if alumno.getSubgrupo():
                comboSubgrupo.set(alumno.getSubgrupo())
            entryGestion.delete(0, "end")
            entryGestion.insert(0, alumno.getGestionRe())
            entryAct.delete(0, "end")
            entryAct.insert(0, str(alumno.getActividades()))
            entryMent.delete(0, "end")
            entryMent.insert(0, str(alumno.getMentorias()))
            entryOblig.delete(0, "end")
            entryOblig.insert(0, str(alumno.getActividadesObligatorias()))
            entryRep.delete(0, "end")
            entryRep.insert(0, str(alumno.getMateriasReprobadas()))
            comboSeminario.set("Si" if alumno.getSeminario() else "No")
            if alumno.getUsaDesglose():
                entryTalleres.delete(0, "end")
                entryTalleres.insert(0, str(alumno.getTalleres()))
                entryVfi.delete(0, "end")
                entryVfi.insert(0, str(alumno.getActividadesVfi()))
                entryDesPers.delete(0, "end")
                entryDesPers.insert(0, str(alumno.getDesarrolloPersonal()))
                entryInteg.delete(0, "end")
                entryInteg.insert(0, str(alumno.getIntegracion()))
            if isinstance(alumno, GestionRe):
                comboTipo.set("GestionRe")
                actualizarEstadoCamposGestion()
                entryPeriodo.delete(0, "end")
                entryPeriodo.insert(0, alumno.getPeriodo())
                comboEstatus.set(alumno.getEstatus())
                entrySemAdmin.delete(0, "end")
                entrySemAdmin.insert(0, str(alumno.getSemestresComoAdmin()))
            else:
                comboTipo.set("Alumno")
                actualizarEstadoCamposGestion()

        def construirObjetoDesdeFormulario(requisitosPrevios=None):
            matricula = validarIdTexto(entryMat.get(), "ID del alumno")
            nombre = validarNombrePersona(entryNom.get(), "Nombre del alumno")
            semestreNum = parsearEnteroTexto(entrySem.get(), "Semestre", 1, maxSemestre, SemestreFueraDeRangoError)
            carrera = validarAreaTexto(comboCarr.get())
            subgrupoVal = validarSubgrupoArea(carrera, comboSubgrupo.get(), True)
            gestionTxt = validarTextoBasico(entryGestion.get(), "Rol o gestion", 3, 60)

            actNum = parsearEnteroTexto(entryAct.get(), "Actividades", 0, maxActividades)
            mentNum = parsearEnteroTexto(entryMent.get(), "Mentorias", 0, maxMentorias)
            obligNum = parsearEnteroTexto(entryOblig.get(), "Actividades obligatorias", 0, maxObligatorias)
            repNum = parsearEnteroTexto(entryRep.get(), "Materias reprobadas", 0, maxReprobadas)

            semIn = comboSeminario.get().strip()
            if semIn not in ["Si", "No"]:
                raise BooleanoInvalidoError("Debes seleccionar Si o No en Seminario")
            seminarioBool = True if semIn == "Si" else False

            tallVal = parsearEnteroTexto(entryTalleres.get(), "Talleres", 0, maxSubActividades)
            vfiVal = parsearEnteroTexto(entryVfi.get(), "Actividades VFI", 0, maxSubActividades)
            desVal = parsearEnteroTexto(entryDesPers.get(), "Desarrollo personal", 0, maxSubActividades)
            intVal = parsearEnteroTexto(entryInteg.get(), "Integracion", 0, maxSubActividades)

            tipoSel = comboTipo.get().strip()
            if tipoSel == "GestionRe":
                periodoTxt = validarPeriodoTexto(entryPeriodo.get())
                estatusTxt = validarEstatusGestion(comboEstatus.get())
                semAdminNum = parsearEnteroTexto(entrySemAdmin.get(), "Semestres como administrador", 1, 2, SemestresAdminInvalidoError)
                reqs = [] if requisitosPrevios is None else requisitosPrevios
                return GestionRe(
                    matricula,
                    nombre,
                    semestreNum,
                    carrera,
                    gestionTxt,
                    repNum,
                    periodoTxt,
                    estatusTxt,
                    semAdminNum,
                    actNum,
                    mentNum,
                    obligNum,
                    requisitos=reqs,
                    seminario=seminarioBool,
                    talleres=tallVal,
                    actividadesVfi=vfiVal,
                    desarrolloPersonal=desVal,
                    integracion=intVal,
                    subgrupo=subgrupoVal
                )
            return Alumno(
                matricula,
                nombre,
                semestreNum,
                carrera,
                gestionTxt,
                repNum,
                actNum,
                mentNum,
                obligNum,
                seminarioBool,
                talleres=tallVal,
                actividadesVfi=vfiVal,
                desarrolloPersonal=desVal,
                integracion=intVal,
                subgrupo=subgrupoVal
            )

        def guardarAlumno():
            try:
                nuevoAlumno = construirObjetoDesdeFormulario()
                estadoCoord["actual"].darDeAltaAlumno(nuevoAlumno)
                etiquetaSaludo.config(
                    text=f"Registrado: {nuevoAlumno.getNombre()} | ID: {nuevoAlumno.getId()} | {nuevoAlumno.getAreaCompleta()}",
                    fg="#117A76"
                )
                messagebox.showinfo("Registro exitoso", "Datos guardados correctamente en la base de datos SQLite")
                abrirVentanaResumen("Resumen del registro", [nuevoAlumno])
                limpiarCampos()
            except (SistemaREError, ValueError, TypeError, sqlite3.Error, OSError) as e:
                enviarError(e, "GUI")
                messagebox.showerror("Error de validacion o registro", str(e))
            except Exception as e:
                enviarError(e, "GUI")
                messagebox.showerror("Error inesperado", str(e))

        def buscarAlumnoGui():
            try:
                alumno = estadoCoord["actual"].mostrarAlumno(entryMat.get())
                cargarAlumnoEnFormulario(alumno)
                etiquetaSaludo.config(text=alumno.mostrarProgreso(), fg="#1B2631")
                abrirVentanaResumen("Alumno Encontrado", [alumno])
            except (SistemaREError, ValueError, TypeError, sqlite3.Error) as e:
                enviarError(e, "GUI")
                messagebox.showerror("Error de busqueda", str(e))
            except Exception as e:
                enviarError(e, "GUI")
                messagebox.showerror("Error inesperado", str(e))

        def actualizarAlumnoGui():
            try:
                matricula = validarIdTexto(entryMat.get(), "ID del alumno")
                existente = estadoCoord["actual"].buscarAlumnoPorId(matricula)
                requisitosPrevios = existente.getRequisitos() if isinstance(existente, GestionRe) else None
                alumnoEditado = construirObjetoDesdeFormulario(requisitosPrevios)
                mismoDesglose = (
                    existente.getUsaDesglose() == alumnoEditado.getUsaDesglose() and
                    existente.getTalleres() == alumnoEditado.getTalleres() and
                    existente.getActividadesVfi() == alumnoEditado.getActividadesVfi() and
                    existente.getDesarrolloPersonal() == alumnoEditado.getDesarrolloPersonal() and
                    existente.getIntegracion() == alumnoEditado.getIntegracion() and
                    existente.getSubgrupo() == alumnoEditado.getSubgrupo()
                )
                if str(existente) == str(alumnoEditado) and mismoDesglose:
                    raise CambioSinModificacionesError("No realizaste cambios en los datos del alumno")
                estadoCoord["actual"].actualizarAlumno(alumnoEditado)
                etiquetaSaludo.config(
                    text=f"Actualizado: {alumnoEditado.getNombre()} | ID: {alumnoEditado.getId()}",
                    fg="#117A76"
                )
                messagebox.showinfo("Actualizacion exitosa", f"Datos de {alumnoEditado.getId()} actualizados en SQLite")
                abrirVentanaResumen("Alumno Actualizado", [alumnoEditado])
            except (SistemaREError, ValueError, TypeError, sqlite3.Error, OSError) as e:
                enviarError(e, "GUI")
                messagebox.showerror("Error al actualizar", str(e))
            except Exception as e:
                enviarError(e, "GUI")
                messagebox.showerror("Error inesperado", str(e))

        frameAcciones = tk.Frame(frameContenido, bg="beige")
        frameAcciones.pack(pady=10)
        if modo == "nuevo":
            tk.Button(frameAcciones, text="Guardar Alumno", command=guardarAlumno, bg="#117A76", fg="white", font=("Arial", 10, "bold"), width=18, pady=4).grid(row=0, column=0, padx=6)
            tk.Button(frameAcciones, text="Limpiar Campos", command=limpiarCampos, bg="#7F8C8D", fg="white", font=("Arial", 10, "bold"), width=16, pady=4).grid(row=0, column=1, padx=6)
        else:
            tk.Button(frameAcciones, text="Buscar por ID", command=buscarAlumnoGui, bg="#1F618D", fg="white", font=("Arial", 10, "bold"), width=15, pady=4).grid(row=0, column=0, padx=6)
            tk.Button(frameAcciones, text="Guardar Cambios", command=actualizarAlumnoGui, bg="#1E8449", fg="white", font=("Arial", 10, "bold"), width=16, pady=4).grid(row=0, column=1, padx=6)
            tk.Button(frameAcciones, text="Limpiar Campos", command=limpiarCampos, bg="#7F8C8D", fg="white", font=("Arial", 10, "bold"), width=14, pady=4).grid(row=0, column=2, padx=6)

        if idInicial:
            try:
                alInicial = estadoCoord["actual"].buscarAlumnoPorId(idInicial)
                cargarAlumnoEnFormulario(alInicial)
            except SistemaREError:
                pass

    def mostrarVistaBaja():
        limpiarContenedor()
        etiquetaSaludo.config(text="Modulo Alumnos: Dar de Baja Permanente", fg="#A93226")

        barraNav = tk.Frame(frameContenido, bg="beige")
        barraNav.pack(fill="x", pady=(0, 8))
        tk.Label(barraNav, text="Inicio > Gestion de Alumnos > Dar de Baja", bg="beige", fg="#A93226", font=("Helvetica", 10, "bold")).pack(side="left")
        tk.Button(barraNav, text="<- Volver a Gestion de Alumnos", command=mostrarSubmenuAlumnos, bg="#566573", fg="white", font=("Arial", 8, "bold")).pack(side="right")

        frameBuscar = tk.Frame(frameContenido, bg="beige")
        frameBuscar.pack(fill="x", pady=6)
        tk.Label(frameBuscar, text="ID del Alumno a dar de baja:", bg="beige", font=("Helvetica", 10, "bold")).pack(side="left", padx=(0, 8))
        entryIdBaja = tk.Entry(frameBuscar, font=("Helvetica", 10), width=18)
        entryIdBaja.pack(side="left", padx=6)

        lblInfoBaja = tk.Label(frameContenido, text="Selecciona un alumno de la lista o escribe su ID", bg="#FDEDEC", fg="#922B21", font=("Helvetica", 9, "bold"), pady=6)
        lblInfoBaja.pack(fill="x", pady=6)

        listaBaja = tk.Listbox(frameContenido, font=("Consolas", 9), height=11)
        listaBaja.pack(fill="both", expand=True, pady=6)

        alumnosRef = {"lista": []}

        def refrescarListaBaja():
            listaBaja.delete(0, "end")
            alumnosRef["lista"] = estadoCoord["actual"].obtenerTodosLosAlumnos()
            for al in alumnosRef["lista"]:
                listaBaja.insert("end", f"{al.getId()} | {al.getNombre()} | Sem {al.getSemestre()} | {al.getAreaCompleta()}")

        def alSeleccionarBaja(evento=None):
            sel = listaBaja.curselection()
            if len(sel) == 0:
                return
            alSel = alumnosRef["lista"][sel[0]]
            entryIdBaja.delete(0, "end")
            entryIdBaja.insert(0, alSel.getId())
            lblInfoBaja.config(text=f"Seleccionado: {alSel.getNombre()} ({alSel.getId()}) - {alSel.getAreaCompleta()}")

        listaBaja.bind("<<ListboxSelect>>", alSeleccionarBaja)
        refrescarListaBaja()

        def ejecutarBaja():
            try:
                matricula = validarIdTexto(entryIdBaja.get(), "ID del alumno")
                alumno = estadoCoord["actual"].buscarAlumnoPorId(matricula)
                confirmar = messagebox.askyesno(
                    "Confirmar baja",
                    f"¿Deseas eliminar permanentemente a {alumno.getNombre()} (ID: {matricula}) de SQLite?"
                )
                if not confirmar:
                    return
                estadoCoord["actual"].darDeBajaAlumno(matricula)
                etiquetaSaludo.config(text=f"Alumno {matricula} eliminado de SQLite", fg="#A93226")
                messagebox.showinfo("Baja exitosa", f"Alumno con ID {matricula} eliminado")
                entryIdBaja.delete(0, "end")
                lblInfoBaja.config(text="Registro eliminado correctamente")
                refrescarListaBaja()
            except (SistemaREError, ValueError, TypeError, sqlite3.Error) as e:
                enviarError(e, "GUI_Baja")
                messagebox.showerror("Error al dar de baja", str(e))

        tk.Button(frameBuscar, text="Eliminar Permanente", command=ejecutarBaja, bg="#A93226", fg="white", font=("Arial", 9, "bold"), width=18).pack(side="left", padx=8)

    def mostrarVistaVerificacion():
        limpiarContenedor()
        etiquetaSaludo.config(text="Seguimiento: Verificacion Individual de Graduacion", fg="#117A76")

        barraNav = tk.Frame(frameContenido, bg="beige")
        barraNav.pack(fill="x", pady=(0, 8))
        tk.Label(barraNav, text="Inicio > Seguimiento y Requisitos > Verificar Graduacion", bg="beige", fg="#117A76", font=("Helvetica", 10, "bold")).pack(side="left")
        tk.Button(barraNav, text="<- Volver a Seguimiento", command=mostrarSubmenuRequisitos, bg="#566573", fg="white", font=("Arial", 8, "bold")).pack(side="right")

        frameBus = tk.Frame(frameContenido, bg="beige")
        frameBus.pack(fill="x", pady=6)
        tk.Label(frameBus, text="ID del Alumno:", bg="beige", font=("Helvetica", 10, "bold")).pack(side="left", padx=(0, 8))
        entryIdVer = tk.Entry(frameBus, font=("Helvetica", 10), width=18)
        entryIdVer.pack(side="left", padx=6)

        cajaDetalle = tk.Text(frameContenido, font=("Consolas", 10), height=15, wrap="word")
        cajaDetalle.pack(fill="both", expand=True, pady=8)
        cajaDetalle.config(state="disabled")

        def verificarAlumnoIndividual():
            try:
                al = estadoCoord["actual"].buscarAlumnoPorId(entryIdVer.get())
                cumplidos = al.obtenerCumplidos()
                pendientes = al.obtenerPendientes()
                graduable = al.verificarGraduacion() == "S"
                cajaDetalle.config(state="normal")
                cajaDetalle.delete("1.0", "end")
                cajaDetalle.insert("end", f"ALUMNO: {al.getNombre()} (ID: {al.getId()})\n")
                cajaDetalle.insert("end", f"Semestre: {al.getSemestre()} | Grupo: {al.getAreaCompleta()} | Gestion: {al.getGestionRe()}\n")
                cajaDetalle.insert("end", f"Porcentaje de Avance: {int(al.calcularPorcentajeAvance())}%\n")
                cajaDetalle.insert("end", f"DICTAMEN DE GRADUACION: {'APROBADO PARA GRADUARSE' if graduable else 'CON REQUISITOS PENDIENTES'}\n")
                cajaDetalle.insert("end", "\n--- REQUISITOS CUMPLIDOS ---\n")
                if len(cumplidos) == 0:
                    cajaDetalle.insert("end", "  (Ninguno aun)\n")
                else:
                    for c in cumplidos:
                        cajaDetalle.insert("end", f"  [OK] {c}\n")
                cajaDetalle.insert("end", "\n--- REQUISITOS PENDIENTES ---\n")
                if len(pendientes) == 0:
                    cajaDetalle.insert("end", "  (Ninguno, todo completo)\n")
                else:
                    for p in pendientes:
                        cajaDetalle.insert("end", f"  [PENDIENTE] {p}\n")
                cajaDetalle.config(state="disabled")
            except (SistemaREError, ValueError, TypeError) as e:
                enviarError(e, "GUI_Verificar")
                messagebox.showerror("Error", str(e))

        tk.Button(frameBus, text="Evaluar Alumno", command=verificarAlumnoIndividual, bg="#117A76", fg="white", font=("Arial", 9, "bold"), width=15).pack(side="left", padx=8)

    def mostrarVistaFiltros():
        limpiarContenedor()
        etiquetaSaludo.config(text="Consultas: Filtrar Alumnos por Grupo, Estado o Club", fg="#117A76")

        barraNav = tk.Frame(frameContenido, bg="beige")
        barraNav.pack(fill="x", pady=(0, 8))
        tk.Label(barraNav, text="Inicio > Consultas y Reportes > Filtrar por Grupo o Club", bg="beige", fg="#117A76", font=("Helvetica", 10, "bold")).pack(side="left")
        tk.Button(barraNav, text="<- Volver a Consultas", command=mostrarSubmenuConsultas, bg="#566573", fg="white", font=("Arial", 8, "bold")).pack(side="right")

        frameFiltros = tk.Frame(frameContenido, bg="beige")
        frameFiltros.pack(fill="x", pady=8)

        tk.Label(frameFiltros, text="Grupo:", bg="beige", font=("Helvetica", 10, "bold")).grid(row=0, column=0, padx=6, pady=4)
        comboGrupoF = ttk.Combobox(frameFiltros, values=areasValidas, state="readonly", width=24)
        comboGrupoF.set("Clubs Anahuac")
        comboGrupoF.grid(row=0, column=1, padx=6, pady=4)

        tk.Label(frameFiltros, text="Club / Estado:", bg="beige", font=("Helvetica", 10, "bold")).grid(row=0, column=2, padx=6, pady=4)
        comboSubF = ttk.Combobox(frameFiltros, values=["Todos"] + clubsAnahuacValidos, state="readonly", width=22)
        comboSubF.set("Todos")
        comboSubF.grid(row=0, column=3, padx=6, pady=4)

        def alCambiarGrupoFiltro(evento=None):
            g = comboGrupoF.get().strip()
            if g == "Clubs Anahuac":
                comboSubF.config(state="readonly", values=["Todos"] + clubsAnahuacValidos)
                comboSubF.set("Todos")
            elif g == "Asociaciones por estado":
                comboSubF.config(state="readonly", values=["Todos"] + asociacionesPorEstadoValidas)
                comboSubF.set("Todos")
            else:
                comboSubF.config(state="normal", values=["Todos"])
                comboSubF.set("Todos")
                comboSubF.config(state="disabled")

        comboGrupoF.bind("<<ComboboxSelected>>", alCambiarGrupoFiltro)

        def ejecutarFiltro():
            try:
                filtrados = estadoCoord["actual"].filtrarAlumnosPorGrupo(comboGrupoF.get(), comboSubF.get())
                abrirVentanaResumen(f"Filtro: {comboGrupoF.get()} ({comboSubF.get()})", filtrados)
            except (SistemaREError, ValueError) as e:
                enviarError(e, "GUI_Filtro")
                messagebox.showerror("Error", str(e))

        tk.Button(frameFiltros, text="Consultar", command=ejecutarFiltro, bg="#117A76", fg="white", font=("Arial", 10, "bold"), width=14).grid(row=0, column=4, padx=10, pady=4)

    def mostrarSubmenuAlumnos():
        limpiarContenedor()
        etiquetaSaludo.config(text="Submenu: Gestion de Alumnos", fg="#117A76")

        barraNav = tk.Frame(frameContenido, bg="beige")
        barraNav.pack(fill="x", pady=(0, 12))
        tk.Label(barraNav, text="Inicio > Gestion de Alumnos", bg="beige", fg="#117A76", font=("Helvetica", 11, "bold")).pack(side="left")
        tk.Button(barraNav, text="<- Volver al Menu Principal", command=mostrarMenuPrincipal, bg="#566573", fg="white", font=("Arial", 9, "bold")).pack(side="right")

        frameOpciones = tk.Frame(frameContenido, bg="beige")
        frameOpciones.pack(pady=15)

        def irRegistrar():
            mostrarFormularioAlumno("nuevo")

        def irActualizar():
            mostrarFormularioAlumno("editar")

        tk.Button(frameOpciones, text="1. Registrar Nuevo Alumno / GestionRe", command=irRegistrar, bg="#117A76", fg="white", font=("Arial", 11, "bold"), width=36, pady=12).grid(row=0, column=0, padx=10, pady=8)
        tk.Button(frameOpciones, text="2. Buscar y Actualizar Alumno", command=irActualizar, bg="#1E8449", fg="white", font=("Arial", 11, "bold"), width=36, pady=12).grid(row=0, column=1, padx=10, pady=8)
        tk.Button(frameOpciones, text="3. Dar de Baja Permanente", command=mostrarVistaBaja, bg="#A93226", fg="white", font=("Arial", 11, "bold"), width=36, pady=12).grid(row=1, column=0, padx=10, pady=8)
        tk.Button(frameOpciones, text="4. Ver Todos los Alumnos", command=mostrarTodosGui, bg="#1F618D", fg="white", font=("Arial", 11, "bold"), width=36, pady=12).grid(row=1, column=1, padx=10, pady=8)

    def mostrarSubmenuRequisitos():
        limpiarContenedor()
        etiquetaSaludo.config(text="Submenu: Seguimiento y Requisitos", fg="#117A76")

        barraNav = tk.Frame(frameContenido, bg="beige")
        barraNav.pack(fill="x", pady=(0, 12))
        tk.Label(barraNav, text="Inicio > Seguimiento y Requisitos", bg="beige", fg="#117A76", font=("Helvetica", 11, "bold")).pack(side="left")
        tk.Button(barraNav, text="<- Volver al Menu Principal", command=mostrarMenuPrincipal, bg="#566573", fg="white", font=("Arial", 9, "bold")).pack(side="right")

        frameOpciones = tk.Frame(frameContenido, bg="beige")
        frameOpciones.pack(pady=15)

        def irActualizarProgreso():
            mostrarFormularioAlumno("editar")

        tk.Button(frameOpciones, text="1. Verificar Graduacion Individual", command=mostrarVistaVerificacion, bg="#117A76", fg="white", font=("Arial", 11, "bold"), width=36, pady=12).grid(row=0, column=0, padx=10, pady=8)
        tk.Button(frameOpciones, text="2. Actualizar Avance del Alumno", command=irActualizarProgreso, bg="#1E8449", fg="white", font=("Arial", 11, "bold"), width=36, pady=12).grid(row=0, column=1, padx=10, pady=8)
        tk.Button(frameOpciones, text="3. Requisitos Especiales (GestionRe)", command=abrirVentanaRequisitos, bg="#1F618D", fg="white", font=("Arial", 11, "bold"), width=36, pady=12).grid(row=1, column=0, columnspan=2, padx=10, pady=8)

    def mostrarSubmenuConsultas():
        limpiarContenedor()
        etiquetaSaludo.config(text="Submenu: Consultas y Reportes", fg="#117A76")

        barraNav = tk.Frame(frameContenido, bg="beige")
        barraNav.pack(fill="x", pady=(0, 12))
        tk.Label(barraNav, text="Inicio > Consultas y Reportes", bg="beige", fg="#117A76", font=("Helvetica", 11, "bold")).pack(side="left")
        tk.Button(barraNav, text="<- Volver al Menu Principal", command=mostrarMenuPrincipal, bg="#566573", fg="white", font=("Arial", 9, "bold")).pack(side="right")

        frameOpciones = tk.Frame(frameContenido, bg="beige")
        frameOpciones.pack(pady=15)

        tk.Button(frameOpciones, text="1. Mostrar Todos los Alumnos", command=mostrarTodosGui, bg="#117A76", fg="white", font=("Arial", 11, "bold"), width=36, pady=12).grid(row=0, column=0, padx=10, pady=8)
        tk.Button(frameOpciones, text="2. Alumnos con Cumplimiento Completo", command=mostrarCumplimientoGui, bg="#1E8449", fg="white", font=("Arial", 11, "bold"), width=36, pady=12).grid(row=0, column=1, padx=10, pady=8)
        tk.Button(frameOpciones, text="3. Alumnos con Requisitos Pendientes", command=mostrarPendientesGui, bg="#B9770E", fg="white", font=("Arial", 11, "bold"), width=36, pady=12).grid(row=1, column=0, padx=10, pady=8)
        tk.Button(frameOpciones, text="4. Filtrar por Grupo, Estado o Club", command=mostrarVistaFiltros, bg="#1F618D", fg="white", font=("Arial", 11, "bold"), width=36, pady=12).grid(row=1, column=1, padx=10, pady=8)

    def mostrarSubmenuAreasYClubs():
        limpiarContenedor()
        etiquetaSaludo.config(text="Submenu: Areas, Asociaciones por Estado y Clubs Anahuac", fg="#117A76")

        barraNav = tk.Frame(frameContenido, bg="beige")
        barraNav.pack(fill="x", pady=(0, 12))
        tk.Label(barraNav, text="Inicio > Areas, Estados y Clubs", bg="beige", fg="#117A76", font=("Helvetica", 11, "bold")).pack(side="left")
        tk.Button(barraNav, text="<- Volver al Menu Principal", command=mostrarMenuPrincipal, bg="#566573", fg="white", font=("Arial", 9, "bold")).pack(side="right")

        frameOpciones = tk.Frame(frameContenido, bg="beige")
        frameOpciones.pack(pady=15)

        def verAreas():
            abrirExploradorGrupos("areas")

        def verEstados():
            abrirExploradorGrupos("estados")

        def verClubs():
            abrirExploradorGrupos("clubs")

        tk.Button(frameOpciones, text="1. Ver Grupos de Relaciones Estudiantiles", command=verAreas, bg="#117A76", fg="white", font=("Arial", 11, "bold"), width=40, pady=12).grid(row=0, column=0, padx=10, pady=8)
        tk.Button(frameOpciones, text="2. Ver Asociaciones por Estado (6)", command=verEstados, bg="#1F618D", fg="white", font=("Arial", 11, "bold"), width=40, pady=12).grid(row=1, column=0, padx=10, pady=8)
        tk.Button(frameOpciones, text="3. Ver Clubs Anahuac (Otra Lista: 5 Clubs)", command=verClubs, bg="#5B2C6F", fg="white", font=("Arial", 11, "bold"), width=40, pady=12).grid(row=2, column=0, padx=10, pady=8)

    def mostrarSubmenuAdmin():
        limpiarContenedor()
        etiquetaSaludo.config(text="Submenu: Administracion y Base de Datos SQLite", fg="#117A76")

        barraNav = tk.Frame(frameContenido, bg="beige")
        barraNav.pack(fill="x", pady=(0, 12))
        tk.Label(barraNav, text="Inicio > Administracion y SQLite", bg="beige", fg="#117A76", font=("Helvetica", 11, "bold")).pack(side="left")
        tk.Button(barraNav, text="<- Volver al Menu Principal", command=mostrarMenuPrincipal, bg="#566573", fg="white", font=("Arial", 9, "bold")).pack(side="right")

        frameOpciones = tk.Frame(frameContenido, bg="beige")
        frameOpciones.pack(pady=15)

        tk.Button(frameOpciones, text="1. Administrar Coordinadores (SQLite)", command=abrirVentanaCoordinador, bg="#5B2C6F", fg="white", font=("Arial", 11, "bold"), width=36, pady=12).grid(row=0, column=0, padx=10, pady=8)
        tk.Button(frameOpciones, text="2. Ver Historial de Acciones (SQLite)", command=verHistorialGui, bg="#1F618D", fg="white", font=("Arial", 11, "bold"), width=36, pady=12).grid(row=0, column=1, padx=10, pady=8)
        tk.Button(frameOpciones, text="3. Ver Bitacora de Errores (SQLite)", command=verLogsErroresGui, bg="#B9770E", fg="white", font=("Arial", 11, "bold"), width=36, pady=12).grid(row=1, column=0, padx=10, pady=8)
        tk.Button(frameOpciones, text="4. Exportar Respaldo TXT", command=exportarRespaldoTxtGui, bg="#117A76", fg="white", font=("Arial", 11, "bold"), width=36, pady=12).grid(row=1, column=1, padx=10, pady=8)

    def mostrarMenuPrincipal():
        limpiarContenedor()
        etiquetaSaludo.config(text="Menu Principal: Selecciona un modulo para continuar", fg="#2C3E50")

        todos = estadoCoord["actual"].obtenerTodosLosAlumnos()
        cumplen = estadoCoord["actual"].mostrarAlumnosCumplimiento()
        pendientes = estadoCoord["actual"].mostrarAlumnosConRequisitosPendientes()
        totalGestion = 0
        for al in todos:
            if isinstance(al, GestionRe):
                totalGestion += 1

        frameStats = tk.Frame(frameContenido, bg="beige")
        frameStats.pack(fill="x", pady=8)
        frameStats.columnconfigure(0, weight=1)
        frameStats.columnconfigure(1, weight=1)
        frameStats.columnconfigure(2, weight=1)
        frameStats.columnconfigure(3, weight=1)

        tk.Label(frameStats, text=f"Total Alumnos\n{len(todos)}", bg="#D1F2EB", fg="#0E5A56", font=("Arial", 10, "bold"), pady=8).grid(row=0, column=0, sticky="ew", padx=4)
        tk.Label(frameStats, text=f"Cumplen\n{len(cumplen)}", bg="#D4EFDF", fg="#196F3D", font=("Arial", 10, "bold"), pady=8).grid(row=0, column=1, sticky="ew", padx=4)
        tk.Label(frameStats, text=f"Pendientes\n{len(pendientes)}", bg="#FADBD8", fg="#922B21", font=("Arial", 10, "bold"), pady=8).grid(row=0, column=2, sticky="ew", padx=4)
        tk.Label(frameStats, text=f"GestionRe\n{totalGestion}", bg="#D6EAF8", fg="#1B4F72", font=("Arial", 10, "bold"), pady=8).grid(row=0, column=3, sticky="ew", padx=4)

        frameGrid = tk.Frame(frameContenido, bg="beige")
        frameGrid.pack(pady=14)

        tk.Button(frameGrid, text="Gestion de Alumnos\n(Altas, Busqueda, Edicion y Bajas)", command=mostrarSubmenuAlumnos, bg="#117A76", fg="white", font=("Arial", 11, "bold"), width=32, height=3).grid(row=0, column=0, padx=10, pady=8)
        tk.Button(frameGrid, text="Seguimiento y Requisitos\n(Graduacion, Avance y GestionRe)", command=mostrarSubmenuRequisitos, bg="#1E8449", fg="white", font=("Arial", 11, "bold"), width=32, height=3).grid(row=0, column=1, padx=10, pady=8)
        tk.Button(frameGrid, text="Consultas y Reportes\n(Listados, Cumplidos y Filtros)", command=mostrarSubmenuConsultas, bg="#1F618D", fg="white", font=("Arial", 11, "bold"), width=32, height=3).grid(row=1, column=0, padx=10, pady=8)
        tk.Button(frameGrid, text="Areas, Estados y Clubs\n(Asociaciones por Estado y Clubs)", command=mostrarSubmenuAreasYClubs, bg="#5B2C6F", fg="white", font=("Arial", 11, "bold"), width=32, height=3).grid(row=1, column=1, padx=10, pady=8)
        tk.Button(frameGrid, text="Administracion y SQLite\n(Coordinadores, Historial y Logs)", command=mostrarSubmenuAdmin, bg="#566573", fg="white", font=("Arial", 11, "bold"), width=32, height=3).grid(row=2, column=0, padx=10, pady=8)
        tk.Button(frameGrid, text="Cerrar Sesion\n(Cambiar de Coordinador)", command=cerrarSesion, bg="#B9770E", fg="white", font=("Arial", 11, "bold"), width=32, height=3).grid(row=2, column=1, padx=10, pady=8)

    barraMenu = tk.Menu(ventana)
    ventana.config(menu=barraMenu)

    menuOpciones = tk.Menu(barraMenu, tearoff=0)
    barraMenu.add_cascade(label="Navegacion", menu=menuOpciones)
    menuOpciones.add_command(label="Menu Principal", command=mostrarMenuPrincipal)
    menuOpciones.add_command(label="Gestion de Alumnos", command=mostrarSubmenuAlumnos)
    menuOpciones.add_command(label="Seguimiento y Requisitos", command=mostrarSubmenuRequisitos)
    menuOpciones.add_command(label="Consultas y Reportes", command=mostrarSubmenuConsultas)
    menuOpciones.add_command(label="Areas, Estados y Clubs", command=mostrarSubmenuAreasYClubs)
    menuOpciones.add_command(label="Administracion y SQLite", command=mostrarSubmenuAdmin)
    menuOpciones.add_separator()
    menuOpciones.add_command(label="Cerrar Sesion", command=cerrarSesion)
    menuOpciones.add_command(label="Salir del Sistema", command=salirDelSistema)

    mostrarMenuPrincipal()
    ventana.mainloop()
    return accionSalida["cerrarSesion"]


def iniciarInterfaz():
    ejecutar = True
    while ejecutar:
        coordAutenticado = mostrarVentanaLogin()
        if coordAutenticado is None:
            ejecutar = False
        else:
            deseaVolverLogin = mostrarVentanaPrincipal(coordAutenticado)
            if not deseaVolverLogin:
                ejecutar = False


if __name__ == "__main__":
    iniciarInterfaz()
