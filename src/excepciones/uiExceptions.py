from abc import ABC, abstractmethod
from excepciones.errorAplicacion import ErrorAplicacion

class UiExceptions(ErrorAplicacion, ABC):
    def __init__(self, mensaje):
        super().__init__(mensaje)

    def formatearCriterios(self, criterios):
        criteriosFormateados = ''

        for i in range (0,len(criterios)):
            if i < len(criterios) - 1:
                criteriosFormateados += ' ' + criterios[i].strip(':') + ','
            else:
                criteriosFormateados = criteriosFormateados[:-2]
                criteriosFormateados += ' y ' + criterios[i].strip(':')

        return criteriosFormateados
    
    @abstractmethod
    def crearMensaje(self):
        pass
            
class UiDefaultValues(UiExceptions):
    def __init__(self, *criterios):
        super().__init__(self.crearMensaje(*criterios))
    
    def crearMensaje(self, criterios):
        if len(criterios) == 1:

            return f'El campo {criterios[0].strip(':')} tiene un valor por defecto'
        
        elif len(criterios) > 1:

            criteriosFormateados = self.formatearCriterios(criterios)

            return f'Los campos:{criteriosFormateados} tienen valores por defecto'

class UiEmptyValues(UiExceptions):
    def __init__(self, *criterios):
        super().__init__(self.crearMensaje(*criterios))
    
    def crearMensaje(self, criterios):
        if len(criterios) == 1:
            
            return f'El campo {criterios[0].strip(':')} está vacío'
        
        elif len(criterios) > 1:

            criteriosFormateados = self._formatearCriterios(criterios)

            return f'Los campos:{criteriosFormateados} tienen valores vacíos'

