
from abc import ABCMeta, abstractmethod
from enum import Enum


class ListaDestinos(Enum):
    LORCA = "LORCA"
    CARTAGENA = "CARTAGENA"
    MURCIA = "MURCIA"
    YECLA = "YECLA"
    JUMILLA = "JUMILLA"


class CanalEntrada(Enum):
    IMPRESO = 0
    TELEFONO = 1
    FAX = 2


class ModalidadEnvio(Enum):
    DOMICILIO = 0
    CENTRAL = 1


class Persona(metaclass=ABCMeta):

    def __init__(self, nombre, direccion, dni):
        self.nombre = nombre
        self.direccion = direccion
        self.dni = dni

    @abstractmethod
    def devolverDatos(self):
        pass


class Paquete:

    def __init__(self, peso, destino):
        self.peso = peso
        self.destino = destino
        self.id = None
        self.entregado = False
        self.asignado = False

    def devolverDatos(self):
        print('Paquete:', self.id, ', Peso:', self.peso, ', Destino:', self.destino,
              ', Entregado:', self.entregado, ', Asignado:', self.asignado)


class Pedido:

    def __init__(self, paquetes, canalEntrada, modalidadEnvio):
        self.id = None
        self.canalEntrada = canalEntrada
        self.modalidadEnvio = modalidadEnvio
        self.paquetes = paquetes

    def calcularCoste(self):
        coste = 0
        for paquete in self.paquetes:
            if paquete.destino == ListaDestinos.LORCA:
                coste += 8
            elif paquete.destino == ListaDestinos.CARTAGENA:
                coste += 7
            elif paquete.destino == ListaDestinos.MURCIA:
                coste += 3
            elif paquete.destino == ListaDestinos.YECLA:
                coste += 12
            elif paquete.destino == ListaDestinos.JUMILLA:
                coste += 10

        # Coste adicional si el envío es a domicilio.
        if self.modalidadEnvio == ModalidadEnvio.DOMICILIO:
            coste += 5

        return coste

    def devolverDatos(self):
        print('Pedido: ', self.id, ', Canal de Entrada: ',
              self.canalEntrada, ', Modalidad de Envio: ', self.modalidadEnvio)

        for paquete in self.paquetes:
            paquete.devolverDatos()


class Cliente(Persona):

    def __init__(self, nombre, direccion, dni):
        Persona.__init__(self, nombre, direccion, dni)
        self.pedidosmensuales = []
        self.cesta = []

    def devolverDatos(self):
        print('Cliente:', self.nombre, ', Direccion:', self.direccion,
              ', DNI:', self.dni, ', Pedidos mensuales:', self.pedidosmensuales, ', Cesta activa:', self.cesta)

    def listadoPaquetes(self):
        print('LISTADO PAQUETES')
        for paquete in self.cesta:
            print('Paquete:', paquete.id, ', Peso:',
                  paquete.peso, ', Destino:', paquete.destino)

    def realizarPedido(self, canal, envio, Empresa):
        pedido = Pedido(self.cesta, canal, envio)
        self.pedidosmensuales.append(pedido)
        self.cesta = []
        Empresa.capturarPedido(pedido)

    def agregarPaquete(self, peso, destino):
        paquete = Paquete(peso, destino)
        paquete.id = len(self.cesta)
        self.cesta.append(paquete)

    def quitarPaquete(self, id):
        for paquete in self.cesta:
            if paquete.id == id:
                self.cesta.remove(paquete)

    def getPedidosMensuales(self):
        facturacion = 0
        for pedido in self.pedidosmensuales:
            facturacion += pedido.calcularCoste()
        self.pedidosmensuales = []
        return facturacion


class Trabajador(Persona, metaclass=ABCMeta):

    def __init__(self, nombre, direccion, dni, salario):
        Persona.__init__(self, nombre, direccion, dni)
        self.salario = salario
        self.disponible = True

    @abstractmethod
    def devolverDatos(self):
        pass

    def cambiarDisponibilidad(self):
        if self.disponible:
            self.disponible = False
        else:
            self.disponible = True


class Conductor(Trabajador):

    def __init__(self, nombre, direccion, dni, salario):
        Trabajador.__init__(self, nombre, direccion, dni, salario)

    def devolverDatos(self):
        print('Conductor:', self.nombre, ', Direccion:', self.direccion,
              ', DNI:', self.dni, ', Salario:', self.salario, ', Disponible:', self.disponible)


class Ayudante(Trabajador):

    def __init__(self, nombre, direccion, dni, salario):
        Trabajador.__init__(self, nombre, direccion, dni, salario)

    def devolverDatos(self):
        print('Ayudante:', self.nombre, ', Direccion:', self.direccion,
              ', DNI:', self.dni, ', Salario:', self.salario, ', Disponible:', self.disponible)


class Ambos(Ayudante, Conductor, Trabajador):  # duda
    def __init__(self, nombre, direccion, dni, salario):
        Ayudante.__init__(self, nombre, direccion, dni, salario)
        Conductor.__init__(self, nombre, direccion, dni, salario)

    def devolverDatos(self):
        print('Ambos:', self.nombre, ', Direccion:', self.direccion,
              ', DNI:', self.dni, ', salario:', self.salario, ', Disponible:', self.disponible)
