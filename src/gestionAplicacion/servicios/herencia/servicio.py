
from abc import ABC, abstractmethod
import random
from gestionAplicacion.servicios.producto import Producto
from gestionAplicacion.servicios.producto import Producto
from gestionAplicacion.usuario.ibuyable import Ibuyable

class Servicio (ABC, Ibuyable):
    cliente  = None
    descuento = True
    def __init__(self, nombre, sucursalUbicacion):
        self._nombre = nombre
        self._inventario = []
        self._orden = []
        self._bonosCliente = []
        self._valorPedido = 0.0
        self._sucursalUbicacion = sucursalUbicacion
        self._sucursalUbicacion.getServicios().append(self)

        
    @abstractmethod
    def descuentarPorCompra(self, metodo):
        pass

    @abstractmethod
    def actualizarInventario(self):
        pass

    @staticmethod
    def mostrarBonos(servicio):
        n = 0
        b = []
        for bono in servicio.getBonosCliente():
            n += 1
            b.append(f"\n{bono.getProducto().getNombre()} {bono.getProducto().getTamaño()}")
        return b

    def actualizarBonos(self):
        for bono in self._sucursalUbicacion.getBonosCreados():
            if bono.getTipoServicio() == self.getNombre() and bono.getCliente().getNombre() == self.cliente.getNombre():
                self.getBonosCliente().append(bono) 

    def descuentarPorGenero(self, cine):
        for producto in self._orden:
            for ticket in cine.getTicketsParaDescuento():
                if producto.getGenero() == ticket.getPelicula().getGenero() and self.cliente == ticket.getDueno():
                    fecha = self._sucursalUbicacion.getFechaActual().date()
                    if fecha == ticket.getHorario().date() and ticket.isDescuento():
                        ticket.setDescuento(False)
                        return producto
        return None

    def calcularTotal(self):
        total = 0
        for producto in self._orden:
            total += producto.getPrecio()
        return total

    def agregarOrden(self, producto):
        if 0 < len(self._orden):
            n=1
            for p in self._orden:
                if producto.getNombre() == p.getNombre() and producto.getTamaño() == p.getTamaño():
                    p.setCantidad(int(p.getCantidad()) + int(producto.getCantidad()))
                    p.setPrecio(p.getPrecio() + producto.getPrecio())
                    break
                elif len(self._orden) == n:
                    self._orden.append(producto)
                    break
                n+=1
        else:
            self._orden.append(producto)

    def descontarProducto(self, producto):
        for p in self.orden:
            if p.getNombre() == producto.getNombre() and p.getTamaño() == producto.getTamaño():
                p.setPrecio(p.getPrecio() - producto.getPrecio())
                break

    @staticmethod
    def validarBono(codigo, servicio):
        for bono in servicio.bonos_cliente:
            if bono.getCodigo() == codigo and bono.getTipoServicio() == servicio.getNombre():
                producto = bono.getProducto
                for b in servicio.getCliente().getCineActual().getBonosCreados():
                    if b.getProducto() == producto and b.getCliente == Servicio.getCliente:
                        servicio.getCliente().getCineActual().getBonosCreados().remove(b)
                for b in servicio.getCliente().getBonos():
                    if b.getProducto() == producto :
                        servicio.getCliente().getBonos().remove(b)
                return producto
        return None

    def mostrarOrden(self):
        pedido = ""
        total = 0
        n = 0
        for producto in self._orden:
            n = n + 1 
            pedido = f"{pedido} \n{n} -- {str(producto.getCantidad())} {producto.getNombre()} {producto.getTamaño()} : ${producto.getPrecio()}"
            total += producto.getPrecio()
        pedido += f"\nTotal: ${total}"
        return pedido

    def mostrarInventario(self):
        p = []
        i = 0
        if len(self._inventario) == 0:
            return p
        for producto in self._inventario:
            i= i+1
            p.append(f"{producto.getNombre()} {producto.getTamaño()}")
        return p

    def hacerPedido(self, indice, cantidad, sucursal):
        producto_inventario = self._inventario[indice]
        if producto_inventario.getCantidad() >= cantidad:
            producto_inventario.setCantidad(producto_inventario.getCantidad() - cantidad)
            producto = Producto(producto_inventario.getNombre(), producto_inventario.getTamaño(),"", (producto_inventario.getPrecio() * cantidad), cantidad, (producto_inventario.getGenero()), sucursal)
            return producto
        return None
    

#################### PORQUE ESTA ESTE METODO AQUI Y EN SUCURSALCINE?????????????????????
#                    LE CORREGI LOS ERRORES QUE CHAT GPT LE HABIA HECHOPARA PODER EJECUTARLO


#Description: Este metodo se encarga de seleccionar las sucursales del arrayList y con el uso de la funcion random de la libreria math,
#se selecciona una sucursal aleatoriamente, ya que esto nos permetira mas adelante el cambio de sucursal de una
#pelicula a otra.
# 	 
    def seleccionar_sucursal_aleatoriamente(self,sucursal_cine):
     if len(sucursal_cine) <= 1:
        raise ValueError("No hay suficientes sucursales para seleccionar una diferente.")
    
     while True:
        numero_aleatorio = random.randint(0, len(sucursal_cine) - 1)
        sucursal_seleccionada = sucursal_cine[numero_aleatorio]
        if sucursal_cine != sucursal_seleccionada:
            return sucursal_seleccionada

    # Getters and setters
    def getNombre(self):
        return self._nombre

    def setNombre(self, nombre):
        self._nombre = nombre

    def getCliente(self):
        return self.cliente

    def setCliente(self, cliente):
        self.cliente = cliente

    def getInventario(self):
        return self._inventario

    def setInventario(self, inventario):
        self._inventario = inventario

    def getOrden(self):
        return self._orden

    def setOrden(self, orden):
        self._orden = orden

    def getValorPedido(self):
        return self._valorPedido

    def setValorPedido(self, valorPedido):
        self._valorPedido = valorPedido

    def getBonosCliente(self):
        return self._bonosCliente

    def setBonosCliente(self, bonosCliente):
        self._bonosCliente = bonosCliente

    def getDescuento(self):
        return self.descuento

    def setDescuento(self, descuento):
        self.descuento= descuento
