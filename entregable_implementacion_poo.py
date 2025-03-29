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

    def registrarParte(self, fecha, localizacion, causa):
        parte = Incidencia(fecha, localizacion, causa)
        return parte

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
    def __init__(self, combustible, vatios):
        self.combustible = combustible
        self.vatios = vatios
        # En el caso de la bicicleta electrica, el combustible es electrico y los vatios son los que consume.
        # En el caso de la bicicleta tradicional, no tiene ni combustible ni vatios, por lo que se le asigna None.


class BicicletaTradicional(Vehiculo, Ecologico):
    def __init__(self, matricula, capacidad):
        Vehiculo.__init__(self, matricula, capacidad)
        Ecologico.__init__(self, combustible=None, vatios=None)

    def devolverDatos(self):
        print('Bicicleta tradicional:', self.matricula, ', Capacidad:', self.capacidad,
              ', Disponible:', self.disponible)


class BicicletaElectrica(Vehiculo, Motorizado, Ecologico):
    def __init__(self, matricula, capacidad, combustible):
        Vehiculo.__init__(self, matricula, capacidad)
        Motorizado.__init__(self, combustible)
        Ecologico.__init__(self, combustible, vatios)

    def devolverDatos(self):
        print('Bicicleta electrica:', self.matricula, ', Capacidad:', self.capacidad, ', Disponible:',
              self.disponible, ', Consumo:', self.combustible, ', Vatios:', self.vatios)

# bien


class Incidencia:
    # El id se asigna cuando se añade la incidencia, viendo el tamaño de la lista de incidencias.
    def __init__(self, fecha, localizacion, causa):
        self.fecha = fecha
        self.localizacion = localizacion
        self.causa = causa
        self.id = None

    def devolverDatos(self):
        print('Incidencia:', self.id, ', Fecha:', self.fecha,
              ', Localizacion:', self.localizacion, ', Causa:', self.causa)


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

    def devolverEstadoViaje(self):
        if self.terminado:
            print(f'Viaje a {self.destino} terminado.')
        else:
            print(f'Viaje a {self.destino} no terminado.')

    def asignarTrabajador(self, Empresa):
        # Si el destino es Yecla o Jumilla, solo se asigna un conductor o una persona que cumpla ambos roles, porque para esos sitios solo es necesario un trabajador.
        if (ListaDestinos.YECLA.value or ListaDestinos.JUMILLA.value) == self.destino:
            for trabajador in Empresa.trabajadores:
                if (isinstance(trabajador, Conductor) or isinstance(trabajador, Ambos)) and trabajador.disponible:
                    trabajador.cambiarDisponibilidad()
                    self.trabajadores.append(trabajador)
                if len(self.trabajadores) == 1:
                    break
        else:  # Pero para Lorca, Cartagena o Murcia, se asignan dos trabajadores, pues si sera necesario un ayudante.
            for trabajador in Empresa.trabajadores:
                if (isinstance(trabajador, Conductor) or isinstance(trabajador, Ambos)) and trabajador.disponible:
                    trabajador.cambiarDisponibilidad()
                    self.trabajadores.append(trabajador)
                if (isinstance(trabajador, Ayudante) or isinstance(trabajador, Ambos)) and trabajador.disponible:
                    trabajador.cambiarDisponibilidad()
                    self.trabajadores.append(trabajador)
                if len(self.trabajadores) == 2:
                    break

    def asignarVehiculosYPedidos(self, Empresa):
        paquetes_por_destino = {}
        for destino in ListaDestinos:
            paquetes_por_destino[destino.value] = []

        for pedido in self.pedidos:
            for paquete in pedido.paquetes:
                if not paquete.asignado:
                    paquetes_por_destino[paquete.destino.value].append(paquete)

        for destino, paquetes in paquetes_por_destino.items():
            carga_total = sum(paquete.peso for paquete in paquetes)
            for vehiculo in Empresa.vehiculos:
                if vehiculo.disponible and vehiculo.capacidad >= carga_total:
                    vehiculo.cambiarDisponibilidad()
                    self.vehiculo = vehiculo
                    print(
                        f"Vehículo asignado: {vehiculo.matricula} con capacidad: {vehiculo.capacidad} para un total de {carga_total}kg a {destino}.")

                    for paquete in paquetes:
                        if paquete.destino == destino:
                            paquete.asignado = True

                    break

    def registrarIncidencia(self, fecha, localizacion, causa):
        for trabajador in self.trabajadores:
            if isinstance(trabajador, Ayudante) or isinstance(trabajador, Ambos):
                incidencia = trabajador.registrarParte(
                    fecha, localizacion, causa)
                incidencia.id = len(self.parte)
                self.parte.append(incidencia)
                break

    def listadoIncidencias(self):
        if self.parte:
            print("LISTADO DE INCIDENCIAS")
            for incidencia in self.parte:
                incidencia.devolverDatos()
        else:
            print("Sin incidencias registradas.")

    def finalizarViaje(self):
        for paquete in self.pedidos:
            paquete.entregado = True
        for trabajador in self.trabajadores:
            trabajador.cambiarDisponibilidad()
        self.vehiculo.cambiarDisponibilidad()
        self.terminado = True


class Empresa:
    def __init__(self):
        self.vehiculos = []
        self.trabajadores = []
        self.clientes = []
        self.pedidos = []
        self.viajes = []

    # Hemos asignado un peso fijo a cada tipo de vehhiculo.
    def registrarVehiculo(self, matricula, tipo, combustible=None, vatios=None):
        if tipo == 'CAMION':
            if combustible == Combustible.GASOLINA.value or combustible == Combustible.DIESEL.value:
                vehiculo = Camion(matricula, 700, combustible)
            else:
                raise ValueError(
                    f"Combustible '{combustible}' no valido para camion.")

        elif tipo == 'FURGONETA':
            if combustible == Combustible.GASOLINA.value or combustible == Combustible.DIESEL.value:
                vehiculo = Furgoneta(matricula, 350, combustible)
            else:
                raise ValueError(
                    f"Combustible '{combustible}' no valido para furgoneta.")

        elif tipo == 'BICICLETA TRADICIONAL':
            vehiculo = BicicletaTradicional(matricula, 20)

        elif tipo == 'BICICLETA ELECTRICA':
            if combustible == Combustible.ELECTRICO.value:
                vehiculo = BicicletaElectrica(
                    matricula, 40, combustible, vatios)
            else:
                raise ValueError(
                    f"Combustible '{combustible}' no valido para bicicleta electrica.")

        else:
            raise ValueError(f"Tipo de vehículo '{tipo}' no reconocido.")
        self.vehiculos.append(vehiculo)

    def registrarTrabajador(self, nombre, direccion, dni, salario, rol):
        if rol == 'CONDUCTOR':
            trabajador = Conductor(nombre, direccion, dni, salario)
        elif rol == 'AYUDANTE':
            trabajador = Ayudante(nombre, direccion,  dni, salario)
        elif rol == 'AMBOS':
            trabajador = Ambos(nombre, direccion, dni, salario)
        else:
            raise ValueError(f"Rol de trabajador '{rol}' no valido.")
        self.trabajadores.append(trabajador)
        return trabajador

    def registrarCliente(self, nombre, direccion, dni):
        cliente = Cliente(nombre, direccion, dni)
        self.clientes.append(cliente)
        return cliente

    def registrarPedido(self, pedido):
        pedido.id = len(self.pedidos)
        self.pedidos.append(pedido)

    def crearViaje(self, fecha, destino):
        viaje = Viaje(fecha, destino)
        viaje.id = len(self.viajes)
        viaje.asignarVehiculosYPedidos(self)
        viaje.asignarTrabajador(self)
        self.viajes.append(viaje)
        return viaje
