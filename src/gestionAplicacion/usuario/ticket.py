import math
from gestionAplicacion.usuario.ibuyable import Ibuyable

class Ticket(Ibuyable):
    
#Attributes
################################################

    _cantidadTicketsCreados = 0

    def __init__(self, pelicula, horario, numeroAsiento, compraEnPresentacion, sucursalCompra):
        self._pelicula = pelicula
        self._horario = horario
        self._numeroAsiento = numeroAsiento
        self._sucursalCompra = sucursalCompra
        self._precio = self._clienteSuertudo()
        self._salaDeCine = pelicula.getSalaCinePresentacion()
        self._compraEnPresentacion = compraEnPresentacion

        self._idTicket = 0
        self._dueno = None
        self._descuento = True

#Methods
################################################

    def _clienteSuertudo(self):

        """
        :Description: Este método se encarga de verificar si se puede aplicar o no un descuento sobre el precio de la película
	    según si la cantidad de tickets creados corresponde a un cuadrado perfecto.
	    
        :return float: Retorna un float que corresponde al precio del ticket en caso de aplicarse o no el descuento.
        """
        
        if math.sqrt(self._sucursalCompra.getCantidadTicketsCreados()) % 1 == 0:
            if self._pelicula.getTipoDeFormato() == "4D" or self._pelicula.getTipoDeFormato() == "3D":
                return self._pelicula.getPrecio() * 0.5
            else:
                return self._pelicula.getPrecio() * 0.2
        else:
            return self._pelicula.getPrecio()
            
    def procesarPagoRealizado(self, cliente):

        """
        Description: Este método se encarga de generar el último paso del proceso de pago y será ejecutado por un ticket luego de ser verificado el pago: 
	    <ol>
	    <li> Se vuelven a settear los metodos de pago que el cliente tendrá disponibles.</li>
	    <li> Se pasa la referencia del ticket al array de tickets del usuario.</li>
	    <li> Se pasa la referencia del cliente al atributo dueño del ticket.</li>
	    <li> Se aumenta la cantidad de tickets genereados en uno.</li>
	    <li> Se crea una referencia de este ticket en el arraylist de los tickets creados en el cine.</li>
	    <li> Se crea el código de descuento para los juegos y se asocian al cliente y a los códigos de descuentos generados en la clase Arkade.</li>
	    <li> Creamos el id del ticket y aumentamos la cantidad de tickets creados (Lógica id).</li>
	    </ol>

	    :param cliente: Se pide como parámetro el cliente (De tipo Cliente) que realizó exitosamente el pago.
        :type cliente: Cliente
        """

        #Implementar solución para las importaciones circulares
        #cliente.getMetodosDePagoDisponibles[0].asignarMetodosDePago(cliente)

        #Implementamos la lógica luego de comprar un ticket

        #Añadimos el ticket a la lista de tickets del cliente y le setteamos su dueño
        cliente.getTickets().append(self)
        self._dueno = cliente

        #Aumentamos la cantidad de tickets creados para aplicar los descuentos
        self._sucursalCompra.setCantidadTicketsCreados(self._sucursalCompra.getCantidadTicketsCreados() + 1)

        #Setteamos su identificador único
        Ticket._cantidadTicketsCreados += 1
        self._idTicket = Ticket._cantidadTicketsCreados

        #Añadimos el ticket a la lista de tickets disponibles
        self._sucursalCompra.getTicketsDisponibles().append(self)

        #Modificamos la disponibilidad de asientos
        asientoCliente = self._numeroAsiento.split('-')
        filaAsiento = int(asientoCliente[0])
        columnaAsiento = int(asientoCliente[1])

        #Modificamos el asiento seleccionado por el cliente, accediendo a estos por medio del horario seleccionado
        self._pelicula.modificarSalaVirtual(self._horario, filaAsiento, columnaAsiento)

        #En caso de que la compra haya sido realizada en un horario en presentación, modificamos la disponibilidad del asiento en la sala
        if self._compraEnPresentacion:
            self._salaDeCine.getAsientos()[filaAsiento - 1][columnaAsiento - 1].setDisponibilidad(False)

        #Proceso para funcionalidad 2
        if self._horario.date() == self._sucursalCompra.getFechaActual().date():
            self._sucursalCompra.getTicketsParaDescuento().append(self)

        #Proceso para funcionalidad 4
        codigoArkade = self.generarCodigoTicket()
        self._dueno.getCodigosDescuento().append(codigoArkade)
		
		#Lógica id
        Ticket._cantidadTicketsCreados +=1
        self._idTicket = Ticket._cantidadTicketsCreados

    def factura(self):
        """
        :Description: Este método se encarga de retornar un string que contiene toda la información del ticket en forma de factura.
	    :return String: Este método retorna un String que representa la factura de compra con el fin de ser mostrada en pantalla
	    luego de realizar una compra.
        """

        return	f"========= Factura Ticket =========\nNombre dueño : {self._dueno.getNombre()}\nDocumento : {self._dueno.getDocumento()}\nPelicula : {self._pelicula.getNombre()}\nNúmero de sala : {self._salaDeCine.getNumeroSala()}\nNúmero de asiento : {self._numeroAsiento}\nFecha Presentación: {self._horario.date()}\nHora Presentación: {self._horario.time()}\nValor ticket (IVA incluido): {self._precio}\nFecha de compra: {self._sucursalCompra.getFechaActual().date()} {self._sucursalCompra.getFechaActual().time()}\nSucursal : {self._sucursalCompra.getUbicacion()}"

    def generarCodigoTicket(self):

        """
        :Description: Este metodo se encarga de generar un codigo de descuento que se le asocia al usuario dueño del ticket para que pueda redimirlo 
	    en el Arkade posteriormente.

        :return String: retorna el codigo 
        """

        return str(self._pelicula.getTipoDeFormato()) + str(self._dueno.getTipoDocumento().name) + str(self._pelicula.getSalaCinePresentacion().getNumeroSala()) + "-" + str(self._pelicula.getGenero())

    @classmethod
    def encontrarGeneroCodigoPelicula(cls, codigo):
        """
        Descripción: Este método se encarga de encontrar el género de la película asociada a un código que está contenido dentro del string del mismo.

        :param codigo: Este método recibe como parámetro el código del cual se sacará un substring con el género de la película.
        :return: Este método retorna un string que contiene la información del género de la película del código.
        """
        indice_guion = codigo.find("-")

        if indice_guion != -1 and indice_guion != len(codigo) - 1:
            return codigo[indice_guion + 1:]
        else:
            return ""

#Getters and Setters
################################################

    def getIdTicket(self):
        return self._idTicket
    
    def setIdTicket(self, idTicket):
        self._idTicket = idTicket

    @classmethod
    def getCantidadTicketsCreados(cls):
        return Ticket._cantidadTicketsCreados
    
    @classmethod
    def setCantidadTicketsCreados(cls, cantidadTicketsCreados):
        Ticket._cantidadTicketsCreados = cantidadTicketsCreados

    def getDueno(self):
        return self._dueno
    
    def setDueno(self, dueno):
        self._dueno = dueno

    def getPelicula(self):
        return self._pelicula
    
    def setPelicula(self, pelicula):
        self._pelicula = pelicula

    def getSalaDeCine(self):
        return self._salaDeCine
    
    def setSalaDeCine(self, salaDeCine):
        self._salaDeCine = salaDeCine

    def getHorario(self):
        return self._horario
    
    def setHorario(self, horario):
        self._horario = horario

    def getNumeroAsiento(self):
        return self._numeroAsiento
    
    def setNumeroAsiento(self, numeroAsiento):
        self._numeroAsiento = numeroAsiento

    def getPrecio(self):
        return self._precio
    
    def setPrecio(self, precio):
        self._precio = precio
    
    def getSucursalCompra(self):
        return self._sucursalCompra
    
    def setSucursalCompra(self, sucursalCompra):
        self._sucursalCompra = sucursalCompra
    
    def isDescuento(self):
        return self._descuento
    
    def setDescuento(self, descuento):
        self._descuento = descuento   