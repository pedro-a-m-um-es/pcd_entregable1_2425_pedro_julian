import pytest
from entregable_implementacion_poo import *


def test_registrar_vehiculo():
    empresa = Empresa()
    empresa.registrarVehiculo(
        '1111AAA', 'CAMION', Combustible.DIESEL, vatios=None)
    empresa.registrarVehiculo('2222BBB', 'FURGONETA',
                              Combustible.GASOLINA, vatios=None)
    empresa.registrarVehiculo(
        '3333CCC', 'BICICLETA ELECTRICA', Combustible.ELECTRICO, 500)
    empresa.registrarVehiculo('4444DDD', 'BICICLETA TRADICIONAL')
    assert (len(empresa.vehiculos)) == 4


def test_registrar_trabajador():
    empresa = Empresa()
    empresa.registrarTrabajador(
        'Perico Palotes', "Calle Central", '34567198F', 2200, "CONDUCTOR")
    empresa.registrarTrabajador(
        'Pepito Grillo', "Calle Derecha", '3476541T', 2000, "AYUDANTE")
    empresa.registrarTrabajador(
        'Maria de la Cruz', "Calle Izquierda", '87654567A', 2400, "AMBOS")
    assert (len(empresa.trabajadores)) == 3


def test_registrar_cliente():
    empresa = Empresa()
    empresa.registrarCliente('Carlos Sobera', "Calle Central", '24680245P')
    assert (len(empresa.clientes)) == 1


def test_registrar_pedido():
    empresa = Empresa()
    cliente = empresa.registrarCliente(
        'Carlos Sobera', "Calle Central", '24680245P')
    cliente.agregarPaquete(18, ListaDestinos.CARTAGENA)
    cliente.realizarPedido(CanalEntrada.FAX, ModalidadEnvio.DOMICILIO, empresa)
    assert (len(empresa.pedidos)) == 1


def test_cliente_agrega_paquete():
    empresa = Empresa()
    cliente = empresa.registrarCliente(
        'Carlos Sobera', "Calle Central", '24680245P')
    cliente.agregarPaquete(18, ListaDestinos.CARTAGENA)
    assert len(cliente.carrito) == 1


def test_cliente_realiza_pedido():
    empresa = Empresa()
    cliente = empresa.registrarCliente(
        'Carlos Sobera', "Calle Central", '24680245P')
    cliente.agregarPaquete(18, ListaDestinos.CARTAGENA)
    cliente.realizarPedido(CanalEntrada.FAX, ModalidadEnvio.DOMICILIO, empresa)
    assert len(empresa.pedidos) == 1


def test_asignar_trabajador():
    empresa = Empresa()
    trabajador = empresa.registrarTrabajador(
        'Carlos Gómez', 'Calle del Sol', '12345678Z', 1500, "CONDUCTOR")
    cliente = empresa.registrarCliente(
        'Ana Garcia', 'Calle del Mar', '87654321A')
    cliente.agregarPaquete(10, ListaDestinos.LORCA)
    cliente.realizarPedido(CanalEntrada.TELEFONO,
                           ModalidadEnvio.CENTRAL, empresa)

    viaje = Viaje("2025-03-29", ListaDestinos.LORCA)
    viaje.asignarTrabajador(empresa)

    assert len(viaje.trabajadores) == 1


def test_asignar_vehiculo():
    empresa = Empresa()
    vehiculo = empresa.registrarVehiculo(
        '9999EEE', 'CAMION', Combustible.DIESEL)
    trabajador = empresa.registrarTrabajador(
        'Juan Pérez', 'Calle del Río', '12345678X', 1800, "CONDUCTOR")
    cliente = empresa.registrarCliente(
        'Laura Lopez', 'Calle Alta', '98765432B')
    cliente.agregarPaquete(15, ListaDestinos.CARTAGENA)
    cliente.realizarPedido(CanalEntrada.IMPRESO,
                           ModalidadEnvio.DOMICILIO, empresa)

    viaje = Viaje("2025-03-29", ListaDestinos.CARTAGENA)
    viaje.asignarVehiculosYPedidos(empresa)

    assert viaje.vehiculo is not None
    assert viaje.vehiculo.matricula == '9999EEE'


def test_finalizar_viaje():
    empresa = Empresa()
    vehiculo = empresa.registrarVehiculo(
        '9999EEE', 'CAMION', Combustible.DIESEL)
    trabajador = empresa.registrarTrabajador(
        'Ana Pérez', 'Calle Azul', '45678901L', 2000, "AMBOS")
    cliente = empresa.registrarCliente(
        'Luis García', 'Calle Roja', '12398745N')
    cliente.agregarPaquete(5, ListaDestinos.MURCIA)
    cliente.realizarPedido(CanalEntrada.TELEFONO,
                           ModalidadEnvio.CENTRAL, empresa)

    viaje = Viaje("2025-03-30", ListaDestinos.MURCIA)
    viaje.asignarVehiculosYPedidos(empresa)
    viaje.asignarTrabajador(empresa)
    viaje.finalizarViaje()

    assert viaje.terminado == True


def test_registrar_incidencia():
    empresa = Empresa()
    trabajador2 = empresa.registrarTrabajador(
        'Juan Pérez', 'Calle Sur', '45678901K', 1600, "AMBOS")
    cliente = empresa.registrarCliente(
        'Pedro Sánchez', 'Calle Norte', '78945612D')
    cliente.agregarPaquete(12, ListaDestinos.YECLA)
    cliente.realizarPedido(CanalEntrada.FAX, ModalidadEnvio.DOMICILIO, empresa)

    viaje = empresa.crearViaje("2025-03-29", ListaDestinos.YECLA)
    viaje.asignarVehiculosYPedidos(empresa)
    viaje.asignarTrabajador(empresa)
    viaje.registrarIncidencia(
        "2025-03-29", "Carretera bloqueada", "Ruta Norte")

    assert len(viaje.parte) == 1
