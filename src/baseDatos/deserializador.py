import pickle
from gestionAplicacion.sucursalCine import SucursalCine
import os



class Deserializador:
    
    #Creamos un método base que deserializa el primer elemento
    @classmethod
    def deserializarLugar(cls, dir):

        doc = open(f'src/baseDatos/temp/sucursales/{dir}/lugar.txt', 'rb')

        lugar = pickle.load(doc)

        doc.close()

        return lugar
    
    @classmethod
    def deserializarDocInstancia(cls, sucursal, archivo):

        doc = open(f'src/baseDatos/temp/sucursales/sucursal{sucursal.getUbicacion()}/{archivo}.txt', 'rb')

        elementoDeserializado = pickle.load(doc)

        doc.close()

        return elementoDeserializado
    
    @classmethod
    def deserializarDocClase(cls, archivo):

        doc = open(f'src/baseDatos/temp/staticAttributes/{archivo}.txt', 'rb')

        lista = pickle.load(doc)

        doc.close()

        return lista

    @classmethod
    def deserializar(cls):

        dirs = os.listdir('src/baseDatos/temp/sucursales')

        for dir in dirs:

            #Construimos una sucursal deserializando el lugar
            sucursal = SucursalCine(Deserializador.deserializarLugar(dir))
            
            #Deserializamos la información de cada sede
            sucursal.setBonosCreados(Deserializador.deserializarDocInstancia(sucursal, 'bonos'))
            sucursal.setCantidadTicketsCreados(Deserializador.deserializarDocInstancia(sucursal, 'cantidadTicketsCreados'))
            sucursal.setInventarioCine(Deserializador.deserializarDocInstancia(sucursal, 'inventarioCine'))
            sucursal.setUbicacion(Deserializador.deserializarDocInstancia(sucursal, 'lugar'))
            sucursal.setSalasDeCine(Deserializador.deserializarDocInstancia(sucursal, 'salasDeCine'))
            sucursal.setServicios(Deserializador.deserializarDocInstancia(sucursal, 'servicios'))
            sucursal.setTarjetasCinemar(Deserializador.deserializarDocInstancia(sucursal, 'tarjetasCinemar'))
            sucursal.setCartelera(Deserializador.deserializarDocInstancia(sucursal, 'tpeliculas'))


        #Deserializamos los atributos de clase
        sedeBase = SucursalCine.getSucursalesCine()[0]
        sedeBase.setClientes(Deserializador.deserializarDocClase('clientes'))
        sedeBase.setFechaActual(Deserializador.deserializarDocClase('fechaActual'))
        SucursalCine.setFechaRevisionLogicaDeNegocio(Deserializador.deserializarDocClase('fechaLogicaNegocio'))
        SucursalCine.setFechaValidacionNuevoDiaDeTrabajo(Deserializador.deserializarDocClase('fechaNuevoDia'))
        SucursalCine.setJuegos(Deserializador.deserializarDocClase('juegos'))
        SucursalCine.setTiposDeMembresia(Deserializador.deserializarDocClase('membresias'))
        SucursalCine.setMetodosDePagoDisponibles(Deserializador.deserializarDocClase('metodosDePagoDisponibles'))
        sedeBase.setTicketsDisponibles(Deserializador.deserializarDocClase('ticketsDisponibles'))

        #Corregimos integridad de los datos de clase deserializados
        Deserializador.asignarReferenciasDeserializador()
    
    @classmethod
    def asignarReferenciasDeserializador(cls):

        #Creamos un apuntador de una sucursal para acceder a métodos setteados como de instancia
        sedeBase = SucursalCine.getSucursalesCine()[0]

        #Iteramos sobre todas las sedes para asignar las referencias 
        for sede in SucursalCine.getSucursalesCine():
            
            #A cada película le setteamos la sucursal y su sala respecto a la sucursal
            for pelicula in sede.getCartelera():
                pelicula.setSucursalCartelera(sede)
                pelicula.setSalaCinePresentacion(sede.obtenerSalaDeCinePorId(pelicula.getSalaCinePresentacion().getSalaCineId()))
            
            #A cada sala de cine le setteamos la sucursal a la que pertenece y su película y horario lo pasamos a None para que se actualice desde la ejecución
            for salaCine in sede.getSalasDeCine():
                salaCine.setSucursalUbicacion(sede)
                salaCine.setPeliculaEnPresentacion(None)
                salaCine.setHorarioPeliculaEnPresentacion(None)
            
            #A cada producto le setteamos la sucursal a la que pertenece
            for producto in sede.getInventarioCine():
                producto.setSucursalSede(sede)
            
            #A cada bono le setteamos el cliente que le corresponde
            for bono in sede.getBonosCreados():
                pass#bono.setCliente(SucursalCine.buscarCliente(bono.getCliente().getDocumento(), bono.getCliente().getTipoDocumento()))
        
        #A cada cliente le eliminamos los ticktes que tienen ya que los volveremos a settear más adelante
        for cliente in sedeBase.getClientes():
            cliente.getTickets().clear()
        
        ticketsAElimiinar = []
        
        #Iteramos sobre los tickets deserializados
        for ticket in sedeBase.getTicketsDisponibles():
            
            #Eliminamos los tickets cuyo horario definitivamente a caducado
            if ticket.getHorario().date() < sedeBase.getFechaActual().date():
                ticketsAElimiinar.append(ticket)
            
            #Reasignamos los datos del ticket
            else:
                ticket.setDueno(SucursalCine.buscarCliente(ticket.getDueno().getDocumento(), ticket.getDueno().getTipoDocumento().value))
                ticket.getDueno().getTickets().append(ticket)
                ticket.setSucursalCompra(SucursalCine.obtenerSucursalPorId(ticket.getSucursalCompra().getIdSucursal()))
                ticket.setPelicula(ticket.getSucursalCompra().obtenerPeliculaPorId(ticket.getPelicula().getIdPelicula()))
                ticket.setSalaDeCine(ticket.getPelicula().getSalaCinePresentacion())

        #Eliminamos los tickets caducados
        for ticket in ticketsAElimiinar:
            sedeBase.getTicketsDisponibles().remove(ticket)
        
        #Eliminamos los tickets para descuento el día de hoy
        for sede in SucursalCine.getSucursalesCine():
            sede.getTicketsParaDescuento().clear()

            #Asignamos los tickets que pueden recibir descuento el día de hoy
            for ticket in sedeBase.getTicketsDisponibles():
                if ticket.getSucursalCompra() is sede and ticket.getHorario().date() == sedeBase.getFechaActual().date():
                    sede.getTicketsParaDescuento().append(ticket)

        #Se itera sobre las membresias para actualizar los apuntadores a los clientes que han adquirido la membresia.
        for membresia in SucursalCine.getTiposDeMembresia():
            clienteTemp = []
            #Se obtiene los nuevos apuntadores para el arreglo de clientes en Membresia
            for cliente in membresia.getClientes():
                clienteTemp.append(SucursalCine.buscarCliente(cliente.getDocumento(), cliente.getTipoDocumento().value))
            membresia.setClientes(clienteTemp)

            #Una vez actualizado el arreglo de clientes, se actualizan los apuntadores de Membresia que tiene cada cliente.
            for cliente in membresia.getClientes():
                cliente.setMembresia(membresia)
        
       
