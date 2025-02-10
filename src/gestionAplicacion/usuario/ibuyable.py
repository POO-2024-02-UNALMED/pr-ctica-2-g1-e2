class Ibuyable():
    _precioTotal = 0

    def procesarPagoRealizado(self, cliente):
        pass
    
    def factura(self):
        pass

    #Getter and setter
    def getPrecioTotal(cls):
        return Ibuyable._precioTotal
    
    def setPrecioTotal(cls, precioTotal):
        Ibuyable._precioTotal = precioTotal