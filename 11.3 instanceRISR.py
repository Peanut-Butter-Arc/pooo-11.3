def main():
    print("Bienvenido al sistema de biblioteca")

    biblioteca = Biblioteca()
    biblioteca.menu()

if __name__ ++ "__main__":
    main()

from enum import *

@unique
class EstadoLibro(Enum):
    DISPONIBLE = 1
    AGOTADO =1

class Usuario:
    def __init__(self,idUsuario,nombre,librosApartados):

        self.__idUsuario = idUsuario
        self.nombre = nombre
        self.librosApartados = librosApartados

    def agregarPrestamo():
        pass

    def mostrarPrestamo():
        pass

    def __str__(self):
        pass
        
class Libro:
    def __init__(self,isbn,titulo,ejemplares,estado):

        self.__isbn = isbn 
        self.titulo =titulo
        self.__ejemplares = ejemplares
        self.estado = estado

    def getEjemplares():
        pass

    def restarEjemplares():
        pass

    def getTitulo():
        pass

    def __str__(self):
        pass

class Biblioteca:
    def __init__(self,catalogo,usuarios):
        self.catalogo = catalogo
        self.usuarios = usuarios

    def AgregarLibro(self,titulo,isbn,ejemplares):
        self.catalogo.nombre = titulo
        self.catalogo.isbn = isbn
        self.catalogo.ejemplares = ejemplares

    def buscarCatalogo(self):
        print Libro1.get
        
    def buscarLibro(self):
        pass
        
    def verDisponibilidad(self):
        pass
    def apartarLibro(self):
        pass
    def registrarUsuario(self):
        pass
        menu()

        
catalogoDiccionario = {

    "1001": Libro(
        "1001",
        "Python desde Cero",
        5,
        EstadoLibro.DISPONIBLE
    ),

    "1002": Libro(
        "1002",
        "POO",
        2,
        EstadoLibro.DISPONIBLE
    ),

    "1003": Libro(
        "1002",
        "Estructura de datos",
        0,
        EstadoLibro.PRESTADO
    )


}

i = 0;

while(i!=0):

    print("=========================")
    print("        Biblioteca       ")
    print("=========================")

    print("1. Mostrar catalogo")
    print("2. Buscar Libro")
    print("3. Ver disponibilidad")
    print("4. Apartar Libro")
    print("5. Mostrar Prestamos")
    print("6. Salir")
    try:
        x=int(input("Seleccione una opcion"))
        if not isinstance(x,str):
            raise ValueError
        
        if ( x = 1):

    
        if ( x = 2):

    
        if ( x = 3):
    except ValueError:


    


    
