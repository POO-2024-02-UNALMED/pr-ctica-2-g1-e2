import random
from gestionAplicacion.servicios.producto import Producto
from gestionAplicacion.usuario.ibuyable import Ibuyable
#from iuMain.administrador import *

class Bono(Ibuyable):
  
  def __init__(self, codigo = None, producto = None, tipoServicio = None, cliente = None):
    self._codigo = codigo
    self._producto = producto
    self._tipoServicio = tipoServicio
    self._cliente = cliente
    cliente.getCineUbicacionActual().getBonosCreados().append(self)

  def factura(self):
        """
        :Description: Este método se encarga de retornar un string que contiene toda la información del ticket en forma de factura.
	    :return String: Este método retorna un String que representa la factura de compra con el fin de ser mostrada en pantalla
	    luego de realizar una compra.
        """

        return	f"========= Factura Ticket =========\nNombre dueño : {self._cliente.getNombre()}\nDocumento : {self._cliente.getDocumento()}\nNombre producto:{self._producto.getNombre()}\nTamaño producto:{self._producto.getTamaño()}"



  @classmethod
  def generarBonoComidaJuegos(cls,sucursal, cliente): 

    """
    Description: Este metodo se encarga primeramente de seleccionar los productos de tipo comida
    del inventario de la sucursal, luego genera un codigo aleatorio de 7 digitos para el bono y 
    ademas escoge de esos productos seleccionados uno de manera aleatoria para ser asociado al bono
    y lo descuenta de la cantidad de disponibles, finalmente imprime por pantalla el bono al usuario

    :param sucursal: Se pasa como parámetro la sucursal de cine asociada en ese momento 
    :param cliente: Se pasa como parámetro el cliente que genera el bono
    :return Bono: Se retorna el bono creado
    """ 
    
    productosComida = []

    for producto in sucursal.getInventarioCine():
      if producto.getTipoProducto() == "comida" and producto.getCantidad() > 0:
          productosComida.append(producto)

    if not productosComida:
      return None

    numeroAleatorio = random.randint(0, len(productosComida) - 1)
    code = Bono.generarCodigoAleatorio(7)

    productoSeleccionado = productosComida[numeroAleatorio]
    productoBono = Producto(productoSeleccionado.getNombre(),productoSeleccionado.getTamaño(),"comida",0,1)

    bono = Bono(code, productoBono, productoSeleccionado.getTipoProducto(), cliente)
    productosComida[numeroAleatorio].setCantidad(productosComida[numeroAleatorio].getCantidad()-1)


    

    return bono
  
  
    

  @classmethod
  def generarBonoSouvenirJuegos(cls,sucursal, cliente): 

    """
    Description: Este metodo se encarga primeramente de seleccionar los productos de tipo souvenir
    del inventario de la sucursal, luego genera un codigo aleatorio de 7 digitos para el bono y 
    ademas escoge de esos productos seleccionados uno de manera aleatoria para ser asociado al bono
    y lo descuenta de la cantidad de disponibles, finalmente imprime por pantalla el bono al usuario

    :param sucursal: Se pasa como parámetro la sucursal de cine asociada en el momento 
    :param cliente: Se pasa como parámetro el cliente que genera el bono
    :return Bono: Se retorna el bono creado
    """ 

    productosSouvenirs = []

    for producto in sucursal.getInventarioCine():
      if producto.getTipoProducto() == "souvenir" and producto.getCantidad() > 0:
          productosSouvenirs.append(producto)

    if not productosSouvenirs:
      return None

    numeroAleatorio = random.randint(0, len(productosSouvenirs) - 1)
    code = Bono.generarCodigoAleatorio(7)

    productoSeleccionado = productosSouvenirs[numeroAleatorio]
    productoBono = Producto(productoSeleccionado.getNombre(),productoSeleccionado.getTamaño(),"souvenir",0,1)

    bono = Bono(code, productoBono, productoSeleccionado.getTipoProducto(), cliente)
    productosSouvenirs[numeroAleatorio].setCantidad(productosSouvenirs[numeroAleatorio].getCantidad()-1)


    

    return bono

  @classmethod
  def generarCodigoAleatorio(cls,longitud):
    """
    Description: Este método se encarga de generar un código aleatorio para los bonos creados.
  
    :param longitud: Se pasa como parámetro la longitud que se desea para el código.
    :return str: Se retorna el código creado.
    """
    caracteres = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
      
    codigo = ''.join(random.choice(caracteres) for _ in range(longitud))
    return codigo


  #Getters y Setters
  def getCodigo(self):
    return self._codigo

  def setCodigo(self, codigo):
    self._codigo = codigo

  def getTipoServicio(self):
    return self._tipoServicio

  def setTipoServicio(self, tipoServicio):
    self._tipoServicio = tipoServicio

  def getProducto(self):
    return self._producto

  def setProducto(self, producto):
    self._producto = producto

  def getCliente(self):
    return self._cliente

  def setCliente(self, cliente):
    self._cliente = cliente