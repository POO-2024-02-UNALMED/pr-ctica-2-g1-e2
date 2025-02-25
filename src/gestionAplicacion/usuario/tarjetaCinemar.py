class TarjetaCinemar:

  def __init__(self, saldo = 0, dueno = None):

    self._saldo = saldo
    self._dueno = dueno


  def ingresarSaldo(self, saldo):
    """
    Description: Este method se encarga de ingresar el saldo dado a la tarjeta Cinemar.

    :param saldo: Este method recibe como parámetro el saldo a ingresar (de tipo float).
    :return void: No hay retorno.
    """
    self._saldo += saldo

  def hacerPago(self, saldo):
    """
    Description: Este metodo descuenta a la tarjeta Cinemar el monto pasado en el parámetro.

    :param saldo: Se le pasa el monto a ser descontado (de tipo float).
    :return void: No hay retorno.
    """
    self._saldo -= saldo

  def getSaldo(self):
    return self._saldo

  def setSaldo(self, saldo):
    self._saldo = saldo

  def getDueno(self):
    return self._dueno

  def setDueno(self, dueno):
    self._dueno = dueno