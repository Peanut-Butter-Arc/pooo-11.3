# -*- coding: utf-8 -*-
#raul isaac santos ruiz
#silvana de alba uribe
#este archivo define las excepciones personalizadas del sistema


#definimos la clase base para los errores propios del sistema
class SistemaREError(Exception):
    pass


#esta clase se lanza cuando se intenta guardar un id que ya existe
class RegistroDuplicadoError(SistemaREError):
    pass


#esta clase se lanza cuando se busca o elimina un id que no existe
class AlumnoNoEncontradoError(SistemaREError):
    pass
