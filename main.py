from pathlib import Path

from sistema_re import (
    AreaRE,
    ASUA,
    FESAL,
    ADEFA,
    PresidenciasASUA,
    SociedadesDeAlumnos,
    AsociacionesPorEstado,
    ClubsAnahuac,
    Coordinador,
    Alumno,
    GestionRe,
    Requisito,
    RequisitoCantidad,
    RequisitoEvento,
    RequisitoAcademico,
    GestorArchivos
)


#usamos la misma carpeta del programa para guardar los archivos
carpeta = Path(__file__).resolve().parent
archivoAlumnos = carpeta / "alumnos.txt"
archivoLog = carpeta / "log_errores.txt"


def main():
    print("===== SISTEMA DE SEGUIMIENTO DE RELACIONES ESTUDIANTILES =====")

    #creamos los grupos que ya habia planteado el equipo
    areaGeneral = AreaRE(0, "General")
    asua = ASUA()
    fesal = FESAL()
    adefa = ADEFA()
    presidencias = PresidenciasASUA()
    sociedades = SociedadesDeAlumnos()
    asociaciones = AsociacionesPorEstado()
    clubs = ClubsAnahuac()

    print("\n1. GRUPOS CREADOS")
    print(areaGeneral)
    print(asua)
    print(fesal)
    print(adefa)
    print(presidencias)
    print(sociedades)
    print(asociaciones)
    print(clubs)

    #creamos los diferentes tipos de requisito
    requisitoGeneral = Requisito("Participacion general", "2026-2027")
    requisitoCantidad = RequisitoCantidad("Plan Formativo", "2026-2027", 8, 8)
    requisitoEvento = RequisitoEvento("Seminario intermedio", "2026-2027", "15/10/2026")
    requisitoAcademico = RequisitoAcademico("Situacion academica", "2026-2027", 70)

    requisitoEvento.registrarAvance(True)
    requisitoAcademico.registrarAvance(True)

    print("\n2. REQUISITOS CREADOS")
    print(requisitoGeneral)
    print(requisitoCantidad)
    print(requisitoEvento)
    print(requisitoAcademico)

    #alumno que cumple con todos los requisitos
    alumno1 = Alumno(
        "A001",
        "Ana Lopez",
        7,
        "Sociedades de alumnos",
        "Miembro General",
        0,
        8,
        2,
        2,
        True
    )

    #alumno de gestion con requisitos pendientes
    alumno2 = GestionRe(
        "A002",
        "Luis Perez",
        6,
        "FESAL",
        "Directivo GestionRe",
        1,
        "2026-2027",
        "Activo",
        1,
        5,
        1,
        1,
        seminario=False
    )

    alumno2.agregarRequisito(requisitoEvento)
    alumno2.agregarRequisito(requisitoAcademico)

    coordinador = Coordinador(
        "C001",
        "1234",
        "Coordinacion RE",
        [],
        "General",
        2026
    )

    coordinador.darDeAltaAlumno(alumno1)
    coordinador.darDeAltaAlumno(alumno2)

    sociedades.agregarAlumno(alumno1)
    fesal.agregarAlumno(alumno2)

    print("\n3. ALUMNOS Y COORDINADOR")
    print(coordinador)
    print(alumno1)
    print(alumno2)

    print("\n4. PROGRESO")
    print(alumno1.mostrarProgreso())
    print("Graduacion Alumno 1:", alumno1.verificarGraduacion())
    print(alumno2.mostrarProgreso())
    print("Pendientes Alumno 2:", alumno2.obtenerPendientes())
    print("Avance requisitos especiales Alumno 2:", alumno2.calcularPorcentajeAvance(), "%")

    #guardamos y cargamos los objetos usando la clase que ya tenia el equipo
    gestor = GestorArchivos(str(archivoAlumnos), str(archivoLog))

    print("\n5. GUARDADO")
    gestor.guardarAlumnos(coordinador.obtenerTodosLosAlumnos())
    print("Alumnos guardados en alumnos.txt")

    print("\n6. CARGA")
    alumnosCargados = gestor.cargarAlumnos()
    for alumno in alumnosCargados:
        print("Objeto reconstruido:", alumno)
        print("Tipo:", type(alumno).__name__)

    print("\n7. ERRORES PROVOCADOS Y CONTROLADOS")

    #Error 1: archivo que no existe
    try:
        with open(carpeta / "archivo_que_no_existe.txt", "r", encoding="utf-8") as archivo:
            archivo.read()
    except FileNotFoundError as error:
        gestor.registrarError("FileNotFoundError", str(error))
        print("Error controlado: FileNotFoundError")

    #Error 2: semestre fuera del rango permitido
    try:
        Alumno(
            "A003",
            "Alumno Prueba",
            20,
            "ASUA",
            "Miembro General",
            0
        )
    except ValueError as error:
        gestor.registrarError("ValueError", str(error))
        print("Error controlado: ValueError")

    #Error 3: se manda texto cuando el requisito necesita un entero
    try:
        requisitoCantidad.registrarAvance("ocho")
    except TypeError as error:
        gestor.registrarError("TypeError", str(error))
        print("Error controlado: TypeError")

    print("\nPrograma terminado correctamente.")
    print("Se generaron alumnos.txt y log_errores.txt")


if __name__ == "__main__":
    main()
