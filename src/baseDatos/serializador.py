import pickle
from gestionAplicacion.sucursalCine import SucursalCine

class Serializador:

    #Creamos un método base que serializa una lista de instancia
    @classmethod
    def serializarListaInstancia(cls, sede, archivo, lista):

        doc = open(f'src/baseDatos/temp/sucursales/sucursal{sede.getUbicacion()}/{archivo}.txt', 'wb')

        pickle.dump(lista, doc)

        doc.close()

    @classmethod
    def serializarListaClase(cls, archivo, lista):

        doc = open(f'src/baseDatos/temp/staticAttributes/{archivo}.txt', 'wb')

        pickle.dump(lista, doc)

        doc.close()

    @classmethod
    def serializar(cls):

        for sucursal in SucursalCine.getSucursalesCine():

            #Serializa los principales atributos de instancia
            Serializador.serializarListaInstancia(sucursal, 'bonos', sucursal.getBonosCreados())
            Serializador.serializarListaInstancia(sucursal, 'cantidadTicketsCreados', sucursal.getCantidadTicketsCreados())
            Serializador.serializarListaInstancia(sucursal, 'inventarioCine', sucursal.getInventarioCine())
            Serializador.serializarListaInstancia(sucursal, 'lugar', sucursal.getUbicacion())
            Serializador.serializarListaInstancia(sucursal, 'salasDeCine', sucursal.getSalasDeCine())
            Serializador.serializarListaInstancia(sucursal, 'servicios', sucursal.getServicios())
            Serializador.serializarListaInstancia(sucursal, 'tarjetasCinemar', sucursal.getTarjetasCinemar())
            Serializador.serializarListaInstancia(sucursal, 'tpeliculas', sucursal.getCartelera())

        #Serializa los atributos de clase
        sedeBase = SucursalCine.getSucursalesCine()[0]
        Serializador.serializarListaClase('clientes', sedeBase.getClientes())
        Serializador.serializarListaClase('fechaActual', sedeBase.getFechaActual())
        Serializador.serializarListaClase('fechaLogicaNegocio', SucursalCine.getFechaRevisionLogicaDeNegocio())
        Serializador.serializarListaClase('fechaNuevoDia', SucursalCine.getFechaValidacionNuevoDiaDeTrabajo())
        Serializador.serializarListaClase('juegos', SucursalCine.getJuegos())
        Serializador.serializarListaClase('membresias', SucursalCine.getTiposDeMembresia())
        Serializador.serializarListaClase('metodosDePagoDisponibles', SucursalCine.getMetodosDePagoDisponibles())
        Serializador.serializarListaClase('ticketsDisponibles', sedeBase.getTicketsDisponibles())



