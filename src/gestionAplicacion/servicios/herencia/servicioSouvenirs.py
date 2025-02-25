import datetime
from gestionAplicacion.servicios.herencia.servicio import Servicio

class ServicioSouvenir(Servicio):
    
    def __init__(self, nombre, sucursalUbicacion):
        super().__init__(nombre, sucursalUbicacion)
    
    def actualizarInventario(self):
        inventario_general = self.cliente.getCineUbicacionActual().getInventarioCine()
        inventario = []
        for producto in inventario_general:
            if producto.getTipoProducto() == "souvenir":
                inventario.append(producto)
        return inventario


    def descontarPorCompra(self, metodo):
        if metodo.getNombre() != "Efectivo":
            for producto in self._orden:
                if (producto.getTamaño() in ["Katana", "Emociones"]) and (producto.getPrecio() > 100000):
                    self._valorPedido -= self._valorPedido * 0.05
                    return True
            return False
        return False
        
    def factura(self):

        factura = (
            "                          CINEMAR \n"
            "==================== Factura de Souvenir ====================\n"
            f" Nombre dueño : {self.cliente.getNombre()}\n"
            f" Fecha de compra: {datetime.date.today()}\n"
            f"{self.mostrarOrden()}\n"
            "===========================================================\n"
        )
        return factura

    def procesarPagoRealizado(self, cliente):
        self.descuento = True
        for productoOrden in self._orden:
            validacionIngresoHistorial = True
            for productoHistorial in cliente.getHistorialDePedidos():
                if (productoOrden._nombre.lower() == productoHistorial._nombre.lower() and
                    productoOrden._tamaño.lower() == productoHistorial._tamaño.lower()):
                    validacionIngresoHistorial = False
                    break
            if validacionIngresoHistorial:
                cliente.getProductosDisponiblesParaCalificar().append(productoOrden)
                cliente.getHistorialDePedidos().append(productoOrden)


                