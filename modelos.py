# -*- coding: utf-8 -*-
#raul isaac santos ruiz
#silvana de alba uribe
#este modulo tiene las clases del negocio, validaciones simples y reglas de graduacion

from excepciones import AlumnoNoEncontradoError, RegistroDuplicadoError
#importamos las excepciones propias para alumnos repetidos o no encontrados

metaActividades = 8
metaMentorias = 2
metaObligatorias = 2
maxSemestre = 13
#estas variables guardan las metas minimas para graduarse de la gestion

gruposValidos = [
    "ASUA",
    "Presidencias ASUA",
    "FESAL",
    "ADEFA",
    "Sociedades de alumnos",
    "Asociaciones por estado",
    "Clubs Anahuac"
]
#esta lista guarda los nombres oficiales para las listas de la interfaz


#esta funcion revisa que un dato sea texto, no este vacio y no tenga simbolos prohibidos
def validarTexto(valor, campo, minLargo=1, maxLargo=80):
    if not isinstance(valor, str):
        raise ValueError(f"El campo {campo} debe ser texto.")
    textoLimpio = valor.strip()
    while "  " in textoLimpio:
        textoLimpio = textoLimpio.replace("  ", " ")
    if textoLimpio == "":
        raise ValueError(f"El campo {campo} no puede estar vacio.")
    if "|" in textoLimpio or "~" in textoLimpio or ";" in textoLimpio:
        raise ValueError(f"El campo {campo} no puede contener '|', '~' ni ';'.")
    if len(textoLimpio) < minLargo or len(textoLimpio) > maxLargo:
        raise ValueError(f"El campo {campo} debe tener entre {minLargo} y {maxLargo} caracteres.")
    return textoLimpio


#esta funcion revisa que el valor sea un numero entero dentro del rango permitido
def validarEntero(valor, campo, minimo, maximo):
    if isinstance(valor, bool) or not isinstance(valor, int):
        raise ValueError(f"El campo {campo} debe ser un numero entero.")
    if valor < minimo or valor > maximo:
        raise ValueError(f"El campo {campo} debe estar entre {minimo} y {maximo}.")
    return valor


#esta funcion revisa que la fecha escrita tenga formato dia mes anio valido
def validarFechaTexto(valor):
    textoLimpio = validarTexto(valor, "Fecha", 8, 10)
    partes = textoLimpio.split("/")
    if len(partes) != 3:
        raise ValueError("La fecha debe tener formato DD/MM/AAAA.")
    try:
        dia = int(partes[0])
        mes = int(partes[1])
        anio = int(partes[2])
    except ValueError:
        raise ValueError("La fecha debe tener formato DD/MM/AAAA.")
    if dia < 1 or dia > 31 or mes < 1 or mes > 12 or anio < 2000 or anio > 2100:
        raise ValueError("La fecha debe tener formato DD/MM/AAAA.")
    return textoLimpio


#definimos la clase padre para las areas de relaciones estudiantiles
class AreaRE:
    #este constructor guarda el nombre del area en un atributo privado
    def __init__(self, nombreArea):
        self.setNombreArea(nombreArea)

    def getNombreArea(self):
        return self.__nombreArea
    #este metodo getter devuelve el nombre privado del area

    def setNombreArea(self, valor):
        self.__nombreArea = validarTexto(valor, "Area", 2, 40)
    #este metodo setter valida y guarda el nombre privado del area

    def obtenerTipoGrupo(self):
        return f"Area RE ({self.__nombreArea})"
    #este metodo se sobreescribe en las clases hijas para aplicar polimorfismo


#definimos la clase hija asua que hereda de area
class ASUA(AreaRE):
    def __init__(self, nombreArea="ASUA"):
        super().__init__(nombreArea)
    #usamos super para llamar al constructor de la clase padre

    def obtenerTipoGrupo(self):
        return "Accion Social Universidad Anahuac"


#definimos presidencias asua que hereda directamente de asua
class PresidenciasASUA(ASUA):
    def __init__(self):
        super().__init__("Presidencias ASUA")

    def obtenerTipoGrupo(self):
        return "Direccion y Presidencias ASUA"


#definimos la clase hija fesal
class FESAL(AreaRE):
    def __init__(self):
        super().__init__("FESAL")

    def obtenerTipoGrupo(self):
        return "Federacion de Sociedades de Alumnos"


#definimos la clase hija adefa
class ADEFA(AreaRE):
    def __init__(self):
        super().__init__("ADEFA")

    def obtenerTipoGrupo(self):
        return "Asociacion de Estudiantes Foraneos"


#definimos la clase hija sociedades de alumnos
class SociedadesDeAlumnos(AreaRE):
    def __init__(self):
        super().__init__("Sociedades de alumnos")

    def obtenerTipoGrupo(self):
        return "Sociedad de Alumnos por Facultad"


#definimos la clase hija asociaciones por estado
class AsociacionesPorEstado(AreaRE):
    def __init__(self):
        super().__init__("Asociaciones por estado")

    def obtenerTipoGrupo(self):
        return "Asociacion de Estudiantes por Estado"


#definimos la clase hija clubs anahuac
class ClubsAnahuac(AreaRE):
    def __init__(self):
        super().__init__("Clubs Anahuac")

    def obtenerTipoGrupo(self):
        return "Club Universitario Anahuac"


#definimos la clase base requisito para los requisitos especiales de gestion
class Requisito:
    def __init__(self, nombreActividad, completado=False):
        self.setNombreActividad(nombreActividad)
        self.setCompletado(completado)
    #este constructor guarda nombre y estado como atributos privados

    def getNombreActividad(self):
        return self.__nombreActividad

    def setNombreActividad(self, valor):
        self.__nombreActividad = validarTexto(valor, "Actividad", 2, 60)

    def getCompletado(self):
        return self.__completado

    def setCompletado(self, valor):
        if not isinstance(valor, bool):
            raise ValueError("El campo Estado del requisito debe ser booleano.")
        self.__completado = valor

    def verificarCumplimiento(self):
        return self.__completado
    #este metodo indica si el requisito ya esta cumplido

    def obtenerEstado(self):
        if self.verificarCumplimiento() == True:
            return "Cumplido"
        else:
            return "Pendiente"
    #este metodo convierte el verdadero o falso en texto para la ventana

    def obtenerDetalle(self):
        return f"{self.__nombreActividad} ({self.obtenerEstado()})"


#esta clase hija mide el cumplimiento segun una cantidad de actividades realizadas
class RequisitoCantidad(Requisito):
    def __init__(self, nombreActividad, cantidadRequerida, cantidadRealizada=0):
        super().__init__(nombreActividad, False)
        self.__cantidadRequerida = 1
        self.__cantidadRealizada = 0
        self.setCantidadRequerida(cantidadRequerida)
        self.setCantidadRealizada(cantidadRealizada)
    #usamos super para iniciar nombre y luego guardamos la meta y lo realizado

    def getCantidadRequerida(self):
        return self.__cantidadRequerida

    def setCantidadRequerida(self, valor):
        self.__cantidadRequerida = validarEntero(valor, "Meta", 1, 100)
        self.setCompletado(self.__cantidadRealizada >= self.__cantidadRequerida)

    def getCantidadRealizada(self):
        return self.__cantidadRealizada

    def setCantidadRealizada(self, valor):
        self.__cantidadRealizada = validarEntero(valor, "Realizadas", 0, 100)
        self.setCompletado(self.__cantidadRealizada >= self.__cantidadRequerida)

    def registrarAvance(self, cantidad):
        self.setCantidadRealizada(cantidad)

    def verificarCumplimiento(self):
        if self.__cantidadRealizada >= self.__cantidadRequerida:
            return True
        else:
            return False
    #aqui se aplica polimorfismo comparando lo realizado contra la meta

    def obtenerDetalle(self):
        return f"{self.getNombreActividad()}: {self.__cantidadRealizada}/{self.__cantidadRequerida} ({self.obtenerEstado()})"


#esta clase hija mide el cumplimiento segun si asistio a un evento con fecha
class RequisitoEvento(Requisito):
    def __init__(self, nombreActividad, fecha, asistencia=False):
        super().__init__(nombreActividad, asistencia)
        self.setFecha(fecha)

    def getFecha(self):
        return self.__fecha

    def setFecha(self, valor):
        self.__fecha = validarFechaTexto(valor)

    def registrarAsistencia(self, asistio=True):
        self.setCompletado(asistio)

    def obtenerDetalle(self):
        if self.verificarCumplimiento() == True:
            estadoTexto = "Asistio"
        else:
            estadoTexto = "Pendiente"
        return f"{self.getNombreActividad()} ({self.__fecha}) - {estadoTexto}"


#esta clase hija mide que el estudiante tenga cero materias reprobadas
class RequisitoAcademico(Requisito):
    def __init__(self, nombreActividad, materiasReprobadas=0):
        super().__init__(nombreActividad, False)
        self.setMateriasReprobadas(materiasReprobadas)

    def getMateriasReprobadas(self):
        return self.__materiasReprobadas

    def setMateriasReprobadas(self, valor):
        self.__materiasReprobadas = validarEntero(valor, "Reprobadas del requisito", 0, 50)
        self.setCompletado(self.__materiasReprobadas == 0)

    def actualizarMateriasReprobadas(self, cantidad):
        self.setMateriasReprobadas(cantidad)

    def verificarCumplimiento(self):
        if self.__materiasReprobadas == 0:
            return True
        else:
            return False
    #aqui se aplica polimorfismo verificando que no existan reprobadas

    def obtenerDetalle(self):
        return f"{self.getNombreActividad()} (Reprobadas: {self.__materiasReprobadas}) - {self.obtenerEstado()}"


#definimos la clase alumno con atributos privados, getters/setters y solo tres decoradores
class Alumno:
    def __init__(self, idAlumno, nombre, semestre, grupo, actividades=0, mentorias=0, obligatorias=0, materiasReprobadas=0, seminario=False):
        self.setIdAlumno(idAlumno)
        self.setNombre(nombre)
        self.semestre = semestre
        self.setGrupo(grupo)
        self.setActividades(actividades)
        self.setMentorias(mentorias)
        self.setObligatorias(obligatorias)
        self.setMateriasReprobadas(materiasReprobadas)
        self.setSeminario(seminario)
    #este constructor manda validar cada dato mediante sus setters y la propiedad semestre

    @property
    def semestre(self):
        return self.__semestre
    #usando property creamos el primer decorador getter para leer el semestre privado

    @semestre.setter
    def semestre(self, x):
        self.__semestre = validarEntero(x, "Semestre", 1, maxSemestre)
    #usando semestre.setter creamos el segundo decorador para validar el rango de uno a trece

    @property
    def porcentajeAvance(self):
        return self.calcularPorcentajeAvance()
    #creamos el tercer decorador de solo lectura para consultar el porcentaje calculado

    def getIdAlumno(self):
        return self.__idAlumno

    def setIdAlumno(self, valor):
        idLimpio = validarTexto(valor, "ID", 2, 20)
        if " " in idLimpio:
            raise ValueError("El ID no puede contener espacios.")
        self.__idAlumno = idLimpio
    #este par get y set valida que el id no tenga espacios y lo guarda en privado

    def getNombre(self):
        return self.__nombre

    def setNombre(self, valor):
        nombreLimpio = validarTexto(valor, "Nombre", 3, 80)
        for letra in nombreLimpio:
            if letra.isdigit():
                raise ValueError("El nombre no puede contener numeros.")
        self.__nombre = nombreLimpio
    #este par get y set revisa letra por letra que el nombre no tenga numeros

    def getGrupo(self):
        return self.__grupo

    def setGrupo(self, valor):
        grupoLimpio = validarTexto(valor, "Grupo", 2, 40)
        if grupoLimpio not in gruposValidos:
            raise ValueError(f"Grupo invalido: '{grupoLimpio}'.")
        self.__grupo = grupoLimpio
        if grupoLimpio == "ASUA":
            self.setAreaObj(ASUA())
        elif grupoLimpio == "Presidencias ASUA":
            self.setAreaObj(PresidenciasASUA())
        elif grupoLimpio == "FESAL":
            self.setAreaObj(FESAL())
        elif grupoLimpio == "ADEFA":
            self.setAreaObj(ADEFA())
        elif grupoLimpio == "Sociedades de alumnos":
            self.setAreaObj(SociedadesDeAlumnos())
        elif grupoLimpio == "Asociaciones por estado":
            self.setAreaObj(AsociacionesPorEstado())
        else:
            self.setAreaObj(ClubsAnahuac())
    #este setter valida que el grupo exista y crea el objeto area que le corresponde

    def getAreaObj(self):
        return self.__areaObj

    def setAreaObj(self, valor):
        if not isinstance(valor, AreaRE):
            raise ValueError("El area debe pertenecer a AreaRE.")
        self.__areaObj = valor

    def getActividades(self):
        return self.__actividades

    def setActividades(self, valor):
        self.__actividades = validarEntero(valor, "Actividades", 0, 100)

    def getMentorias(self):
        return self.__mentorias

    def setMentorias(self, valor):
        self.__mentorias = validarEntero(valor, "Mentorias", 0, 50)

    def getObligatorias(self):
        return self.__obligatorias

    def setObligatorias(self, valor):
        self.__obligatorias = validarEntero(valor, "Obligatorias RE", 0, 50)

    def getMateriasReprobadas(self):
        return self.__materiasReprobadas

    def setMateriasReprobadas(self, valor):
        self.__materiasReprobadas = validarEntero(valor, "Materias reprobadas", 0, 50)

    def getSeminario(self):
        return self.__seminario

    def setSeminario(self, valor):
        if not isinstance(valor, bool):
            raise ValueError("El campo Seminario debe ser booleano.")
        self.__seminario = valor

    def actualizarDatos(self, nombre, semestre, grupo):
        self.setNombre(nombre)
        self.semestre = semestre
        self.setGrupo(grupo)
    #este metodo actualiza nombre, semestre y grupo usando los setters

    def verificarActividades(self):
        if self.__actividades >= metaActividades:
            return True
        else:
            return False

    def verificarSeminario(self):
        if self.__seminario == True:
            return True
        else:
            return False

    def verificarMentorias(self):
        if self.__mentorias >= metaMentorias:
            return True
        else:
            return False

    def verificarSituacionAcademica(self):
        if self.__materiasReprobadas == 0:
            return True
        else:
            return False

    def verificarActividadesObligatorias(self):
        if self.__obligatorias >= metaObligatorias:
            return True
        else:
            return False
    #estas cinco funciones revisan cada uno de los requisitos base del reglamento

    def obtenerCumplidos(self):
        cumplidos = []
        if self.verificarActividades() == True:
            cumplidos.append(f"Plan Formativo ({self.__actividades}/{metaActividades})")
        if self.verificarSeminario() == True:
            cumplidos.append("Seminario intermedio")
        if self.verificarMentorias() == True:
            cumplidos.append(f"Mentorias ({self.__mentorias}/{metaMentorias})")
        if self.verificarSituacionAcademica() == True:
            cumplidos.append("Situacion academica (0 reprobadas)")
        if self.verificarActividadesObligatorias() == True:
            cumplidos.append(f"Obligatorias RE ({self.__obligatorias}/{metaObligatorias})")
        return cumplidos
    #esta funcion junta en una lista todos los requisitos que el alumno ya completo

    def obtenerPendientes(self):
        pendientes = []
        if self.verificarActividades() == False:
            pendientes.append(f"Plan Formativo ({self.__actividades}/{metaActividades})")
        if self.verificarSeminario() == False:
            pendientes.append("Seminario intermedio")
        if self.verificarMentorias() == False:
            pendientes.append(f"Mentorias ({self.__mentorias}/{metaMentorias})")
        if self.verificarSituacionAcademica() == False:
            pendientes.append(f"Materias reprobadas ({self.__materiasReprobadas})")
        if self.verificarActividadesObligatorias() == False:
            pendientes.append(f"Obligatorias RE ({self.__obligatorias}/{metaObligatorias})")
        return pendientes
    #esta funcion junta en una lista todo lo que todavia le falta al alumno

    def calcularPorcentajeAvance(self):
        totalCumplidos = len(self.obtenerCumplidos())
        porcentaje = (totalCumplidos / 5.0) * 100.0
        return round(porcentaje, 1)

    def verificarGraduacion(self):
        faltantes = self.obtenerPendientes()
        if len(faltantes) == 0:
            return True
        else:
            return False

    def mostrarProgreso(self):
        if self.verificarGraduacion() == True:
            estado = "Cumple"
        else:
            estado = "Pendiente"
        return f"{self.__idAlumno} | {self.__nombre} | {self.__areaObj.obtenerTipoGrupo()} | {self.porcentajeAvance:.0f}% | {estado}"


#esta clase hija hereda de alumno y agrega el periodo y requisitos especiales
class GestionRe(Alumno):
    def __init__(self, idAlumno, nombre, semestre, grupo, actividades=0, mentorias=0, obligatorias=0, materiasReprobadas=0, seminario=False, periodo="2026-2027", requisitos=[]):
        super().__init__(idAlumno, nombre, semestre, grupo, actividades, mentorias, obligatorias, materiasReprobadas, seminario)
        self.setPeriodo(periodo)
        self.__requisitos = []
        if len(requisitos) > 0:
            self.setRequisitos(requisitos)
    #usamos super para pasar los datos base a la clase padre alumno

    def getPeriodo(self):
        return self.__periodo

    def setPeriodo(self, valor):
        self.__periodo = validarTexto(valor, "Periodo", 4, 25)

    def getRequisitos(self):
        return list(self.__requisitos)

    def setRequisitos(self, listaRequisitos):
        self.__requisitos = []
        for req in listaRequisitos:
            self.agregarRequisito(req)

    def agregarRequisito(self, requisito):
        if not isinstance(requisito, Requisito):
            raise ValueError("El objeto debe ser un Requisito valido.")
        for item in self.__requisitos:
            if item.getNombreActividad().lower() == requisito.getNombreActividad().lower():
                raise ValueError(f"Ya existe el requisito '{requisito.getNombreActividad()}'.")
        self.__requisitos.append(requisito)
    #este metodo valida el tipo y que no se repita el nombre antes de agregarlo

    def eliminarRequisito(self, indice):
        if indice < 0 or indice >= len(self.__requisitos):
            raise ValueError("Selecciona un requisito de la lista.")
        self.__requisitos.pop(indice)

    def obtenerCumplidos(self):
        lista = super().obtenerCumplidos()
        for item in self.__requisitos:
            if item.verificarCumplimiento() == True:
                lista.append("Req: " + item.obtenerDetalle())
        return lista
    #este metodo polimorfico suma los requisitos extras que ya se cumplieron

    def obtenerPendientes(self):
        lista = super().obtenerPendientes()
        for item in self.__requisitos:
            if item.verificarCumplimiento() == False:
                lista.append("Req: " + item.obtenerDetalle())
        return lista
    #este metodo polimorfico suma los requisitos extras que aun faltan

    def calcularPorcentajeAvance(self):
        total = 5 + len(self.__requisitos)
        cumplidos = len(self.obtenerCumplidos())
        return round((cumplidos / float(total)) * 100.0, 1)


#definimos la clase coordinador que administra la lista privada de alumnos
class Coordinador:
    def __init__(self, gestorArchivos, alumnos="", idNombre="C001", nombre="Coordinacion RE"):
        self.setGestorArchivos(gestorArchivos)
        self.setIdNombre(idNombre)
        self.setNombre(nombre)
        if isinstance(alumnos, list):
            self.setAlumnos(alumnos)
        else:
            cargados = self.__gestorArchivos.cargarAlumnos()
            self.setAlumnos(cargados)
    #este constructor recibe el gestor de archivos y carga los alumnos guardados

    def getGestorArchivos(self):
        return self.__gestorArchivos

    def setGestorArchivos(self, valor):
        if isinstance(valor, (str, int, float, bool)):
            raise ValueError("Se requiere un gestor de archivos valido.")
        self.__gestorArchivos = valor

    def getIdNombre(self):
        return self.__idNombre

    def setIdNombre(self, valor):
        self.__idNombre = validarTexto(valor, "ID Coordinador", 2, 20)

    def getNombre(self):
        return self.__nombre

    def setNombre(self, valor):
        self.__nombre = validarTexto(valor, "Nombre Coordinador", 2, 80)

    def getAlumnos(self):
        return list(self.__alumnos)

    def setAlumnos(self, listaAlumnos):
        nuevaLista = []
        for item in listaAlumnos:
            if not isinstance(item, Alumno):
                raise ValueError("Todos los registros deben ser objetos Alumno.")
            nuevaLista.append(item)
        self.__alumnos = nuevaLista

    def mostrarAlumnosCumplimiento(self):
        lista = []
        for registro in self.__alumnos:
            if registro.verificarGraduacion() == True:
                lista.append(registro)
        return lista
    #este ciclo junta en una lista solo los alumnos que ya cumplen todo

    def mostrarAlumnosConRequisitosPendientes(self):
        lista = []
        for registro in self.__alumnos:
            if registro.verificarGraduacion() == False:
                lista.append(registro)
        return lista
    #este ciclo junta en una lista los alumnos que aun tienen pendientes

    def darDeAltaAlumno(self, alumno):
        for item in self.__alumnos:
            if item.getIdAlumno().lower() == alumno.getIdAlumno().lower():
                raise RegistroDuplicadoError(f"Ya existe un alumno con el ID '{alumno.getIdAlumno()}'.")
        self.__alumnos.append(alumno)
        self.__gestorArchivos.guardarAlumnos(self.__alumnos)
    #revisamos que no se repita el id antes de agregarlo y guardamos el archivo

    def buscarAlumnoPorId(self, idAlumno):
        idLimpio = validarTexto(idAlumno, "ID", 1, 20)
        for alumno in self.__alumnos:
            if alumno.getIdAlumno().lower() == idLimpio.lower():
                return alumno
        raise AlumnoNoEncontradoError(f"No se encontro ningun alumno con ID '{idLimpio}'.")
    #buscamos por id sin importar mayusculas o mandamos error si no existe

    def buscarAlumnos(self, texto="", estado="Todos"):
        filtro = texto.strip().lower()
        resultados = []
        for alumno in self.__alumnos:
            cumpleEstado = True
            if estado == "Cumple" and alumno.verificarGraduacion() == False:
                cumpleEstado = False
            elif estado == "Pendiente" and alumno.verificarGraduacion() == True:
                cumpleEstado = False

            coincideTexto = False
            if filtro == "":
                coincideTexto = True
            elif filtro in alumno.getIdAlumno().lower():
                coincideTexto = True
            elif filtro in alumno.getNombre().lower():
                coincideTexto = True
            elif filtro in alumno.getGrupo().lower():
                coincideTexto = True

            if cumpleEstado == True and coincideTexto == True:
                resultados.append(alumno)
        return resultados
    #este ciclo filtra los alumnos por estado y por texto buscado

    def actualizarAlumno(self, idOriginal, alumnoEditado):
        for indice, existente in enumerate(self.__alumnos):
            if existente.getIdAlumno().lower() == idOriginal.lower():
                self.__alumnos[indice] = alumnoEditado
                self.__gestorArchivos.guardarAlumnos(self.__alumnos)
                return
        raise AlumnoNoEncontradoError(f"No se encontro ningun alumno con ID '{idOriginal}'.")

    def darDeBajaAlumno(self, idAlumno):
        alumno = self.buscarAlumnoPorId(idAlumno)
        self.__alumnos.remove(alumno)
        self.__gestorArchivos.guardarAlumnos(self.__alumnos)

    def guardarCambios(self):
        self.__gestorArchivos.guardarAlumnos(self.__alumnos)

    def obtenerEstadisticas(self):
        total = len(self.__alumnos)
        if total == 0:
            return {"total": 0, "cumplen": 0, "pendientes": 0, "promedio": 0.0}
        cumplen = 0
        sumaPorcentaje = 0.0
        for item in self.__alumnos:
            if item.verificarGraduacion() == True:
                cumplen = cumplen + 1
            sumaPorcentaje = sumaPorcentaje + item.porcentajeAvance
        promedio = round(sumaPorcentaje / total, 1)
        pendientes = total - cumplen
        return {"total": total, "cumplen": cumplen, "pendientes": pendientes, "promedio": promedio}
    #este ciclo cuenta cuantos alumnos cumplen y calcula el promedio general
