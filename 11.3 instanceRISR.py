from enum import *

@unique
class EstadoLibro(Enum):
    DISPONIBLE = 1
    AGOTADO = 2
    PRESTADO = 3

class Usuario:
    def __init__(self,idUsuario,nombre,librosApartados=None,estado=EstadoLibro.DISPONIBLE):
        self.__idUsuario = idUsuario
        self.nombre = nombre
        if librosApartados is None:
            self.librosApartados = []
        else:
            self.librosApartados = librosApartados
        self.estado = estado

    def agregarPrestamo(self,libro):
        self.librosApartados.append(libro)

    def mostrarPrestamo(self):
        if len(self.librosApartados) == 0:
            print("No tiene libros apartados")
        else:
            for libro in self.librosApartados:
                print(libro)

    def getUsuario(self):
        return self.__idUsuario

    def __str__(self):
        return f"ID: {self.__idUsuario} | Nombre: {self.nombre} | Libros apartados: {len(self.librosApartados)}"

class Libro:
    def __init__(self,isbn,titulo,ejemplares,estado):
        self.__isbn = isbn 
        self.titulo = titulo
        self.__ejemplares = ejemplares
        self.estado = estado

    def getIsbn(self):
        return self.__isbn

    def getEjemplares(self):
        return self.__ejemplares

    def restarEjemplares(self):
        self.__ejemplares -= 1
        if self.__ejemplares == 0:
            self.estado = EstadoLibro.AGOTADO

    def getTitulo(self):
        return self.titulo

    def __str__(self):
        return f"ISBN: {self.__isbn} | Titulo: {self.titulo} | Ejemplares: {self.__ejemplares} | Estado: {self.estado.name}"

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
        "1003",
        "Estructura de datos",
        0,
        EstadoLibro.PRESTADO
    )
}

usuariosLista = [
    Usuario(1, "Ana López"),
    Usuario(2, "Luis Pérez"),
    Usuario(3, "María García")
]

#CLASE LIBRO

class Libro:
    def __init__(self,isbn,titulo,ejemplares,estado):

        self.__isbn = isbn 
        self.titulo = titulo
        self.__ejemplares = ejemplares
        self.estado = estado


    #Regresa la cantidad de ejemplares disponibles
    def getEjemplares(self):
        return self.__ejemplares


    #Resta un ejemplar cuando alguien aparta un libro
    def restarEjemplares(self):

        if self.__ejemplares > 0:

            self.__ejemplares = self.__ejemplares - 1

            #Si ya no quedan ejemplares, el libro cambia a agotado
            if self.__ejemplares == 0:
                self.estado = EstadoLibro.AGOTADO

        else:
            raise ValueError(
                "Lo sentimos este libro no esta disponible"
            )


    #Regresa el título del libro
    def getTitulo(self):
        return self.titulo


    #Permite imprimir la información del libro
    def __str__(self):

        return (
            "ISBN: " + self.__isbn
            + " | Titulo: " + self.titulo
            + " | Ejemplares: " + str(self.__ejemplares)
            + " | Estado: " + self.estado.name
        )

class Biblioteca:
    def __init__(self,catalogo=catalogoDiccionario,usuarios=usuariosLista):
        self.catalogo = catalogo
        self.usuarios = usuarios

    def AgregarLibro(self,titulo,isbn,ejemplares):
        estado = EstadoLibro.DISPONIBLE if ejemplares > 0 else EstadoLibro.AGOTADO
        self.catalogo[isbn] = Libro(isbn,titulo,ejemplares,estado)

    def mostrarCatalogo(self):
        for isbn, libro in self.catalogo.items():
            print(libro)

    def buscarCatalogo(self,isbn):
        if isbn in self.catalogo:
            return self.catalogo[isbn]
        return None
        
    def buscarLibro(self):
        try:
            isbn = input("Ingrese el ISBN del libro: ")
            if not isinstance(isbn,str) or isbn == "":
                raise ValueError
            libro = self.buscarCatalogo(isbn)
            if (libro != None):
                print(libro)
            else:
                print("Libro no encontrado")
        except ValueError:
            print("Lo sentimos hubo un error en el sistema")
        
    def verDisponibilidad(self):
        try:
            isbn = input("Ingrese el ISBN del libro: ")
            libro = self.buscarCatalogo(isbn)
            if (libro != None):
                print(f"La cantidad disponible del libro: {libro.getTitulo()} es de {libro.getEjemplares()} ({libro.estado.name})")
            else:
                print("Libro no encontrado")
        except ValueError:
            print("Lo sentimos hubo un error en el sistema")

    def apartarLibro(self):
        try:
            idU = int(input("Ingrese el id del usuario: "))
            usuarioEncontrado = None
            for u in self.usuarios:
                if (u.getUsuario() == idU):
                    usuarioEncontrado = u
                    break

            if (usuarioEncontrado == None):
                print("Usuario no encontrado")
                return

            isbn = input("Ingrese el ISBN del libro a apartar: ")
            libro = self.buscarCatalogo(isbn)

            if (libro == None):
                print("Libro no encontrado")
                return

            disponibilidad = libro.getEjemplares()
            if (disponibilidad <= 0):
                raise ValueError("Lo sentimos este libro no esta disponible")
            else:
                libro.restarEjemplares()
                usuarioEncontrado.agregarPrestamo(libro)
                print(f"Libro '{libro.getTitulo()}' apartado con exito por {usuarioEncontrado.nombre}")

        except ValueError:
            print("Lo sentimos hubo un error en el sistema o el libro no esta disponible")

    def mostrarPrestamos(self):
        for u in self.usuarios:
            print(u)
            u.mostrarPrestamo()

    def registrarUsuario(self):
        try:
            x = input("Ingrese el nombre del usuario: ")
            y = int(input("Ingrese el id del usuario: "))
            z = int(input("Ingrese la cantidad de libros apartados del usuario: "))

            usuario1 = Usuario(y,x,[])
            self.usuarios.append(usuario1)
        except ValueError:
            print("Lo sentimos hubo un error en el sistema")

    def menu(self):
        i = 1
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
                x = int(input("Seleccione una opcion: "))
                if not isinstance(x,int):
                    raise ValueError
        
                if (x == 1):
                    self.mostrarCatalogo()

                elif (x == 2):
                    self.buscarLibro()

                elif (x == 3):
                    self.verDisponibilidad()

                elif (x == 4):
                    self.apartarLibro()

                elif (x == 5):
                    self.mostrarPrestamos()

                elif (x == 6):
                    print("Saliendo del sistema...")
                    i = 0
                else:
                    print("Opcion no valida")
            
            except ValueError:
                print("Entrada invalida, ingrese un numero")

def main():
    print("Bienvenido al sistema de biblioteca")

    biblioteca1 = Biblioteca()
    biblioteca1.menu()

if __name__ == "__main__":
    main()
