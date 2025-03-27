from abc import ABCMeta, abstractmethod
from enum import Enum


# Enumerados
class CanalEntrada(Enum):
    IMPRESO = 0
    TELEFONO = 1
    FAX = 2


class ModalidadEnvio(Enum):
    DOMICILIO = 0
    CENTRAL = 1


class ListaDestinos(Enum):
    LORCA = "LORCA"
    CARTAGENA = "CARTAGENA"
    MURCIA = "MURCIA"
    YECLA = "YECLA"
    JUMILLA = "JUMILLA"


class Persona(metaclass=ABCMeta):
    def __init__(self, dni: str, edad: int, nombre: str, direccion: str):
        self.dni = dni
        self.edad = edad
        self.nombre = nombre
        self.direccion = direccion

    @abstractmethod
    def get_persona(self):
        pass
