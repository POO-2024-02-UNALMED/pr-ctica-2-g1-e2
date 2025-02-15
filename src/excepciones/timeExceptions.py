from abc import ABC, abstractmethod
from excepciones.errorAplicacion import ErrorAplicacion
from datetime import timedelta

class TimeException(ErrorAplicacion, ABC):
    def __init__(self, itemComun):
        self._itemComun = itemComun
        super().__init__(self.crearMensaje())

    @abstractmethod
    def crearMensaje(self):
        pass
        
class ExpiredMembershipException(TimeException):
    def __init__(self, diasRestantes):
        super().__init__(diasRestantes)
    
    def crearMensaje(self):
        mensaje = f'Estimado cliente, recuerde que le quedan {self._itemComun} dia(s) para que caduque su membresía.' if self._itemComun > 0 else "Su membresia ha expirado. Le invitamos a renovarla para no perder sus beneficios."
        return mensaje

class NoMoreFilmsException(TimeException):
    def __init__(self, dateTimeActual):
        super().__init__(dateTimeActual)
    
    def crearMensaje(self):
        mensaje = f'Hemos detectado que han concluido todas las presentaciones del día {self._itemComun.date()}, por lo tanto, se pasará a {(self._itemComun + timedelta(days = 1)).replace(hour = 10, minute = 0, microsecond = 0)} de forma automática. Gracias por su compresión'
        return mensaje
        


    

    

