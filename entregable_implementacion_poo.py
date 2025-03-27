from abc import ABCMeta, abstractmethod
from enum import Enum


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


class Trabajador(Persona):
    def __init__(self, dni: str, edad: int, nombre: str, direccion: str, disponible: bool, salario: float):
        Persona.__init__(self, dni, edad, nombre, direccion)
        self.disponible = disponible
        self.salario = salario

    def cambiar_disponibilidad(self, disponible: bool):
        self.disponible = disponible
    '''
    def AsignarViaje(self, viaje: 'Viaje'):
        pass
    def CerrarParte(self, parte: 'Parte'):
        pass
    '''
    @abstractmethod
    def get_trabajador(self):
        pass


class Conductor(Trabajador):
    def __init__(self, dni: str, edad: int, nombre: str, direccion: str, disponible: bool, salario: float, licencia: str):
        Trabajador.__init__(self, dni, edad, nombre,
                            direccion, disponible, salario)
        self.licencia = licencia

    def get_conductor(self) -> str:
        return f"Conductor: {self.nombre}, Licencia: {self.licencia}, Disponible: {self.disponible}, Salario: {self.salario}, Edad: {self.edad}, DNI: {self.dni}, Dirección: {self.direccion}"


# ayudante aún tiene que añadir cosas de herencia de Viaje y ParteViaje
class Ayudante(Trabajador):
    def __init__(self, dni: str, edad: int, nombre: str, direccion: str, disponible: bool, salario: float, experiencia_laboral: int):
        Trabajador.__init__(self, dni, edad, nombre,
                            direccion, disponible, salario)
        self.experiencia_laboral = experiencia_laboral

    def get_ayudante(self) -> str:
        return f"Ayudante: {self.nombre}, Experiencia laboral: {self.experiencia_laboral}, Disponible: {self.disponible}, Salario: {self.salario}, Edad: {self.edad}, DNI: {self.dni}, Dirección: {self.direccion}"


class Cliente(Persona):
    def __init__(self, dni: str, edad: int, nombre: str, direccion: str):
        Persona.__init__(self, dni, edad, nombre, direccion)

    def get_cliente(self):
        return f"Cliente: {self.nombre}, Edad: {self.edad}, DNI: {self.dni}, Dirección: {self.direccion}"


class Paquete(metaclass=ABCMeta):
    def __init__(self, paquete_id: str, peso: float, destino: str):
        self.paquete_id = paquete_id
        self.peso = peso
        self.destino = destino


class Pedido(Paquete):
    def __init__(self, pedido_id: str, paquetes: List[Paquete], canal_entrada: CanalEntrada, modalidad_envio: ModalidadEnvio):
        Paquete.__init__(self, paquete_id, peso, destino)
        self.pedido = pedido
        self.cliente = cliente
        self.paquetes = paquetes
        self.canal_entrada = canal_entrada
        self.modalidad_envio = modalidad_envio
        self.conductor = None

    def calcular_coste(self) -> float:
        coste = sum(p.peso for p in self.paquetes)
        if self.modalidad_envio == ModalidadEnvio.DOMICILIO:
            coste += 10
        return coste

    def asignar_trabajador(self, trabajadores: List[Trabajador]):
        for trabajador in trabajadores:
            if isinstance(trabajador, Conductor) and trabajador.disponible:
                self.conductor = trabajador
                trabajador.cambiar_disponibilidad(False)
                print(
                    f"Conductor {trabajador.nombre} asignado al pedido {self.pedido_id}")
                return

        raise Exception("No hay conductores disponibles para este pedido.")

    def asignar_vehiculo(self, vehiculo: Vehiculo):
        if self.conductor is None:
            raise Exception("No se puede asignar vehículo sin conductor.")
        for paquete in self.paquetes:
            vehiculo.asignar_paquete(paquete)


class Vehiculo(metaclass=ABCMeta):
    def __init__(self, matricula: str, capacidad: float, paquetes: list[Paquete], disponible: bool):
        self.matricula = matricula
        self.capacidad = capacidad
        self.paquetes = paquetes
        self.disponible = disponible
