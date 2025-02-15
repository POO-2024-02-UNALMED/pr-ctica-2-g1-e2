from abc import ABC, abstractmethod
from excepciones.errorAplicacion import ErrorAplicacion

class PagosExceptions(ErrorAplicacion, ABC):
    
    def __init__(self, mensaje):
        super().__init__(mensaje)

class PagoSinCompletar(PagosExceptions):

    def __init__(self, valor):
        super().__init__(f'Su pago ha quedado inconcluso, saldo pendiente por pagar : ${valor}; por favor elija otro método de pago entre los disponibles')

class CerrarPago(PagosExceptions):
    
    def __init__(self):
        super().__init__(f'No puede ejecutar la acción sobre el widget menú hasta concluir el proceso de pago')
