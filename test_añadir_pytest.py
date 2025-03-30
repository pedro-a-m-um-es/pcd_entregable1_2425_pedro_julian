'''import pytest
from entregable_implementacion_poo import *


def test_registrar_vehiculo():
    empresa = Empresa()
    empresa.registrarVehiculo(
        '1111AAA', 'CAMION', Combustible.DIESEL, vatios=None)
    empresa.registrarVehiculo(
        '2222BBB', 'FURGONETA', Combustible.GASOLINA, vatios=None)
    empresa.registrarVehiculo(
        '3333CCC', 'BICICLETA ELECTRICA', Combustible.ELECTRICO, 500)
    empresa.registrarVehiculo(
        '4444DDD', 'BICICLETA TRADICIONAL')
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
    empresa.registrarCliente(
        'Carlos Sobera', "Calle Central", '24680245P')
    assert (len(empresa.clientes)) == 1


def test_registrar_pedido():
    empresa = Empresa()
    empresa.registrarCliente(
        'Carlos Sobera', "Calle Central", '24680245P')
    assert (len(empresa.clientes)) == 1


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


def test_cliente_factura_mensual():
    empresa = Empresa()
    cliente = empresa.registrarCliente(
        'Carlos Sobera', "Calle Central", '24680245P')
    cliente.agregarPaquete(18, ListaDestinos.CARTAGENA)
    cliente.agregarPaquete(25, ListaDestinos.MURCIA)
    cliente.realizarPedido(
        CanalEntrada.FAX, ModalidadEnvio.DOMICILIO, empresa)

    cliente.facturaMensual()

    assert len(empresa.pedidos) == 1
    assert cliente.facturaMensual() == 43



def test_cliente_creacion():
    cliente = Cliente("Juan Perez", "Calle Falsa 123", "12345678A")
    assert cliente.nombre == "Juan Perez"
    assert cliente.direccion == "Calle Falsa 123"
    assert cliente.dni == "12345678A"


def test_cliente_agregar_paquete():
    cliente = Cliente("Juan Perez", "Calle Falsa 123", "12345678A")
    cliente.agregarPaquete(10, ListaDestinos.LORCA)
    assert len(cliente.carrito) == 1
    assert cliente.carrito[0].peso == 10
    assert cliente.carrito[0].destino == ListaDestinos.LORCA


def test_pedido_calculo_coste():
    paquete1 = Paquete(5, ListaDestinos.LORCA)
    paquete2 = Paquete(10, ListaDestinos.LORCA)
    paquete3 = Paquete(8, ListaDestinos.MURCIA)
    pedido = Pedido([paquete1, paquete2, paquete3],
                    CanalEntrada.TELEFONO, ModalidadEnvio.DOMICILIO)
    assert pedido.calcularCoste() == 16  # 8 (Lorca) + 3 (Murcia) + 5 (Domicilio)


def test_trabajador_disponibilidad():
    conductor = Conductor("Carlos Lopez", "Av. Central 45", "87654321B", 2000)
    assert conductor.disponible == True
    conductor.cambiarDisponibilidad()
    assert conductor.disponible == False
    conductor.cambiarDisponibilidad()
    assert conductor.disponible == True


def test_asignacion_vehiculo():
    empresa = Empresa()
    camion = Camion("1234ABC", 1000, Combustible.DIESEL)
    empresa.vehiculos.append(camion)
    viaje = Viaje("2025-03-30", ListaDestinos.LORCA)
    paquete1 = Paquete(500, ListaDestinos.LORCA)
    paquete2 = Paquete(300, ListaDestinos.LORCA)
    pedido = Pedido([paquete1, paquete2],
                    CanalEntrada.TELEFONO, ModalidadEnvio.CENTRAL)
    empresa.registrarPedido(pedido)
    viaje.pedidos.append(pedido)
    viaje.asignarVehiculosYPedidos(empresa)
    assert viaje.vehiculo is not None
    assert viaje.vehiculo.matricula == "1234ABC"
    assert all(paquete.asignado for paquete in pedido.paquetes)


if __name__ == "__main__":
    pytest.main()
'''
