#from ..sucursalCine import SucursalCine
from gestionAplicacion.sucursalCine import SucursalCine

class Arkade:

  PUNTUACION_MAXIMA = 10.0 #Atributo de clase Constante
  
  #Inicializador
  def __init__(self,nombreServicio= None,valorServicio = 0 ,generoServicio= None, palabras = []):

    self._nombreServicio = nombreServicio
    self._valorServicio = valorServicio         #Atributos y encapsulamiento
    self._generoServicio = generoServicio
    self._palabras = palabras
    SucursalCine.getJuegos().append(self)

  @classmethod
  def verificarTarjetasEnInventario(cls, sucursalCine):

    """
    Description: Este metodo se encarga de verificar si almenos hay 
    alguna tarjeta disponible en el array de tarjetas en inventario
    de la sucursal.

    :param sucursalCine: Se pasa como parámetro la sucursal de cine asociada en ese momento 
    :return boolean: Se retorna true o false dependiendo de si hay o no tarjetas.
    """ 

    value = False
    if sucursalCine.getInventarioTarjetasCinemar().lenght() > 0:
      value = True
    return value

  @classmethod
  def asociarTarjetaCliente(cls, cliente):

    """
    Description: Este metodo toma la primera tarjeta cinemar disponible y le asocia el cliente,  se le asigna saldo 0,
	  y ademas, al Cliente se le asocia la tajeta cinemar y se elimina esa tarjeta de la lista de tarjetas en inventario
    en la sucursal.

    :param cliente: Se pasa como parametro el cliente que adquirirá la tarjeta
    :return void: No hay retorno.

    """ 

    cliente.getCineUbicacionActual().getTarjetasCinemar()[0].setDueno(cliente)
    cliente.getCineUbicacionActual().getTarjetasCinemar()[0].setSaldo(-5000)
    cliente.setCuenta(cliente.getCineUbicacionActual().getTarjetasCinemar()[0])
    cliente.getCineUbicacionActual().getTarjetasCinemar().pop(0)

  @classmethod
  def mostrarJuegos(cls):

    """
    Description: Este metodo se encarga de retornar el string usado
    para mostrar al usuario los juegos por pantalla

    :param None: No hay parametros
    :return String: retorna el string con la descripcion de los juegos.
    """

    juegos = ""
    i = 1
    precios = [15000.0, 20000.0, 10000.0, 30000.0, 7500.0]

    for juego in SucursalCine.getJuegos():
      
      if juego.getValorServicio() == precios[i - 1]:
        juegos += f"{i}. {juego.nombreServicio}--{juego.generoServicio}--{juego.valorServicio}.\n"
      else:
        juegos += f"{i}. {juego.nombreServicio}--{juego.generoServicio}--{juego.valorServicio} --> Precio anterior: {precios[i - 1]}.\n"
      i += 1

    juegos += "6. Volver al inicio\n7. Salir\n"
    return f"¿Cuál juego desea jugar?\n{juegos}"

 

  @classmethod
  def aplicarDescuentoJuegos(cls, genero):

    """
    Description: Este metodo se encarga de aplicar un descuento del 20% 
    al valor de los juegos que tengan igual genero al género pasado en el parámetro.

    :param genero: Se pasa como parámetro el género del juego al cual aplicar el descuento.
    :return Void: No hay retorno.
    """ 
    
    for juego in SucursalCine.getJuegos():
        if juego.getGeneroServicio() == genero:
            juego.setValorServicio(juego.getValorServicio() - (juego.getValorServicio() * 20 / 100))

  @staticmethod
  def reestablecerPrecioJuegos(valores):
    
    """
    Description: Este metodo se encarga de restablecer el valor del precio de todos los juegos

    :param valores: Se pasa como parámetro una lista con los valores del cada juego.
    :return Void: No hay retorno.
    """ 

    for i in range(0, len(SucursalCine.getJuegos())):
      SucursalCine.getJuegos()[i].setValorServicio(valores[i])


  # Metodos get
  def getNombreServicio(self):
    return self._nombreServicio

  def getValorServicio(self):
    return self._valorServicio

  @classmethod
  def getPuntuacionMaxima(cls):
    return cls.PUNTUACION_MAXIMA

  def getGeneroServicio(self):
    return self._generoServicio
  
  def getPalabras(self):
    return self._palabras

  # Metodos set
  def setNombreServicio(self, nombreServicio):
    self._nombreServicio = nombreServicio

  def setValorServicio(self, valorServicio):
    self._valorServicio = valorServicio

  def setGeneroServicio(self, generoServicio):
    self._generoServicio = generoServicio
  
  def setPalabras(self, palabras):
    self._palabras = palabras