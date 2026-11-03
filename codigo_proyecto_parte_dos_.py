#segunda entrega de proyecto final de python

from pathlib import Path
import sqlite3
from datetime import datetime

#librerias

#Raul Isaac Santos Ruiz
#Silvana De Alba Uribe

#v1.2
indiceWhile = 1
AreaRe = [
    "ASUA",
    "FESAL",
    "ADEFA",
    "Presidencias ASUA",
    "Sociedades de alumnos",
    "Asociaciones por estado",
    "Clubs Anahuac"
]
cuentas = []
coordinadorActual = ""

registrado = 1

limiteActividades = 5
limiteMentorias = 3
limiteActividadesObligatorias = 2

#implementacion de clases

class AreaRE:
    def __init__(self, idArea, nombreArea):
        if not str(idArea).strip():
            raise ValueError("El ID del area no puede estar vacio")
        if not str(nombreArea).strip():
            raise ValueError("El nombre del area no puede estar vacio")
        
        self._idArea = idArea
        self._nombreArea = nombreArea
        self._alumnos = []

    def getIdArea(self):
        return self._idArea

    def getNombreArea(self):
        return self._nombreArea

    def getAlumnos(self):
        return self._alumnos

    def agregarAlumno(self, alumno):
        if alumno is None:
            raise ValueError("El alumno no existe")
        self._alumnos.append(alumno)

    def eliminarAlumno(self, idAlumno):
        for a in self._alumnos:
            if a.getId() == idAlumno:
                self._alumnos.remove(a)
                return True
        raise ValueError(f"El alumno con ID {idAlumno} no se encuentra en el grupo {self._nombreArea}")



    def __str__(self):
        return f"ID {self._idArea} | Grupo: {self._nombreArea} | Inscritos: {len(self._alumnos)}"

    #la clase AreaRe es una lista en donde agarrar para que un alumno pueda pertenecer a 
    #solo uno un alumno puede pertenecer a una area y una area puede tener muchos alumnos


class ASUA(AreaRE):
    def __init__(self, idArea=1, nombreArea="ASUA"):
        super().__init__(idArea, nombreArea)

    def obtenerTipoGrupo(self):
        return "Accion Social Universidad Anahuac"


class FESAL(AreaRE):
    def __init__(self, idArea=2, nombreArea="FESAL"):
        super().__init__(idArea, nombreArea)

    def obtenerTipoGrupo(self):
        return "Federacion de Sociedades de Alumnos"


class ADEFA(AreaRE):
    def __init__(self, idArea=3, nombreArea="ADEFA"):
        super().__init__(idArea, nombreArea)

    def obtenerTipoGrupo(self):
        return "Asociacion de Estudiantes Foraneos Anahuac"


class PresidenciasASUA(ASUA):
    def __init__(self, idArea=4, nombreArea="Presidencias ASUA"):
        super().__init__(idArea, nombreArea)

    def obtenerTipoGrupo(self):
        return "Direccion y Presidencias ASUA"


class SociedadesDeAlumnos(AreaRE):
    def __init__(self, idArea=5, nombreArea="Sociedades de alumnos",carrera="General"):
        super().__init__(idArea, nombreArea)

        if not str(carrera).strip():
            raise ValueError("La carrera de la sociedad de alumnos no puede estar vacia")
        self._facultad = carrera

    def obtenerTipoGrupo(self):
        return f"Sociedad de Alumnos ({self._facultad})"


class AsociacionesPorEstado(AreaRE):
    def __init__(self, idArea=6, nombreArea="Asociaciones por estado",estadoRepresentado="Queretaro"):
        super().__init__(idArea, nombreArea)
        if not str(estadoRepresentado).strip():
            raise ValueError("El estado representado no puede estar vacio")
        self._estadoRepresentado = estadoRepresentado

    def obtenerTipoGrupo(self):
        return f"Asociacion Estatal ({self._estadoRepresentado})"


class ClubsAnahuac(AreaRE):
    def __init__(self, idArea=7, nombreArea="Clubs Anahuac",categoriaClub="CategoriaNombre"):
        super().__init__(idArea, nombreArea)
        if not str(categoriaClub).strip():
            raise ValueError("La categoria del club no puede estar vacia")
        self._categoriaClub = categoriaClub

    def obtenerTipoGrupo(self):
        return f"Club Universitario ({self._categoriaClub})"


gruposDisponibles = {
    1: ASUA(),
    2: FESAL(),
    3: ADEFA(),
    4: PresidenciasASUA(),
    5: SociedadesDeAlumnos(),
    6: AsociacionesPorEstado(),
    7: ClubsAnahuac()
}


class Coordinador:
    def __init__(self, idNombre, contrasena, nombre, catalogoAlumnos, area="General", anioAdministracion=2026):
        if not str(idNombre).strip():
            raise ValueError("El ID del coordinador no puede estar vacio")
        if not str(nombre).strip():
            raise ValueError("El nombre del coordinador no puede estar vacio")
        if len(str(contrasena).strip()) < 4:
            raise ValueError("La contraseña del coordinador debe tener al menos 4 caracteres")
        if int(anioAdministracion) < 2000 or int(anioAdministracion) > 2100:
            raise ValueError("El año de administracion no es valido")
        self._idNombre = str(idNombre).strip()
        self._contrasena = str(contrasena).strip()
        self._nombre = str(nombre).strip()
        self._catalogoAlumnos = catalogoAlumnos if catalogoAlumnos is not None else []
        self._area = str(area).strip() if str(area).strip() else "General"
        self._anioAdministracion = int(anioAdministracion)
    #un area puede tener de 1 a muchos coordinadores por area

    #aqui a funciona como verdadero o falso
    def darDeAltaAlumno(self, alumno):
        if alumno is None:
            raise ValueError("No se puede registrar un alumno vacio")
        for existente in self._catalogoAlumnos:
            if existente.getId() == alumno.getId():
                raise ValueError(f"Ya existe un alumno registrado con el ID {alumno.getId()}")
        self._catalogoAlumnos.append(alumno)
        a = True
        return a

    #los coordinadores pueden dar de alta a un alumno
    #aqui igual 

    def darDeBajaAlumno(self, idAlumno):
        if not str(idAlumno).strip():
            raise ValueError("Debe proporcionar un ID valido para dar de baja")
        for alumno in self._catalogoAlumnos:
            if alumno.getId() == str(idAlumno).strip():
                self._catalogoAlumnos.remove(alumno)
                a = True
                return a
        raise ValueError(f"No se encontro al alumno con ID {idAlumno}")
    #los coordinadores pueden dar de baja a un alumno

    def mostrarAlumno(self, idAlumno):
        if not str(idAlumno).strip():
            raise ValueError("El ID a buscar no puede estar vacio")
        for alumno in self._catalogoAlumnos:
            if alumno.getId() == str(idAlumno).strip():
                print(alumno)
                return alumno
        raise ValueError(f"Alumno {idAlumno} no encontrado")
    #los coordinadores puedes mediante codigo mostrar a un alumno en concreto

    def mostrarAlumnosCumplimiento(self):
        lista = []
        for a in self._catalogoAlumnos:
            if a.verificarGraduacion() == "S":
                lista.append(a)
        return lista
    #los coordinadores puedes checar el progreso de todos los alumnos 

    def mostrarAlumnosConRequisitosPendientes(self):
        lista = []
        for a in self._catalogoAlumnos:
            if a.verificarGraduacion() != "S":
                lista.append(a)
        return lista
    #los coordinadores puedes verificar si un alumno tiene requisitos pendientes

    def obtenerTodosLosAlumnos(self):
        lista = self._catalogoAlumnos
        return lista
    #los coordinadores puedes obtener todos los alumnos

    def __str__(self):
        return f"Coordinador: {self._nombre} | Area: {self._area} | Administracion: {self._anioAdministracion}"
    #cuando se pone esto el coordinador debe de aparecer que area dirije y su administracion de que año es


class Alumno:
    #se inicializa si o si con id nombre semestre area y gestion
    def __init__(self, idAlumno, nombre, semestre, areaDeRe, gestion, materiasReprobadas, actividades=0, mentorias=0, actividadesObligatorias=0):
        if not str(idAlumno).strip():
            raise ValueError("El ID del alumno no puede estar vacio")
        if not str(nombre).strip():
            raise ValueError("El nombre del alumno no puede estar vacio")
        if int(semestre) <= 0 or int(semestre) > 16:
            raise ValueError("El semestre debe estar entre 1 y 16")
        if str(areaDeRe).strip() not in AreaRe:
            raise ValueError(f"El grupo '{areaDeRe}' no pertenece a los grupos validos de la universidad")
        if int(materiasReprobadas) < 0:
            raise ValueError("Las materias reprobadas no pueden ser negativas")
        if int(actividades) < 0 or int(mentorias) < 0 or int(actividadesObligatorias) < 0:
            raise ValueError("Las actividades y mentorias no pueden ser numeros negativos")

        self._idAlumno = str(idAlumno).strip()
        self._nombre = str(nombre).strip()
        self._semestre = int(semestre)
        self._areaDeRe = str(areaDeRe).strip()
        self._gestionRe = str(gestion).strip()
        self._materiasReprobadas = int(materiasReprobadas)
        self._actividades = int(actividades)
        self._mentorias = int(mentorias)
        self._actividadesObligatorias = int(actividadesObligatorias)

    #estas funciones son ecenciales para obtener todos las variables privadas
    def getId(self):
        return self._idAlumno

    def getNombre(self):
        return self._nombre

    def getSemestre(self):
        return self._semestre

    def getArea(self):
        return self._areaDeRe

    def getGestionRe(self):
        return self._gestionRe

        #esta funcion cambia los datos de un alumno en especifico
    def actualizarDatos(self, nombre, semestre, areaDeRe):
        if not str(nombre).strip():
            raise ValueError("El nombre no puede estar vacio al actualizar")
        if int(semestre) <= 0 or int(semestre) > 16:
            raise ValueError("El semestre debe ser mayor a 0 y menor o igual a 16")
        if str(areaDeRe).strip() not in AreaRe:
            raise ValueError("El grupo seleccionado para actualizar no es valido")
        self._nombre = str(nombre).strip()
        self._semestre = int(semestre)
        self._areaDeRe = str(areaDeRe).strip()

    def actualizarProgreso(self, actividades, mentorias, actividadesObligatorias, materiasReprobadas):
        if int(actividades) < 0 or int(mentorias) < 0 or int(actividadesObligatorias) < 0 or int(materiasReprobadas) < 0:
            raise ValueError("Los valores de progreso no pueden ser negativos")
        self._actividades = int(actividades)
        self._mentorias = int(mentorias)
        self._actividadesObligatorias = int(actividadesObligatorias)
        self._materiasReprobadas = int(materiasReprobadas)

        #las funciones verificar debuelven un valor % sobre la cantidad de acitvidades que le faltan  
    
    #aqui verificamos si las actividades del alumno estan en el limite correcto
    def verificarActividades(self, cantidadActividades=None):
        try:
            if cantidadActividades is not None:
                cant = int(cantidadActividades)
            else:
                cant = self._actividades

            if cant < 0:
                raise ValueError("La cantidad de actividades no puede ser negativa")
            if cant < limiteActividades:
                return False
            else:
                return True
        except (TypeError, ValueError):
            raise ValueError("Error en verificar Actividades")
        
   #aqui verificamos si las mentorias estan en el limite correcto
    def verificarMentorias(self, cantidadMentorias=None):
        try:
            if cantidadMentorias is not None:
                cant = int(cantidadMentorias)
            else:
                cant = self._mentorias

            if cant < 0:
                raise ValueError("La cantidad de mentorias no puede ser negativa")
            if cant < limiteMentorias:
                return False
            else:
                return True
        except (TypeError, ValueError):
            raise ValueError("Error en verificar Mentorias")

    #aqui verificamos la situacion academica en caso de una materia reprobada entonces Regresa fale
    def verificarSituacionAcademica(self):
        try:
            if self._materiasReprobadas < 0:
                raise ValueError("Materias reprobadas invalidas")
            if self._materiasReprobadas >= 1:
                return False
            else:
                return True
        except (TypeError, ValueError):
            raise ValueError("Error en verificar situacion Academica")

    #aqui checamos las actividades obligatorias 
    def verificarActividadesObligatorias(self):
        try:
            if self._actividadesObligatorias < 0:
                raise ValueError("Actividades obligatorias invalidas")
            if self._actividadesObligatorias < limiteActividadesObligatorias:
                return False
            else:
                return True
        except (TypeError, ValueError):
            raise ValueError("Error en verificar Actividades Obligatorias")

    #aqui checamos si todos los datos que le pedimos al usuario son verdad si es asi entonces si se puede graduar

    def verificarGraduacion(self):
        try:
            if self.verificarActividades() == True and self.verificarActividadesObligatorias() == True and self.verificarSituacionAcademica() == True and self.verificarMentorias() == True:
                return "S"
            else:
                return self.obtenerPendientes()
        except Exception:
            raise ValueError("Error en verificar Actividades Graduacion")

    def obtenerPendientes(self):
        try:
            pendientes = []
            if not self.verificarActividades():
                pendientes.append("Actividades")
            if not self.verificarMentorias():
                pendientes.append("Mentorias")
            if not self.verificarSituacionAcademica():
                pendientes.append("Materias Reprobadas")
            if not self.verificarActividadesObligatorias():
                pendientes.append("Actividades Obligatorias")
            return pendientes
        except Exception as e:
            enviarError(e)
            raise ValueError("Error al calcular los requisitos pendientes")

    def mostrarProgreso(self):
        return f"{self._nombre}|Act:{self._actividades}/{limiteActividades}|Ment:{self._mentorias}/{limiteMentorias}|Oblig:{self._actividadesObligatorias}/{limiteActividadesObligatorias}|Reprobadas:{self._materiasReprobadas}"
    #el mostrar progreso debe de imprimir en este formato alumno|actividades|mentorias|etc

    
    def __str__(self):
        return f"{self._idAlumno}|{self._nombre}|{self._semestre}|{self._areaDeRe}|{self._gestionRe}|{self._materiasReprobadas}|{self._actividades}|{self._mentorias}|{self._actividadesObligatorias}"
    #cuando se imprima el alumno manda a llamar todo


class GestionRe(Alumno):

    def __init__(self, idAlumno, nombre, semestre, areaDeRe, gestion, materiasReprobadas, periodo, estatus, semestresComoAdmin=1, actividades=0, mentorias=0, actividadesObligatorias=0, requisitos=None):
        super().__init__(idAlumno, nombre, semestre, areaDeRe, gestion, materiasReprobadas, actividades, mentorias, actividadesObligatorias)
        if not str(periodo).strip():
            raise ValueError("El periodo de gestion no puede estar vacio")
        if not str(estatus).strip():
            raise ValueError("El estatus de gestion no puede estar vacio")
        if int(semestresComoAdmin) <= 0 or int(semestresComoAdmin) > 2:
            raise ValueError("Un miembro de GestionRe solo puede estar maximo 2 semestres como admin")
        self._periodo = str(periodo).strip()
        self._estatus = str(estatus).strip()
        self._semestresComoAdmin = int(semestresComoAdmin)
        if requisitos is not None:
            self._requisitos = requisitos
        else:
            self._requisitos = []
        #GestionRe son los admins de cada uno y estos son un poco diferentes solo 
        #estos tienen que si o si hacer sus mentorias y estar en el programa como admins maximo 2 semestres


    def agregarRequisito(self, requisito):
        if not isinstance(requisito, Requisito):
            raise ValueError("El objeto agregado debe ser una instancia de Requisito")
        self._requisitos.append(requisito)

    def calcularPorcentajeAvance(self):
        if len(self._requisitos) == 0:
            return 0.0
        cumplidos = 0
        for r in self._requisitos:
            if r.verificarCumplimiento():
                cumplidos += 1
        return (cumplidos / len(self._requisitos)) * 100

    def __str__(self):
        return f"{super().__str__()}|{self._periodo}|{self._estatus}|SemestresAdmin:{self._semestresComoAdmin}"

class Requisito:

    def __init__(self, nombreActividad, periodo, completado=False):
        if not str(nombreActividad).strip():
            raise ValueError("El nombre de la actividad del requisito no puede estar vacio")
        if not str(periodo).strip():
            raise ValueError("El periodo del requisito no puede estar vacio")
        self._nombreActividad = str(nombreActividad).strip()
        self._periodo = str(periodo).strip()
        self._completado = bool(completado)

    def verificarCumplimiento(self):
        return self._completado

    def obtenerEstado(self):
        if self._completado:
            return "Completado"
        else:
            return "Pendiente"

    def registrarAvance(self, estado=True):
        if not isinstance(estado, bool):
            raise ValueError("El estado del requisito debe ser booleano")
        self._completado = estado

    def __str__(self):
        return f"{self._nombreActividad} ({self._periodo}) - {self.obtenerEstado()}"
    #esto es para agregar requisitos por ejemplo si hay un evento que si hay que ir o
    #academico

class RequisitoEvento(Requisito):
    def __init__(self, nombreActividad, periodo, fechaEvento=""):
        super().__init__(nombreActividad, periodo)
        if not str(fechaEvento).strip():
            raise ValueError("La fecha del evento no puede estar vacia")
        self._fechaEvento = str(fechaEvento).strip()

    def __str__(self):
        return f"Evento: {super().__str__()} | Fecha: {self._fechaEvento}"

class RequisitoAcademico(Requisito):
    def __init__(self, nombreActividad, periodo, calificacionMinima=70):
        super().__init__(nombreActividad, periodo)
        if float(calificacionMinima) < 0 or float(calificacionMinima) > 100:
            raise ValueError("La calificacion minima debe estar entre 0 y 100")
        self._calificacionMinima = float(calificacionMinima)

    def __str__(self):
        return f"Academico: {super().__str__()} | Minimo: {self._calificacionMinima}"

class GestorArchivos:
    #hay una clase dedicada a gestor de archivos para el log los errorres y asi
    def __init__(self, archivoAlumnos="alumnos.txt", archivoLog="logErrores.txt"):
        self._archivoAlumnos = archivoAlumnos
        self._archivoLog = archivoLog

    def registrarError(self, tipoError, mensaje):
        fechaHora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        linea = f"{fechaHora} | ERROR | {tipoError}: {mensaje}\n"
        with open(self._archivoLog, "a", encoding="utf-8") as archivo:
            archivo.write(linea)

    def guardarAlumnos(self, listaAlumnos):
        try:
            with open(self._archivoAlumnos, "a", encoding="utf-8") as archivo:
                for alumno in listaAlumnos:
                    archivo.write(str(alumno) + "\n")
        except PermissionError as e:
            self.registrarError("PermissionError", str(e))
            raise ValueError("No se tienen permisos para guardar el archivo de alumnos")

    def cargarAlumnos(self):
        lista = []
        try:
            with open(self._archivoAlumnos, "r", encoding="utf-8") as archivo:
                for linea in archivo:
                    lineaLimpia = linea.strip()
                    if not lineaLimpia:
                        continue
                    datos = lineaLimpia.split("|")
                    if len(datos) >= 9:
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
                    elif len(datos) >= 6:
                        alumno = Alumno(
                            datos[0],
                            datos[1],
                            int(datos[2]),
                            datos[3],
                            datos[4],
                            int(datos[5])
                        )
                        lista.append(alumno)
        except FileNotFoundError:
            self.registrarError("FileNotFoundError", f"No se encontro {self._archivoAlumnos}")
            with open(self._archivoAlumnos, "w", encoding="utf-8") as archivo:
                pass
        except Exception as e:
            self.registrarError(type(e).__name__, str(e))
        return lista

    def __str__(self):
        return f"GestorArchivos(Alumnos: {self._archivoAlumnos}, Log: {self._archivoLog})"


gestorGlobal = GestorArchivos()


def enviarError(error):
    fechaHora = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    tipo = type(error).__name__
    with open("logErrores.txt", "a", encoding="utf-8") as archivo:
        archivo.write(f"{fechaHora} | ERROR | {tipo}: {error}\n")


def seleccionarGrupoHerencia():
    print("\n--- Grupos Universitarios Disponibles ---")
    for clave, grupoObj in gruposDisponibles.items():
        print(f"{clave}.- {grupoObj}")
    opcionGrupo = input("Seleccione el numero del grupo: ").strip()
    if not opcionGrupo.isdigit():
        raise ValueError("La opcion de grupo debe ser un numero entero")
    indiceGrupo = int(opcionGrupo)
    if indiceGrupo not in gruposDisponibles:
        raise ValueError(f"El grupo con opcion {indiceGrupo} no existe")
    return gruposDisponibles[indiceGrupo]


def menuUsuarioNoRegistrado():
    global indiceWhile, registrado, coordinadorActual
    print(
    """
    Bienvenido al sistema de Gestion De Area
        
            Seleccione una opcion 
        1.-Ingresar Cuenta Coordinador
        2.-Registrar Cuenta Coordinador
        3.-Salir""" )
    
    try:
        entrada = input("Opcion: ").strip()
        if not entrada.isdigit():
            raise ValueError("Debe ingresar un numero valido en el menu principal")
        seleccion = int(entrada)
        if seleccion not in (1, 2, 3):
            raise ValueError("Opcion fuera de rango en el menu de inicio")

        if seleccion == 1:
            if len(cuentas) == 0:
                raise ValueError("No hay cuentas registradas")
            nombre = input("Ingrese nombre de usuario: ").strip()
            contrasena = input("Ingrese la contrasena: ").strip()
            if not nombre or not contrasena:
                raise ValueError("El usuario y la contrasena no pueden estar vacios")

            cuentaEncontrada = None
            for cuenta in cuentas:
                if cuenta._nombre == nombre:
                    cuentaEncontrada = cuenta
                    break

            if cuentaEncontrada is None:
                raise ValueError("Error en el nombre de la cuenta")
            if cuentaEncontrada._contrasena != contrasena:
                raise ValueError("Error en la contrasena de la cuenta")

            coordinadorActual = cuentaEncontrada
            print(f"Bienvenido {coordinadorActual._nombre}")
            print("Su Id es:", coordinadorActual._idNombre)
            registrado = 0

        elif seleccion == 2:
            idCoord = input("Ingrese ID: ").strip()
            if not idCoord:
                raise ValueError("El ID del coordinador no puede estar vacio")
            for c in cuentas:
                if c._idNombre == idCoord:
                    raise ValueError(f"El ID de coordinador {idCoord} ya esta registrado")
            nombre = input("Ingrese nombre: ").strip()
            if not nombre:
                raise ValueError("El nombre del coordinador no puede estar vacio")
            contrasena = input("Ingrese contrasena (minimo 4 caracteres): ").strip()
            grupoCoord = seleccionarGrupoHerencia()
            alumnosCargados = gestorGlobal.cargarAlumnos()
            nuevoCoord = Coordinador(idCoord, contrasena, nombre, alumnosCargados, grupoCoord.getNombreArea())
            with open("cuentas.txt", "a", encoding="utf-8") as archivo:
                archivo.write(f"{nuevoCoord._idNombre}|{nuevoCoord._nombre}|{nuevoCoord._area}|{nuevoCoord._anioAdministracion}\n")
            cuentas.append(nuevoCoord)
            print("Coordinador registrado correctamente.")

        elif seleccion == 3:
            indiceWhile = 0

    except ValueError as e:
        print(f"[ERROR DE VALIDACION]: {e}")
        enviarError(e)
    except Exception as e:
        print(f"[ERROR]: {e}")
        enviarError(e)


def menuUsuarioRegistrado():
    global registrado, coordinadorActual, indiceWhile
    print(f"""
    ================================================
    Panel de Coordinacion - {coordinadorActual}
    ================================================
    1.- Registrar Alumno en Grupo (ASUA, FESAL, ADEFA, etc.)
    2.- Dar de Baja Alumno
    3.- Buscar y Mostrar Alumno por ID
    4.- Actualizar Datos o Avance de Alumno
    5.- Agregar Requisito Especial (Evento / Academico) a Alumno GestionRe
    6.- Mostrar Alumnos en Cumplimiento (Listos para Graduacion)
    7.- Mostrar Alumnos con Requisitos Pendientes
    8.- Mostrar Todos los Alumnos y Grupos en Herencia
    9.- Cerrar Sesion
    10.- Salir del Programa
    """)
    try:
        entrada = input("Seleccione una opcion: ").strip()
        if not entrada.isdigit():
            raise ValueError("La opcion del menu de coordinador debe ser numerica")
        opcion = int(entrada)
        if opcion < 1 or opcion > 10:
            raise ValueError("Opcion de menu de coordinador fuera de rango (1-10)")

        if opcion == 1:
            idAlumno = input("ID del Alumno: ").strip()
            nombre = input("Nombre completo del Alumno: ").strip()
            semestreStr = input("Semestre actual (1-16): ").strip()
            if not semestreStr.isdigit():
                raise ValueError("El semestre debe ser un numero entero")
            semestre = int(semestreStr)

            grupoSeleccionado = seleccionarGrupoHerencia()
            areaNombre = grupoSeleccionado.getNombreArea()

            esAdmin = input("¿Es miembro directivo / GestionRe? (S/N): ").strip().upper()
            if esAdmin not in ("S", "N"):
                raise ValueError("Debe responder S o N para indicar si pertenece a GestionRe")

            reprobadasStr = input("Cantidad de materias reprobadas: ").strip()
            if not reprobadasStr.isdigit():
                raise ValueError("La cantidad de materias reprobadas debe ser un numero entero")
            materiasReprobadas = int(reprobadasStr)

            actStr = input(f"Actividades realizadas (meta {limiteActividades}): ").strip()
            mentStr = input(f"Mentorias realizadas (meta {limiteMentorias}): ").strip()
            obligStr = input(f"Actividades obligatorias realizadas (meta {limiteActividadesObligatorias}): ").strip()
            if not (actStr.isdigit() and mentStr.isdigit() and obligStr.isdigit()):
                raise ValueError("Las actividades y mentorias deben ser valores enteros no negativos")

            if esAdmin == "S":
                periodo = input("Periodo de gestion (ej. 2026-1): ").strip()
                estatus = input("Estatus (Activo/Inactivo): ").strip()
                semAdminStr = input("Semestres como admin (1 o 2): ").strip()
                if not semAdminStr.isdigit():
                    raise ValueError("Los semestres como admin deben ser un numero entero")
                nuevoAlumno = GestionRe(
                    idAlumno,
                    nombre,
                    semestre,
                    areaNombre,
                    "Directivo GestionRe",
                    materiasReprobadas,
                    periodo,
                    estatus,
                    int(semAdminStr),
                    int(actStr),
                    int(mentStr),
                    int(obligStr)
                )
            else:
                nuevoAlumno = Alumno(
                    idAlumno,
                    nombre,
                    semestre,
                    areaNombre,
                    "Miembro General",
                    materiasReprobadas,
                    int(actStr),
                    int(mentStr),
                    int(obligStr)
                )

            coordinadorActual.darDeAltaAlumno(nuevoAlumno)
            grupoSeleccionado.agregarAlumno(nuevoAlumno)
            gestorGlobal.guardarAlumnos(coordinadorActual.obtenerTodosLosAlumnos())
            print(f"Alumno '{nombre}' registrado exitosamente en {grupoSeleccionado.getNombreArea()}.")

        elif opcion == 2:
            idEliminar = input("Ingrese el ID del alumno a dar de baja: ").strip()
            coordinadorActual.darDeBajaAlumno(idEliminar)
            for grp in gruposDisponibles.values():
                for al in grp.getAlumnos():
                    if al.getId() == idEliminar:
                        grp.eliminarAlumno(idEliminar)
            gestorGlobal.guardarAlumnos(coordinadorActual.obtenerTodosLosAlumnos())
            print(f"Alumno con ID {idEliminar} dado de baja correctamente.")

        elif opcion == 3:
            idBuscar = input("Ingrese el ID del alumno a consultar: ").strip()
            alumno = coordinadorActual.mostrarAlumno(idBuscar)
            print("Progreso detallado:", alumno.mostrarProgreso())
            estadoGrad = alumno.verificarGraduacion()
            if estadoGrad == "S":
                print("Estatus de Graduacion: CUMPLE CON TODOS LOS REQUISITOS")
            else:
                print("Pendientes para graduarse:", ", ".join(estadoGrad))
            if isinstance(alumno, GestionRe):
                print(f"Avance de requisitos especiales GestionRe: {alumno.calcularPorcentajeAvance():.1f}%")

        elif opcion == 4:
            idActualizar = input("Ingrese el ID del alumno a modificar: ").strip()
            alumno = coordinadorActual.mostrarAlumno(idActualizar)
            print("1.- Actualizar datos personales y cambio de grupo")
            print("2.- Actualizar avance de actividades, mentorias y materias")
            subOp = input("Seleccione que desea actualizar (1 o 2): ").strip()
            if subOp == "1":
                nuevoNombre = input("Nuevo nombre: ").strip()
                nuevoSemStr = input("Nuevo semestre (1-16): ").strip()
                if not nuevoSemStr.isdigit():
                    raise ValueError("El semestre debe ser numerico")
                nuevoGrupo = seleccionarGrupoHerencia()
                alumno.actualizarDatos(nuevoNombre, int(nuevoSemStr), nuevoGrupo.getNombreArea())
                print("Datos actualizados correctamente.")
            elif subOp == "2":
                act = input("Nuevo total de actividades: ").strip()
                ment = input("Nuevo total de mentorias: ").strip()
                oblig = input("Nuevo total de actividades obligatorias: ").strip()
                rep = input("Nuevo total de materias reprobadas: ").strip()
                if not (act.isdigit() and ment.isdigit() and oblig.isdigit() and rep.isdigit()):
                    raise ValueError("Todos los campos de progreso deben ser enteros no negativos")
                alumno.actualizarProgreso(int(act), int(ment), int(oblig), int(rep))
                print("Progreso actualizado correctamente.")
            else:
                raise ValueError("Subopcion de actualizacion invalida")
            gestorGlobal.guardarAlumnos(coordinadorActual.obtenerTodosLosAlumnos())

        elif opcion == 5:
            idAl = input("Ingrese el ID del alumno GestionRe: ").strip()
            alumno = coordinadorActual.mostrarAlumno(idAl)
            if not isinstance(alumno, GestionRe):
                raise ValueError("El alumno seleccionado no pertenece a la modalidad GestionRe")
            tipoReq = input("Tipo de requisito (1: Evento / 2: Academico): ").strip()
            nomAct = input("Nombre del requisito: ").strip()
            perReq = input("Periodo: ").strip()
            completadoIn = input("¿Ya esta completado? (S/N): ").strip().upper()
            if completadoIn not in ("S", "N"):
                raise ValueError("Debe indicar S o N para el estado del requisito")
            estadoBool = True if completadoIn == "S" else False

            if tipoReq == "1":
                fechaEv = input("Fecha del evento (DD/MM/AAAA): ").strip()
                req = RequisitoEvento(nomAct, perReq, fechaEv)
            elif tipoReq == "2":
                calMinStr = input("Calificacion minima requerida (0-100): ").strip()
                if not calMinStr.replace(".", "", 1).isdigit():
                    raise ValueError("La calificacion minima debe ser un numero valido")
                req = RequisitoAcademico(nomAct, perReq, float(calMinStr))
            else:
                raise ValueError("Tipo de requisito invalido, debe ser 1 o 2")

            req.registrarAvance(estadoBool)
            alumno.agregarRequisito(req)
            print("Requisito agregado:", req)

        elif opcion == 6:
            cumplidos = coordinadorActual.mostrarAlumnosCumplimiento()
            if len(cumplidos) == 0:
                print("Ningun alumno cumple aun con todos los requisitos de graduacion.")
            else:
                print("\n--- Alumnos Listos para Graduarse ---")
                for a in cumplidos:
                    print(a, "|", a.mostrarProgreso())

        elif opcion == 7:
            pendientes = coordinadorActual.mostrarAlumnosConRequisitosPendientes()
            if len(pendientes) == 0:
                print("No hay alumnos con requisitos pendientes.")
            else:
                print("\n--- Alumnos con Requisitos Pendientes ---")
                for a in pendientes:
                    faltantes = ", ".join(a.obtenerPendientes())
                    print(f"{a.getId()} - {a.getNombre()} ({a.getArea()}) | Faltan: {faltantes}")

        elif opcion == 8:
            todos = coordinadorActual.obtenerTodosLosAlumnos()
            print(f"\nTotal de alumnos en catalogo: {len(todos)}")
            for a in todos:
                print(a)
            print("\n--- Estado de Grupos Estudiantiles (Herencia AreaRE) ---")
            for grp in gruposDisponibles.values():
                print(grp)

        elif opcion == 9:
            gestorGlobal.guardarAlumnos(coordinadorActual.obtenerTodosLosAlumnos())
            coordinadorActual = None
            registrado = 1
            print("Sesion cerrada correctamente.")

        elif opcion == 10:
            gestorGlobal.guardarAlumnos(coordinadorActual.obtenerTodosLosAlumnos())
            indiceWhile = 0
            print("Saliendo del sistema...")

    except ValueError as e:
        print(f"[ERROR DE VALIDACION]: {e}")
        enviarError(e)
    except Exception as e:
        print(f"[ERROR]: {e}")
        enviarError(e)

def main():
    global indiceWhile
    while(indiceWhile != 0):
        if(registrado == 1):
            menuUsuarioNoRegistrado()
        else:
            menuUsuarioRegistrado()

#inicializamos el codigo

main()
