from gestionAplicacion.sucursalCine import SucursalCine
from datetime import timedelta

class Cliente():
    
    def __init__(self, nombre = "", edad = 0 , documento = 0, tipoDocumento = None, cineUbicacionActual = None):

        self._nombre = nombre
        self._edad = edad
        self._documento = documento
        self._tipoDocumento = tipoDocumento
        self._cineUbicacionActual = cineUbicacionActual

        #Atributos Funcionalidad 1
        self._tickets = []
        self._historialDePeliculas = []
        self._historialDePedidos = []

        #Atributos Funcionalidad 2

        #Atributos Funcionalidad 3
        self._peliculasDisponiblesParaCalificar = []
        self._productosDisponiblesParaCalificar = []

        #Atributos Funcionalidad 4
        self._cuenta = None
        self._codigosDescuento = []
        self._codigosBonos = []
        self._bonos = []
        self._colorFondoTarjeta = "white"  #blanco por defecto
        self._fuenteTarjeta = "Times New Roman"
        self._colorTextoTarjeta = "black"

        #Atributos Funcionalidad 5
        self._membresia = None
        self._metodosDePago = []
        self._fechaLimiteMembresia = 0
        self._puntos = 0
        self._origenMembresia = 0


        self._cineUbicacionActual.getClientes().append(self)

    #Metodos

    #Description: Este metodo se encarga de mostrar el historial de peliculas que cada cliente ha visto hasta el momento para poder 
    #hacer una calificacion en concreto de las peliculas que el cliente se vio, evitando que el cliente pueda calificar 
    #una pelicula que no haya visto.

    def mostrarPeliculaParaCalificar(peliculasDisponiblesParaCalificar):
        peliculas = []
        for  pelicula in peliculasDisponiblesParaCalificar:
            peliculas.append(f"{pelicula.getNombre()}-{pelicula.getTipoDeFormato()}")
            
        return peliculas
        
    #Description:Este metodo se encarga de mostrar el historial de comida que cada cliente ha consumido hasta el momento
    # para poder  hacer una calificacion en concreto de los productos que el cliente cosnumio, evitando que el cliente pueda calificar 
    #un producto que no haya consumido.

    def mostrarProductosParaCalificar(productosDisponiblesParaCalificar):
        pedidos = []
        for producto in productosDisponiblesParaCalificar:
           pedidos.append(f" {producto.getNombre()}-{producto.getTamaño()}")
            
        return pedidos

    def verificarCuenta(self):

        """
        Description: Este method verifica si el usuario tiene asociada una cuenta de tarjeta cinemar.

        :return boolean: Retorna true or false dependiendo si el cliente tiene cuenta Cinemar o no.
        """
        if self._cuenta != None:
            return True
        else:
            return False
        
    def mostrarCodigosDescuento(self):

        """
        :Description: Este metodo se encarga de retornar la lista de los codigos de descuento que el usuario
	    tiene disponibles para redimir por la compra de tickets de peliculas.

        :return String: retorna la Lista de codigos disponibles
        """
        
        cadena = ""

        for i in range(0,len(self._codigosDescuento)):
            cadena+= (i+1) + ". "+ self._codigosDescuento[i]+"\n"

        cadena+= (len(self._codigosDescuento)+1) + ". Ninguno\n" + (len(self._codigosDescuento)+2) + ". Salir y Guardar\n"
 
    #def mostrarTicketsParaUsar(self, ticketsParaUsar):

    def dropTicketsCaducados(self):

        """
        :Description: Este method se encarga de eliminar los tickets cuyo horario, más la duración de la película para la cuál fue adquirido
	    es menor a la fecha actual.
        """
        
        ticketsAEliminar = []

        for ticket in self._tickets:
            if ticket.getHorario() + ticket.getPelicula().getDuracion() < self._cineUbicacionActual.getFechaActual():
                ticketsAEliminar.append(ticket)
        
        for ticket in ticketsAEliminar:
            self._tickets.remove(ticket)

    def filtrarTicketsParaSede(self):

        """
        :Description: Este method se encarga de retornar los tickets correspondientes a la sucursal de cine en la que se encuentra el cliente.
	    
        :return list(Ticket): Este method retorna el resultado de la verifcación, con el fin de que el cliente solo pueda acceder a las salas de cine
	    o a la sala de espera si este posee al menos un ticket de esta sucursal.
        """

        ticketsParaUsar = []

        for ticket in self._tickets:
            if ticket.getSucursalCompra() is self._cineUbicacionActual:
                ticketsParaUsar.append(ticket)
        
        return ticketsParaUsar
    
    def mostrarTicketsParaSalaDeEspera(self):

        """
        :Description: Este method se encarga de retornar los tickets correspondientes a la sucursal de cine en la que se encuentra el cliente
        cuyo horario aún no se encuentra en presentación.
	    
        :return list(Ticket): Este method retorna el resultado de la verifcación, con el fin de que el cliente solo pueda usar los tickets
	    en la sala de espera cuyo horario sea estrictamente mayor y sean de esta sucursal.
        """

        ticketsParaUsar = []

        for ticket in self._tickets:
            if ticket.getSucursalCompra() is self._cineUbicacionActual and ticket.getHorario() > self._cineUbicacionActual.getFechaActual():
                ticketsParaUsar.append(ticket)
        
        return ticketsParaUsar

    def generoMasVisto(self):

        """
        :Description: Este method se encarga de encontrar el género más visto por un cliente, para realizar este proceso, iteramos sobre su historial
	    de películas, luego, obtenemos el género de cada una y alamacenamos las veces que se repite este género en arraylists distintos, conservando
	    el mismo índice, por último, evaluamos cuál género tiene más visualizaciones y se retorna este, en caso de coincidir en visualizaciones con 
	    otro género, retornamos el género más reciente.

	    :return String: Este method retorna el género (De tipo String) con más visualizaciones.
        """

        generosVistos = []
        cantidadVisualizaciones = []

        for pelicula in self._historialDePeliculas:

            if generosVistos.__contains__(pelicula.getGenero()):
                
                indiceGenero = generosVistos.index(pelicula.getGenero())

                cantidadVisualizaciones[indiceGenero] += 1

            else:
                generosVistos.append(pelicula.getGenero())

                cantidadVisualizaciones.append(1)
        
        primeraComparacion = True
        generoMasVisto = ""
        visualizacionesGeneroMasVisto = 0

        for genero in generosVistos:

            if primeraComparacion:
                generoMasVisto = genero
                visualizacionesGeneroMasVisto = cantidadVisualizaciones[generosVistos.index(genero)]

            if cantidadVisualizaciones[generosVistos.index(genero)] >= visualizacionesGeneroMasVisto:
                generoMasVIsto = genero
                visualizacionesGeneroMasVisto = cantidadVisualizaciones[generosVistos.index(genero)]

        
        return generoMasVisto
    
    #Getters and Setters
    def getNombre(self):
        return self._nombre

    def setNombre(self, nombre):
        self._nombre = nombre

    def getMembresia(self):
        return self._membresia

    def setNombre(self, membresia):
        self._membresia = membresia

    def getCodigosDescuento(self):
        return self._codigosDescuento

    def setCodigosDescuento(self, codigosDescuento):
        self._codigosDescuento = codigosDescuento

    def getCodigosBonos(self):
        return self._codigosBonos

    def setCodigosBonos(self, codigosBonos):
        self._codigosBonos = codigosBonos

    def getBonos(self):
        return self._bonos

    def setBonos(self, bonos):
        self._bonos = bonos

    def getEdad(self):
        return self._edad

    def setEdad(self, edad):
        self._edad = edad

    def getDocumento(self):
        return self._documento

    def setDocumento(self, documento):
        self._documento = documento

    def getTipoDocumento(self):
        return self._tipoDocumento

    def setTipoDocumento(self, tipoDocumento):
        self._tipoDocumento = tipoDocumento

    def getTickets(self):
        return self._tickets
    
    def setTickets(self, tickets):
        self._tickets = tickets

    def getHistorialDePeliculas(self):
        return self._historialDePeliculas
    
    def setHistorialDePeliculas(self, historialDePeliculas):
        self._historialDePeliculas = historialDePeliculas

    def getHistorialDePedidos(self):
        return self._historialDePedidos
    
    def setHistorialDePeliculas(self, historialDePedidos):
        self._historialDePedidos = historialDePedidos    

    def getCineUbicacionActual(self):
        return self._cineUbicacionActual

    def setCineUbicacionActual(self, cineUbicacionActual):
        self._cineUbicacionActual = cineUbicacionActual

    def getMetodosDePago(self):
        return self._metodosDePago
    
    def setMetodosdePago(self, metodosDePago):
        self._metodosDePago = metodosDePago

    def getPeliculasDisponiblesParaCalificar(self):
        return self._peliculasDisponiblesParaCalificar

    def setNombre(self, peliculasDisponiblesParaCalificar):
        self._peliculasDisponiblesParaCalificar = peliculasDisponiblesParaCalificar    
    
    def getProductosDisponiblesParaCalificar(self):
        return self._productosDisponiblesParaCalificar

    def setNombre(self, productosDisponiblesParaCalificar):
        self._productosDisponiblesParaCalificar = productosDisponiblesParaCalificar 
    
    def getCuenta(self):
        return self._cuenta
    
    def setCuenta(self, cuenta):
        self._cuenta = cuenta

    def getMembresia(self):
        return self._membresia
    
    def setMembresia(self, membresia):
        self._membresia = membresia

    def getFechaLimiteMembresia(self):
        return self._fechaLimiteMembresia
    
    def setFechaLimiteMembresia(self, fechaLimiteMembresia):
        self._fechaLimiteMembresia = fechaLimiteMembresia

    def getPuntos(self):
        return self._puntos
    
    def setPuntos(self, puntos):
        self._puntos = puntos

    def getOrigenMembresia(self):
        return self._origenMembresia
    
    def setOrigenMembresia(self, origenMembresia):
        self._origenMembresia = origenMembresia