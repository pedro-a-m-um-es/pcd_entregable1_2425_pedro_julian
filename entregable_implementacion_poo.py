from enum import Enum
from abc import ABCMeta, abstractmethod


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


class Combustible(Enum):
    GASOLINA = "GASOLINA"
    DIESEL = "DIESEL"
    ELECTRICO = "ELECTRICO"


class Persona(metaclass=ABCMeta):
    def __init__(self, nombre, direccion, dni):
        self.nombre = nombre
        self.direccion = direccion
        self.dni = dni

    @abstractmethod
    def devolverDatos(self):
        pass


class Paquete:
    # El id se asigna cuando se añade el paquete, viendo el tamaño del carrito.
    # El entregado y asignado se inicializan a False, ya que todavia no se ha entregado ni asignado a un viaje.
    def __init__(self, peso, destino):
        self.id = None
        self.peso = peso
        self.destino = destino
        self.entregado = False
        self.asignado = False

    def devolverDatos(self):
        print('Paquete:', self.id, ', Peso:', self.peso, ', Destino:', self.destino,
              ', Entregado:', self.entregado, ', Viaje Asignado:', self.asignado)


class Pedido:
    # Aqui ocurre lo mismo, el id se asigna cuando se añade el pedido a la lista de pedidos de la empresa.
    def __init__(self, paquetes, canalEntrada, modalidadEnvio):
        self.paquetes = paquetes
        self.canalEntrada = canalEntrada
        self.modalidadEnvio = modalidadEnvio
        self.id = None

    def calcularCoste(self):
        # En funcion de a donde vaya el paquete, se le asigna un coste diferente. Sin embargo, si dos o mas paquetes del pedido van a la misma ciudad,
        # solo se cobrara una vez. Ademas, si el envio es a domicilio, se le añade un coste adicional.
        # El peso no afecta al coste.
        elegido = set()
        coste = 0
        if self.modalidadEnvio == ModalidadEnvio.DOMICILIO.value:
            coste += 5
        for paquete in self.paquetes:
            if paquete.destino in elegido:
                coste += 0
            else:
                if paquete.destino == ListaDestinos.LORCA.value:
                    coste += 8
                elif paquete.destino == ListaDestinos.CARTAGENA.value:
                    coste += 7
                elif paquete.destino == ListaDestinos.MURCIA.value:
                    coste += 3
                elif paquete.destino == ListaDestinos.YECLA.value:
                    coste += 12
                elif paquete.destino == ListaDestinos.JUMILLA.value:
                    coste += 10
                elegido.add(paquete.destino)
        elegido.clear()
        return coste

    # Devolvemos los datos del pedido, el canal de entrada y la modalidad de envio, además de los paquetes que contiene.
    def devolverDatos(self):
        print('Pedido: ', self.id, ', Canal de Entrada: ',
              self.canalEntrada, ', Modalidad de Envio: ', self.modalidadEnvio)
        for paquete in self.paquetes:
            paquete.devolverDatos()


class Cliente(Persona):
    # El cliente x ira añadiendo paquetes a su carrito, hasta que decida realizar un pedido con ellos. Ahi, se añade el pedido a la lista de pedidos mensuales
    # y se vacia la carrito.
    def __init__(self, nombre, direccion, dni):
        Persona.__init__(self, nombre, direccion, dni)
        self.carrito = []
        self.pedidosmensuales = []

    def devolverDatos(self):
        print('Cliente:', self.nombre, ', Direccion:', self.direccion,
              ', DNI:', self.dni, ', Pedidos mensuales:', self.pedidosmensuales, ', Carrito:', self.carrito)

    def agregarPaquete(self, peso, destino):
        paquete = Paquete(peso, destino)
        paquete.id = len(self.carrito)
        self.carrito.append(paquete)

    def quitarPaquete(self, id):
        for paquete in self.carrito:
            if paquete.id == id:
                self.carrito.remove(paquete)

    # Se registra el pedido en la empresa, en los pedidos mensuales del cliente y se vacia el carrito.
    def realizarPedido(self, canal, envio, Empresa):
        pedido = Pedido(self.carrito, canal, envio)
        Empresa.registrarPedido(pedido)
        self.pedidosmensuales.append(pedido)
        self.carrito.clear()

    def listadoPaquetes(self):
        print('LISTADO DE PAQUETES')
        for paquete in self.carrito:
            print('Paquete:', paquete.id, ', Peso:',
                  paquete.peso, ', Destino:', paquete.destino)

    # Calculamos la factura mensual del cliente, sumando el coste de todos los pedidos mensuales.
    def facturaMensual(self):
        factura_mensual = 0
        for pedido in self.pedidosmensuales:
            factura_mensual += pedido.calcularCoste()
        self.pedidosmensuales = []
        return factura_mensual


class Trabajador(Persona, metaclass=ABCMeta):
    def __init__(self, nombre, direccion, dni, salario):
        Persona.__init__(self, nombre, direccion, dni)
        self.salario = salario
        # El trabajador inicialmente esta siempre disponible, pues todavia no ha sido asignado a ningun viaje.
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

    def registrarParte(self, fecha, causa, lugar):
        incidencia = Incidencia(fecha, causa, lugar)
        return incidencia

    def devolverDatos(self):
        print('Ayudante:', self.nombre, ', Direccion:', self.direccion,
              ', DNI:', self.dni, ', Salario:', self.salario, ', Disponible:', self.disponible)


class Ambos(Ayudante, Conductor, Trabajador):
    def __init__(self, nombre, direccion, dni, salario):
        Ayudante.__init__(self, nombre, direccion, dni, salario)
        Conductor.__init__(self, nombre, direccion, dni, salario)

    def devolverDatos(self):
        print('Ambos:', self.nombre, ', Direccion:', self.direccion,
              ', DNI:', self.dni, ', salario:', self.salario, ', Disponible:', self.disponible)


class Vehiculo(metaclass=ABCMeta):
    def __init__(self, matricula, capacidad):
        self.matricula = matricula
        self.capacidad = capacidad
        # Al igual que con trabajador, el vehiculo inicialmente esta disponible, pues todavia no ha sido asignado a ningun viaje.
        self.disponible = True

    @abstractmethod
    def devolverDatos(self):
        pass

    def cambiarDisponibilidad(self):
        if self.disponible:
            self.disponible = False
        else:
            self.disponible = True


class Motorizado(metaclass=ABCMeta):
    def __init__(self, combustible):
        self.combustible = combustible


class Camion(Vehiculo, Motorizado):
    def __init__(self, matricula, capacidad, combustible):
        Vehiculo.__init__(self, matricula, capacidad)
        Motorizado.__init__(self, combustible)

    def devolverDatos(self):
        print('Camion:', self.matricula, ', Capacidad:', self.capacidad,
              ', Disponible:', self.disponible, ', Combustible:', self.combustible)


class Furgoneta(Vehiculo, Motorizado):
    def __init__(self, matricula, capacidad, combustible):
        Vehiculo.__init__(self, matricula, capacidad)
        Motorizado.__init__(self, combustible)

    def devolverDatos(self):
        print('Furgoneta:', self.matricula, ', Capacidad:', self.capacidad,
              ', Disponible:', self.disponible, ', Combustible:', self.combustible)


class Ecologico(metaclass=ABCMeta):
    def __init__(self, tipo_energia):
        self.tipo_energia = tipo_energia


class BicicletaTradicional(Vehiculo, Ecologico):
    def __init__(self, matricula, capacidad):
        Vehiculo.__init__(self, matricula, capacidad)
        Ecologico.__init__(self, tipo_energia=None)

    def devolverDatos(self):
        print('Bicicleta tradicional:', self.matricula, ', Capacidad:', self.capacidad,
              ', Disponible:', self.disponible)


class BicicletaElectrica(Vehiculo, Motorizado, Ecologico):
    def __init__(self, matricula, capacidad, combustible, tipo_energia):
        Vehiculo.__init__(self, matricula, capacidad)
        Motorizado.__init__(self, combustible)
        Ecologico.__init__(self, tipo_energia)

    def devolverDatos(self):
        print('Bicicleta electrica:', self.matricula, ', Capacidad:', self.capacidad, ', Disponible:',
              self.disponible, ', Consumo:', self.combustible, ', Tipo de energia:', self.tipo_energia)

# bien


class Incidencia:
    # El id se asigna cuando se añade la incidencia, viendo el tamaño de la lista de incidencias.
    def __init__(self, fecha, causa, lugar):
        self.fecha = fecha
        self.causa = causa
        self.lugar = lugar
        self.id = None

    def devolverDatos(self):
        print(
            f'Incidencia ID: {self.id}, Fecha: {self.fecha}, Causa: {self.causa}, Lugar: {self.lugar}')


class Viaje:
    def __init__(self, fecha, destino):
        self.id = None
        self.fecha = fecha
        self.destino = destino
        self.pedidos = []
        self.trabajadores = []
        self.vehiculo = None
        self.parte = []
        self.terminado = False

    def devolverDatos(self):
        print('Viaje ID:', self.id)
        print('Fecha inicio:', self.fecha, ', Destino:', self.destino,
              ', Vehiculo:', self.vehiculo,  ', Finalizado:', Viaje.estadoViaje(self))
        print('Trabajadores:')
        for trabajador in self.trabajadores:
            trabajador.devolverDatos()
        print('Pedidos:')
        for pedido in self.pedidos:
            pedido.devolverDatos()

        if self.terminado:
            if len(self.parte) == 0:
                print('Sin parte de incidencias.')
            else:
                print('Parte de incidencias:')
                for incidencia in self.parte:
                    incidencia.devolverDatos()

    def estadoViaje(self):
        if self.terminado:
            print(f'Si.')
        else:
            print(f'No.')


class Empresa:
    def __init__(self):
        self.vehiculos = []
        self.trabajadores = []
        self.clientes = []
        self.pedidos = []
        self.viajes = []
