class Asiento:

    def __init__(self, fila, columna):
        self._numeroAsiento = f"{fila + 1}-{columna + 1}"
        self._disponibilidad = True
    
    def getNumeroAsiento(self):
        return self._numeroAsiento
    
    def setNumeroAsiento(self, numeroAsiento):
        self._numeroAsiento = numeroAsiento

    def isDisponibilidad(self):
        return self._disponibilidad
    
    def setDisponibilidad(self, disponibilidad):
        self._disponibilidad = disponibilidad