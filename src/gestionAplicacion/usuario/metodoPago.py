class MetodoPago():

    #Inicializador
    def __init__(self, nombre, descuentoAsociado, limiteMaximoPago, sucursalCine, tipo = 0):
        self._nombre = nombre
        self._descuentoAsociado = descuentoAsociado
        self._limiteMaximoPago = limiteMaximoPago
        self._tipo = tipo
        self._sucursalCine = sucursalCine

        if (nombre != "Puntos"):
            self._sucursalCine.getMetodosDePagoDisponibles().append(self)


    #Metodos
  
    def realizarPago(self, precio, clienteProceso):
        """<b>Description</b> : Este método se encarga de tomar el valor a pagar, aplicar el descuento del método de pago elegido por el cliente y restarle el monto máximo que se puede pagar con ese método de pago, si el método de pago cubre el valor a pagar, éste se cambia se cambia a 0.
	    Además, este método se encarga de pasar la referencia del método de pago a los métodos de pago usados y quita la referencia de métodos de pago disponibles asociados al cliente.
	    En caso de que el cliente tenga una membresía, se realiza la acumulación de puntos en base al valor pagado.

	    <b>Parameter</b>: precio : Se pide el valor a pagar, este se obtuvo anteriormente como variable durante el proceso de la funcionalidad
	    <b>Parameter</b>: cliente : Se pide al cliente que va a efectuar el proceso de realizar pago. Se revisa si tiene asignado una membresía.

	    <b>Return</b>: <b>double</b> : En caso de que el método de pago cubra el valor a pagar retorna 0, en caso de que no
	    retorna el valor restante a pagar. 
        """

        #Creamos un atributo con scope de método donde obtenemos el precio del producto, aplicamos el descuentoAsociado al metodoDePago y le restamos el LimiteMaximoPago
        valorAPagar = precio * (1-self.getDescuentoAsociado()) - self.getLimiteMaximoPago()
        if (valorAPagar < 0):
            valorAPagar = 0

        #Cuando el método usado sea efectivo, no se pasará a usados y no se acumularan los puntos por la logica de negocios gracias a los convenios.
        if (self.getNombre() == "Efectivo"):
            return valorAPagar
        
        #Cuando el método sea Puntos, se realiza el descuento de esos puntos en el saldo.
        if (self.getNombre() == "Puntos"):
            self.setLimiteMaximoPago(self.getLimiteMaximoPago() - precio)
            if (self.getLimiteMaximoPago() < 0):
                self.setLimiteMaximoPago(0)
            return valorAPagar
        
        #Se verifica si el cliente tiene membresia para realizar la acumulación de puntos
        membresia = clienteProceso.getMembresia()
        tipoMembresia = 0
        if (membresia != None and self.getNombre() != "Puntos"):
            tipoMembresia = clienteProceso.getMembresia().getTipoMembresia()
            puntos = None
            for metodoPago in clienteProceso.getMetodosDePago():
                if (metodoPago.getNombre() == "Puntos"):
                    puntos = metodoPago
                    break

        #Partimos de 1 para contar el método de pago puntos
        totalMetodosDePagoPorTipo = 1

        #Se realiza un ciclo para contar los métodos de pago por el tipoMembresia del cliente
        for metodoPago in self._sucursalCine.getMetodosDePagoDisponibles():
            if (tipoMembresia == metodoPago.getTipo()):
                totalMetodosDePagoPorTipo+=1



        #En caso de que el cliente no pudo cubrir la totalidad del pago y se haya llegado al limite de ese método de pago,
		#la acumulación de puntos solo se hara sobre el primer precio calculado luego del descuento. Los siguientes pagos ya estan cubiertos.
        if (len(clienteProceso.getMetodosDePago()) == totalMetodosDePagoPorTipo):
            if (tipoMembresia == 1):
                puntos.setLimiteMaximoPago(puntos.getLimiteMaximoPago() + (precio * (1- self.getDescuentoAsociado())) * 0.05)
               
            elif (tipoMembresia == 2):
                puntos.setLimiteMaximoPago(puntos.getLimiteMaximoPago() + (precio * (1- self.getDescuentoAsociado())) * 0.10)
            clienteProceso.setPuntos(int(puntos.getLimiteMaximoPago()))

        #Eliminamos su referencia de los metodos de pago asociados al cliente
        clienteProceso.getMetodosDePago().remove(self)

        #Retornamos el valor tras efectuar el pago, puede generar un saldo pendiente a pagar o 0
        return valorAPagar


    #Getters and Setters
    def getNombre(self):
        return self._nombre
    
    def setNombre(self, nombre):
        self._nombre = nombre

    def getTipo(self):
        return self._tipo
    
    def setTipo(self, tipo):
        self._tipo = tipo

    def getDescuentoAsociado(self):
        return self._descuentoAsociado
    
    def setDescuentoAsociado(self, descuentoAsociado):
        self._descuentoAsociado = descuentoAsociado

    def getLimiteMaximoPago(self):
        return self._limiteMaximoPago
    
    def setLimiteMaximoPago(self, limiteMaximoPago):
        self._limiteMaximoPago = limiteMaximoPago

    def getSucursalCine(self):
        return self._sucursalCine
    
    def setSucursalCine(self, sucursalCine):
        self._sucursalCine = sucursalCine