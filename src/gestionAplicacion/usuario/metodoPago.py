from multimethod import multimethod
class MetodoPago():

    #Inicializador
    #sobre carga de constructores
    @multimethod
    def __init__(self):
        """Constructor vacío que añade la instancia a la lista estática."""
        self.nombre = None
        self.limite_maximo_pago = 0.0
        self.descuento_asociado = 0.0
        self.tipo = 0

    @multimethod
    def __init__(self, descuentoAsociado: float, limiteMaximoPago:int, sucursalCine):
        """Constructor que añade la instancia a la lista estática."""
        self.__init__(self) #Se llama al constructor vacío
        self.limite_maximo_pago = limiteMaximoPago
        self.descuento_asociado = descuentoAsociado
        self.sucursalCine = sucursalCine

    @multimethod
    def __init__(self, nombre: str, descuentoAsociado: float, limiteMaximoPago:int, sucursalCine, tipo:int = 0):
        self._nombre = nombre
        self._descuentoAsociado = descuentoAsociado
        self._limiteMaximoPago = limiteMaximoPago
        self._tipo = tipo
        self._sucursalCine = sucursalCine

        if (nombre != "Puntos"):
            self._sucursalCine.getMetodosDePagoDisponibles().append(self)

    @multimethod
    def __init__(self, nombre: str, descuentoAsociado: float, limiteMaximoPago: float, sucursalCine, tipo: int = 0):
        self._nombre = nombre
        self._descuentoAsociado = descuentoAsociado
        self._limiteMaximoPago = limiteMaximoPago
        self._tipo = tipo
        self._sucursalCine = sucursalCine

        if (nombre != "Puntos"):
            self._sucursalCine.getMetodosDePagoDisponibles().append(self)

    #Metodos
    
    @classmethod
    def mostrarMetodosDePago(cls, clienteProceso):
        """
        <b>Description</b>: Este método se encarga de mostrar los métodos de pago disponibles con
	    sus descuentos. El resultado puede cambiar si el cliente posee membresia y el tipo de esta.
	    
        <b>Parameter</b>: <b>cliente</b> : Se usa el objeto de tipo Cliente para acceder a su lista de métodos de pago.
	    
        <b>return</b>: <b>string</b> : Se retorna un texto mostrando el nombre de los métodos de pago con sus descuentos.
        """
        resultado = []
        i = 1

        #Se recorre la lista de los medios de pagos disponibles en la lista del cliente.
        for metodoPago in clienteProceso.getMetodosDePago():
            if (resultado == []):
                texto =  f"{i}. {metodoPago.getNombre()} - Descuento: {int(metodoPago.getDescuentoAsociado()*100)}% - Límite Máximo de pago: {metodoPago.getLimiteMaximoPago()}"
                resultado.append(texto)
            
            else:
                if (metodoPago.getNombre() == "Puntos"):
                    texto = f"{i}. {metodoPago.getNombre()} - Saldo: {int(metodoPago.getLimiteMaximoPago())}"
                    resultado.append(texto)
                    continue
                texto = f"{i}. {metodoPago.getNombre()} - Descuento: {int(metodoPago.getDescuentoAsociado()*100)}% - Límite Máximo de pago: {metodoPago.getLimiteMaximoPago()}"
                resultado.append(texto)
            i+=1

        return resultado


    @classmethod
    def asignarMetodosDePago(cls, clienteProceso):
        """<b>Description</b>: Este método se encarga de asignar los métodos de pago disponibles por 
	    su tipo de membresia a su lista de métodos de pago.
	    que tiene el cliente.

	    <b>Parameters</b>: <b>cliente</b> : Se usa el objeto de tipo Cliente para revisar su membresia y poder asignar
	    los métodos de pago.

	    <b>Return</b>: <b>Lista de métodos de pago</b> : Se retorna una lista mostrando los métodos de pago luego
	    de realizar el filtrado por la membresia.
        """

        #Se limpia la lista de métodos de pago, esto en caso de que el cliente haya adquirido una membresia.
        puntos = None

        for metodoPagoCliente in clienteProceso.getMetodosDePago():
            if (metodoPagoCliente.getNombre() == "Puntos"):
                puntos = metodoPagoCliente

        clienteProceso.getMetodosDePago().clear()

        #Se revisa si el cliente posee una membresia y de ser el caso, se asigna el canje de puntos como método de pago.
        tipoMembresia = clienteProceso.getMembresia()
        tipoMembresiaInt = 0

        if (tipoMembresia != None):
            tipoMembresiaInt = tipoMembresia.getTipoMembresia()
            if (puntos == None):
                clienteProceso.setPuntos(2500)
                puntos = MetodoPago("Puntos", 0.0, clienteProceso.getPuntos(), clienteProceso.getCineUbicacionActual(), tipoMembresiaInt)

        #Se realiza un ciclo para filtrar los métodos de pago por el tipoMembresia del cliente y se añaden sus lista de métodos de pago.
        for metodoPago in clienteProceso.getCineUbicacionActual().getMetodosDePagoDisponibles():
            if (tipoMembresiaInt == metodoPago.getTipo()):
                clienteProceso.getMetodosDePago().append(metodoPago)

        #Una vez se actualizan el arreglo de tipo MetodoPago en cliente, se añaden los puntos a este arreglo.
        if (puntos != None):
            clienteProceso.getMetodosDePago().append(puntos)
        
        return clienteProceso.getMetodosDePago()


    @classmethod
    def metodoPagoPorTipo(cls, metodoPago):
        """<b>Description</b>: Este método se encarga de crear varias instancias de los métodos de
	    pago con distinto tipo. Esto para usarse en la funcionalidad 5.

	    <b>Parameters</b>: <b>metodopago</b> : Se usa el objeto de MetodoPago para crear sus instancias.

	    <b>Return</b> <b>void</b> : No se retorna dato. Se toman los atributos del objeto para crear varias instancias. Estos valores son modificados dependiendo del número de tipo en el ciclo for.
        """

        #Se realiza un ciclo para crear varias instancias de los métodos de pago variando sus atributos.
        for i in range (1, 3):
            nombre = metodoPago.getNombre()
            tipo = metodoPago.getTipo() + i
            descuentoAsociado = metodoPago.getDescuentoAsociado() + 0.05 * tipo
            limiteMaximoPago = metodoPago.getLimiteMaximoPago() + 25000 * tipo
            MetodoPago(nombre, descuentoAsociado, limiteMaximoPago, metodoPago._sucursalCine, tipo)


    @classmethod
    def usarMetodoPago(cls, clienteProceso, metodoPagoAUsar):
        """<b>Description</b>: Este método de asignar el método de pago para ser usado.

	    <b>Parameters</b>: metodoPagoAUsar : Se usa el número de la selección para poder escoger el método de pago.
	    <b>Parameters</b>: cliente : Se usa el objeto de cliente para acceder a los métodos de pago.
	    <b>Return</b>: <b>MetodoPago</b> : Se retorna el método de pago que coincide con la opción seleccionada.
        """

        usar = None
        #Se busca en los métodos de pago del cliente y se hace un apuntador al método de pago que coincida con el indice del método de pago más 1.
        for metodoPago in clienteProceso.getMetodosDePago():
            if (metodoPagoAUsar == clienteProceso.getMetodosDePago().index(metodoPago) + 1):
                usar = metodoPago
                break
        
        return usar
    
      
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