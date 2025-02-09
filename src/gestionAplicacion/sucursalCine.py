from datetime import datetime, time, timedelta
import random
from gestionAplicacion.servicios.producto import Producto
from gestionAplicacion.proyecciones.pelicula import Pelicula
from gestionAplicacion.usuario.metodoPago import MetodoPago

class SucursalCine:

#Attributes
################################################

    #Static Attributes
    _cantidadSucursales = 0
    _fechaActual = None
    _fechaValidacionNuevoDiaDeTrabajo = None
    _fechaRevisionLogicaDeNegocio = None
    _sucursalesCine = []
    _ticketsDisponibles = []
    _juegos = []
    _clientes = []
    _metodosDePagoDisponibles = []
    _tiposDeMembresia = []

    #Constants
    _INICIO_HORARIO_LABORAL = time(10,00)
    _FIN_HORARIO_LABORAL = time(23, 00)
    _TIEMPO_LIMPIEZA_SALA_DE_CINE = timedelta( minutes=30 )
    _TIEMPO_LIMITE_RESERVA_TICKET = timedelta( minutes=15 )
   

    #Instance Attributes
    def __init__(self, ubicacion):
        self._ubicacion = ubicacion
        
        SucursalCine._cantidadSucursales += 1
        self._idSucursal = SucursalCine._cantidadSucursales
        SucursalCine._sucursalesCine.append(self)

        self._inventarioCine = []
        self._ticketsParaDescuento = []
        self._servicios = []
        self._bonosCreados = []
        self._salasDeCine = []
        self._cartelera = []
        self._tarjetasCinemar = []
        self._cantidadTicketsCreados = 1
    
#Methods
################################################

    #def mostrarSucursalesCine(cls)

    @classmethod
    def _dropHorariosVencidos(cls):

        """
        :Description: Este método se encarga de eliminar los horarios que ya no pueden ser presentados al pasar de día
	    o luego de la deserialización, de todas las películas de cada sucursal, eliminando los horarios anteriores al día
	    de la fecha actual.
        """

        for sede in SucursalCine._sucursalesCine:

            for pelicula in sede._cartelera:

                horariosAEliminar = []

                for horario in pelicula.getHorariosPresentacion():

                    if horario.date() < SucursalCine._fechaActual.date():
                        horariosAEliminar.append(horario)

                for horario in horariosAEliminar:

                    pelicula.getAsientosSalasVirtuales().pop(pelicula.getHorariosPresentacion().index(horario))
                    pelicula.getHorariosPresentacion().remove(horario)

    def _distribuirPeliculasPorSala(self):

        """
        :Description: Este método se encarga de distribuir las películas en cartelera en las distintas salas de cine 
	    de la sucursal de cine que ejecuta este método, para esta distribución se tienen encuenta 3 casos posibles:
	    <ol>
	    <li>Hay menos películas que salas de cine o igual cantidad de ambas.</li>
	    <li>Hay más películas que salas de cine, pero caben exactamente la misma cantidad de películas en cada sala.</li>
	    <li>Hay más películas que salas de cine, pero al menos una sala de cine debe tener 1 película más que todas 
	    las otras (Principio de Dirichlet o del palomar).</li>
	    </ol>
        """
        
        formatos = ["2D", "3D", "4D"]

        for formato in formatos:

            grupoSalasPorFormato = []
            grupoPeliculasPorFormato = []

            cantidadMaxPeliculaPorSala = 0
            contador = 0

            indiceSalaDeCine = 0

            for salaDeCine in self._salasDeCine:
                if salaDeCine.getTipoSala() == formato:
                    grupoSalasPorFormato.append(salaDeCine)

            for pelicula in self._cartelera:
                if pelicula.getTipoDeFormato() == formato:
                    grupoPeliculasPorFormato.append(pelicula)
            
            if len(grupoPeliculasPorFormato) > len(grupoSalasPorFormato):

                cantidadMaxPeliculaPorSala = int(len(grupoPeliculasPorFormato) / len(grupoSalasPorFormato)) if len(grupoPeliculasPorFormato) % len(grupoSalasPorFormato) == 0 else int(len(grupoPeliculasPorFormato) / len(grupoSalasPorFormato)) + 1

                for pelicula in grupoPeliculasPorFormato:
                    pelicula.setSalaCinePresentacion(grupoSalasPorFormato[indiceSalaDeCine])
                    contador += 1

                    if contador == cantidadMaxPeliculaPorSala:
                        contador = 0
                        indiceSalaDeCine += 1

            else:
                
                for pelicula in grupoPeliculasPorFormato:

                    pelicula.setSalaCinePresentacion(grupoSalasPorFormato[indiceSalaDeCine])
                    indiceSalaDeCine += 1

    @classmethod
    def logicaSemanalSistemNegocio(cls):

        """
        :Description: Este método se encarga de realizar los preparativos para ejecutar la lógica de la funcionalidad #3:
	    <ol>
	    <li>Renueva las cantidades disponibles de los productos en inventario</li>
	    <li>Eliminar los horarios de la semana anterior.</li>
	    <li>Distribución de películas en las salas de cine y la creación de sus horarios.</li>
	    <li>Eliminar los tickets comprados de películas de la semana anterior.</li>
	    </ol>
        """
        
        SucursalCine._ticketsDisponibles.clear()

        for sede in SucursalCine._sucursalesCine:
            
            sede._distribuirPeliculasPorSala()
            sede._crearHorariosPeliculasPorSala()

    @classmethod
    def logicaInicioSIstemaReservarTicket(cls):

        """
        :Description: Este método se encarga de ejecutar toda la lógica para realizar reservas de ticket por primera vez,
	    se compone de 3 puntos principales:
	    <ol>
	    <li>Distribuir las películas en cartelera de cada sucursal de forma equitativa respecto a sus salas de cine.</li>
	    <li>Una vez realizada la distribución, crear los horarios en los que se presentará cada película.</li>
	    <li>Actualizar las películas cuyo horario se esta presentando en estos momentos.</li>
	    <li>Establecer las fechas cuando se ejecutarán la lógica diaria y semanal del negocio.</li>
	    </ol>
        """

        SucursalCine._fechaActual = datetime.now().replace(hour = SucursalCine._INICIO_HORARIO_LABORAL.hour, minute = SucursalCine._INICIO_HORARIO_LABORAL.minute)

        for sede in SucursalCine._sucursalesCine:

            sede._distribuirPeliculasPorSala()
            sede._crearHorariosPeliculasPorSala()
        
        SucursalCine.actualizarPeliculasSalasDeCine()
        SucursalCine._fechaValidacionNuevoDiaDeTrabajo = SucursalCine._fechaActual.date() + timedelta(days = 1)
        SucursalCine._fechaRevisionLogicaDeNegocio = SucursalCine._fechaActual.date() + timedelta(weeks = 1)


    @classmethod
    def logicaDiariaReservarTicket(cls):

        """
        :Description : Este método se encarga de evaluar la lógica diaria de la reserva de tickets, para esto evalua los siguientes criterios:
	    <ol>
	    <li>Añade los tickets de películas que serán presentadas el día de hoy al array de tickets para descuento y elimina los tickets
	    caducados de los clientes y del array de tickets disponibles.</li>
	    </ol>
        """
        SucursalCine._dropHorariosVencidos()

        ticketsAEliminar = []

        for sede in SucursalCine._sucursalesCine:

            sede._ticketsParaDescuento.clear()

            for ticket in SucursalCine._ticketsDisponibles:
                
                if ticket.getSucursalCompra() == sede._ubicacion and ticket.getHorario().date() == SucursalCine._fechaActual.date():
                    sede._ticketsParaDescuento.append(ticket)

                if (ticket.getHorario()).date() < SucursalCine._fechaActual.date():
                    if ticket not in ticketsAEliminar: ticketsAEliminar.append(ticket)

        for ticket in ticketsAEliminar:
            SucursalCine._ticketsDisponibles.remove(ticket)
        
        for cliente in SucursalCine._clientes:
            cliente.dropTicketsCaducados() 
